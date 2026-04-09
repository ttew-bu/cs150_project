## placeholder, but wrapper code which runs a set of simulations
## given a fixed set of players, games, and prompts from constants
from dotenv import load_dotenv

load_dotenv()

from .agents import OpenAIUltimatumAgent
from .constants import *
from .game import UltimatumGameInstance


def run_demo_llm_flow():
    """Run demo flow and print out results json block. """

    # initialize agents w/ roles
    responder = OpenAIUltimatumAgent(
        role="responder",
        strategy="greedy_llm",
        system_prompt=GREEDY_TO_FLEX_SYSTEM_PROMPT,
        turn_prompt=BASE_RESPONDER_TURN_PROMPT,
    )

    splitter = OpenAIUltimatumAgent(
        role="splitter",
        strategy="greedy_llm",
        system_prompt=GREEDY_TO_FLEX_SYSTEM_PROMPT,
        turn_prompt=BASE_SPLITTER_TURN_PROMPT,
    )

    game = UltimatumGameInstance(
        splitter=splitter, responder=responder, comms_allowed=True, rounds=3
    )

    game.play_game()
