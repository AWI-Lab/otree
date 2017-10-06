from otree.api import Currency as c, currency_range, safe_json
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

class CollectParticipants(WaitPage):
	title_text = "Bitte warten"
	body_text = "Bitte warten Sie, bis alle Teilnehmer die Entscheidungsrunden absolviert haben."


class RiskTask(Page):
	form_model = models.Player
	form_fields = ['eg_choice']

	# timeout_submission = {'eg_choice': 1}

	def before_next_page(self):
		self.player.play_Lottery()

class TimePressure(Page):
	form_model = models.Player
	form_fields = ['time_pressure_start', 'time_pressure_end']


class Questionnaire(Page):
	form_model = models.Player
	form_fields = ['instructions_sufficient', 'num_experiments', 'goal_of_experiment', 'payoff_importance']


class Demographics(Page):
	form_model = models.Player
	form_fields = ['age', 'gender', 'studies', 'native_german', 'smoking', 'free_income', 'math_grade', 'risk_soep', 'dentist']

	
class End(Page):
	def vars_for_template(self):
		return {
			'relevant_round': self.participant.vars['relevant_round'],
			'lottery_outcome': self.participant.vars['lottery_outcome'],
			'low_payoff': self.participant.vars['low_payoff'],
			'high_payoff': self.participant.vars['high_payoff'],
			'payoff': self.participant.payoff,
			'payoff_euro': self.participant.payoff.to_real_world_currency(self.session),
			'participation_fee': self.session.config['participation_fee'],
			'payoff_total': self.participant.payoff_plus_participation_fee()
		}



page_sequence = [
	CollectParticipants,
	TimePressure,
	RiskTask,
	Questionnaire,
	Demographics,
	End
]
