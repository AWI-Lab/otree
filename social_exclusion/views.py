from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants



class Instructions(Page):
    pass

class FirstContribution(Page):
    form_model = models.Player
    form_fields = ['cont_first']



class FirstWaitPage(WaitPage):
    def after_all_players_arrive(self):
        self.group.set_payoffs_first()



class FirstResults(Page):
    def vars_for_template(self):
        data = {}
        #TODO: you wouldnt need the dic assignment because getplayers is ordered
        #TODO: But I find this safer
        #TODO: Note Vars for template cannot be tested, therefore this has to be safe and doublechecked
        for player in self.group.get_players():
            #remove whitespace from label so that it can be displayed in the template
            data[(player.label).replace(' ','')] = player.cont_first
        return data



class Vote(Page):
    form_model = models.Player
    form_fields = ['invite_A', 'invite_B','invite_C','invite_D','invite_E','exclude_A','exclude_B', 'exclude_C', 'exclude_D', 'exclude_E']
    #TODO: In general you should really deeply think about these error messages
    #TODO: they work for now, but caution is needed, if e. g. you would change default settings of the Booleans
    #TODO: should be implemented in tests detailed to ensure no surprises occur in further steps of developing
    def error_message(self, values):
        if self.player.treatment == 'inclusion':
            vote_count = 0
            #count how many invitations the player distributed
            #including all players here is no problem because the player itself has for his own invite variable False or NAN
            #even if it would be true per default nothing would happen
            for vote in [values['invite_A'],values['invite_B'],values['invite_C'],values['invite_D'],values['invite_E']]:
                if vote == True:
                    vote_count += 1
            if vote_count<3:
                return 'Please choose to invite 3 or 4 players.'
        elif self.player.treatment=='exclusion':
            vote_count = 0
            #note: we can use here the same definition, as the inverting of the variable takes place on the next wait page
            #so vote == True if the player did not deselect the respective choice. Also vote == False here for the players own exclude variables
            for vote in [values['exclude_A'],values['exclude_B'],values['exclude_C'],values['exclude_D'],values['exclude_E']]:
                if vote == True:
                    vote_count += 1
            if vote_count<3:
                return 'Please only exclude one player'


class VoteWaitPage(WaitPage):
    def after_all_players_arrive(self):
        #invert exclusion variable in exclusion treatment
        if self.session.config['treatment'] == 'exclusion':
            self.group.invert_exclusions()
        #count the votes (exclusions or invitations) for every player
        self.group.set_myvotes()
        #assign for each player if he plays the second pg game
        self.group.set_second_game()
        #assign the excluded player, if there is one, on a group variable
        self.group.set_excluded_player()


class VoteResults(Page):
   def vars_for_template(self):
       treatment = self.group.get_players()[0].treatment
       data = {}
       # TODO: you wouldnt need the dic assignment because getplayers is ordered
       # TODO: But I find this safer
       # TODO: Note Vars for template cannot be tested, therefore this has to be safe and doublechecked
       for player in self.group.get_players():
           if treatment == 'inclusion':
               data[(player.label).replace(' ', '') + '_votes'] = player.myvotes_inclusion
           elif treatment == 'exclusion':
               data[(player.label).replace(' ', '') + '_votes'] = player.myvotes_exclusion

           data[(player.label).replace(' ', '') + '_plays'] = player.plays_secondpg

       return data

class InsteadOfSecondContribution(Page):
    def is_displayed(self):
        if self.player.plays_secondpg == True:
            return False
        elif self.player.plays_secondpg == False:
            return True

class SecondContribution(Page):
    form_model = models.Player
    form_fields = ['cont_second']
    def is_displayed(self):
        if self.player.plays_secondpg == True:
            return True
        elif self.player.plays_secondpg == False:
            return False



class SecondWaitPage(WaitPage):
    def after_all_players_arrive(self):
        #this sets payoff and initializes the indiv share and total cont variables
        self.group.set_payoffs_second()


class SecondResults(Page):
    def vars_for_template(self):
        data = {}
        #TODO: you wouldnt need the dic assignment because getplayers is ordered
        #TODO: But I find this safer
        #TODO: Note Vars for template cannot be tested, therefore this has to be safe and doublechecked
        for player in self.group.get_players():
            #regard all players here but in template only display the ones who actually played
            #remove whitespace from label so that it can be displayed in the template
            data[(player.label).replace(' ','')] = player.cont_second
        return data


class LastPage(Page):
  def is_displayed(self):
      if self.player.round_number == Constants.num_rounds:
          return True
      else:
          return False




page_sequence = [
    Instructions,
    FirstContribution,
    FirstWaitPage,
    FirstResults,
    Vote,
    VoteWaitPage,
    VoteResults,
    InsteadOfSecondContribution,
    SecondContribution,
    SecondWaitPage,
    SecondResults,
    LastPage
]
