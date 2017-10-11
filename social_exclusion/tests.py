from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants
from otree.api import SubmissionMustFail




class PlayerBot(Bot):


    # in allplay_1 all players invite
    # in allplay_2 some not invite but no majority
    # in notallplay there is a majority
    cases = ['allplay_1', 'allplay_2', 'notallplay']

    #the voting of a player is a complex behavior, because each player only can vote for the other players, but not himself
    #therefore the input a player makes, depends on his player label
    #function returns a dic with the correct voting behavior of a player
    #all players invite all players
    def set_voting_behavior(self, in_ex):
        votealldic = {in_ex+'_A':True, in_ex+'_B':True, in_ex+'_C':True, in_ex+'_D':True, in_ex+'_E':True}
        label = self.player.label[-1]
        icanvotefor = {}
        for poss in votealldic.keys():
            if label not in poss:
                icanvotefor[poss] = votealldic[poss]
        print('Bot ' + self.player.label + ' will make vote decisions: ' + str(icanvotefor))
        return icanvotefor

    #note: votes here can be used as invitations or as exclusions
    def complex_voting_behavior(self,in_ex, majority):
        if majority == 'nomajority':
            return {'Player A': {in_ex+'_B':False, in_ex+'_C':True, in_ex+'_D':True, in_ex+'_E':True},
                'Player B': {in_ex+'_A':False, in_ex+'_C':True, in_ex+'_D':True, in_ex+'_E':True},
                'Player C': {in_ex+'_A':True, in_ex+'_B':True, in_ex+'_D':True, in_ex+'_E':True},
                'Player D': {in_ex+'_A':False, in_ex+'_B':True, in_ex+'_C':True, in_ex+'_E':True},
                'Player E': {in_ex+'_A':True, in_ex+'_B':False, in_ex+'_C':True, in_ex+'_D':True},}
        elif majority == 'yesmajority':
            return {'Player A': {in_ex+'_B':True, in_ex+'_C':True, in_ex+'_D':False, in_ex+'_E':True },
                'Player B': {in_ex+'_A':True, in_ex+'_C':True, in_ex+'_D':False, in_ex+'_E':True },
                'Player C': {in_ex+'_A':True, in_ex+'_B':True, in_ex+'_D':False, in_ex+'_E':True },
                'Player D': {in_ex+'_A':True, in_ex+'_B':True, in_ex+'_C':True, in_ex+'_E':True },
                'Player E': {in_ex+'_A':True, in_ex+'_B':True, in_ex+'_C':True, in_ex+'_D':False },}
        else:
            raise Exception ('wrong input of function complex voting behavior')



    def play_round(self):

        if self.player.treatment == 'inclusion':
            yield (views.Instructions)

            for wrong_input in [-1,-0.01, 'hello', '!', 101, 55.5, '']:
                yield SubmissionMustFail(views.FirstContribution, {'cont_first': wrong_input})


            yield (views.FirstContribution, {'cont_first':100})
            assert self.group.total_cont_first == 500
            assert self.group.indiv_share_first == 200
            assert self.player.payoff == 200
            yield (views.FirstResults)

            #all players invite all players
            if self.case == 'allplay_1':
                print('Ive been here: allplay 1')
                yield (views.Vote, self.set_voting_behavior('invite'))
                assert self.group.all_play == 'True'
                assert self.player.plays_secondpg == True

            #player A and B only get 2 invitations, others get all, no majority
            elif self.case == 'allplay_2':
                print('Ive been here: allplay 2')
                yield (views.Vote, self.complex_voting_behavior('invite','nomajority')[self.player.label])
                if self.player.label == 'Player A' or self.player.label == 'Player B':
                    assert self.player.myvotes_inclusion == 2
                else:
                    assert self.player.myvotes_inclusion == 4
                assert self.group.all_play == 'True'
            #player D gets 0 invitations
            elif self.case == 'notallplay':
                print('Ive been here: notallplay')
                yield (views.Vote, self.complex_voting_behavior('invite','yesmajority')[self.player.label])
                if self.player.label == 'Player D':
                    assert self.player.myvotes_inclusion == 0
                else:
                    assert self.player.myvotes_inclusion == 4
                assert self.group.all_play=='False'

            else:
                print('titanic sinks in 1 sec...')


            yield (views.VoteResults)

            if self.player.plays_secondpg == False:
                yield (views.InsteadOfSecondContribution)
            elif self.player.plays_secondpg == True:

                for wrong_input in [-1,-0.01, 'hello', '!', 101, 55.5, '']:
                    yield SubmissionMustFail(views.SecondContribution, {'cont_second': wrong_input})

                yield (views.SecondContribution, {'cont_second': 50})
                if self.group.all_play == 'True':
                    assert self.group.total_cont_second == 250
                #if only 4 players contribute 50
                else:
                    assert self.group.total_cont_second == 200

            yield (views.SecondResults)

            if self.round_number == Constants.num_rounds:
                yield (views.LastPage)


        elif self.player.treatment == 'exclusion':

            yield (views.Instructions)

            for wrong_input in [-1, -0.01, 'hello', '!', 101, 55.5, '']:
                yield SubmissionMustFail(views.FirstContribution, {'cont_first': wrong_input})

            yield (views.FirstContribution, {'cont_first': 100})
            assert self.group.total_cont_first == 500
            assert self.group.indiv_share_first == 200
            assert self.player.payoff == 200
            yield (views.FirstResults)

            # all players invite all players
            if self.case == 'allplay_1':
                print('Ive been here: allplay 1')
                yield (views.Vote, self.set_voting_behavior('exclude'))
                assert self.group.all_play == 'True'
                assert self.player.plays_secondpg == True

            # player A and B only get 2 exclusions, others get non exclusions, no majority
            elif self.case == 'allplay_2':
                print('Ive been here: allplay 2')
                yield (views.Vote, self.complex_voting_behavior('exclude','nomajority')[self.player.label])
                if self.player.label == 'Player A' or self.player.label == 'Player B':
                    assert self.player.myvotes_exclusion == 2
                else:
                    assert self.player.myvotes_exclusion == 0
                assert self.group.all_play == 'True'
            # player D gets 4 exclusions, other get non exclusio
            elif self.case == 'notallplay':
                print('Ive been here: notallplay')
                yield (views.Vote, self.complex_voting_behavior('exclude','yesmajority')[self.player.label])
                if self.player.label == 'Player D':
                    assert self.player.myvotes_exclusion == 4
                else:
                    assert self.player.myvotes_exclusion == 0
                assert self.group.all_play == 'False'

            else:
                print('titanic sinks in 1 sec...')

            yield (views.VoteResults)

            if self.player.plays_secondpg == False:
                yield (views.InsteadOfSecondContribution)
            elif self.player.plays_secondpg == True:

                for wrong_input in [-1, -0.01, 'hello', '!', 101, 55.5, '']:
                    yield SubmissionMustFail(views.SecondContribution, {'cont_second': wrong_input})

                yield (views.SecondContribution, {'cont_second': 50})
                if self.group.all_play == 'True':
                    assert self.group.total_cont_second == 250
                # if only 4 players contribute 50
                else:
                    assert self.group.total_cont_second == 200

            yield (views.SecondResults)

            if self.round_number == Constants.num_rounds:
                yield (views.LastPage)


