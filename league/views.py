from django.shortcuts import render, redirect
from league.models import League
from league.forms import LeagueForm, NewTeamForm, PlayerOnDeckForm
from league.util import fill_league_with_players

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
            fill_league_with_players(league)
            return redirect('/league/%s/' % league.id)

    data['form'] = form
    return render(request, 'index.html', data)


def view_league(request, league_id):
    ''' Main dashboard for league '''
    data = {}
    league = get_league(league_id)
    
    if request.method == 'POST':
        if request.POST['action'] == 'newteam':
            # handle new team stuff here
            f = NewTeamForm(request.POST)
            if f.is_valid():
                roster = f.save(commit=False)
                roster.league = league
                roster.save()
            else:
                data['new_team_form'] = f
        elif request.POST['action'] == 'assignplayer':
            player_on_deck_form = PlayerOnDeckForm(request.POST)
            if player_on_deck_form.is_valid():
                print 'valid form'
                form_player = player_on_deck_form.save(commit=False)
                if form_player.cost and form_player.roster:
                    stats = form_player.roster.get_bid_stats()
                    if form_player.cost <= stats['max_bid']:
                        player = league.player_set.get(id=request.POST['playerid'])
                        player.cost = form_player.cost
                        player.roster = form_player.roster
                        player.save()

                    else:
                        print 'cost too high'
                else:
                    print 'no cost or roster'
            else:
                print request.POST
                print player_on_deck_form
                raise Exception()

    elif request.method == 'GET':
        if 'next-player' in request.path:
            next_player = league.get_random_undraftend()

            if next_player:
                print next_player.name
                data['next_player'] = next_player
                data['player_on_deck_form'] = PlayerOnDeckForm(instance=next_player)

    remaining_players = [i for i in league.player_set.all()
                         if not i.is_drafted()]
    rosters = []
    for r in league.roster_set.all():
        rdata = r.get_bid_stats()
        rdata['name'] = r.name
        rdata['players'] = r.player_set.all()
        rosters.append(rdata)

    data['league'] = league
    data['remaining_players'] = remaining_players
    data['rosters'] = rosters
    if 'new_team_form' not in data:
        data['new_team_form'] = NewTeamForm()

    return render(request, 'league.html', data)


def get_league(id):
    return League.objects.get(id=id)
