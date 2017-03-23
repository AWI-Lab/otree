from otree.api import Currency as c, currency_range, safe_json
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class MainTask(Page):
	form_model = models.Player
	form_fields = ['low_payoff', 'high_payoff']

	def is_displayed(self):
		return self.round_number <= self.session.config['main_task_rounds']

	def vars_for_template(self):
		return {
			'small_step': safe_json(self.session.vars['small_step']),
			'big_step': safe_json(self.session.vars['big_step']),
			'max_steps': safe_json(self.session.vars['max_steps']), 
			'interval': safe_json(self.session.vars['interval']),
			'default': safe_json(self.participant.vars['default']),
			'mode': safe_json(self.participant.vars['mode']),
			'lottery_outcome': safe_json(self.player.lottery_outcome),
			'round_number': safe_json(self.round_number),
			'max_rounds': safe_json(self.session.config['main_task_rounds'])
		}

	def before_next_page(self):
		self.player.set_payoff();


page_sequence = [
	MainTask
]
