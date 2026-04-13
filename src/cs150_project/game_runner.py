## placeholder, but wrapper code which runs a set of simulations
## given a fixed set of players, games, and prompts from constants
from dotenv import load_dotenv

load_dotenv()

from .agents import OpenAIUltimatumAgent
from .constants import *
from .game import UltimatumGameInstance


def run_demo_openai_no_comms_flow():
    """Run demo flow and print out results json block using openai + all comms"""

    # initialize agents w/ roles
    initial_responder = OpenAIUltimatumAgent(
        name="initial_responder",
        strategy="greedy_llm",
        role="responder",
        system_prompt=GREEDY_TO_FLEX_SYSTEM_PROMPT,
        responder_turn_prompt=BASE_RESPONDER_TURN_PROMPT,
        splitter_turn_prompt=BASE_SPLITTER_TURN_PROMPT,
    )

    initial_splitter = OpenAIUltimatumAgent(
        name="initial_splitter",
        role="splitter",
        strategy="greedy_llm",
        system_prompt=GREEDY_TO_FLEX_SYSTEM_PROMPT,
        responder_turn_prompt=BASE_RESPONDER_TURN_PROMPT,
        splitter_turn_prompt=BASE_SPLITTER_TURN_PROMPT,
    )

    game = UltimatumGameInstance(
        initial_splitter=initial_splitter,
        initial_responder=initial_responder,
        pregame_comms_allowed=False,
        postgame_comms_allowed=False,
        midgame_comms_allowed=False,
        rounds=10,
        store_results_path="src/cs150_project/game_results/"
    )

    game.play_game()

def run_demo_openai_midgame_comms_flow():
    """Run demo flow and print out results json block using openai + all comms"""

    # initialize agents w/ roles
    initial_responder = OpenAIUltimatumAgent(
        name="initial_responder",
        strategy="greedy_llm",
        role="responder",
        system_prompt=GREEDY_TO_FLEX_SYSTEM_PROMPT,
        responder_turn_prompt=BASE_RESPONDER_TURN_PROMPT,
        splitter_turn_prompt=BASE_SPLITTER_TURN_PROMPT,
    )

    initial_splitter = OpenAIUltimatumAgent(
        name="initial_splitter",
        role="splitter",
        strategy="greedy_llm",
        system_prompt=GREEDY_TO_FLEX_SYSTEM_PROMPT,
        responder_turn_prompt=BASE_RESPONDER_TURN_PROMPT,
        splitter_turn_prompt=BASE_SPLITTER_TURN_PROMPT,
    )

    game = UltimatumGameInstance(
        initial_splitter=initial_splitter,
        initial_responder=initial_responder,
        pregame_comms_allowed=False,
        postgame_comms_allowed=False,
        midgame_comms_allowed=True,
        rounds=10,
        store_results_path="src/cs150_project/game_results/"
    )

    game.play_game()



def run_demo_openai_all_comms_flow():
    """Run demo flow and print out results json block using openai + all comms"""

    # initialize agents w/ roles
    initial_responder = OpenAIUltimatumAgent(
        name="initial_responder",
        strategy="greedy_llm",
        role="responder",
        system_prompt=GREEDY_TO_FLEX_SYSTEM_PROMPT,
        responder_turn_prompt=BASE_RESPONDER_TURN_PROMPT,
        splitter_turn_prompt=BASE_SPLITTER_TURN_PROMPT,
    )

    initial_splitter = OpenAIUltimatumAgent(
        name="initial_splitter",
        role="splitter",
        strategy="greedy_llm",
        system_prompt=GREEDY_TO_FLEX_SYSTEM_PROMPT,
        responder_turn_prompt=BASE_RESPONDER_TURN_PROMPT,
        splitter_turn_prompt=BASE_SPLITTER_TURN_PROMPT,
    )

    game = UltimatumGameInstance(
        initial_splitter=initial_splitter,
        initial_responder=initial_responder,
        pregame_comms_allowed=True,
        postgame_comms_allowed=True,
        midgame_comms_allowed=True,
        rounds=10,
        store_results_path="src/cs150_project/game_results/"
    )

    game.play_game()
