from otree.api import Currency as c, currency_range
from otree.api import SubmissionMustFail
from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

	cases = [
		{
			# inputs:
			'winning_color': "green",
			'reward_good': 80,
			'reward_bad': 20,
			'expected_transfer_good': 70,
			'expected_transfer_bad': 30,
			'outcome_satisfaction': 5,
			'decision_satisfaction': 7,
			'age': 18,
			'gender': 'male',
			'education': 2,
			'studies': "economics",
			'occupation': "student",

			# results:
			'agent_bad_payoff': 100 + 20,
			'agent_good_payoff': 100 + 80,
			'principal_bad_payoff': 100 - 20 + 100,
			'principal_good_payoff': 100 + 300 - 80,
		},
	]

	# the following dictionary defines inputs that should prevent moving on in the experiment
	must_fail = {
		'colors': ["", "red"], # invalid colors
		'rewards': [ # rewards out of bounds
			{'good': None, 'bad': None},
			{'good': -1, 'bad': -1},
			{'good': -1, 'bad': 20},
			{'good': 20, 'bad': -1},
			{'good': 105, 'bad': 105},
			{'good': 106, 'bad': 20},
			{'good': 19, 'bad': 107},
		],
		'expectations': [ # expectations out of bounds
			{'good': None, 'bad': None},
			{'good': -1, 'bad': -1},
			{'good': -1, 'bad': 20},
			{'good': 20, 'bad': -1},
			{'good': 105, 'bad': 105},
			{'good': 106, 'bad': 20},
			{'good': 19, 'bad': 107},
		],
		'satisfaction': [ # satisfaction out of bounds
			{'decision': None, 'outcome': None },
			{'decision': 0, 'outcome': 0 },
			{'decision': 8, 'outcome': 8 },
			{'decision': 0, 'outcome': 2 },
			{'decision': 2, 'outcome': -1 },
			{'decision': 9, 'outcome': 2 },
			{'decision': 3, 'outcome': 10 },
		],
		'demographics': [ 
			{ # no input on demographics
				'age': None,
				'gender': None,
				'education': None,
				'studies': "asd",
				'occupation': None
			},
			{ # wrong age and gender
				'age': -1,
				'gender': "stuff",
				'education': 0,
				'studies': "economics",
				'occupation': "student"
			},
			{ # education level 3 requires input for "studies"
				'age': 20,
				'gender': "male",
				'education': 3,
				'studies': "",
				'occupation': "student"
			},

		]
	}

	def play_round(self):
		# role assignment
		if self.player.id_in_group == 1:
			assert self.player.role() == 'agent'
		else:
			assert self.player.role() == 'principal'

		# treatment assignment
		if self.group.id_in_subsession in [0, 2, 4, 6, 8, 10]:
			assert self.group.treatment == 'agent'
		else:
			assert self.group.treatment == 'computer'


		# submit welcome page
		yield (views.Welcome)


		# test Winning Color Choice for agents
		if self.player.role() == 'agent' and self.group.treatment == 'agent':
			for failcase in self.must_fail['colors']:
				yield SubmissionMustFail(views.WinningColorChoice, {'winning_color': failcase})
			
			yield (views.WinningColorChoice, {'winning_color': self.case['winning_color']})
			assert self.group.winning_color == self.case['winning_color']


		# test reward decision for principals
		if self.player.role() == 'principal':
			for failcase in self.must_fail['rewards']:
				yield SubmissionMustFail(views.RewardDecision, {'reward_good': failcase['good'], 'reward_bad': failcase['bad']})

			yield (views.RewardDecision, {'reward_good': self.case['reward_good'], 'reward_bad': self.case['reward_bad'] })
			assert self.group.reward_good == self.case['reward_good']
			assert self.group.reward_bad == self.case['reward_bad']

		# test expected transfer inputs by agents
		if self.player.role() == 'agent':
			for failcase in self.must_fail['expectations']:
				yield SubmissionMustFail(views.Expectation, {'expected_transfer_good': failcase['good'], 'expected_transfer_bad': failcase['bad']})
			
			yield (views.Expectation, {'expected_transfer_good': self.case['expected_transfer_good'], 'expected_transfer_bad': self.case['expected_transfer_bad']})
			assert self.player.expected_transfer_bad == self.case['expected_transfer_bad']
			assert self.player.expected_transfer_good == self.case['expected_transfer_good']


		# payoff calculations
		# missing timeout checks!
		if self.group.lottery_outcome == "good":
			assert self.group.lottery_pay == 300
			assert self.group.reward == self.case['reward_good']
			
			if self.player.role() == 'agent':
				assert self.player.payoff == self.case['agent_good_payoff']
				assert self.group.a_payoff == self.case['agent_good_payoff']
			else: # principal
				assert self.player.payoff == self.case['principal_good_payoff']
				assert self.group.b_payoff == self.case['principal_good_payoff']
		
		else: # bad outcome
			assert self.group.lottery_pay == 100
			assert self.group.reward == self.case['reward_bad']

			if self.player.role() == 'agent':
				assert self.player.payoff == self.case['agent_bad_payoff']
				assert self.group.a_payoff == self.case['agent_bad_payoff']
			else: # principal
				assert self.player.payoff == self.case['principal_bad_payoff']
				assert self.group.b_payoff == self.case['principal_bad_payoff']

		assert self.player.GXPProfit == self.player.payoff

		
		# test result for principal
		if self.player.role() == 'principal':
			for failcase in self.must_fail['satisfaction']:
				yield SubmissionMustFail(views.Results, {'outcome_satisfaction': failcase['outcome'], 'decision_satisfaction': failcase['decision']})
			
			yield (views.Results, {'outcome_satisfaction': self.case['outcome_satisfaction'], 'decision_satisfaction': self.case['decision_satisfaction']})
			assert self.player.outcome_satisfaction == self.case['outcome_satisfaction']
			assert self.player.decision_satisfaction == self.case['decision_satisfaction']

		# and for the agent
		else: 
			yield (views.Results)


		# test demographics
		for failcase in self.must_fail['demographics']:
			yield SubmissionMustFail(views.Demographics, {
				'age': failcase['age'],
				'gender': failcase['gender'],
				'education': failcase['education'],
				'studies': failcase['studies'],
				'occupation': failcase['occupation']
			})

		yield (views.Demographics, {
				'age': self.case['age'],
				'gender': self.case['gender'],
				'education': self.case['education'],
				'studies': self.case['studies'],
				'occupation': self.case['occupation']
			})
