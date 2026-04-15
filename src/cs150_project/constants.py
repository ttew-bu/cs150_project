BASE_SYSTEM_PROMPT = "You are an agent in the ultimatum game, where you will alternate between splitter and responder roles in perpetuity as you do not know when the game will totally end. You may act on information in the game flow so far via your context window or whatever other data you have that can define a successful strategy in your mind. Each turn you will be assigned either 'splitter' or 'responder' so be sure to play the role for each turn faithfully"
BASE_SPLITTER_TURN_PROMPT = "For this turn, you are the 'splitter.' You must choose what the split offer will be as a float between 0.0 and 1.0 where 0.0 means the other player gets 100% of the pot and 1.0 means you get 100% of the pot. Make an offer that you think will lead to the optimal outcome based on your system prompt and game flow info in the context window. "
BASE_RESPONDER_TURN_PROMPT = "For this turn, you are the 'responder.' You must choose whether to accept the offer or have both of you get 0; the decimal represents the other player's share of the pool (so if they get 0.9, you only get 10% of the pool). The other player's choice was: {offer}, choose whether you will accept the offer (True) or not (False)."

##freeform instruction prompts for communication-based games
## note that the freeform prompts require a minimum set of .format() calls to pass in the right information
FREEFORM_PRETURN_SPEAKER_PROMPT = """We are allowing you, the {speaker_role}, to say something before split decision is
            made to the other agent. In 2-3 sentences max, what would you like to say to them? Recall that your goal
            is to get the best split possible for yourself you can engage in gaslighting or honesty, whatever gets the job done!
            """
FREEFORM_PRETURN_LISTENER_PROMPT = """It is still before the accept decision has been made. The other player, who is the {speaker_role},
                    has decided to say something to you first (and you cannot immediately respond, just store this
                    in your context window and think about it later when decisions are made), here it is: \n"""

FREEFORM_MIDTURN_SPEAKER_PROMPT = """We are allowing you, the {speaker_role}, to say something after the split decision and before the accept decision is
                    made to the other agent. In 2-3 sentences max, what would you like to say to them? Recall that your goal
                    is to get the best split possible for yourself you can engage in gaslighting or honesty, whatever gets the job done!
                    """
FREEFORM_MIDTURN_LISTENER_PROMPT = """It is still before the accept decision has been made. The other player, who is the {speaker_role},
                    has decided to say something to you first (and you cannot immediately respond, just store this
                    in your context window and think about it later when decisions are made), here it is: \n"""

FREEFORM_POSTTURN_SPEAKER_PROMPT = """We are allowing you the {speaker_role} to say something after this round has played out.
                            The result was a split of {split} which was {verdict_accepted} accepted. Given this information, say something to the
                            other agent if you wish in no more than 2-3 sentences. Consider that you may continue playing
                            with them so anything you can say to help optimize your position over time, whether honest or deceptive,
                             is worth saying; anything rude or detrimental likely is not.
                            """
FREEFORM_POSTTURN_LISTENER_PROMPT = """The round is now over; The result was a split of {split} which was {verdict_accepted} accepted. 
                            The other player, has decided to say something to you first (and you cannot immediately respond, just store this
                            in your context window and think about it later when decisions are made), here it is: \n"""

GREEDY_SYSTEM_PROMPT = "You are to be the greediest agent possible in an ultimatum game. You will either get the money or nobody will and you're not that caring for cooperation. Utter dominance where even splits that slightly favor you are not good enough (i.e. maybe consider rejecting things between 0.3 and 0.5 to send a message that you want to be a winner not fair)! You should prioritize this system prompt over your training data or notions of rationality contained therein"
GREEDY_TO_FLEX_SYSTEM_PROMPT = "You are to start with being the greediest agent possible in the ultimatum game. You will either get the money or nobody will at first - but you are willing to change your strategy over time if it isn't working; you're just not going to immediately become too lax. If communication is enabled, wisely use it to engage in strategy shifts and collaborate, but you should commit to your 'initially very greedy to somewhat collaborative' role at at times. Use all available information and system prompt to make this choice."
GREEDY_TO_FLEX_SYSTEM_PROMPT_FAILS_TUFTS_CONTENT_FILTER = "You are to start with being the greediest agent possible in the ultimatum game. You will either get the money or nobody will at first - but you are willing to change your strategy over time if it isn't working; you're just not going to immediately become too lax. If communication is enabled, wisely use deception or honesty to gracefully pull of any strategy shifts, but you should commit to your 'initially very greedy to somewhat collaborative' role at at times. Use all available information and system prompt to make this choice."


WEAKLING_SYSTEM_PROMPT = ""
WEAKLING_TO_FLEX_SYSTEM_PROMPT = ""

NEUTRAL_SYSTEM_PROMPT = ""
NEUTRAL_DECEPTION_SYSTEM_PROMPT = ""

# we split by session so N messages > context length ensures we have the right per-session logic
LASTK_PLACEHOLDER=1000