from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'social_exclusion'
    players_per_group = 5
    num_rounds = 2
    endowment = c(100)
    multiplier = 2



class Subsession(BaseSubsession):

    #TODO this is deterministic but should be fine as I group randomly?
    def define_label(self):
        labellist = ['Player A', 'Player B', 'Player C', 'Player D', 'Player E']
        for group in self.get_group_matrix():
            for player in group:
                player.label = labellist[player.id_in_group-1]

    def creating_session(self):
        #assign treatment
        for player in self.get_players():
            player.treatment = self.session.config['treatment']
            player.city = self.session.config['city']
        #TODO: is group randomly the desired impementation?
        if self.round_number == 1:
            self.group_randomly()
        else:
            self.group_like_round(1)
        #assign the labels
        self.define_label()


class Group(BaseGroup):

    total_cont_first = models.CurrencyField(
        doc='The overall contribution of the group in the first public good game of the round')

    indiv_share_first = models.CurrencyField(
        doc='The share the players get after the first public good game')

    total_cont_second = models.CurrencyField(
        doc='The overall contribution of the group in the second public good game of the round')

    indiv_share_second = models.CurrencyField(
        doc='The share the players get after the second public good game')


    all_play = models.CharField(
        doc='Equals True if all players play the second Public Good game in the round')

    #is needed so that we can display on any template the excluded player
    excluded_player = models.CharField(
        doc='The player, who is excluded from the second public good game.')

    def set_excluded_player(self):
        for player in self.get_players():
            if player.plays_secondpg == False:
                self.excluded_player = player.label


    #first pg game;function also sets total_cont and individual share
    def set_payoffs_first(self):
        self.total_cont_first = sum([p.cont_first for p in self.get_players()])
        self.indiv_share_first = self.total_cont_first * Constants.multiplier / Constants.players_per_group
        for p in self.get_players():
            p.payoff = (Constants.endowment - p.cont_first) + self.indiv_share_first


    def set_payoffs_second(self):
        self.total_cont_second = sum([p.cont_second for p in self.get_players() if p.plays_secondpg == True])
        if self.all_play == 'False':
            self.indiv_share_second = self.total_cont_second * Constants.multiplier / 4
            for player in self.get_players():
                if player.plays_secondpg == True:
                    player.payoff = player.payoff + (Constants.endowment - player.cont_second) + self.indiv_share_second
        elif self.all_play =='True':
            self.indiv_share_second = self.total_cont_second * Constants.multiplier / 5
            for player in self.get_players():
                player.payoff = player.payoff + (Constants.endowment - player.cont_second) + self.indiv_share_second



    #assigns for all the players how many votes (exclusions in exclusion treatment; invitations in inclusion treatment) the player had
    #the variables that are assigned are 'myvotes_inclusion' and 'myvotes_exclusion'
    #TODO: in exclusion treatment the function invert_exclusions has to be run first!
    def set_myvotes(self):
        for set_player in self.get_players():
            vote_count = 0
            if set_player.treatment=='inclusion':
                #screen the invitations of all players
                for voter in self.get_players():
                    votesdic = {'Player A': voter.invite_A,
                                'Player B': voter.invite_B,
                                'Player C': voter.invite_C,
                                'Player D': voter.invite_D,
                                'Player E': voter.invite_E}
                    #check if the voter did invite the set_player
                    if votesdic[set_player.label] == True:
                        vote_count +=1
                set_player.myvotes_inclusion = vote_count

            elif set_player.treatment == 'exclusion':
                for voter in self.get_players():
                    votesdic = {'Player A': voter.exclude_A,
                                'Player B': voter.exclude_B,
                                'Player C': voter.exclude_C,
                                'Player D': voter.exclude_D,
                                'Player E': voter.exclude_E}
                    # check if the voter did invite the set_player
                    if votesdic[set_player.label] == True:
                        vote_count += 1
                set_player.myvotes_exclusion = vote_count


    #find out if there is a majority at the invitations
    #assign for all players if they play in the second game
    #assign if the second game will be with all
    #TODO: in exclusion treatment invert_exclusions has to be run first!
    def set_second_game(self):
        treatment = self.get_players()[0].treatment
        invitationslist = []
        min_max = None

        if treatment == 'inclusion':
            for player in self.get_players():
                invitationslist.append(player.myvotes_inclusion)
            #find the smalltest number of invitations a player had
            min_max = min(invitationslist)

        elif treatment == 'exclusion':
            for player in self.get_players():
                invitationslist.append(player.myvotes_exclusion)
            #find the highest number of exclusions a player had
            min_max = max(invitationslist)

        #check if min_max is unique
        occurence = invitationslist.count(min_max)
        #unique min_max, there is a majority
        if occurence == 1:
            self.all_play = 'False'
            if treatment == 'inclusion':
                #identify the player with the least invitations
                for player in self.get_players():
                    if player.myvotes_inclusion == min_max:
                        #the default is True
                        player.plays_secondpg = False
            elif treatment == 'exclusion':
                #identify the player with the most exclusions
                for player in self.get_players():
                    if player.myvotes_exclusion == min_max:
                        #the default is True
                        player.plays_secondpg = False
        #not unique, no majority
        elif occurence > 1:
            self.all_play = 'True'


    #TODO: I want that exclude_X in the database is one, if the player unchecks the prechecked box
    #TODO: I use this inversing function for this. Might be a better solution out there.
    def invert_exclusions(self):
        for player in self.get_players():
            attlist = [player.exclude_A, player.exclude_B, player.exclude_C, player.exclude_D, player.exclude_E]
            #invert the list
            attlist = [not i for i in attlist]
            #assign the players own exclude variable a 0, so it will not be counted for myvotes exclusions
            indexdic = {'Player A':0, 'Player B':1, 'Player C':2, 'Player D':3, 'Player E':4}
            index = indexdic[player.label]
            attlist[index] = 0
            #assign the values back to the players exclusions
            player.exclude_A, player.exclude_B, player.exclude_C, player.exclude_D, player.exclude_E = attlist[0], attlist[1], attlist[2], attlist[3], attlist[4]


