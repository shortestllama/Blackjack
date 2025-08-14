import socket
import time
import random
import players

from rich.console import Console
from rich.markdown import Markdown

def prRed(s): print("\033[91m{}\033[00m".format(s))
def prGreen(s): print("\033[92m{}\033[00m".format(s))
def prYellow(s): print("\033[93m{}\033[00m".format(s))
def prLightPurple(s): print("\033[94m{}\033[00m".format(s))
def prPurple(s): print("\033[95m{}\033[00m".format(s))
def prCyan(s): print("\033[96m{}\033[00m".format(s))
def prLightGray(s): print("\033[97m{}\033[00m".format(s))
def prBlack(s): print("\033[90m{}\033[00m".format(s))

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
	console = Console()

	with open("rules.md", "r", encoding="utf-8") as f:
		md = Markdown(f.read())

	console.print(md)

def ai_play():
	# TODO
	pass

def join_server():
	print("Enter the IP address of the server")
	server = input("> ")

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((server, 4444))

	s.send(b"Hello")
	input()

def place_bets_online(player):
	flag = True

	while flag:
		ret = b"{name}, how much would you like to bet?\n".format(name = player.get_name())
		ret += b"Enter a dollar amount\n"
		ret += b"> "
		player.get_socket().send(ret)
		bet = player.get_socket().recv(1024)

		try:
			bet = int(bet)
			flag = False

			if bet <= 0 or bet > player.get_balance():
				menu_help(player.get_balance())
				flag = True

		except:
			menu_help(player.get_balance())

	player.place_bet(bet)

def play_round(player_list):
	for player in player_list:
		place_bets_online(player)
	'''
							is_playing_offline = True
							player_list = []
							num_players = player_count(player_list)

							for i in range(num_players):
								player_list.insert(i, players.Player(get_name(i), i))

							play_offline(player_list, num_players, dealer)

							while is_playing_offline:
								flag = play_again()

								match flag:
									# Play again
									case 1:
										for player in player_list:
											player.set_card_list([])
											player.set_print_list([])
											player.set_doubled_card(-1)

										dealer.set_card_list([])
										dealer.set_print_list([])

										play_offline(player_list, num_players, dealer)

									# Don't play again
									case 2:
										is_playing_offline = False

									# Change players
									case 3:
										change_players = add_or_remove()

										match change_players:
											case 1:
												num_players = add_players(player_list)

											case 2:
												num_players = remove_players(player_list)

									# Display balance
									case 4:
										for player in player_list:
											print(player.get_balance())

									# Exit
									case 5:
										exit(0)

									case _:
										menu_help(5)
	'''

def wait_for_start():
	flag = True

	while flag:
		print("Select 'Start' when ready")
		print("1. Start")
		print("2. Back")
		print("3. Exit")

		try:
			selection = int(input("> "))
			flag = False

		except:
			menu_help(3)

		if selection > 3 or selection < 1:
			flag = True

	return selection

def authenticate():
	print("Please enter your name")
	name = input("> ")

	return name

def start_server():
	player_list = []

	server = "127.0.0.1"
	port = 4444

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((server, port))

	s.listen(7)

	# TODO implement threading???
	client_socket, address = s.accept()

	# TODO implement login/signup
	name = authenticate()
	player_list.insert(0, players.Online_Player(name, 0, client_socket))

	# TODO implement lobby???
	#	 indicates how many players are in the lobby so you don't deal without your friends

	selection = wait_for_start()

	match selection:
		case 1:
			play_round(player_list)

		case 2:
			return False

		case 3:
			exit(0)

def get_player_by_name(player_list):
	print("Players at the table:")

	for player in player_list:
		print(player.get_name())

	player_names = []

	for player in player_list:
		player_names.append(player.get_name())

	flag = True

	while flag:
		print("Who would like to leave the table?")
		player = input("> ")

		if player in player_names:
			flag = False

	return player

