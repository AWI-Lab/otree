from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)

import itertools, random


author = 'Christan König-Kersting'

doc = """
Questionnaires for active / passive risk taking experiment
"""


class Constants(BaseConstants):
	name_in_url = 'ristaking_lastpart'
	players_per_group = None
	num_rounds = 1

	lotteries = {
		1: {
			'win': 600,
			'lose': 600,
		},
		2: {
			'win': 690,
			'lose': 540,
		},
		3: {
			'win': 780,
			'lose': 480,
		},
		4: {
			'win': 870,
			'lose': 420,
		},
		5: {
			'win': 960,
			'lose': 360,
		},
		6: {
			'win': 1050,
			'lose': 300,
		},
		7: {
			'win': 1140,
			'lose': 240,
		},
		8: {
			'win': 1230,
			'lose': 180,
		},
		9: {
			'win': 1320,
			'lose': 120,
		},
		10: {
			'win': 1410,
			'lose': 90,
		},
		11: {
			'win': 1500,
			'lose': 0
		}
	}


class Subsession(BaseSubsession):
	pass

class Group(BaseGroup):
	pass


class Player(BasePlayer):
	age = models.PositiveIntegerField(min=0, max=110, doc="age in years")
	gender = models.CharField(choices=['männlich', 'weiblich', 'anderes', 'keine Angabe'], widget=widgets.RadioSelectHorizontal, doc="gender")
	studies = models.CharField(doc="field of studies")	

	native_german = models.BooleanField(choices=[(True, 'Ja'), (False, 'Nein')], doc="is German native language")
	free_income = models.IntegerField(doc="free income in euro", min=0, max=1000000)
	smoking = models.PositiveSmallIntegerField(choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], widget=widgets.RadioSelectHorizontal, doc="smoking intensity on 0-10 likert")
	dentist = models.PositiveSmallIntegerField(choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], widget=widgets.RadioSelectHorizontal, doc="likelihood of going to regular dentist checkups on 1-7 likert")
	risk_soep = models.PositiveSmallIntegerField(choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], widget=widgets.RadioSelectHorizontal, doc="SOEP risk question on 0-10 likert")
	math_grade = models.CharField(choices=[
		'1.0 (14-15 Punkte)', 
		'1.3 (13 Punkte)', 
		'1.7 (12 Punkte)', 
		'2.0 (11 Punkte)',
		'2.3 (10 Punkte)', 
		'2.7 (9 Punkte)', 
		'3.0 (8 Punkte)', 
		'3.3 (7 Punkte)',
		'3.7 (6 Punkte)',
		'4.0 (5 Punkte)',
		'5.0 (<5 Punkte)'], doc="Abitur math grade")


	goal_of_experiment = models.TextField(doc="free form input for believed goal of experiment")
	payoff_importance = models.PositiveSmallIntegerField(choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], widget=widgets.RadioSelectHorizontal, doc="0-10 likert on how important payoff considerations are for the participant")
	num_experiments = models.PositiveSmallIntegerField(doc="guessed number of previous experiment participations at AWI Lab", min=0, max=100)
	instructions_sufficient = models.TextField(doc="comments on the instructions / clarity")

	# Eckel and Grossman risk elicitation task
	eg_choice = models.PositiveSmallIntegerField(doc="eckel grossman task selected", min=1, max=11)
	eg_outcome = models.CharField(doc="eckel grossman task lottery outcome")
	eg_payoff = models.PositiveIntegerField(doc="eckel grossman task payoff if selected")

	time_pressure_start = models.PositiveSmallIntegerField(choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], widget=widgets.RadioSelectHorizontal, doc="beginning of rounds time pressure 0-10 likert")
	time_pressure_end = models.PositiveSmallIntegerField(choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], widget=widgets.RadioSelectHorizontal, doc="end of rounds time pressure on 0-10 likert")

	def play_Lottery(self):
		winning_probability = 0.5
		self.eg_outcome = "win" if random.random() < winning_probability else "lose"
		self.eg_payoff = Constants.lotteries[self.eg_choice][self.eg_outcome]

		if self.participant.vars['relevant_round'] == 0:
			self.payoff = c(self.eg_payoff/100)
			self.participant.vars['lottery_outcome'] = 'gelb' if self.eg_outcome == 'win' else 'grün'
			self.participant.vars['low_payoff'] = c(Constants.lotteries[self.eg_choice]['lose']/100)
			self.participant.vars['high_payoff'] = c(Constants.lotteries[self.eg_choice]['win']/100)