import random
from openai import OpenAI
from dotenv import load_dotenv
from .models import ChatterResponse, SplitterResponse, ResponderResponse


class BaseUltimatumAgent:
    def __init__(self, role: str, strategy: str):
        self.role = role
        self.strategy = strategy

    def choose_split(self) -> float:
        """In the role of the splitter, we must choose a split that we both want and will be accepted by the
        other player"""
        raise NotImplementedError("This should be handled by the child class")

    def choose_response(self, offer: float) -> bool:
        """In the role of responder, we must take a split and use some logic to determine if we should take
        an offer or not"""
        raise NotImplementedError("This should be handled by the child class")

    def generate_freeform_chatter(self, freeform_prompt) -> str:
        raise NotImplementedError("This should be handled by the child class")

    def accept_freeform_chatter(self, param) -> None:
        raise NotImplementedError("This should be handled by the child class")


class UnsophisticatedUltimatumAgent(BaseUltimatumAgent):
    def __init__(self, role: str, strategy: str, fixed_ratio: float = None):
        super().__init__(role, strategy)
        self.fixed_ratio = fixed_ratio

    def choose_split(self) -> float:
        """In the role of the splitter, we must choose a split that we both want and will be accepted by the
        other player"""

        if self.strategy == "random":
            return random.random()

        elif self.strategy == "fixed":
            return self.fixed_ratio

        else:
            raise NotImplementedError(
                f"Strategy {self.strategy} not yet implemented, please use a valid strategy!"
            )

    def choose_response(self, offer: float) -> bool:
        """In the role of responder, we must take a split and use some logic to determine if we should take
        an offer or not.

        False if rejected and True if accepted"""

        if self.strategy == "random":
            return random.random() > 0.5

        elif self.strategy == "fixed":

            ## 1-fixed value since we assume that the offer is given from the perspective of the Splitter
            return (1 - offer) >= self.fixed_ratio

        else:

            raise NotImplementedError(
                f"Strategy {self.strategy} not yet implemented, please use a valid strategy!"
            )


## if we want, something which incorporates basic strategy like in the homework
# class SemiSophisticatedUltimatumAgent(BaseUltimatumAgent):
#     def __init__(self, role:str, strategy:str, fixed_ratio:float=None):
#         super().__init__(role)
#         self.strategy = strategy
#         self.fixed_ratio = fixed_ratio


class OpenAIUltimatumAgent(BaseUltimatumAgent):
    def __init__(
        self,
        role: str,
        strategy: str,
        system_prompt: str,
        turn_prompt: str,
        model: str = "gpt-5.4",
        api_key: str = None,
    ):

        # in this agent strategy is pretty much just an internal tracker for the prompt versions and such
        super().__init__(role, strategy)
        self.system_prompt = (
            system_prompt  ## we need to define the game state, rules etc.
        )
        self.turn_prompt = turn_prompt
        self.client = (
            OpenAI(api_key=api_key) if api_key else OpenAI()
        )  ## we shouldn't be throwing tokens around, use .env w/ gitignore instead
        self.model = model

        ## used for chaining responses/context windows over time
        self.previous_response_id = None

    def update_response_id(self, response: object):
        """Given response object from OpenAI extract the session ID and hook it up so this isn't one shot
        and instead some semblance of a chained session"""

        self.previous_response_id = response.id

    def reset_response_id(self):
        """remove the set value for previous_response_id which effectively ends a session"""
        self.previous_response_id = None

    ## todo simplify duplicative code?
    def choose_split(self, round_chat_logs: list[str] = None) -> None | float:
        """Given the agent's prompt (which should indiciate its role as a splitter),
        determine how to split the pot"""
        if self.previous_response_id:
            response = self.client.responses.parse(
                model=self.model,
                input=self.turn_prompt,
                text_format=SplitterResponse,
                previous_response_id=self.previous_response_id,
                instructions=self.system_prompt,
            )

        else:
            response = self.client.responses.parse(
                model=self.model,
                input=self.turn_prompt,
                text_format=SplitterResponse,
                instructions=self.system_prompt,
            )

        self.update_response_id(response)
        if type(round_chat_logs) == list:
            round_chat_logs.append(
                {
                    "agent": self.role,
                    "function": "choose_split",
                    "reason": response.output_parsed.reason,
                    "value": response.output_parsed.value,
                }
            )

        return response.output_parsed.value

    def choose_response(self, offer: float, round_chat_logs: list[str] = None) -> bool:
        """Given an agent's offer split, use the baked in turn prompt and system prompt
        to determine some outcome. Returns a bool whether or not the offer's accepted"""

        if self.previous_response_id:
            response = self.client.responses.parse(
                model=self.model,
                input=self.turn_prompt + str(offer),
                text_format=ResponderResponse,
                previous_response_id=self.previous_response_id,
                instructions=self.system_prompt,
            )

        else:
            response = self.client.responses.parse(
                model=self.model,
                input=self.turn_prompt + str(offer),
                text_format=ResponderResponse,
                instructions=self.system_prompt,
            )

        if type(round_chat_logs) == list:
            round_chat_logs.append(
                {
                    "agent": self.role,
                    "function": "choose_response",
                    "reason": response.output_parsed.reason,
                    "value": response.output_parsed.value,
                }
            )
        return response.output_parsed.value

    def generate_freeform_chatter(
        self, message: str, round_chat_logs: list[str] = None
    ) -> str:
        """Helper function which allows an agent to send a verbal message to another outside
        the scope of the game functions of 'split' and 'accept|not' to see if more complex behaviors arise
        """

        if self.previous_response_id:
            response = self.client.responses.parse(
                model=self.model,
                input=message,
                text_format=ChatterResponse,
                previous_response_id=self.previous_response_id,
                instructions=self.system_prompt,
            )

        else:
            response = self.client.responses.parse(
                model=self.model,
                input=message,
                text_format=ChatterResponse,
                instructions=self.system_prompt,
            )

        self.update_response_id(response)

        # store ordered chat logs for analysis if we see interesting emerging trends

        if type(round_chat_logs) == list:
            round_chat_logs.append(
                {
                    "agent": self.role,
                    "function": "generate_freeform_chatter",
                    "reason": response.output_parsed.reason,
                    "value": response.output_parsed.value,
                }
            )
        return response.output_parsed.value

    def accept_freeform_chatter(
        self, message: str, round_chat_logs: list[str] = None
    ) -> None:
        """Helper function which establishes a hear-only functionality
        that stores another agents comments in the context window for our agent"""

        if self.previous_response_id:
            response = self.client.responses.parse(
                model=self.model,
                input=message,
                previous_response_id=self.previous_response_id,
                instructions=self.system_prompt,
            )

        else:
            response = self.client.responses.parse(
                model=self.model,
                input=message,
                previous_response_id=self.previous_response_id,
                instructions=self.system_prompt,
            )

        self.update_response_id(response)