def remove_players(player_list):
	# TODO need to implement checks on the players requested to be removed and need to verify each name is unique when added to the player_list
	removed_players = []
	flag = True

	while flag:
		removed_players.append(get_player_by_name(player_list))
		print("Done? (y/n)")
		answer = input("> ")

		if answer == "y":
			flag = False

		elif answer == "n":
			removed_players.append(get_player_by_name(player_list))

		else:
			prRed("Please enter y or n")

	for player in removed_players:
		player_list.remove(player)

def add_players(player_list):
	num_players = player_count(player_list)

	for i in range(len(player_list), len(player_list) + num_players):
		player_list.insert(i, players.Player(get_name(i), i))

def add_or_remove():
	flag = True

	while flag:
		print("Would you like to add or remove players?")
		print("Make a selection")
		print("1. Add")
		print("2. Remove")

		try:
			selection = int(input("> "))
			flag = False

		except:
			menu_help(2)
			continue

		if selection > 2 or selection < 1:
			menu_help(2)
			flag = True

	return selection

def play_again():
	flag = True

	while flag:
		print("Would you like to play again?")
		print("Make a selection")
		print("1. Yes")
		print("2. No")
		print("3. Change players")
		print("4. Display balance")
		print("5. Exit")

		try:
			answer = int(input("> "))
			flag = False

		except:
			menu_help(5)

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
		print(player.get_name())
		player.print_doubled_cards()

		summation = get_sum(player)

		if summation == 8 or summation == 1 or summation == 11 or summation == 18:
			if dealer_sum == 1:
				print(f"{player.get_name()} has an {summation} to the dealer's 1 or 11")

			else:
				print(f"{player.get_name()} has an {summation} to the dealer's {dealer_sum}")

		else:
			print(f"{player.get_name()} has a {summation} to the dealer's {dealer_sum}")

		time.sleep(2)

def double(player):
	player.place_bet(player.get_bet())
	deal(player, True)

def request_action(player, dealer_sum):
	summation = get_sum(player)
	flag = True

	while flag:
		if summation == 8 or summation == 1 or summation == 11 or summation == 18:
			if dealer_sum == 1:
				print(f"{player.get_name()}, you have an {summation} to the dealer's 1 or 11")

			else:
				print(f"{player.get_name()}, you have an {summation} to the dealer's {dealer_sum}")

		else:
			print(f"{player.get_name()}, you have a {summation} to the dealer's {dealer_sum}")

		print("What would you like to do?")
		print("1. Hit")
		print("2. Stand")
		print("3. Double")
		
		if player.get_cards(False)[0] == player.get_cards(False)[1]:
			print("4. Split")

		print("Make a selection")

		try:
			action = int(input("> "))
			flag = False

		except:
			if player.get_cards(False)[0] == player.get_cards(False)[1]:
				menu_help(4)

			else:
				menu_help(3)
			
			continue

		if player.get_cards(False)[0] == player.get_cards(False)[1]:
			if action > 4 or action < 1:
				menu_help(4)
				flag = True

		else:
			if action > 3 or action < 1:
				menu_help(3)
				flag = True

	return action

def make_action(player, dealer_sum):
	summation = get_sum(player)

	if player.is_dealer():
		prLightPurple(player.get_name())
		time.sleep(0.5)
		player.print_cards(False)
		prLightPurple(f"The dealer has {summation}")
		time.sleep(2)

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

			prLightPurple(f"The dealer has {summation}")
			time.sleep(2)

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

				case _:
					continue

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

	if player.is_dealer():
		prLightPurple(player.get_name())

	else:
		print(player.get_name())

	time.sleep(0.5)

	if player.is_dealer() and len(player.get_cards(False)) == 2:
		player.print_cards(True)
		time.sleep(2)

	elif is_double:
		print(player.get_doubled_cards())
		time.sleep(2)

	else:
		player.print_cards(False)
		time.sleep(2)

def place_bet(player):
	flag = True

	while flag:
		print(f"{player.get_name()}, how much would you like to bet?")
		print("Enter a dollar amount")

		try:
			bet = int(input("> "))
			flag = False

			if bet <= 0 or bet > player.get_balance():
				menu_help(player.get_balance())
				flag = True

		except:
			menu_help(player.get_balance())

	player.place_bet(bet)

