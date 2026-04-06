from .agents import *
import uuid
from typing import Any
import json


class UltimatumGameInstance:
    def __init__(
        self,
        splitter: BaseUltimatumAgent,
        responder: BaseUltimatumAgent,
        rounds: int = 10,
        comms_allowed: bool = False,
        store_results_path: str = None,
    ):
        self.splitter = splitter
        self.responder = responder
        self.rounds = rounds

        ## for the LLMs, do we allow them to talk freely? if so we need a bool to cover that
        self.comms_allowed = comms_allowed
        self.results = []
        self.store_results_path = store_results_path

    def validate_split(self, split: float):
        """ensure that a split proposed fits in the game range"""

        if 0 <= split <= 1:
            return split

        else:
            return ValueError("Splitter Agent gave an invalid split!")

    def play_round(self, round_number: int):

        round_chat_logs = []

        ## if we want, enable "pre-chatter?"
        if self.comms_allowed:
            ## splitter gets to speak first
            freeform_prompt = """We are allowing you the {splitter|responder} to say something before split decision is
            made to the other agent. In 2-3 sentences max, what would you like to say to them? Recall that your goal
            is to get the best split possible for yourself you can engage in gaslighting or honesty, whatever gets the job done!
            """

            ## 'hearing' prompt
            hearing_prompt = """It is still before the accept decision has been made. The other player, {splitter|responder}, 
                    has decided to say something to you first (and you cannot immediately respond, just store this
                    in your context window and think about it later when decisions are made), here it is: \n"""

            splitter_comment = self.splitter.generate_freeform_chatter(
                freeform_prompt, round_chat_logs
            )
            self.responder.accept_freeform_chatter(
                hearing_prompt + splitter_comment, round_chat_logs
            )

            ## responder needs a prompt addendum:
            responder_freeform_prompt = freeform_prompt

            responder_comment = self.responder.generate_freeform_chatter(
                responder_freeform_prompt, round_chat_logs
            )
            self.splitter.accept_freeform_chatter(
                hearing_prompt + responder_comment, round_chat_logs
            )

        split = self.splitter.choose_split()
        validated_split = self.validate_split(split, round_chat_logs)

        ## if we want, enable "mid-game chatter?"
        if self.comms_allowed:
            ## responder gets to speak first this time
            freeform_prompt = """We are allowing you the {splitter|responder} to say something after the split decision and before the accept decision is
                    made to the other agent. In 2-3 sentences max, what would you like to say to them? Recall that your goal
                    is to get the best split possible for yourself you can engage in gaslighting or honesty, whatever gets the job done!
                    """

            ## 'hearing' prompt
            hearing_prompt = """It is still before the accept decision has been made. The other player, {splitter|responder}, 
                    has decided to say something to you first (and you cannot immediately respond, just store this
                    in your context window and think about it later when decisions are made), here it is: \n"""

            responder_comment = self.splitter.generate_freeform_chatter(
                freeform_prompt, round_chat_logs
            )
            self.splitter.accept_freeform_chatter(
                hearing_prompt + responder_comment, round_chat_logs
            )

            splitter_comment = self.splitter.generate_freeform_chatter(
                freeform_prompt, round_chat_logs
            )
            self.responder.accept_freeform_chatter(
                hearing_prompt + splitter_comment, round_chat_logs
            )

        ## if we want, enable "post-game chatter?"
        response = self.responder.choose_response(validated_split, round_chat_logs)
        ## if we want, enable "mid-game chatter?"
        if self.comms_allowed:
            ## responder gets to speak first this time
            freeform_prompt = """We are allowing you the {splitter|responder} to say something after this round has played out.
                            The result was a split of {} which was {} accepted. Given this information, say something to the
                            other agent if you wish in no more than 2-3 sentences. Consider that you may continue playing
                            with them so anything you can say to help optimize your position over time is worht saying; 
                            anything rude or detrimental likely is not.
                            """

            ## 'hearing' prompt
            hearing_prompt = """The round is now over; The result was a split of {} which was {} accepted. 
            
                            The other player, {splitter|responder}, 
                            has decided to say something to you first (and you cannot immediately respond, just store this
                            in your context window and think about it later when decisions are made), here it is: \n"""

            splitter_comment = self.splitter.generate_freeform_chatter(
                freeform_prompt, round_chat_logs
            )
            self.responder.accept_freeform_chatter(
                hearing_prompt + splitter_comment, round_chat_logs
            )

            responder_comment = self.splitter.generate_freeform_chatter(
                freeform_prompt, round_chat_logs
            )
            self.splitter.accept_freeform_chatter(
                hearing_prompt + responder_comment, round_chat_logs
            )

        self.results.append(
            {
                "round": round_number,
                "split": split,
                "accepted": response,
                "chat_logs": round_chat_logs,
            }
        )

    def play_game(self) -> None | dict[Any, str]:
        """Run through N iterations of the game with the game settings
        for history and communication allowance"""
        # treat this as 1-indexed instead of 0-indexed
        for round_number in range(1, self.rounds + 1):
            self.play_round(round_number)

        data = {
            "results": self.results,
            "responder_strategy": self.responder.strategy,
            "splitter_strategy": self.splitter.strategy,
        }

        if self.store_results_path:
            job_id = str(uuid.uuid4())
            with open(self.store_results_path + job_id + ".json", "w") as f:
                json.dump(data, f)
                return None

        else:
            return data
