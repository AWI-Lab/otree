from otree.api import Currency as c, currency_range
from otree.api import SubmissionMustFail
from . import views
from ._builtin import Bot
from .models import Constants

class PlayerBot(Bot):
    def play_round(self):
        # come up with failing inputs
        too_high = 10000000
        too_low = -10000000
        valid = 5
        empty = ''
        non_empty = 'yeah'

        # Time pressure page
        # failing
        yield SubmissionMustFail(views.TimePressure, {'time_pressure_start': too_low, 'time_pressure_end': too_low})
        yield SubmissionMustFail(views.TimePressure, {'time_pressure_start': too_high, 'time_pressure_end': too_high})
        yield SubmissionMustFail(views.TimePressure, {'time_pressure_start': valid, 'time_pressure_end': too_low})
        yield SubmissionMustFail(views.TimePressure, {'time_pressure_start': too_high, 'time_pressure_end': valid})

        # passing 
        yield (views.TimePressure, {
            'time_pressure_start': valid,
            'time_pressure_end': valid,
        })


        # Eckel-Grossan Task
        # failing
        yield SubmissionMustFail(views.RiskTask, {'eg_choice': too_low })
        yield SubmissionMustFail(views.RiskTask, {'eg_choice': too_high })

        # passing
        yield (views.RiskTask, {'eg_choice': valid})


        # Questionnaire
        # failing
        yield SubmissionMustFail(views.Questionnaire, {
            'instructions_sufficient': empty,
            'num_experiments': valid,
            'goal_of_experiment': non_empty,
            'payoff_importance': valid
        })

        yield SubmissionMustFail(views.Questionnaire, {
            'instructions_sufficient': non_empty,
            'num_experiments': valid,
            'goal_of_experiment': empty,
            'payoff_importance': valid
        })

        yield SubmissionMustFail(views.Questionnaire, {
            'instructions_sufficient': non_empty,
            'num_experiments': too_low,
            'goal_of_experiment': non_empty,
            'payoff_importance': valid
        })

        yield SubmissionMustFail(views.Questionnaire, {
            'instructions_sufficient': non_empty,
            'num_experiments': too_high,
            'goal_of_experiment': non_empty,
            'payoff_importance': valid
        })


        # passing
        yield (views.Questionnaire, {
            'instructions_sufficient': non_empty,
            'num_experiments': valid,
            'goal_of_experiment': non_empty,
            'payoff_importance': valid
        })
        
        # Demographics
        # failing
        yield SubmissionMustFail(views.Demographics, {
            'age': too_low,
            'gender': 'männlich',
            'studies': 'Economics', 
            'native_german': True, 
            'smoking': valid, 
            'free_income': 400, 
            'math_grade': '2.0 (11 Punkte)', 
            'risk_soep': valid,
            'dentist': valid,
        })

        yield SubmissionMustFail(views.Demographics, {
            'age': too_high,
            'gender': 'männlich',
            'studies': 'Economics', 
            'native_german': True, 
            'smoking': valid, 
            'free_income': 400, 
            'math_grade': '2.0 (11 Punkte)', 
            'risk_soep': valid,
            'dentist': valid,
        })

        yield SubmissionMustFail(views.Demographics, {
            'age': 20,
            'gender': 'männlich',
            'studies': 'Economics', 
            'native_german': True, 
            'smoking': valid, 
            'free_income': too_low, 
            'math_grade': '2.0 (11 Punkte)', 
            'risk_soep': valid,
            'dentist': valid,
        })

        yield SubmissionMustFail(views.Demographics, {
            'age': 20,
            'gender': 'männlich',
            'studies': 'Economics', 
            'native_german': True, 
            'smoking': valid, 
            'free_income': too_high, 
            'math_grade': '2.0 (11 Punkte)', 
            'risk_soep': valid,
            'dentist': valid,
        })

        # passing
        yield (views.Demographics, {
            'age': 20,
            'gender': 'männlich',
            'studies': 'Economics', 
            'native_german': True, 
            'smoking': valid, 
            'free_income': 400, 
            'math_grade': '2.0 (11 Punkte)', 
            'risk_soep': valid,
            'dentist': valid,
        })
    