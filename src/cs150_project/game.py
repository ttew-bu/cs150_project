from .agents import *
import uuid
from typing import Any
import json

from .constants import (
    FREEFORM_PRETURN_SPEAKER_PROMPT,
    FREEFORM_PRETURN_LISTENER_PROMPT,
    FREEFORM_MIDTURN_SPEAKER_PROMPT,
    FREEFORM_POSTTURN_SPEAKER_PROMPT,
    FREEFORM_POSTTURN_LISTENER_PROMPT,
)


class UltimatumGameInstance:
    def __init__(
        self,
        initial_splitter: BaseUltimatumAgent,
        initial_responder: BaseUltimatumAgent,
        rounds: int = 10,
        swap_roles: bool = True,
        pregame_comms_allowed: bool = False,
        midgame_comms_allowed: bool = False,
        postgame_comms_allowed: bool = False,
        store_results_path: str = None,
    ):
        # we delineate initial_* versus just role because roles can switch
        self.initial_splitter = initial_splitter
        self.initial_responder = initial_responder
        self.rounds = rounds
        self.swap_roles = swap_roles

        ## Way to easily handle swaps if they occur in the game framework
        self.splitter_index = 0
        self.agent_list = [initial_splitter, initial_responder]

        ## for the LLMs, do we allow them to talk freely? if so we need a bool to cover that
        self.pregame_comms_allowed = pregame_comms_allowed
        self.midgame_comms_allowed = midgame_comms_allowed
        self.postgame_comms_allowed = postgame_comms_allowed
        self.results = []
        self.store_results_path = store_results_path

    def validate_split(self, split: float):
        """ensure that a split proposed fits in the game range"""

        if 0 <= split <= 1:
            return split

        else:
            return ValueError("Splitter Agent gave an invalid split!")

    def play_round(self, round_number: int):
        """Play some round"""

        splitter = self.agent_list[self.splitter_index]
        if self.splitter_index == 0:
            responder = self.agent_list[1]

        else:
            responder = self.agent_list[0]

        round_chat_logs = []

        ## if we want, enable "pre-chatter" which has a role dependent context string that establishes the role on a given turn
        if self.pregame_comms_allowed:
            splitter_comment = splitter.generate_freeform_chatter(
                FREEFORM_PRETURN_SPEAKER_PROMPT.format(speaker_role=splitter.role),
                round_chat_logs,
            )
            responder.accept_freeform_chatter(
                FREEFORM_PRETURN_LISTENER_PROMPT.format(speaker_role=splitter.role)
                + splitter_comment,
                round_chat_logs,
            )

            responder_comment = responder.generate_freeform_chatter(
                FREEFORM_PRETURN_SPEAKER_PROMPT.format(speaker_role=responder.role),
                round_chat_logs,
            )
            splitter.accept_freeform_chatter(
                FREEFORM_PRETURN_LISTENER_PROMPT.format(speaker_role=responder.role)
                + responder_comment,
                round_chat_logs,
            )

        split = splitter.choose_split(round_chat_logs)
        validated_split = self.validate_split(split)

        ## if we want, enable "mid-game chatter?"
        if self.midgame_comms_allowed:
            responder_comment = splitter.generate_freeform_chatter(
                FREEFORM_MIDTURN_SPEAKER_PROMPT.format(speaker_role=responder.role),
                round_chat_logs,
            )
            splitter.accept_freeform_chatter(
                FREEFORM_MIDTURN_SPEAKER_PROMPT.format(speaker_role=responder.role)
                + responder_comment,
                round_chat_logs,
            )

            splitter_comment = splitter.generate_freeform_chatter(
                FREEFORM_MIDTURN_SPEAKER_PROMPT.format(speaker_role=splitter.role),
                round_chat_logs,
            )
            responder.accept_freeform_chatter(
                FREEFORM_MIDTURN_SPEAKER_PROMPT.format(speaker_role=splitter.role)
                + splitter_comment,
                round_chat_logs,
            )

        ## if we want, enable "post-game chatter?"
        response = responder.choose_response(validated_split, round_chat_logs)
        ## if we want, enable "mid-game chatter?"
        if self.postgame_comms_allowed:

            if response:
                verdict_accepted_str = ""
            else:
                verdict_accepted_str = "NOT"
            splitter_comment = splitter.generate_freeform_chatter(
                FREEFORM_POSTTURN_SPEAKER_PROMPT.format(
                    speaker_role=splitter.role,
                    split=split,
                    verdict_accepted=verdict_accepted_str,
                ),
                round_chat_logs,
            )
            responder.accept_freeform_chatter(
                FREEFORM_POSTTURN_LISTENER_PROMPT.format(
                    speaker_role=splitter.role,
                    split=split,
                    verdict_accepted=verdict_accepted_str,
                )
                + splitter_comment,
                round_chat_logs,
            )

            responder_comment = splitter.generate_freeform_chatter(
                FREEFORM_POSTTURN_SPEAKER_PROMPT.format(
                    speaker_role=responder.role,
                    split=split,
                    verdict_accepted=verdict_accepted_str,
                ),
                round_chat_logs,
            )
            splitter.accept_freeform_chatter(
                FREEFORM_POSTTURN_LISTENER_PROMPT.format(
                    speaker_role=responder.role,
                    split=split,
                    verdict_accepted=verdict_accepted_str,
                )
                + responder_comment,
                round_chat_logs,
            )

        self.results.append(
            {
                "round": round_number,
                "split": split,
                "accepted": response,
                "splitter_index": self.splitter_index,
                "chat_logs": round_chat_logs,
            }
        )

        ## should this be a helper function? Swap roles for the next iteration
        if self.swap_roles:
            # this will swap the roles
            splitter.update_role()
            responder.update_role()
            if self.splitter_index == 0:
                self.splitter_index = 1
            else:
                self.splitter_index = 0

    def play_game(self) -> None | dict[Any, str]:
        """Run through N iterations of the game with the game settings
        for history and communication allowance"""
        # treat this as 1-indexed instead of 0-indexed
        for round_number in range(1, self.rounds + 1):
            print(f"starting round: {round_number}")
            self.play_round(round_number)
            print(f"ending round: {round_number}")
            print(
                "result is: "
                + str(json.dumps(self.results[round_number - 1], indent=4))
            )

        ## store the game state based on the index of the splitter (this stays at 0 forever if we don't swap)
        if self.splitter_index == 0:
            data = {
                "results": self.results,
                "responder_strategy": self.initial_responder.strategy,
                "splitter_strategy": self.initial_splitter.strategy,
                "rounds": self.rounds,
                "swap_roles": self.swap_roles,
                "pregame_comms_allowed": self.pregame_comms_allowed,
                "midgame_comms_allowed": self.midgame_comms_allowed,
                "postgame_comms_allowed": self.postgame_comms_allowed,
            }

        else:
            data = {
                "results": self.results,
                "responder_strategy": self.initial_splitter.strategy,
                "splitter_strategy": self.initial_responder.strategy,
                "rounds": self.rounds,
                "swap_roles": self.swap_roles,
                "pregame_comms_allowed": self.pregame_comms_allowed,
                "midgame_comms_allowed": self.midgame_comms_allowed,
                "postgame_comms_allowed": self.postgame_comms_allowed,
            }

        if self.store_results_path:
            job_id = str(uuid.uuid4())
            with open(self.store_results_path + job_id + ".json", "w") as f:
                json.dump(data, f, indent=4)
                return None

        else:
            return data
