deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]*4


def P_bust(n,placementdeck,minusten):
    if n < 17:
        p_sum = 0
        choices = list(set(placementdeck))
        randomlist = []
        randomlist.append(minusten)
        for choice in choices:
            new_deck = placementdeck.copy()
            new_deck.remove(choice)
            new_minusten = randomlist[0]
            total = n + choice
            if choice == 11:
                    new_minusten += 1
            if total > 21 and new_minusten > 0:
                new_minusten -= 1
                total -= 10
            p_sum += P_bust(total,new_deck,new_minusten)*(new_deck.count(choice)+1)/(len(new_deck)+1)
        return p_sum
    elif 16 < n < 22:
        return 0
    else:
        return 1
faceup_card = 5
deck.remove(faceup_card)
starting_hands = []
choices_2 = [2,3,4,5,6,7,8,9,10,11]
starting_minus_tens = []
matching_probability = []
bust_probability = 0
for choice_2 in choices_2:
    matching_probability.append(deck.count(choice_2)/len(deck))
    if choice_2 == 11 and faceup_card == 11:
        choice_2 = 1
        starting_minus_tens.append(1)
    elif choice_2 == 11 or faceup_card == 11:
        starting_minus_tens.append(1)
    else:
        starting_minus_tens.append(0)
    starting_hands.append(faceup_card+choice_2)
for hand in starting_hands:
    matching_deck = deck.copy()
    matching_deck.remove(choices_2[starting_hands.index(hand)])
    bust_probability += P_bust(hand,matching_deck,starting_minus_tens[starting_hands.index(hand)]) * matching_probability[starting_hands.index(hand)]
print(bust_probability*100)
