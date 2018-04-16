from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Welcome(Page):
	pass

class CategoryElicitation(Page):
	form_model = "player"
	form_fields = [
		'cat_end_rel_1', 
		'cat_end_rel_2', 
		'cat_end_rel_3',
		'cat_end_rel_4',
		'cat_end_rel_5',

		'cat_end_abs_1', 
		'cat_end_abs_2', 
		'cat_end_abs_3',
		'cat_end_abs_4',
		'cat_end_abs_5',
	]


class Instructions1(Page):
	form_model = "player"
	form_fields = ["question_1", "question_2"]

	def question_1_error_message(self, value):
		if value == "Falsch":
			return "Bitte lesen Sie die Instruktionen erneut genau durch und korrigieren Sie Ihre Antwort."

	def question_2_error_message(self, value):
		if value == "Richtig":
			return "Bitte lesen Sie die Instruktionen erneut genau durch und korrigieren Sie Ihre Antwort."

class Instructions2(Page):
	form_model = "player"
	form_fields = ["question_3", "question_4"]

	def question_3_error_message(self, value):
		if value != 20:
			return "Bitte lesen Sie die Instruktionen erneut genau durch und korrigieren Sie Ihre Antwort."

	def question_4_error_message(self, value):
		if value != 4:
			return "Bitte lesen Sie die Instruktionen erneut genau durch und korrigieren Sie Ihre Antwort."


class Instructions3(Page):
	form_model = "player"
	form_fields = ["question_5", "question_6"]

	def question_5_error_message(self, value):
		if value == "Richtig":
			return "Bitte lesen Sie die Instruktionen erneut genau durch und korrigieren Sie Ihre Antwort."

	def question_6_error_message(self, value):
		if value == "Richtig":
			return "Bitte lesen Sie die Instruktionen erneut genau durch und korrigieren Sie Ihre Antwort."



class CategoryPick(Page):
	form_model = "player"
	form_fields = ["category"]

	def vars_for_template(self):
		return {
			'width_a': self.player.cat_end_abs_1,
			'width_b': self.player.cat_end_abs_2 - self.player.cat_end_abs_1,
			'width_c': self.player.cat_end_abs_3 - self.player.cat_end_abs_2,
			'width_d': self.player.cat_end_abs_4 - self.player.cat_end_abs_3,
			'width_e': self.player.cat_end_abs_5 - self.player.cat_end_abs_4,
		}


class CategoryWaitPage(WaitPage):
	wait_for_all_groups = True

	def after_all_players_arrive(self):
		self.subsession.set_groups()
		# weil wait_for_all_groups gesetzt ist, wird die Funktion nur einmal aufgerufen,
		# folglich muss ich dann noch eine Ebene über die Gruppe hinaus auf die Subsession
		# in der aufgerufenen Funktion auf der Subsession-Ebene wird dann durch alle Gruppen gegangen
		# und da dann jeweils durch jeden Spieler um die Category zu kommunizieren.
		self.subsession.communicate_categories()


class Agent(Page):
	form_model = "player"
	form_fields = ["decision_for_p1", "decision_for_p2", "decision_for_p3", "decision_for_p4","decision_for_p5"]

	def vars_for_template(self):
		group = self.group.get_players()

		return {
			'p1_category': group[int(self.player.c_principal_1)-1].category, 
			'p2_category': group[int(self.player.c_principal_2)-1].category, 
			'p3_category': group[int(self.player.c_principal_3)-1].category, 
			'p4_category': group[int(self.player.c_principal_4)-1].category, 
			'p5_category': group[int(self.player.c_principal_5)-1].category,

			'width_a': self.player.cat_end_abs_1,
			'width_b': self.player.cat_end_abs_2 - self.player.cat_end_abs_1,
			'width_c': self.player.cat_end_abs_3 - self.player.cat_end_abs_2,
			'width_d': self.player.cat_end_abs_4 - self.player.cat_end_abs_3,
			'width_e': self.player.cat_end_abs_5 - self.player.cat_end_abs_4,
		}
	
	def before_next_page(self):
		self.player.determine_outcome()


class WaitForAgents(WaitPage):

	def after_all_players_arrive(self):
		self.group.after_investments()


class Results_Principals(Page):

	def is_displayed(self):
		return self.player.role() == "Principal"

	form_model = "player"
	form_fields = ["message"]


class WaitForPrincipals(WaitPage):
	def after_all_players_arrive(self):
		self.group.after_results_principals()


class Results_Agents(Page):

	def is_displayed(self):
		return self.player.role() == "Agent"


class Questionnaire(Page):

	form_model = "player"
	form_fields = ["age", "gender", "studies", "nonstudent", "financial_advice", "income"]

	# This works now, but is not in compliance with the oTree manual.. I guess we found a bug.
	# returns an error message if a participant...
	def error_message(self, values):
		# ... indicates field of studies and ticks the box "non-student".
		if values["studies"]:
			if values["nonstudent"]:
				return "Bitte geben Sie entweder ein Studienfach an oder wählen Sie \"Kein Student\""
		# ... states no field of studies and and does not tick the box.
		else:
		#elif "studies" not in values:
			if not values["nonstudent"]:
				return "Sie haben kein Studienfach angegeben. Wenn Sie kein Student sind, treffen Sie bitte eine entsprechende Auswahl."

class Last_Page(Page):

	pass


page_sequence = [
	Welcome,
	CategoryElicitation,
	Instructions1,
	Instructions2,
	Instructions3,
	CategoryPick,
	CategoryWaitPage,
	Agent,
	WaitForAgents,
	Results_Principals,
	WaitForPrincipals,
	Results_Agents,
	Questionnaire,
	Last_Page
]
