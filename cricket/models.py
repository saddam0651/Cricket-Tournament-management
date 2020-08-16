from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.


class Team(models.Model):
    name = models.CharField(max_length=50)
    logoUrl = models.ImageField(upload_to='team', default='default.jpg')
    clubState = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.clubState} {self.name}'

    @property
    def teamMatch(self):
        return self.mteam1.objects.all()


class Player(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    imageUrl = models.ImageField(upload_to='player', default='default.png')
    jerseyNumber = models.IntegerField()
    country = models.CharField(
        max_length=50,
        choices=(
            ('India', 'India'),
            ('Australia', 'Australia'),
            ('West Indies', 'West Indies'),
            ('South Africa', 'South Africa'),
            ('New Zealand', 'New Zealand'),
            ('Sri Lanka', 'Sri Lanka'),
            ('Afghanistan', 'Afghanistan'),
            ('Pakistan', 'Pakistan'),
            ('England', 'England')
        ),
        default='India'
    )
    role = models.CharField(
        max_length=50,
        choices=(
            ('Batsman', 'Batsman'),
            ('Wicket Keeper', 'Wicket Keeper'),
            ('All Rounder', 'All Rounder'),
            ('Bowler', 'Bowler')
        ),
        default='Batsman'
    )
    matches = models.IntegerField()
    runs = models.IntegerField()
    wickets = models.IntegerField()
    highestScore = models.IntegerField()
    fifties = models.IntegerField()
    hundreds = models.IntegerField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return f'''{self.firstName} {self.lastName} |
            {self.team.clubState} {self.team.name}'''


class Match(models.Model):
    team1 = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='mteam1')
    team2 = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='mteam2')
    result = models.CharField(
        max_length=50,
        null=True,
        choices=(
            ('Team1', 'Team1'),
            ('Team2', 'Team2'),
            ('Tie', 'Tie'),
        )
    )

    def __str__(self):
        return f'''{self.team1.clubState} {self.team1.name} vs
            {self.team2.clubState} {self.team2.name} | {self.result}'''


class Point(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE)
    played = models.IntegerField(default=0)
    won = models.IntegerField(default=0)
    lost = models.IntegerField(default=0)
    tied = models.IntegerField(default=0)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.team.name


@receiver(post_save, sender=Team)
def TeamPoint(sender, instance, created, *args, **kwargs):
    if created:
        point = Point.objects.create(team=instance)
        point.save()


@receiver(post_save, sender=Match)
def MatchPoint(sender, instance, created, **kwargs):
    if not created:
        c = Point.objects.get(team=instance.team1)
        d = Point.objects.get(team=instance.team2)

        if instance.result == 'Team1':
            c.played += 1
            c.won += 1
            c.points += 2
            c.save()
            d.played += 1
            d.lost += 1
            d.save()
        elif instance.result == 'Team2':
            d.played += 1
            d.won += 1
            d.points += 2
            d.save()
            c.played += 1
            c.lost += 1
            c.save()
        else:
            c.played += 1
            c.tied += 1
            c.points += 1
            c.save()
            d.played += 1
            d.tied += 1
            d.points += 1
            d.save()
