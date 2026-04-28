## placeholder, but wrapper code which runs a set of simulations
## given a fixed set of players, games, and prompts from constants
from dotenv import load_dotenv

load_dotenv()

from .agents import OpenAIUltimatumAgent, TuftsLLMProxyAgent
from .constants import *
from .game import UltimatumGameInstance


### sample interoperable flows provided for openai no/mid comms. We used the Tufts proxy for these, but this makes
### for an easier interoperable experience if somebody wanted to explore this code further
def run_openai_no_comms_flow():
    """Run demo flow and print out results json block using openai + all comms"""

    # initialize agents w/ roles
    initial_responder = OpenAIUltimatumAgent(
        name="initial_responder",
        strategy="banker",
        role="responder",
        system_prompt=BANKER_AGENT,
        responder_turn_prompt=BASE_RESPONDER_TURN_PROMPT,
        splitter_turn_prompt=BASE_SPLITTER_TURN_PROMPT,
    )

    initial_splitter = OpenAIUltimatumAgent(
        name="initial_splitter",
        role="splitter",
        strategy="ftc",
        system_prompt=FTC_AGENT,
        responder_turn_prompt=BASE_RESPONDER_TURN_PROMPT,
        splitter_turn_prompt=BASE_SPLITTER_TURN_PROMPT,
    )

    game = UltimatumGameInstance(
        initial_splitter=initial_splitter,
        initial_responder=initial_responder,
        pregame_comms_allowed=False,
        postgame_comms_allowed=False,
        midgame_comms_allowed=False,
        rounds=5,
        store_results_path="src/cs150_project/game_results/openai/",
    )

    game.play_game()


def run_openai_midgame_comms_flow():
    """Run demo flow and print out results json block using openai + all comms"""

    # initialize agents w/ roles
    initial_responder = OpenAIUltimatumAgent(
        name="initial_responder",
        strategy="banker",
        role="responder",
        system_prompt=BANKER_AGENT,
        responder_turn_prompt=BASE_RESPONDER_TURN_PROMPT,
        splitter_turn_prompt=BASE_SPLITTER_TURN_PROMPT,
    )

    initial_splitter = OpenAIUltimatumAgent(
        name="initial_splitter",
        role="ftc",
        strategy="greedy_llm",
        system_prompt=FTC_AGENT,
        responder_turn_prompt=BASE_RESPONDER_TURN_PROMPT,
        splitter_turn_prompt=BASE_SPLITTER_TURN_PROMPT,
    )

    game = UltimatumGameInstance(
        initial_splitter=initial_splitter,
        initial_responder=initial_responder,
        pregame_comms_allowed=False,
        postgame_comms_allowed=False,
        midgame_comms_allowed=True,
        rounds=5,
        store_results_path="src/cs150_project/game_results/openai/",
    )

    game.play_game()


def run_openai_all_comms_flow():
    """Run demo flow and print out results json block using openai + all comms"""

    # initialize agents w/ roles
    initial_responder = OpenAIUltimatumAgent(
        name="initial_responder",
        strategy="greedy_llm",
        role="responder",
        system_prompt=BANKER_AGENT,
        responder_turn_prompt=BASE_RESPONDER_TURN_PROMPT,
        splitter_turn_prompt=BASE_SPLITTER_TURN_PROMPT,
    )

    initial_splitter = OpenAIUltimatumAgent(
        name="initial_splitter",
        role="splitter",
        strategy="greedy_llm",
        system_prompt=FTC_AGENT,
        responder_turn_prompt=BASE_RESPONDER_TURN_PROMPT,
        splitter_turn_prompt=BASE_SPLITTER_TURN_PROMPT,
    )

    game = UltimatumGameInstance(
        initial_splitter=initial_splitter,
        initial_responder=initial_responder,
        pregame_comms_allowed=True,
        postgame_comms_allowed=True,
        midgame_comms_allowed=True,
        rounds=5,
        store_results_path="src/cs150_project/game_results/openai/",
    )

    game.play_game()


