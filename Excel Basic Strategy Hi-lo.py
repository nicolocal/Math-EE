import random
import sys
import xlsxwriter
sys.setrecursionlimit(1000)
workbook = xlsxwriter.Workbook("BSHi-Lo 150k 10k.xlsx")
worksheet = workbook.add_worksheet("Sheet 1")
worksheet.write(0,0,"Hand")
worksheet.write(0,1,"Money")
worksheet.write(0,2,"Bet")
worksheet.write(0,3,"Wins")
worksheet.write(0,4,"Losses")
worksheet.write(0,5,"True count")

def set_bet(deck_still,deck_gone):
    global true_count
    true_count = (deck_still.count(10)+deck_still.count(11)-deck_still.count(2)-deck_still.count(3)-deck_still.count(4)-deck_still.count(5)-deck_still.count(6))/(len(deck_still)/52)
    print("True count is = "+str(true_count))
    rounded_tc = round(true_count)
    if rounded_tc <= 1:
        return 10 
    else:
        return (rounded_tc-1)*10

decks_number = 6
deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]*(int(decks_number)*4)
card_reset_amount = 75
hands_to_play = int(input("How many hands should the AI play: "))
money = int(input("How much money does the player start with: "))
initial_bank = str(money)
random.shuffle(deck)
wins = 0
losses = 0
hands_played = 0
counting_deck = []
profits = 0

def reset():
    global deck
    deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]*(int(decks_number)*4)
    random.shuffle(deck)

def deal(deck):
    hand = []
    for i in range(2):
        card = deck.pop()
        counting_deck.append(card)
        hand.append(card)
    return hand

def play_again():
    global hands_to_play;global hands_played;global diddle
    hands_played += 1
    hands_to_play -= 1
    if len(deck) > card_reset_amount:
        again = "y"
    else:
        reset()
        again = "y"
    if again == "y" and hands_to_play != 0:
        print(bet,money)
        global player_hand;global player_hand_2; global diddle
        player_hand.clear()
        player_hand_2.clear()
        diddle = 1
    else:
        print(wins,losses,wins/(losses+wins),hands_played,money-float(initial_bank),profits)
        diddle = 0

def total(hand):
    total = 0
    ace_minus_count = hand.count(11)
    for card in hand:
        total += card
    while total > 21 and ace_minus_count > 0:
        total -= 10
        ace_minus_count -= 1
    return total

def hit(hand):
    card = deck.pop()
    counting_deck.append(card)
    hand.append(card)
    return hand

def blackjack(dealer_hand, player_hand):
    global wins;global losses;global money;global bet
    if total(player_hand) == 21 == total(dealer_hand):
        print(wins, losses)
        dealer_hand = []
        player_hand = []
        game()
    elif total(player_hand) == 21:
        money += bet*1.5
        wins += 1.5
        print(wins, losses)
        global quit;quit=True
    elif total(dealer_hand) == 21:
        money -= bet
        losses += 1
        print(wins, losses)
        quit=True
    
def score(player_hand):
        global wins;global losses;global money;global bet;global dealer_hand
        if total(player_hand) > 21:
            money -= bet
            losses += 1
        if total(player_hand)<22:
            while total(dealer_hand)<17:
                hit(dealer_hand)
            if total(dealer_hand) > 21:
                money += bet
                wins += 1
            elif total(player_hand) == 21  and total(dealer_hand)==21:
                print("push")
            elif total(player_hand) == 21:
                money += bet
                wins += 1
            elif total(dealer_hand) == 21:
                money -= bet
                losses += 1
            elif total(player_hand) > 21:
                money -= bet
                losses += 1
            elif total(dealer_hand) > 21:
                money += bet
                wins += 1
            elif total(player_hand) < total(dealer_hand):
                money -= bet
                losses += 1
            elif total(player_hand) > total(dealer_hand):
                money += bet
                wins += 1
        print(wins, losses)

def game():
    global wins;global losses;global player_hand;global quit;global quit_2;global player_hand_2;global bet;global stop;global dealer_hand
    player_hand_2 = []
    quit=False
    quit_2=False
    stop = False
    bet=set_bet(deck,counting_deck)
    dealer_hand = deal(deck)
    player_hand = deal(deck)
    print ("The dealer is showing a " + str(dealer_hand[0]))
    print ("You have a " + str(player_hand) + " for a total of " + str(total(player_hand)))
    blackjack(dealer_hand, player_hand) 
    while not quit:
        decision(player_hand, dealer_hand)
    while quit_2:
        hit(player_hand_2)
        quit_2 = False
        while not stop:
            decision(player_hand_2, dealer_hand)

