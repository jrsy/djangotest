from django.shortcuts import render
from BeautifulSoup import BeautifulSoup
import re
import requests
import json

EPL_LEAGUE_TABLE_URL = 'http://www.premierleague.com/en-gb/matchday/league-table.html'
EPL_RESULTS_URL = 'http://www.premierleague.com/pa-services/api/football/desktop/competition/fandr/currentResultsComp/%7Bapikey%7D/query.json?competitionId=8&'

def get_epl_league_table():

	resp = requests.get(EPL_LEAGUE_TABLE_URL)
	html = BeautifulSoup(resp.text)

	club_rows = html.findAll('tr', {'class':re.compile('club-row .*')})

	league_table = list()

	for row in club_rows:

		current_club = {}
		current_club['name'] = row.find('td', {'class':'col-club'}).text
		current_club['played'] = row.find('td', {'class':'col-p'}).text
		current_club['wins'] = row.find('td', {'class':'col-w'}).text
		current_club['draws'] = row.find('td', {'class':'col-d'}).text
		current_club['losses'] = row.find('td', {'class':'col-l'}).text
		current_club['for'] = row.find('td', {'class':'col-gf'}).text
		current_club['against'] = row.find('td', {'class':'col-ga'}).text
		current_club['diff'] = row.find('td', {'class':'col-gd'}).text
		current_club['pts'] = row.find('td', {'class':'col-pts'}).text
		league_table.append(current_club)

	return league_table

def get_epl_results():

	resp = requests.get(EPL_RESULTS_URL)
	result_json = json.loads(resp.text)

	result_table = {}

	for result in result_json['abstractCacheWebRootElement']['matches']:

		if not result_table.has_key(result):
			result_table[result] = list()

		match_list = result_json['abstractCacheWebRootElement']['matches'][result]['8']
		for match in match_list:

			current_match = {}
			current_match['home_team'] = match['displayHomeTeamFullName']
			current_match['away_team'] = match['displayAwayTeamFullName']
			current_match['home_score'] = match['homeTeam90Score']
			current_match['away_score'] = match['awayTeam90Score']
			current_match['stadium'] = match['stadium']
			current_match['ko_time'] = match['koTime']
			result_table[result].append(current_match)

	return result_table

def index(request):

	epl_table = get_epl_league_table()
	epl_results = get_epl_results()

	context = {'epl_league_table': epl_table,
				'epl_results': epl_results }

	return render(request, 'soccer/index.html', context)