from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)

import random


author = 'Christian König-Kersting'

doc = """
Outcome Bias Add on. 
"""


class Constants(BaseConstants):
	name_in_url = 'outcomebias'
	players_per_group = 2
	num_rounds = 1

	lottery_high_payoff = 300
	lottery_low_payoff = 100

	agent_fix_pay = 100
	principal_fix_pay = 100
	reward_pot = 100

	long_timeout = 180
	decision_timeout = 180

	LikertScale = [1, 2, 3, 4, 5, 6, 7]


class Subsession(BaseSubsession):
	pass


class Group(BaseGroup):
	treatment = models.CharField()
	winning_color = models.CharField(choices=['yellow', 'green'], widget=widgets.RadioSelectHorizontal)
	lottery_outcome = models.CharField()
	lottery_pay = models.PositiveIntegerField(min=0, max=Constants.lottery_high_payoff)
	reward_good = models.PositiveIntegerField(min=0, max=Constants.reward_pot)
	reward_bad = models.PositiveIntegerField(min=0, max=Constants.reward_pot)
	reward = models.PositiveIntegerField(min=0, max=Constants.reward_pot)

	a_payoff = models.CurrencyField()
	b_payoff = models.CurrencyField()

	intact = models.BooleanField(initial=True)

	def set_treatment(self):
		self.treatment = 'agent' if self.id_in_subsession % 2 == 0 else 'computer'
		self.lottery_outcome = random.choice(['good', 'bad'])
		if self.treatment == 'computer':
			self.winning_color = random.choice(['yellow', 'green'])

	def set_payoffs(self):
		if self.intact:
			self.lottery_pay = Constants.lottery_high_payoff if self.lottery_outcome == "good" else Constants.lottery_low_payoff
			self.reward = self.reward_good if self.lottery_outcome == "good" else self.reward_bad
			for player in self.get_players():
				player.payoff_calculated = True
				if player.role() == "agent":
					player.payoff = Constants.agent_fix_pay + self.reward
					self.a_payoff = player.payoff
				else:
					player.payoff = Constants.principal_fix_pay - self.reward + self.lottery_pay
					self.b_payoff = player.payoff
		else:
			for player in self.get_players():
				if player.role() == "agent":
					player.payoff = Constants.agent_fix_pay
					self.a_payoff = player.payoff
					if player.timed_out:
						player.payoff = 0
				else:
					player.payoff = Constants.principal_fix_pay	
					self.b_payoff = player.payoff
					if player.timed_out:
						player.payoff = 0

		for player in self.get_players():
			player.GXPProfit = player.payoff



class Player(BasePlayer):
	
	def role(self):
		if self.id_in_group == 1:
			return 'agent'
		else:
			return 'principal'


	timed_out = models.BooleanField(initial=False)

	payoff_calculated = models.BooleanField(initial=False)

	outcome_satisfaction = models.PositiveIntegerField(choices=Constants.LikertScale, widget=widgets.RadioSelectHorizontal)
	decision_satisfaction = models.PositiveIntegerField(choices=Constants.LikertScale, widget=widgets.RadioSelectHorizontal)

	expected_transfer_good = models.PositiveIntegerField(min=0, max=100)
	expected_transfer_bad = models.PositiveIntegerField(min=0, max=100)

	age = models.PositiveIntegerField(verbose_name="How old are you?")
	gender = models.CharField(
		choices=['female', 'male', 'other', 'prefer not to tell'],
		verbose_name="What is your gender?",
		widget=widgets.RadioSelectHorizontal)

	education = models.PositiveIntegerField(
		choices=[
			[1, 'some High School'], 
			[2, 'High School graduate'],
			[3, 'some College, no degree'],
			[4, "Associate's degree"],
			[5, "Bachelor's degree"],
			[6, "Master's degree"],
			[7, "Doctorate degree"]
		 ],
		 verbose_name="What is the highest level of education you have attained?",
		 widget=widgets.RadioSelect)
	
	studies = models.CharField(
		blank=True, 
		verbose_name="If you have at least some college education, what is/was your field of studies?")

	occupation = models.CharField(verbose_name="What is your main occupation?")

	GXPProfit = models.CurrencyField()

