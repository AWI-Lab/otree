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


class Subsession(BaseSubsession):
	def before_session_starts(self):
		treatment = itertools.cycle([1, 2, 3, 4])
		for player in self.get_players():
			current_treatment = next(treatment)
			if current_treatment in [1, 2]:
				player.participant.vars['default'] = "Safe"
			else:
				player.participant.vars['default']  = "Risky"

			if current_treatment in [1, 3]:
				player.participant.vars['mode']  = "Active"
			else:
				player.participant.vars['mode']  = "Passive"

			player.participant.vars['relevant_round'] = random.randint(1, self.session.config['main_task_rounds'])

		self.session.vars['small_step'] = 8
		self.session.vars['big_step'] = 12
		self.session.vars['interval'] = 5
		self.session.vars['max_steps'] = 20 


class Group(BaseGroup):
	pass


class Player(BasePlayer):
	pass