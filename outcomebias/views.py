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

class ColorChoiceWaitPage(WaitPage):
	template_name = 'outcomebias/MyWaitPage.html'
	title_text = "Please Wait"

class RewardDecision(Page):
	form_model = models.Group
	form_fields = ['reward_good', 'reward_bad']

	timeout_seconds = Constants.decision_timeout

	def before_next_page(self):
		if self.timeout_happened:
			self.player.timed_out = True
			self.group.intact = False

	def is_displayed(self):
		return self.group.intact and self.player.role() == 'principal'

class Expectation(Page):
	def is_displayed(self):
		return self.group.intact and self.player.role() == 'agent'

	def before_next_page(self):
		if self.timeout_happened:
			self.player.timed_out = True
			self.group.intact = False

	form_model = models.Player
	form_fields = ['expected_transfer_good', 'expected_transfer_bad']

	timeout_seconds = Constants.decision_timeout


class ResultsWaitPage(WaitPage):
	template_name = 'outcomebias/MyWaitPage.html'
	title_text = "Please Wait"

	def after_all_players_arrive(self):
		self.group.set_payoffs()

class Results(Page):
	timeout_seconds = Constants.decision_timeout

	form_model = models.Player

	def get_form_fields(self):
		if self.player.role() == 'principal':
			return ['outcome_satisfaction', 'decision_satisfaction']
		else:
			return []

	def is_displayed(self):
		return self.group.intact


class Demographics(Page):
	def is_displayed(self):
		return self.group.intact

	form_model = models.Player
	form_fields = ['age', 'gender', 'education', 'studies', 'occupation']

	timeout_seconds = Constants.long_timeout

	def error_message(self, values):
		if values['education'] >= 3 and not values['studies'] :
			return 'Please provide your field of studies.'


class Payment(Page):
	def is_displayed(self):
		return self.group.intact

	def vars_for_template(self):
		return {'money_to_pay': self.participant.payoff_plus_participation_fee()}


class Failure(Page):
	def is_displayed(self):
		return not self.group.intact 

page_sequence = [
	Arrival,
	Welcome,
	WinningColorChoice,
	ColorChoiceWaitPage,
	RewardDecision,
	Expectation,
	ResultsWaitPage,
	Results,
	Demographics,
	Payment,
	Failure
]
