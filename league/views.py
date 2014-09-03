from django.shortcuts import render, redirect
from league.models import League, Roster, Player
from league.forms import LeagueForm
import logging

logger = logging.getLogger(__name__)

# Create your views here.
# '/'
def index(request, *args, **kwargs):
    ''' Create the league page or select one '''
    data = {}
    data['leagues'] = League.objects.all()
    if request.method == 'GET':
        form = LeagueForm()
    elif request.method == 'POST':
        form = LeagueForm(request.POST)
        if form.is_valid():
            league = form.save()
            return redirect('/league/%s/' % league.id)
    data['form'] = form
    return render(request, 'index.html', data)
    

def view_league(request, league_id):
    ''' Main dashboard for league '''
    print league_id
    if request.method == 'GET':
        data = {'league': League.objects.get(id=league_id)}
        return render(request, 'league.html', data)
