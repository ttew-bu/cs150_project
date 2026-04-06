# CS150: Multi-Agent Systems Final Project
### Tyler Hammerling and Tristan Tew

The ultimatum game has common solutions based on Game Theory, many of which LLMs are inevitably trained on. We've built a simple Ultimatum Game interface suitable for rules-based agents and those which use OpenAI's models as the thinking apparatus. 

We would like to test two hypotheses: 
- How faithfully do agents play roles that are given to them? Specifically those which may not align with their training data. 
- If we give the agents enhanced communication protocols (read: the ability to speak to each either before and during the turn), do the outcomes change? Do the LLMs reach cooperation or try to decieve each other?

As we look through both of these, we hope to engage in behavioral shaping through different system prompts that allows us to explore these defaults and compare to a trivial set of fixed agents (i.e. did we just spend $50 in tokens to get the same result as running two fixed strategies against each other by telling the LLMs to execute greedy strategies? Will they deviate at some point?)

Installation (using uv package manager):

Ensure you have a .env file or environment variable set for OPENAI_API_KEY
for the demo runner to automatically pick this up.

If you don't have uv installed:
```
pip install uv
```

With uv installed, you can install dependencies + create a virtualenv in the root dir using:
```uv sync```


Initiate the test runner using:
```uv run play_demo_openai_game```

OR 

```uv run play_demo_heuristic_game```