### Games Using Tufts LLM Proxy, for actual testing


def run_tufts_no_comms_flow():
    """Run demo flow and print out results json block using openai + all comms"""

    # initialize agents w/ roles
    initial_responder = TuftsLLMProxyAgent(
        name="initial_responder",
        strategy="DOC_AGENT",
        role="responder",
        system_prompt=DOC_AGENT,
        responder_turn_prompt=BASE_RESPONDER_TURN_PROMPT,
        splitter_turn_prompt=BASE_SPLITTER_TURN_PROMPT,
        model="gpt-5-mini",
    )

    initial_splitter = TuftsLLMProxyAgent(
        name="initial_splitter",
        role="splitter",
        strategy="STEIN_AGENT",
        system_prompt=STEIN_AGENT,
        responder_turn_prompt=BASE_RESPONDER_TURN_PROMPT,
        splitter_turn_prompt=BASE_SPLITTER_TURN_PROMPT,
        model="gpt-5-mini",
    )

    game = UltimatumGameInstance(
        initial_splitter=initial_splitter,
        initial_responder=initial_responder,
        pregame_comms_allowed=False,
        postgame_comms_allowed=False,
        midgame_comms_allowed=False,
        rounds=5,
        store_results_path="src/cs150_project/game_results/tufts/",
    )

    game.play_game()


def run_tufts_midgame_comms_flow():
    """Run demo flow and print out results json block using openai + all comms"""

    # initialize agents w/ roles
    initial_responder = TuftsLLMProxyAgent(
        name="initial_responder",
        strategy="DOC_AGENT",
        role="responder",
        system_prompt=DOC_AGENT,
        responder_turn_prompt=BASE_RESPONDER_TURN_PROMPT,
        splitter_turn_prompt=BASE_SPLITTER_TURN_PROMPT,
        model="gpt-5-mini",
    )

    initial_splitter = TuftsLLMProxyAgent(
        name="initial_splitter",
        role="splitter",
        strategy="STEIN_AGENT",
        system_prompt=STEIN_AGENT,
        responder_turn_prompt=BASE_RESPONDER_TURN_PROMPT,
        splitter_turn_prompt=BASE_SPLITTER_TURN_PROMPT,
        model="gpt-5-mini",
    )

    game = UltimatumGameInstance(
        initial_splitter=initial_splitter,
        initial_responder=initial_responder,
        pregame_comms_allowed=False,
        postgame_comms_allowed=False,
        midgame_comms_allowed=True,
        rounds=5,
        store_results_path="src/cs150_project/game_results/tufts/",
    )

    game.play_game()


## we ran into significant issues with content filtering, so this was used in a limited capacity in the project
def run_tufts_all_comms_flow():
    """Run demo flow and print out results json block using openai + all comms"""

    # initialize agents w/ roles
    initial_responder = TuftsLLMProxyAgent(
        name="initial_responder",
        strategy="DOC_AGENT",
        role="responder",
        system_prompt=DOC_AGENT,
        responder_turn_prompt=BASE_RESPONDER_TURN_PROMPT,
        splitter_turn_prompt=BASE_SPLITTER_TURN_PROMPT,
        model="gpt-5-mini",
    )

    initial_splitter = TuftsLLMProxyAgent(
        name="initial_splitter",
        role="splitter",
        strategy="STEIN_AGENT",
        system_prompt=STEIN_AGENT,
        responder_turn_prompt=BASE_RESPONDER_TURN_PROMPT,
        splitter_turn_prompt=BASE_SPLITTER_TURN_PROMPT,
        model="gpt-5-mini",
    )

    game = UltimatumGameInstance(
        initial_splitter=initial_splitter,
        initial_responder=initial_responder,
        pregame_comms_allowed=True,
        postgame_comms_allowed=True,
        midgame_comms_allowed=True,
        rounds=5,
        store_results_path="src/cs150_project/game_results/tufts/",
    )

    game.play_game()