class Player(BasePlayer):

    label = models.CharField(
        doc='The player name. Player A - Player E',
        choices=['Player A', 'Player B', 'Player C', 'Player D', 'Player E'])

    treatment = models.CharField(
        doc='Defines the treatment of the session. The treatment is the same for all players in one session.',
        choices=['inclusion', 'exclusion'])

    city = models.CharField(
        doc='Defines the city where the experiment took place ',
        choices=['heidelberg', 'karlsruhe'])


    cont_first = models.CurrencyField(
        doc='The players contribution in the first public good game of the round.',
        verbose_name='What do you want to contribute to the project?',
        min=0,
        max=Constants.endowment)

    plays_secondpg = models.BooleanField(
        doc='A bool that displays if the player plays in the second public good game.',
        default=True)



    cont_second = models.CurrencyField(
        doc='The players contribution in the second public good game of the round.',
        verbose_name='What do you want to contribute to the project?',
        min=0,
        max=Constants.endowment)

    myvotes_inclusion = models.IntegerField(
        doc='The number of invitations the player got for the second public good game')

    myvotes_exclusion = models.IntegerField(
        doc='The number of negative votes the player got for the second public good game')


    #inclusion treatment
    # these vars have a one if the processing player did invite the player by clicking the invite checkbox in inclusive treatment
    invite_A = models.BooleanField(
        widget=widgets.CheckboxInput(),
        verbose_name='Player A')
    invite_B = models.BooleanField(
        widget=widgets.CheckboxInput(),
        verbose_name='Player B')
    invite_C = models.BooleanField(
        widget=widgets.CheckboxInput(),
        verbose_name='Player C')
    invite_D = models.BooleanField(
        widget=widgets.CheckboxInput(),
        verbose_name='Player D')
    invite_E = models.BooleanField(
        widget=widgets.CheckboxInput(),
        verbose_name='Player E')


    #these vars have a one if the processing player did exclude the player by deselecting the checkbox in exclusive treatments
    #note this variable definition is obtained by invterting the raw variable after the voting occured
    exclude_A = models.BooleanField(
        widget=widgets.CheckboxInput(),
        verbose_name='Player A',
        initial=True,)
    exclude_B = models.BooleanField(
        widget=widgets.CheckboxInput(),
        verbose_name='Player B',
        initial=True)
    exclude_C = models.BooleanField(
        widget=widgets.CheckboxInput(),
        verbose_name='Player C',
        initial=True)
    exclude_D = models.BooleanField(
        widget=widgets.CheckboxInput(),
        verbose_name='Player D',
        initial=True)
    exclude_E = models.BooleanField(
        widget=widgets.CheckboxInput(),
        verbose_name='Player E',
        initial=True)














