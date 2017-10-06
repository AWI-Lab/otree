from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants

import random


class PlayerBot(Bot):
    def play_round(self):
        if 'simulation' in self.session.config:
            if self.session.config['simulation']:
                return self.simulate_data()
            else:
                return self.test_experiment()
        else:
            return self.test_experiment()


    def test_experiment(self):
        # this function runs regular tests. In fact, it always selects the same lottery.
        if self.player.round_number <= self.session.config['main_task_rounds']:
            yield (views.MainTask, {'low_payoff': 50, 'high_payoff': 100})

            if self.player.lottery_outcome == 'high':
                correct_payoff = c(100)
            else:
                correct_payoff = c(50)

            assert self.player.lottery_payoff == correct_payoff

            if self.player.round_number == self.player.participant.vars['relevant_round']:
                assert self.player.payoff == correct_payoff

    def simulate_data(self):
        # this function is for simulating data.
        if self.player.round_number <= self.session.config['main_task_rounds']:

            player_id = self.player.id_in_group
            round_number = self.player.round_number
            order = self.player.participant.vars['lottery_order']
            small_step = self.player.participant.vars['steps'][self.player.round_number - 1]['small_step']
            big_step = self.player.participant.vars['steps'][self.player.round_number - 1]['big_step']
            steps = self.session.vars['max_steps']

            # simulate lower risk taking for Active treatment:
            if self.player.participant.vars['mode'] == 'Active':
                lottery_choice = self.random_draw(self.get_payoff_list(small_step, big_step, steps), 'bias_safe')
            else:
                lottery_choice = self.random_draw(self.get_payoff_list(small_step, big_step, steps), 'bias_risky')                

            #print(lottery_choice)

            yield (views.MainTask, lottery_choice)


    def get_payoff_list(self, small_step, big_step, steps):
        payoff_list = []
        for i in range(steps):
            payoff_list.append({'low_payoff': i*small_step, 'high_payoff': steps*small_step + big_step*(steps-i)})
        payoff_list.append({'low_payoff': steps*small_step, 'high_payoff': steps*small_step})
        return payoff_list


    def normal_draw(self, payoff_list, mu, sigma):
        list_length = len(payoff_list)
        draw = random.gauss(mu, sigma)

        closest_int = int(round(draw))
        if closest_int >= list_length:
            closest_int = list_length - 1
        if closest_int < 0:
            closest_int = 0

        return payoff_list[closest_int]

    def random_draw(self, payoff_list, method='uniform'):
        calc_length = len(payoff_list)-1

        if method == 'bias_risky':
            mu = calc_length/4
            sigma = 1/6 * calc_length

            return self.normal_draw(payoff_list, mu, sigma)


        if method == 'bias_safe':
            mu = calc_length/4*3
            sigma = 1/6 * calc_length

            return self.normal_draw(payoff_list, mu, sigma)


        if method == 'normal':
            mu = calc_length/2
            sigma = 1/6 * calc_length

            return self.normal_draw(payoff_list, mu, sigma)


        return random.choice(payoff_list)