from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)

import itertools, random

author = 'Christian König gen. Kersting'

doc = """
Active / Passive Risk Taking Experiment
"""


class Constants(BaseConstants):
	name_in_url = 'risktaking'
	players_per_group = None
	num_rounds = 10


class Subsession(BaseSubsession):
	def before_session_starts(self):
		for player in self.get_players():
			player.lottery_outcome = random.choice(['low', 'high'])


class Group(BaseGroup):
	pass


class Player(BasePlayer):

	low_payoff = models.FloatField(doc="current round's low payoff in cent")
	high_payoff = models.FloatField(doc="current round's high payoff in cent")
	lottery_outcome = models.CharField(doc="current round's lottery outcome (high/low)")
	lottery_payoff = models.CurrencyField(doc="resulting lottery payoff if round is selected for payment")


	def set_payoff(self):
		if self.lottery_outcome == "high":
			self.lottery_payoff = c(self.high_payoff)
		else:
			self.lottery_payoff = c(self.low_payoff)

		if self.round_number == self.participant.vars['relevant_round']:
			self.payoff = self.lottery_payoff
			self.participant.vars['lottery_outcome'] = 'gelb' if self.lottery_outcome == 'high' else 'grün'
			self.participant.vars['low_payoff'] = c(self.low_payoff)
			self.participant.vars['high_payoff'] = c(self.high_payoff)
