import time
import random
import players

cards = {
	1: "Ace",
	2: 2,
	3: 3,
	4: 4,
	5: 5,
	6: 6,
	7: 7,
	8: 8,
	9: 9,
	10: 10,
	11: "Jack",
	12: "Queen",
	13: "King"
}

def display_strategy():
	# TODO
	pass

def display_rules():
	# TODO
	pass

def ai_play():
	# TODO
	pass

def again():
	print("Would you like to play again?")
	print("Make a selection")
	print("1. Yes")
	print("2. No")
	print("3. Change players")
	print("4. Display balance")
	print("5. Exit")
	answer = int(input("> "))

	return answer

def get_sum(player):
	if "Ace" in player.print_list:
		res = (sum(player.get_cards(False)), sum(player.get_cards(False), 10))

		if res[1] > 21:
			res = res[0]

	else:
		res = sum(player.get_cards(False))

	return res

def showdown(player_list, dealer_sum):
	for player in player_list:
		player.print_doubled_cards()

		summation = get_sum(player)

		if summation == 8 or summation == 1 or summation == 11 or summation == 18:
			if dealer_sum == 1:
				print(f"{player.get_name()} has an {summation} to the dealer's 1 or 11")

			else:
				print(f"{player.get_name()} has an {summation} to the dealer's {dealer_sum}")

		else:
			print(f"{player.get_name()} has a {summation} to the dealer's {dealer_sum}")

def double(player):
	player.place_bet(player.get_bet())
	deal(player, True)

def request_action(player, dealer_sum):
	summation = get_sum(player)

	if summation == 8 or summation == 1 or summation == 11 or summation == 18:
		if dealer_sum == 1:
			print(f"You have an {summation} to the dealer's 1 or 11")

		else:
			print(f"You have an {summation} to the dealer's {dealer_sum}")

	else:
		print(f"You have a {summation} to the dealer's {dealer_sum}")

	print(f"What would you like to do, {player.get_name()}?")
	print("1. Hit")
	print("2. Stand")
	print("3. Double")
	
	if player.get_cards(False)[0] == player.get_cards(False)[1]:
		print("4. Split")

	print("Make a selection")
	action = int(input("> "))

	return action

def make_action(player, dealer_sum):
	summation = get_sum(player)

	if player.is_dealer():
		print(player.get_name())
		time.sleep(1)
		player.print_cards(False)
		print(f"The dealer has {summation}")

		if type(summation) is tuple:
			check = summation[1]

		else:
			check = summation

		while check < 17 or (check == 17 and len(player.get_cards(False)) == 2 and (player.get_cards(False)[0] == 1 or player.get_cards(False)[1] == 1)):
			deal(player, False)

			summation = get_sum(player)

			if type(summation) is tuple:
				check = summation[1]

			else:
				check = summation

			print(f"The dealer has {summation}")

			if check > 21:
				return -1

		return summation

	else:
		if summation == 21:
			print("BLACKJACK")
			return 1

		flag = True

		while flag:
			summation = get_sum(player)

			if type(summation) is tuple:
				check = summation[0]

			else:
				check = summation

			if check > 21:
				print("BUST")
				return -1

			action = request_action(player, dealer_sum)
			
			match action:
				# Hit
				case 1:
					deal(player, False)

				# Stand
				case 2:
					flag = False

				# Double
				case 3:
					double(player)
					flag = False

				# Split
				case 4:
					# TODO this is wrong - need to figure out a better way to split TODO
					# TODO ok, wait actually maybe this could work... TODO
					# make a new player and insert it in the player list right after the player chosing to split
					player_list.insert(player.get_index() + 1, players.Player(player.get_name() + "_split", player.get_index() + 1))
					deal(player, False)

		return get_sum(player)

def has_blackjack(player):
	first_card = player.get_cards(False)[0]
	second_card = player.get_cards(False)[1]

	if first_card == 10 or first_card == 1:
		if first_card == 10 and second_card == 1:
			return True

		if first_card == 1 and second_card == 10:
			return True

	return False

