from otree.api import Currency as c, currency_range
from otree.api import SubmissionMustFail
from . import pages
from ._builtin import Bot
from .models import Constants

from random import randint, choice
import itertools


class PlayerBot(Bot):

	def play_round(self):
		# data definition
		test_data = {
			'Category_Elicitation': {
				'invalid_inputs': {
					'cat_end_abs_1': 'a',
					'cat_end_abs_2': '2000',
					'cat_end_abs_3': '',
					'cat_end_abs_4': 'a',
					'cat_end_abs_5': 5.4,

					'cat_end_rel_1': -1,
					'cat_end_rel_2': -1,
					'cat_end_rel_3': -1,
					'cat_end_rel_4': -1,
					'cat_end_rel_5': -1,
				},
				'valid_inputs': {
					'cat_end_abs_1': 200,
					'cat_end_abs_2': 400,
					'cat_end_abs_3': 600,
					'cat_end_abs_4': 800,
					'cat_end_abs_5': 1000,

					'cat_end_rel_1': 0.2,
					'cat_end_rel_2': 0.4,
					'cat_end_rel_3': 0.6,
					'cat_end_rel_4': 0.8,
					'cat_end_rel_5': 1.0,
				}
			},
			'Comprehension_1': {
				'invalid_inputs': {
					"question_1": ['a', 5], 
					"question_2": ['a', ''], 
					"question_3": ['a', ''], 
					"question_4": ['a', ''], 
					"question_5": ['a', '']
				},
				'valid_inputs': {
					"question_1": "Falsch", 
					"question_2": "Richtig", 
					"question_3": "Falsch", 
					"question_4": 10, 
					"question_5": 6
				},
			},
			'Comprehension_2': {
				'invalid_inputs': {
					"question_1": ['a', '', True], 
					"question_2": ['a', '', True], 
					"question_3": ['a', '', True], 
					"question_4": ['a', '', True], 
					"question_5": ['a', '', True]
				},
				'valid_inputs': {
					"question_1": "Falsch", 
					"question_2": "Richtig", 
					"question_3": "Falsch", 
					"question_4": 10, 
					"question_5": 6
				},
			},
			'Questionnaire': {
				'invalid_inputs': {
					'age': [-1, 'a', '', 130],
					'gender': [1, 'cool', ''],
					'studies': 'yay', 
					'nonstudent': 'asd',
					'financial_advice' : ['a', ''], 
					'income': ['a', '']
				},
				'valid_inputs': {
					'age': randint(18, 60),
					'gender': choice(["männlich", "weiblich", "anderes"]),
					'studies': "Economics",
					'nonstudent': False,
					'financial_advice': choice([True, False]), 
					'income': randint(0, 2500)
				}         
			}
		}

		# set whether you want to test all combinations of invalid inputs:
		excessive = False


		# welcome
		yield (pages.Welcome)

		yield (pages.CategoryElicitation, test_data['Category_Elicitation']['valid_inputs'])

		# instructions 1
		yield SubmissionMustFail(pages.Instructions1, {'question_1': 'Falsch', 'question_2': 'Falsch'})
		yield SubmissionMustFail(pages.Instructions1, {'question_1': 'Falsch', 'question_2': 'Richtig'})
		yield (pages.Instructions1, {'question_1': 'Richtig', 'question_2': 'Falsch'})

		# instructions 2
		yield SubmissionMustFail(pages.Instructions2, {'question_3': randint(21, 2500), 'question_4': randint(0, 3)})
		yield (pages.Instructions2, {'question_3': 20, 'question_4': 4})

		# instructions 3
		yield SubmissionMustFail(pages.Instructions3, {'question_5': 'Richtig', 'question_6': 'Falsch'})
		yield (pages.Instructions3, {'question_5': 'Falsch', 'question_6': 'Falsch'})


		# category picker
		yield (pages.CategoryPick, {'category': choice(Constants.category_names)})
		
		# agents' decision
		yield (pages.Agent, {'decision_for_p1': 7.5, 'decision_for_p2': 7.5, 'decision_for_p3': 7.5, 'decision_for_p4': 7.5, 'decision_for_p5': 7.5})

		# principal's results
		if self.player.role() == "Principal":
			assert self.player.investment == 7.5
			if self.player.investment_outcome == 0:
				assert self.player.payoff == 2.5
			else:
				assert self.player.payoff == 28.75
			yield (pages.Results_Principals, {'message': 'Ich bin sehr zufrieden mit Ihrer Entscheidung'})


		# agents' results
		if self.player.role() == "Agent": 
			assert self.player.message_from_principal == "Ich bin sehr zufrieden mit Ihrer Entscheidung"
			if self.player.outcome_of_principal == 0:
				assert self.player.payoff_of_principal == 2.5
				assert self.player.profit_of_principal == 0
				if self.player.compensation == "variable_result":
					assert self.player.payoff == 5.625
				else:
					assert self.player.payoff == Constants.fixed_payment
			else:
				assert self.player.payoff_of_principal == 28.75
				assert self.player.profit_of_principal == 18.75
				if self.player.compensation == "fixed":
					assert self.player.payoff == Constants.fixed_payment
				elif self.player.compensation == "variable_result":
					assert self.player.payoff == 12.1875
				elif self.player.compensation == "variable_profit":
					assert self.player.payoff == 11.5625
			yield (pages.Results_Agents)

		# questionnaire
		# 
		if excessive:
			keys, values = zip(*test_data['Questionnaire']['invalid_inputs'].items())
			for v in itertools.product(*values):
				yield SubmissionMustFail(pages.Questionnaire, dict(zip(keys, v)))

		# manually check field of studies + non student
		yield SubmissionMustFail(pages.Questionnaire, {
					'age': randint(18, 60),
					'gender': choice(["männlich", "weiblich", "anderes"]),
					'studies': "Economics",
					'nonstudent': True,
					'financial_advice': choice([True, False]), 
					'income': randint(0, 2500)
		})

		# manually check no field of studies + indicated that subject is student
		yield SubmissionMustFail(pages.Questionnaire, {
					'age': randint(18, 60),
					'gender': choice(["männlich", "weiblich", "anderes"]),
					'studies': "",
					'nonstudent': False,
					'financial_advice': choice([True, False]), 
					'income': randint(0, 2500)
		})

		# check valid inputs
		yield (pages.Questionnaire, test_data['Questionnaire']['valid_inputs'])

		# last page!
		if self.player.role() == "Agent":
			if self.player.outcome_of_principal == 0:
				if self.player.compensation == "variable_result":
					assert self.player.payoff + self.player.participation_fee == 8.625
				else:
					assert self.player.payoff + self.player.participation_fee == 8
		if self.player.role() == "Principal":
			if self.player.investment_outcome == 0:
				assert self.player.payoff + self.player.participation_fee == 5.5
			else:
				assert self.player.payoff + self.player.participation_fee == 31.75
	#	yield (pages.Last_Page)



	# Welcome,
	# CategoryElicitation,
	# Instructions1,
	# Instructions2,
	# Instructions3,
	# CategoryPick,
	# CategoryWaitPage,
	# Agent,
	# WaitForAgents,
	# Results_Principals,
	# WaitForPrincipals,
	# Results_Agents,
	# Questionnaire,
	# Last_Page