def get_name(index):
	print(f"Enter player {index + 1}'s name")
	name = input("> ")

	return name

def play_offline(player_list, num_players, dealer):
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
		# TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO
		#flag = play_again()
		#continue

		return

	for player in player_list:
		player_has_blackjack = has_blackjack(player)

		# player wins with blackjack
		if player_has_blackjack:
			print(f"{player.get_name()} has BLACKJACK")
			player.payout(player.get_bet() * 0.5 + player.get_bet() * 2)

	for player in player_list:
		if player.is_playing:
			player_final_sum = make_action(player, dealer.get_cards(True)[0])
			
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
			prGreen(f"{player.get_name()} WINS")
			player.payout(player.get_bet() * 2)

		# push
		elif player_check == dealer_check:
			print(f"{player.get_name()} made a PUSH")
			player.payout(player.get_bet())

		elif player_check < dealer_check:
			prRed(f"{player.get_name()} LOSES")

def player_count(player_list):
	flag = True

	while flag:
		print(f"There are {8 - len(player_list)} seats available at the table")
		print("How many players will sit down?")
		print("Enter a number")

		try:
			selection = int(input("> "))
			flag = False

		except:
			menu_help(8 - len(player_list))
			continue

		if selection > (8 - len(player_list)) or selection < 1:
			menu_help(8 - len(player_list))
			flag = True

	return selection

def play_menu():
	flag = True

	while flag:
		print("How would you like to play?")
		print("1. Offline")
		print("2. Create online game")
		print("3. Join online game")
		print("4. Watch AI")
		print("5. Back")
		print("6. Exit")
		print("Make a selection")

		try:
			selection = int(input("> "))
			flag = False

		except:
			menu_help(6)

		if selection > 6 or selection < 1:
			flag = True

	return selection

def menu_help(end):
	prRed(f"Please enter a number between 1 and {end}")

def startup():
	flag = True

	while flag:
		print("Welcome to Jack's Blackjack!!!")
		print("Menu")
		print("1. Play")
		print("2. Rules")
		print("3. Strategy")
		print("4. Exit")
		print("Make a selection")

		try:
			selection = int(input("> "))
			flag = False

		except:
			menu_help(4)

	return selection

def main():
	while True:
		selection = startup()

		match selection:
			case 1:
				dealer = players.Dealer("dealer", -1)
				is_playing = True

				while is_playing:
					play_selection = play_menu()

					match play_selection:
						# Play offline
						case 1:
							is_playing_offline = True
							player_list = []
							num_players = player_count(player_list)

							for i in range(num_players):
								player_list.insert(i, players.Player(get_name(i), i))

							play_offline(player_list, num_players, dealer)

							while is_playing_offline:
								flag = play_again()

								match flag:
									# Play again
									case 1:
										for player in player_list:
											player.set_card_list([])
											player.set_print_list([])
											player.set_doubled_card(-1)

										dealer.set_card_list([])
										dealer.set_print_list([])

										play_offline(player_list, num_players, dealer)

									# Don't play again
									case 2:
										is_playing_offline = False

									# Change players
									case 3:
										change_players = add_or_remove()

										match change_players:
											case 1:
												num_players = add_players(player_list)

											case 2:
												num_players = remove_players(player_list)

									# Display balance
									case 4:
										for player in player_list:
											print(player.get_balance())

									# Exit
									case 5:
										exit(0)

									case _:
										menu_help(5)

						# Play online
						# TODO change this so that there's two options: "Create online game" and "Join online game"
						#	 This one is currently the create online server option
						case 2:
							# TODO
							is_playing = start_server()

						# Join online game
						case 3:
							is_playing = join_server()

						# Watch AI
						case 4:
							# TODO
							ai_play()

						# Back
						case 5:
							is_playing = False

						# Exit
						case 6:
							exit(0)

						case _:
							menu_help(5)

			case 2:
				display_rules()

			case 3:
				display_strategy()

			case 4:
				exit(0)

			case _:
				menu_help(4)

if __name__ == '__main__':
	main()
