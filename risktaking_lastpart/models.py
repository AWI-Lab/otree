from otree.api import (
	models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
	Currency as c, currency_range
)

import itertools, random


author = 'Christan König-Kersting'

doc = """
Questionnaires for risk taking experiment
"""


class Constants(BaseConstants):
	name_in_url = 'ristaking_lastpart'
	players_per_group = None
	num_rounds = 1


class Subsession(BaseSubsession):
	pass

class Group(BaseGroup):
	pass


class Player(BasePlayer):
	ch_no = models.PositiveIntegerField(min=1, max=4)
	sq_act = models.PositiveIntegerField(min=1, max=4)
	sq_no = models.PositiveIntegerField(min=1, max=4)
	ch_act = models.PositiveIntegerField(min=1, max=4)

	age = models.PositiveIntegerField(min=0, max=110)
	gender = models.CharField(choices=['männlich', 'weiblich'], widget=widgets.RadioSelectHorizontal)
	studies = models.CharField()	
