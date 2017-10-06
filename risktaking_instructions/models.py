from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)
import itertools, random

author = 'Christian König-Kersting'

doc = """
Instructions for risktaking experiment
"""


class Constants(BaseConstants):
	name_in_url = 'risktaking_instructions'
	players_per_group = None
	num_rounds = 1

	lotteries = [ # in cent
		{'small_step': 20, 'big_step': 30}, # 0, faktor 1.5
		{'small_step': 40, 'big_step': 60}, # 1
		{'small_step': 60, 'big_step': 90}, # 2
		{'small_step': 80, 'big_step': 120}, # 3
		{'small_step': 100, 'big_step': 150}, # 4

		{'small_step': 10, 'big_step': 30}, # 5, faktor 3
		{'small_step': 30, 'big_step': 90}, # 6
		{'small_step': 50, 'big_step': 150}, # 7
		{'small_step': 70, 'big_step': 210}, # 8 
		{'small_step': 90, 'big_step': 270}, # 9
	]

	lottery_orders = [
		[2, 4, 0, 3, 2, 7, 9, 5, 8, 6], # 0 (1.5: M H L h l -- 3:   M H L h l)
		[7, 9, 5, 8, 6, 2, 4, 0, 3, 2], # 1 (3:   M H L h l -- 1.5: M H L h l)
	]


class Subsession(BaseSubsession):
	def before_session_starts(self):
		treatment = itertools.cycle([1, 2, 3, 4])
		for player in self.get_players():
			current_treatment = next(treatment)
			player.treatment = current_treatment
			if current_treatment in [1, 2]:
				player.participant.vars['default'] = "Safe"
			else:
				player.participant.vars['default']  = "Risky"

			if current_treatment in [1, 3]:
				player.participant.vars['mode']  = "Active"
			else:
				player.participant.vars['mode']  = "Passive"

			player.participant.vars['relevant_round'] = random.randint(0, self.session.config['main_task_rounds'])
			player.relevant_round = player.participant.vars['relevant_round']
			player.participant.vars['lottery_order'] = random.choice([0, 1])
			player.lottery_order = player.participant.vars['lottery_order']
			player.participant.vars['steps'] = []
			# create steps variable from selected lottery order
			for lottery in Constants.lottery_orders[player.participant.vars['lottery_order']]:
				player.participant.vars['steps'].append(Constants.lotteries[lottery])

		# used in training
		self.session.vars['small_step'] = 8
		self.session.vars['big_step'] = 12
		self.session.vars['interval'] = 5
		self.session.vars['max_steps'] = 10


class Group(BaseGroup):
	pass


class Player(BasePlayer):
	lottery_order = models.IntegerField(doc="Stores which of the two lottery orders was randomly selected")
	relevant_round = models.IntegerField(doc="Stores the round randomly selected for payment. If 0, Eckel-Grossman is paid")
	treatment = models.SmallIntegerField(doc="Stores treatment: 1=Safe/Active, 2=Safe/Passive, 3=Risky/Active, 4=Risky/Passive")