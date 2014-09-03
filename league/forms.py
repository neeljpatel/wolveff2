from django.forms import ModelForm
from league.models import League

class LeagueForm(ModelForm):
    class Meta:
        model = League
        fields = ('name', )