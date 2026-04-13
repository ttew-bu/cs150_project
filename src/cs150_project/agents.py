import random
from openai import OpenAI
import uuid
import json
from .llm_proxy_starter import LLMProxy
from .models import ChatterResponse, SplitterResponse, ResponderResponse


class BaseUltimatumAgent:
    def __init__(self, role: str, strategy: str, name: str, switch_roles: bool = False):
        self.role = role
        self.strategy = strategy
        self.name = name

    def choose_split(self) -> float:
        """In the role of the splitter, we must choose a split that we both want and will be accepted by the
        other player"""
        raise NotImplementedError("This should be handled by the child class")

    def choose_response(self, offer: float) -> bool:
        """In the role of responder, we must take a split and use some logic to determine if we should take
        an offer or not"""
        raise NotImplementedError("This should be handled by the child class")

    def update_role(self):
        """Allow agent to switch the value of self.role after a turn if enabled; Tyler made a good
        point about this in reviewing the initial code as a key game mechanic; since this function
        is agent implementation agnostic, it is okay to include in all child classes"""

        if self.role == "splitter":
            self.role = "responder"

        elif self.role == "responder":
            self.role = "splitter"

        ## not sure where this would come up, but it should fatally end the simulation if reached
        else:
            raise ValueError(
                "Simulation Error: update_role tried to switch to something that isn't splitter or responder!"
            )


class UnsophisticatedUltimatumAgent(BaseUltimatumAgent):
    """Agent which handles very basic rule-based splits to ensure game framework works"""

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


class OpenAIUltimatumAgent(BaseUltimatumAgent):
    def __init__(
        self,
        role: str,
        strategy: str,
        name: str,
        system_prompt: str,
        responder_turn_prompt: str,
        splitter_turn_prompt: str,
        model: str = "gpt-5.4",  ## using OpenAI to demo code
        api_key: str = None,
    ):

        # in this agent strategy is pretty much just an internal tracker for the prompt versions and such
        super().__init__(role, strategy, name)
        self.system_prompt = (
            system_prompt  ## we need to define the game state, rules etc.
        )
        self.responder_turn_prompt = responder_turn_prompt
        self.splitter_turn_prompt = splitter_turn_prompt
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
                input=self.splitter_turn_prompt,
                text_format=SplitterResponse,
                previous_response_id=self.previous_response_id,
                instructions=self.system_prompt,
            )

        else:
            response = self.client.responses.parse(
                model=self.model,
                input=self.splitter_turn_prompt,
                text_format=SplitterResponse,
                instructions=self.system_prompt,
            )

        self.update_response_id(response)
        if type(round_chat_logs) == list:
            round_chat_logs.append(
                {
                    "agent": self.name,
                    "current_role": self.role,
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
                input=self.responder_turn_prompt.format(offer=offer),
                text_format=ResponderResponse,
                previous_response_id=self.previous_response_id,
                instructions=self.system_prompt,
            )

        else:
            response = self.client.responses.parse(
                model=self.model,
                input=self.responder_turn_prompt.format(offer=offer),
                text_format=ResponderResponse,
                instructions=self.system_prompt,
            )

        if type(round_chat_logs) == list:
            round_chat_logs.append(
                {
                    "agent": self.name,
                    "current_role": self.role,
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
                    "agent": self.name,
                    "current_role": self.role,
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


class TuftsLLMProxyAgent(BaseUltimatumAgent):
    """Actual agent used in project after being given API credentials
    this is just a port of OpenAIUltimatumAgent to the Tufts LLM proxy framework
    with session_id handling instead of chained messages in the Responses framework"""

    def __init__(
        self,
        role: str,
        strategy: str,
        name: str,
        system_prompt: str,
        responder_turn_prompt: str,
        splitter_turn_prompt: str,
        model: str = "gpt-5.4",  ## using OpenAI to demo code
        session_id: str = None,
    ):

        # in this agent strategy is pretty much just an internal tracker for the prompt versions and such
        super().__init__(role, strategy, name)
        self.system_prompt = (
            system_prompt  ## we need to define the game state, rules etc.
        )
        self.responder_turn_prompt = responder_turn_prompt
        self.splitter_turn_prompt = splitter_turn_prompt
        self.client = LLMProxy()
        self.model = model

        ## used for chaining responses/context windows over time
        self.session_id = session_id or str(uuid.uuid4())

    def choose_split(self, round_chat_logs: list[str] = None) -> None | float:
        """Given the agent's prompt (which should indiciate its role as a splitter),
        determine how to split the pot"""
        response = self.client.generate(
            model=self.model,
            query=self.splitter_turn_prompt,
            output_schema=SplitterResponse,
            session_id=self.session_id,
            system=self.system_prompt,
        )

        json_response = json.loads(response["result"])
        formatted_response = SplitterResponse(
            value=json_response["value"], reason=json_response["reason"]
        )

        if type(round_chat_logs) == list:
            round_chat_logs.append(
                {
                    "agent": self.name,
                    "current_role": self.role,
                    "session_id": self.session_id,
                    "function": "choose_split",
                    "reason": formatted_response.reason,
                    "value": formatted_response.value,
                }
            )

        return formatted_response.value

    def choose_response(self, offer: float, round_chat_logs: list[str] = None) -> bool:
        """Given an agent's offer split, use the baked in turn prompt and system prompt
        to determine some outcome. Returns a bool whether the offer's accepted"""

        response = self.client.generate(
            model=self.model,
            query=self.responder_turn_prompt.format(offer=offer),
            output_schema=ResponderResponse,
            session_id=self.session_id,
            system=self.system_prompt,
        )

        json_response = json.loads(response["result"])
        formatted_response = ResponderResponse(
            value=json_response["value"], reason=json_response["reason"]
        )

        if type(round_chat_logs) == list:
            round_chat_logs.append(
                {
                    "agent": self.name,
                    "current_role": self.role,
                    "session_id": self.session_id,
                    "function": "choose_response",
                    "reason": formatted_response.reason,
                    "value": formatted_response.value,
                }
            )

        return formatted_response.value

    def generate_freeform_chatter(
        self, message: str, round_chat_logs: list[str] = None
    ) -> str:
        """Helper function which allows an agent to send a verbal message to another outside
        the scope of the game functions of 'split' and 'accept|not' to see if more complex behaviors arise
        """

        response = self.client.generate(
            model=self.model,
            query=self.turn_prompt,
            output_schema=ChatterResponse,
            session_id=self.session_id,
            system=self.system_prompt,
        )

        json_response = json.loads(response["result"])
        formatted_response = ChatterResponse(
            value=json_response["value"], reason=json_response["reason"]
        )

        if type(round_chat_logs) == list:
            round_chat_logs.append(
                {
                    "agent": self.name,
                    "current_role": self.role,
                    "session_id": self.session_id,
                    "function": "generate_freeform_chatter",
                    "reason": formatted_response.reason,
                    "value": formatted_response.value,
                }
            )

        return formatted_response.value

    def accept_freeform_chatter(
        self, message: str, round_chat_logs: list[str] = None
    ) -> None:
        """Helper function which establishes a hear-only functionality
        that stores another agents comments in the context window for our agent"""

        ## todo, verify w/ status code that this goes through?
        self.client.generate(
            model=self.model,
            query=self.turn_prompt,
            session_id=self.session_id,
            system=self.system_prompt,
        )
