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
	print("4. Exit")
	answer = int(input("> "))

	if answer == 1:
		return True

	elif answer == 4:
		exit(0)

	else:
		return False

def get_sum(player):
	if "Ace" in player.print_list:
		res = (sum(player.get_cards(False)), sum(player.get_cards(False), 10))

		if res[1] > 21:
			res = res[0]

	else:
		res = sum(player.get_cards(False))

	return res

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
		time.sleep(0.5)
		player.print_cards(False)
		print(f"The dealer has {summation}")

		if type(summation) is tuple:
			check = summation[1]

		else:
			check = summation

		while check < 17 or (check == 17 and (player.get_cards(False)[0] == 1 or player.get_cards(False)[1] == 1)):
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
		print(player.get_cards(False))
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

def deal(player, is_double):
	card = cards[random.randint(1, 13)] # TODO change cards from numbers to cards and change from random to an actual deck of cards TODO
	player.add_card(card)
	print(player.get_name())
	time.sleep(0.5)

	if player.is_dealer() and len(player.get_cards(False)) == 2:
		player.print_cards(True)
		time.sleep(0.5)

	elif is_double:
		print(player.get_doubled_cards())
		time.sleep(0.5)

	else:
		player.print_cards(False)
		time.sleep(0.5)

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

					flag = True

					while flag:
						for player in player_list:
							place_bet(player)

						num_cards = 2

						while num_cards > 0:
							for player in player_list:
								if player.get_bet() > 0:
									deal(player, False)

							deal(dealer, False)

							num_cards -= 1

						for player in player_list:
							result = make_action(player, dealer.get_cards(True)[0])
							
							if result == -1:
								player_list.remove(player)

							elif result == 0:
								player.payout(player.get_bet() * 2)

							elif result == 1:
								player.payout(player.get_bet() * 0.5 + player.get_bet() * 2)

						summation = get_sum(dealer)

						dealer_sum = make_action(dealer, summation)

						# add the final sum to a member variable of each player object

						flag = again()

						for player in player_list:
							player.set_card_list([])
							player.set_print_list([])

						dealer.set_card_list([])
						dealer.set_print_list([])

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
