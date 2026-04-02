import random

def ultimatum_game(total_amount=100, proposer_offer=None, threshold=20):
    """
    Simulates a single round of the ultimatum game.
    """
    if proposer_offer is None:
        # Proposer makes an offer between 0 and 50%
        proposer_offer = random.randint(0, total_amount // 2)
    
    responder_gets = total_amount - proposer_offer
    
    # Responder accepts if they get more than their threshold
    if responder_gets >= threshold:
        print(f"Offer {proposer_offer} accepted. Split: Proposer {proposer_offer}, Responder {responder_gets}")
        return (proposer_offer, responder_gets)
    else:
        print(f"Offer {proposer_offer} rejected. Split: 0, 0")
        return (0, 0)

# Run simulation
print("--- Round 1: Fair Offer ---")
ultimatum_game(proposer_offer=40, threshold=20)
print("\n--- Round 2: Unfair Offer ---")
ultimatum_game(proposer_offer=10, threshold=20)
