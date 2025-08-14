#import cards

def prRed(s): print("\033[91m{}\033[00m".format(s))
def prGreen(s): print("\033[92m{}\033[00m".format(s))
def prYellow(s): print("\033[93m{}\033[00m".format(s))
def prLightPurple(s): print("\033[94m{}\033[00m".format(s))
def prPurple(s): print("\033[95m{}\033[00m".format(s))
def prCyan(s): print("\033[96m{}\033[00m".format(s))
def prLightGray(s): print("\033[97m{}\033[00m".format(s))
def prBlack(s): print("\033[90m{}\033[00m".format(s))

class Player:
	def __init__(self, name, index):
		self.name = name
		self.index = index
		self.money = 100
		self.card_list = []
		self.print_list = []
		self.is_playing = True
		self.doubled_card = -1

	def place_bet(self, value):
		self.bet = value
		self.money = self.money - value

	def add_card(self, card):
		self.card_list.append(card)
		self.print_list.append(card)

	def add_result(self, final_sum):
		self.final_sum = final_sum

	def payout(self, value):
		self.money += value
		self.is_playing = False

	def print_cards(self, is_player_action):
		prYellow(self.print_list)

	def print_doubled_cards(self):
		if self.doubled_card == -1:
			prYellow(self.print_list)

		else:
			self.print_list[-1] = self.doubled_card
			prYellow(self.print_list)

	def is_dealer(self):
		return False

	def set_card_list(self, cards):
		self.card_list = cards

	def set_print_list(self, cards):
		self.print_list = cards

	def set_doubled_card(self, card):
		self.doubled_card = card

	def get_doubled_cards(self):
		self.doubled_card = self.print_list[-1]
		self.print_list[-1] = '[]'
		return self.print_list

	def get_doubled_card(self):
		return self.doubled_card

	def get_cards(self, is_player_action):
		for i, card in enumerate(self.card_list):
			if card == "Ace":
				self.card_list[i] = 1

			if card == "Jack":
				self.card_list[i] = 10

			if card == "Queen":
				self.card_list[i] = 10

			if card == "King":
				self.card_list[i] = 10

		return self.card_list

	def get_final_sum(self):
		return self.final_sum

	def get_bet(self):
		return self.bet

	def get_name(self):
		return self.name

	def get_balance(self):
		return self.money

class Dealer(Player):
	def is_dealer(self):
		return True

	def print_cards(self, is_player_action):
		if is_player_action:
			temp = []

			for i in self.print_list:
				temp.append(i)

			temp[1] = '[]'
			prYellow(temp)

		else:
			prYellow(self.print_list)

	def get_cards(self, is_player_action):
		for i, card in enumerate(self.card_list):
			if card == "Ace":
				self.card_list[i] = 1

			if card == "Jack":
				self.card_list[i] = 10

			if card == "Queen":
				self.card_list[i] = 10

			if card == "King":
				self.card_list[i] = 10

		if is_player_action:
			temp = []

			for i in self.card_list:
				temp.append(i)

			temp[1] = '[]'
			return temp

		return self.card_list
