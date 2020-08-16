from django.contrib import admin
from .models import *
from django.urls import path
from django.http import HttpResponseRedirect
import random

# Register your models here.
admin.site.site_header = 'Tournament Administration'
admin.site.index_title = 'Tournament Admin Panel'
admin.site.site_title = 'Tournament'

admin.site.register(Team)
admin.site.register(Player)


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    readonly_fields = ['team1', 'team2']
    change_list_template = 'admin/cricket/match_change_list.html'

    def has_add_permission(self, request):
        return False

    def get_urls(self):
        urls = super().get_urls()
        customUrls = [
            path('randomMatch/', self.createRandomMatch)
        ]
        return customUrls + urls

    def createRandomMatch(self, request):
        teams = Team.objects.all()
        teamsList = [team for team in teams]
        teamsListPair = []

        for i in range(len(teamsList)):
            for j in range(i + 1, len(teamsList)):
                teamsListPair.append([teamsList[i], teamsList[j]])

        random.shuffle(teamsListPair)

        for item in teamsListPair:
            match = Match(team1=item[0], team2=item[1])
            match.save()

        self.message_user(request, 'Random matches created successfully!')
        return HttpResponseRedirect('../')


@admin.register(Point)
class PointAdmin(admin.ModelAdmin):
    list_display = ['team', 'played', 'won', 'lost', 'tied', 'points']
    readonly_fields = ['team', 'played', 'won', 'lost', 'tied', 'points']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
