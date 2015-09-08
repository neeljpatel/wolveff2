from django.db import models
from random import randint
import csv


BUDGET = 100
MAX_PLAYERS = 14
AVAILABLE_POSITIONS = (
        ('qb','quarterback'),
        ('rb', 'running back'),
        ('wr', 'wide receiver'),
        ('te', 'tight end'),
        ('k', 'kicker'),
        ('def', 'defense')
    )

# Create your models here.
class League(models.Model):
    name = models.CharField(max_length=200, unique=True)
    player_on_deck = models.ForeignKey('Player', null=True, related_name='player_on_deck')

    @property
    def rosters(self):
        return self.roster_set.all()

    def next_player(self):
        self.player_on_deck = self.remaining_players[randint(0, len(self.remaining_players) - 1)]
        self.save()

    def trash_player(self):
        self.player_on_deck.is_garbage = True
        self.player_on_deck.save()
        self.player_on_deck = None
        self.save()

    def assign_player(self, team, cost):
        if not team.afford(cost):
            return False

        self.player_on_deck.cost = cost
        self.player_on_deck.save()

        team.player_set.add(self.player_on_deck)
        self.player_on_deck = None
        self.save()

        return True

    @property
    def remaining_players(self):
        return [i for i in self.player_set.all() if i.is_available()]

    def populate_players(self):
        players = [Player(number=tp.id_number,
                          name=tp.name,
                          position=tp.position,
                          team=tp.position,
                          league=self)
                   for tp in TemplatePlayer.objects.all()]
        self.player_set.bulk_create(players)
        # for tp in TemplatePlayer.objects.all():
        #     self.player_set.create(number=tp.id_number,
        #                            name=tp.name,
        #                            position=tp.position,
        #                            team=tp.position)

    def __str__(self):
        return self.name


class Roster(models.Model):
    name = models.CharField(max_length=200)
    budget = models.IntegerField(default=BUDGET)
    league = models.ForeignKey(League)

    def get_bid_stats(self):
        players = self.player_set.all()
        # print 'players = %d' % len(players)
        # print 'total cost = %d' % sum([i.cost for i in players])
        spent = sum([i.cost for i in players])
        remaining = BUDGET - spent
        max_bid = remaining - (MAX_PLAYERS - len(players))
        return {'spent': spent, 'remaining': remaining, 'max_bid': max_bid}

    @property
    def players(self):
        return self.player_set.all()
    

    @property
    def bid_stats(self):
        return self.get_bid_stats()

    @property
    def spent(self):
        return sum([i.cost for i in self.player_set.all()])
    
    @property
    def remaining(self):
        return BUDGET - self.spent
    
    @property
    def max_bid(self):
        return self.remaining - (MAX_PLAYERS - len(self.player_set.all()))

    def afford(self, cost):
        return cost <= self.get_bid_stats()['max_bid']

    def __str__(self):
        return self.name

class Player(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=200)
    team = models.CharField(max_length=200)
    position = models.CharField(max_length=200, choices=AVAILABLE_POSITIONS)
    # bye_week = models.IntegerField()
    league = models.ForeignKey(League)
    is_garbage = models.BooleanField(default=False)
    roster = models.ForeignKey(Roster, null=True, blank=True)
    cost = models.IntegerField(null=True, blank=True)

    def is_drafted(self):
        return self.roster is not None

    def is_available(self):
        return self.roster is None and not self.is_garbage

    def __str__(self):
        return '{}, {}, ({})'.format(self.name, self.position, self.team)

    class Meta:
        ordering = ['number']


class TemplatePlayer(models.Model):
    id_number = models.IntegerField()
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=5)
    team = models.CharField(max_length=10)

    @classmethod
    def load_csv(cls, data):
        reader = csv.DictReader(data.read().splitlines())
        players_to_add = []
        for row in reader:
            id_number = int(row['Id'])
            player = row['Player']
            position = row['Pos']
            team = row['Team']

            tplayer = cls(id_number=id_number,
                          name=player,
                          position=position,
                          team=team)

            players_to_add.append(tplayer)
        print 'added %d players' % len(players_to_add)
        TemplatePlayer.objects.bulk_create(players_to_add)