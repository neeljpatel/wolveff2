from django import forms
from league.models import League, Roster, Player

class LeagueForm(forms.ModelForm):
    class Meta:
        model = League
        fields = ('name',)

class NewTeamForm(forms.ModelForm):
    class Meta:
        model = Roster
        fields = ('name',)

class PlayerOnDeckForm(forms.ModelForm):
    # READONLY_FIELDS = (
    #     'name',
    #     'team',
    #     'number',
    #     'position',
    #     'bye_week',
    # )

    class Meta:
        model = Player
        fields = ('id', 'roster', 'cost',)