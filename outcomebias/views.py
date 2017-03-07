from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

import random


class Arrival(WaitPage):
	group_by_arrival_time = True

	title_text = "Arrival Hall"
	body_text = "For this experiment, we need groups of two. \
	Please wait for another participant to log on."

	def after_all_players_arrive(self):
		self.group.set_treatment()

class Welcome(Page):
	timeout_seconds = Constants.long_timeout

	def before_next_page(self):
		if self.timeout_happened:
			self.player.timed_out = True
			self.group.intact = False

class WinningColorChoice(Page):
	form_model = models.Group
	form_fields = ['winning_color']

	timeout_seconds = Constants.decision_timeout
	timeout_submission = { 'winning_color': 'none' }

	def before_next_page(self):
		if self.timeout_happened:
			self.player.timed_out = True
			self.group.intact = False

	def is_displayed(self):
		return self.group.intact and self.group.treatment == 'agent' and self.player.role() == 'agent'

class RewardDecision(Page):
	form_model = models.Group
	form_fields = ['reward_good', 'reward_bad']

	timeout_seconds = Constants.decision_timeout
	timeout_submission = {'reward_good': 0, 'reward_bad': 0}

	def before_next_page(self):
		if self.timeout_happened:
			self.player.timed_out = True
			self.group.intact = False

	def is_displayed(self):
		return self.group.intact and self.player.role() == 'principal'

class ResultsWaitPage(WaitPage):
	template_name = 'outcomebias/MyWaitPage.html'
	title_text = "Please Wait"

	def after_all_players_arrive(self):
		self.group.set_payoffs()

class Results(Page):
	def is_displayed(self):
		return self.group.intact

class Failure(Page):
	def is_displayed(self):
		return not self.group.intact 

page_sequence = [
	Arrival,
	Welcome,
	WinningColorChoice,
	RewardDecision,
	ResultsWaitPage,
	Results,
	Failure
]