def deal(player, is_double):
	card = cards[random.randint(1, 13)] # TODO change cards from numbers to cards and change from random to an actual deck of cards TODO
	player.add_card(card)
	print(player.get_name())
	time.sleep(1)

	if player.is_dealer() and len(player.get_cards(False)) == 2:
		player.print_cards(True)
		time.sleep(1)

	elif is_double:
		print(player.get_doubled_cards())
		time.sleep(1)

	else:
		player.print_cards(False)
		time.sleep(1)

def place_bet(player):
	print("How much would you like to bet?")
	print("Enter a dollar amount")
	bet = int(input("> "))
	player.place_bet(bet)

def get_name(index):
	print(f"Enter player {index + 1}'s name")
	name = input("> ")

	return name

def player_play():
	print("How many players are playing?")
	print("Enter a number")
	selection = int(input("> "))

	return selection

def play_menu():
	print("Would you like to play or watch the AI?")
	print("1. I would like to play")
	print("2. I would like to watch the AI")
	print("Make a selection")
	selection = int(input("> "))

	return selection

def menu_help():
	print("Please enter a number between 1 and 3")

def startup():
	print("Welcome to Jack's Blackjack!!!")
	print("Menu")
	print("1. Play")
	print("2. Rules")
	print("3. Strategy")
	print("Make a selection")
	selection = int(input("> "))

	return selection

def main():
	selection = startup()

	match selection:
		case 1:
			dealer = players.Dealer("dealer", -1)
			play_selection = play_menu()

			match play_selection:
				case 1:
					player_list = []
					num_players = player_play()

					for i in range(num_players):
						player_list.insert(i, players.Player(get_name(i), i))

					flag = 1

					while flag:
						for player in player_list:
							player.is_playing = True
							place_bet(player)

						num_cards = 2

						while num_cards > 0:
							for player in player_list:
								if player.get_bet() > 0:
									deal(player, False)

							deal(dealer, False)

							num_cards -= 1

						dealer_has_blackjack = has_blackjack(dealer)

						# dealer wins with blackjack
						if dealer_has_blackjack:
							print("Dealer has BLACKJACK")
							flag = again()
							continue

						for player in player_list:
							player_has_blackjack = has_blackjack(player)

							# player wins with blackjack
							if player_has_blackjack:
								print(f"{player.get_name()} has BLACKJACK")
								player.payout(player.get_bet() * 0.5 + player.get_bet() * 2)

						for player in player_list:
							if player.is_playing:
								player_final_sum = make_action(player, dealer.get_cards(True)[0])
								
								# TODO fix/change this because players should stay in the list
								if player_final_sum == -1:
									player.payout(0)

								# add the final sum to a member variable of each player object
								player.add_result(player_final_sum)

						showdown(player_list, dealer.get_cards(True)[0])

						summation = get_sum(dealer)
						dealer_final_sum = make_action(dealer, summation)

						# add the final sum to a member variable of each player object
						dealer.add_result(dealer_final_sum)

						for player in player_list:
							player_summation = player.get_final_sum()
							dealer_summation = dealer.get_final_sum()

							if type(player_summation) is tuple:
								player_check = player_summation[1]

							else:
								player_check = player_summation

							if type(dealer_summation) is tuple:
								dealer_check = dealer_summation[1]

							else:
								dealer_check = dealer_summation

							# normal win
							if player_check > dealer_check:
								print(f"{player.get_name()} WINS")
								player.payout(player.get_bet() * 2)

							# push
							elif player_check == dealer_check:
								print(f"{player.get_name()} made a PUSH")
								player.payout(player.get_bet())

							elif player_check < dealer_check:
								print(f"{player.get_name()} LOSES")

						flag = again()

						for player in player_list:
							player.set_card_list([])
							player.set_print_list([])
							player.set_doubled_card(-1)

						dealer.set_card_list([])
						dealer.set_print_list([])

						match flag:
							case 2:
								pass

							case 3:
								pass

							case 4:
								for player in player_list:
									print(player.get_balance())

							case 5:
								exit(0)

				case 2:
					ai_play()

		case 2:
			display_rules()

		case 3:
			display_strategy()

		case _:
			menu_help()

if __name__ == '__main__':
	main()