hard_totals = [
    ["st","st","st","st","st","st","st","st","st","st"],
    ["st","st","st","st","st","h","h","h","h","h"],
    ["st","st","st","st","st","h","h","h","h","h"],
    ["st","st","st","st","st","h","h","h","h","h"],
    ["st","st","st","st","st","h","h","h","h","h"],
    ["h","h","st","st","st","h","h","h","h","h"],
    ["d","d","d","d","d","d","d","d","d","d"],
    ["d","d","d","d","d","d","d","d","h","h"],
    ["h","d","d","d","d","h","h","h","h","h"],
    ["h","h","h","h","h","h","h","h","h","h"],
]
soft_totals =[
    ["st","st","st","st","st","st","st","st","st","st"],
    ["st","st","st","st","d","st","st","st","st","st"],
    ["d","d","d","d","d","st","st","h","h","h"],
    ["h","d","d","d","d","h","h","h","h","h"],
    ["h","h","d","d","d","h","h","h","h","h"],
    ["h","h","d","d","d","h","h","h","h","h"],
    ["h","h","h","d","d","h","h","h","h","h"],
    ["h","h","h","d","d","h","h","h","h","h"],
]
pair_splitting = [
    ["sp","sp","sp","sp","sp","sp","sp","sp","sp","sp"],
    ["st","st","st","st","st","st","st","st","st","st"],
    ["sp","sp","sp","sp","sp","sp","st","sp","st","st"],
    ["sp","sp","sp","sp","sp","sp","sp","sp","sp","sp"],
    ["sp","sp","sp","sp","sp","sp","h","h","h","h"],
    ["sp","sp","sp","sp","sp","h","h","h","h","h"],
    ["d","d","d","d","d","d","d","d","h","h"],
    ["h","h","h","h","h","h","h","h","h","h"],
    ["h","h","sp","sp","sp","sp","h","h","h","h"],
    ["h","h","sp","sp","sp","sp","h","h","h","h"],
]
dictionary_dealer = {2:0,3:1,4:2,5:3,6:4,7:5,8:6,9:7,10:8,11:9,}
dictionary_player_hard = {21:0,20:0,19:0,18:0,17:0,16:1,15:2,14:3,13:4,12:5,11:6,10:7,9:8,8:9,7:9,6:9,5:9,4:9,3:9,}
dictionary_player_soft = {21:0,20:0,19:1,18:2,17:3,16:4,15:5,14:6,13:7,12:7,}
dictionary_player_pair = {12:0,20:1,18:2,16:3,14:4,12:5,10:6,8:7,6:8,4:9,}

def decision(playerhand, dealerhand):
        global money;global bet;global stop;global quit_2
        if playerhand[0] == playerhand [1] and len(playerhand) == 2 and len(player_hand_2) == 0:
            choice = pair_splitting[dictionary_player_pair[total(playerhand)]][dictionary_dealer[dealerhand[0]]]
        elif playerhand.count(11) > 0 and sum(playerhand) - (10*(playerhand.count(11)-1)) < 22:
            choice = soft_totals[dictionary_player_soft[total(playerhand)]][dictionary_dealer[dealerhand[0]]]
        else:
            choice = hard_totals[dictionary_player_hard[total(playerhand)]][dictionary_dealer[dealerhand[0]]]
        if choice == "d" and len(playerhand) > 3 or choice == "d" and len(player_hand_2)>0:
            choice = "h"
        global wins;global losses
        if choice == "h":
            global quit
            if len(player_hand_2) > 1:
                hit(player_hand_2)
                if total(player_hand_2) < 22:
                    print(player_hand_2)
                elif total(player_hand_2) >= 22:
                    score(player_hand)
                    score(player_hand_2)
                    stop = True
            elif len(player_hand_2)==1:
                hit(player_hand)
                if total(player_hand) > 21:
                    quit = True
            else:
                hit(player_hand)
                print(player_hand)
                if total(player_hand)>21:
                    losses += 1
                    money -= bet
                    quit=True
        elif choice == "st":
            if len(player_hand_2)==1:
                print("next hand")
            elif len(player_hand_2) >= 2:
                quit=True
                stop = True
                score(player_hand)
                score(player_hand_2)
            else:
                score(player_hand)
            quit=True
        elif choice == "sp" and len(playerhand)==2 and playerhand[0]==playerhand[1]:
            player_hand_2.append(player_hand.pop())
            hit(player_hand)
            quit_2 = True
        elif choice == "d" and len(playerhand) <= 3 and len(player_hand_2)<1:
                hit(playerhand)
                print("Hand total: " + str(total(playerhand)))
                if total(player_hand)>21:
                    money -= bet*2
                    losses += 2
                else:
                    score(player_hand);score(player_hand)
                quit=True
        elif choice == "q":
            print(wins,losses)
            quit=True;quit_2=True
            exit()

def The_Great_Reset(bankroll):
    global profits
    profits += bankroll;profits -= float(initial_bank)
    return float(initial_bank)

diddle = 1;hand = 0;bet = 0;true_count = 0
if __name__ == "__main__":
    while diddle == 1:
       worksheet.write(hand+1 ,0,hand)
       worksheet.write(hand+1 ,1,money)
       worksheet.write(hand+1 ,2,bet)
       worksheet.write(hand+1 ,3,wins)
       worksheet.write(hand+1 ,4,losses)
       worksheet.write(hand+1 ,5,true_count)
       hand += 1
       game()
       play_again()
       if money < 0.5*float(initial_bank) or money > 2*float(initial_bank):
           money = The_Great_Reset(money)
    worksheet.write(2,7,profits)
    workbook.close()
