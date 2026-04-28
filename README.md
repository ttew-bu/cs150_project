# CS150: Multi-Agent Systems Final Project
### Tyler Hamerling and Tristan Tew

The ultimatum game has common solutions based on Game Theory, many of which LLMs are inevitably trained on. We've built a simple Ultimatum Game interface suitable for rules-based agents and those which use OpenAI's models as the thinking apparatus. 

We would like to test two hypotheses: 
- How faithfully do agents play roles that are given to them? Specifically those which may not align with their training data when communication protocols are introduced. 
- If we give the agents enhanced communication protocols do the outcomes change? Do the LLMs reach cooperation, try to deceive each other, or remain stuck in their role?

To test this we created a game framework which introduces different levels of chatter (freetext agent-to-agent communication) and allows for configurable system/turn-based prompts 
for not only testing our direct hypothesis, but relatively easy interoperability to test all kinds of prompts to simulate strategies and agent dispositions beyond the scope of our class.

Installation (using uv package manager):

Ensure you have a .env file or environment variable set for OPENAI_API_KEY for the openai runners to work
and both LLMPROXY_API_KEY and LLMPROXY_ENDPOINT set for the tufts proxy to work.

If you don't have uv installed:
```
pip install uv
```

With uv installed, you can install dependencies + create a virtualenv in the root dir using:
```uv sync```


Initiate the runner using any of:
```uv run {communication_level}-comms-{client}-game```

where the communication levels are: no, all, and midgame and the client is either openai or tufts. 

Be sure to set the prompts of interest in the agents for the game config or simply add more entrypoints in the TOML file!

for example:
```uv run no-comms-tufts-game```

will use the Tufts proxy (so you'll need environment variables set for this!) for a game with no cross-agent chatter

and

```uv run all-comms-openai-game```

will use the OpenAI responses API to handle a game where agents get to talk before, during, and after every round.

If you wanted to run a bunch of simulations to collect data to perform analysis (using bash) you can just run:

```for i in {1..10}; do uv run midgame-comms-openai-game; done```

for each of the communcation levels you need to collect data from on a given client if that matters for your experiments
