from otree.api import Currency as c, currency_range
from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    def play_round(self):
        
        # check if treatments are assigned correclty
        # the program cycles through treatments 1-4
        # remainder > 0 -> remainder = treatment number
        # remainder = 0 -> treatment number is 4
        correct_treatment = self.player.id % 4 if self.player.id % 4 > 0 else 4

        # correct mapping of treatment number to default
        correct_default = {
            1: "Safe",
            2: "Safe",
            3: "Risky",
            4: "Risky"
        }

        # correct mapping of treatment number to mode
        correct_mode = {
            1: "Active",
            2: "Passive",
            3: "Active",
            4: "Passive"
        }


        # check correct treatment number, mode and default
        assert self.player.treatment == correct_treatment
        assert self.player.participant.vars['default'] == correct_default[self.player.treatment]
        assert self.player.participant.vars['mode'] == correct_mode[self.player.treatment]


        yield (views.Welcome)
        yield (views.Instructions1)

        # check if the correct instructions are shown for Safe / Risky
        if self.player.participant.vars['default'] == "Safe":
            assert "risktaking_instructions/safe.png" in self.html
        else:
            assert "risktaking_instructions/risky.png" in self.html

        # check if the correct instructions are shown for Active / Passive
        if self.player.participant.vars['mode'] == "Active":
            assert "müssen Sie nichts tun" in self.html
        else:
            assert "müssen Sie innerhalb von" in self.html

        yield (views.Instructions2)

        # check correct instructions before trial page
        if self.player.participant.vars['mode'] == "Active":
            assert "des Balkens anzupassen, klicken Sie auf" in self.html
        else:
            assert "wird automatisch alle 5 Sekunden angepasst." in self.html

        yield (views.TryOutAnnouncement)


        yield (views.TryOut)
        yield (views.MainTaskPrep)