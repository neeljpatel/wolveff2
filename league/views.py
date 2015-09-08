from django.shortcuts import render, redirect
# from django.http import HttpResponseRedirect
from league.models import League, TemplatePlayer
from league.forms import LeagueForm, NewTeamForm, UploadFileForm, MovePlayerForm, NextPlayerForm
# from league.util import fill_league_with_players


def upload_player(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            TemplatePlayer.load_csv(request.FILES['file'])
        else:
            print 'form not valid'
            print form.errors

    return redirect('index')


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
            # fill_league_with_players(league)
            league.populate_players()
            return redirect('/league/%s/' % league.id)

    data['form'] = form
    data['upload'] = UploadFileForm()
    return render(request, 'index.html', data)


def view_league(request, league_id):
    ''' Main dashboard for league '''
    league = get_league(league_id)

    # if request.method == 'POST':
    #     if request.POST['action'] == 'newteam':
    #         # handle new team stuff here
    #         f = NewTeamForm(request.POST)
    #         if f.is_valid():
    #             roster = f.save(commit=False)
    #             roster.league = league
    #             roster.save()
    #         else:
    #             data['new_team_form'] = f
    # elif request.POST['action'] == 'assignplayer':
    #     player_on_deck_form = PlayerOnDeckForm(request.POST)
    #     if player_on_deck_form.is_valid():
    #         # print 'valid form'
    #         form_player = player_on_deck_form.save(commit=False)
    #         if form_player.cost and form_player.roster:
    #             stats = form_player.roster.get_bid_stats()
    #             if form_player.cost <= stats['max_bid']:
    #                 player = league.player_set.get(id=request.POST['playerid'])
    #                 player.cost = form_player.cost
    #                 player.roster = form_player.roster
    #                 player.save()

    #             else:
    #                 print 'cost too high'
    #         else:
    #             print 'no cost or roster'
    #     else:
    #         print request.POST
    #         print player_on_deck_form
    #         raise Exception()

    # elif request.method == 'GET':
    #     if 'next-player' in request.path:
    #         next_player = league.get_random_undraftend()

    #         if next_player:
    #             # print next_player.name
    #             data['next_player'] = next_player
    #             data['player_on_deck_form'] = PlayerOnDeckForm(instance=next_player)

    # remaining_players = league.remaining_players
    # rosters = []
    # for r in league.roster_set.all():
    #     rdata = r.get_bid_stats()
    #     rdata['name'] = r.name
    #     rdata['players'] = r.player_set.all()
    #     rosters.append(rdata)
    data = {}
    data['league'] = league
    # data['remaining_players'] = remaining_players
    # data['rosters'] = rosters
    # if 'new_team_form' not in data:
    data['new_team_form'] = NewTeamForm()
    data['move_player_form'] = MovePlayerForm()
    data['move_player_form'].fields['player'].queryset = league.player_set.all()
    data['move_player_form'].fields['roster'].queryset = league.roster_set.all()

    data['next_player_form'] = NextPlayerForm()
    data['next_player_form'].fields['roster'].queryset = league.roster_set.all()

    return render(request, 'league.html', data)


def assign_player(request, league_id):
    form = NextPlayerForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        league = get_league(league_id)
        roster = league.roster_set.get(name=data['roster'])
        cost = int(data['cost'])
        league.assign_player(roster, cost)
        # roster = form.roster
        # player = league.player_on_deck
        # if roster.afford(form.cost):
        #     player.cost = form.cost
        #     player.save()

        #     roster.player_set.add(league.player_on_deck)
        #     roster.save()

        #     league.player_on_deck = None
        #     league.save()

    return redirect('/league/%s/' % league_id)


def move_player(request, league_id):
    # league = get_league(league_id)
    form = MovePlayerForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        player = data['player']
        if data['roster']:
            player.cost = int(data['cost'])
            player.roster = data['roster']
            player.save()
        else:
            if player.roster:
                player.roster.player_set.remove(player)

    return redirect('/league/%s/' % league_id)


def next_player(request, league_id):
    league = get_league(league_id)
    league.next_player()
    return redirect('/league/%s/' % league_id)


def trash_player(request, league_id):
    get_league(league_id).trash_player()

    return redirect('/league/%s/' % league_id)


def create_team(request, league_id):
    # pdb.set_trace()
    if request.method == 'POST':
        league = get_league(league_id)
        form = NewTeamForm(request.POST)
        if form.is_valid():
            roster = form.save(commit=False)
            roster.league = league
            roster.save()
        
    return redirect('/league/%s/' % league_id)


def get_league(id):
    return League.objects.get(id=id)
