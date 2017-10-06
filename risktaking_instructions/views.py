from otree.api import Currency as c, currency_range, safe_json
from . import models
from ._builtin import Page, WaitPage
from .models import Constants



class Welcome(Page):
	def vars_for_template(self):
		return {
			'participation_fee': self.session.config['participation_fee']
		}

class Instructions1(Page):
	pass

class Instructions2(Page):
	def vars_for_template(self):
		return {
			'default': self.participant.vars['default'],
			'mode': self.participant.vars['mode'],
			'interval': safe_json(self.session.vars['interval']),
		}

class InstructionsWait(WaitPage):
	title_text = "Bitte warten"
	body_text = "Bitte warten Sie, bis alle Teilnehmer die Instruktionen gelesen haben."

class TryOutAnnouncement(Page):
	def vars_for_template(self):
		return {
			'mode': self.participant.vars['mode']
		}

class TryOut(Page):

	def vars_for_template(self):
		return {
			'big_step': safe_json(self.session.vars['big_step']), 
			'small_step': safe_json(self.session.vars['small_step']),
			'interval': safe_json(self.session.vars['interval']),
			'default': safe_json(self.participant.vars['default']),
			'mode': safe_json(self.participant.vars['mode'])
		}

class TryWait(WaitPage):
	title_text = "Bitte warten"
	body_text = "Bitte warten Sie, bis alle Teilnehmer die Proberunde absolviert haben."

class MainTaskPrep(Page):
	pass


page_sequence = [
	Welcome,
	Instructions1,
	Instructions2,
	InstructionsWait,
	TryOutAnnouncement,
	TryOut,
	TryWait,
	MainTaskPrep
]
