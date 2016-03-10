import csv
import requests

def derive_mmr():
	return -1



def process_player(account_id, hero_id):
	match_count = 0
	wins = 0
	losses = 0
	kills = 0
	deaths = 0
	assists = 0
	gold_per_min = 0
	xp_per_min = 0
	hero_damage = 0
	tower_damage = 0
	last_hits = 0
	denies = 0
	wins = 0
	losses = 0

	params = {"key": "ACABEB1FD8894A44B2A5AB4B79209C75", "account_id": account_id, "game_mode": 22}
	r = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001", params=params).json()

	try:
		matches = r["result"]["matches"]
	except KeyError:
		print "Error accessing account information: " + r
		return -1, -1

	for match in matches:
		# Get Match Details
		match_id = match["match_id"]
		params = {"key": "ACABEB1FD8894A44B2A5AB4B79209C75", "match_id": match_id}
		match_details = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001", params=params).json()

		# Get Player Stats from this match
		for player in match_details["result"]["players"]:
			if player.get("account_id", "") == account_id:
				
				# Features
				try:
					this_kills = player["kills"]
					this_deaths = player["deaths"]
					this_assists = player["assists"]
					this_gold_per_min = player["gold_per_min"]
					this_xp_per_min = player["xp_per_min"]
					this_hero_damage = player["hero_damage"]
					this_tower_damage = player["tower_damage"]
					this_last_hits = player["last_hits"]
					this_denies = player["denies"]
				except KeyError:
					continue

				kills += this_kills
				deaths += this_deaths
				assists += this_assists
				gold_per_min += this_gold_per_min
				xp_per_min += this_xp_per_min
				hero_damage += this_hero_damage
				tower_damage += this_tower_damage
				last_hits += this_last_hits
				denies += this_denies

				# Determine what team they were on
				player_slot = player["player_slot"]
				if player_slot <= 4:
					# This player was on Radiant team
					on_radiant = True
				else:
					on_radiant = False

			# Calculate their winrate for the current hero
			if player["hero_id"] == hero_id:
				if match_details["result"]["radiant_win"] == on_radiant:
					wins += 1	

				match_count += 1

		print "Match #%d recorded for account_id %d in category %d." % (match_count, account_id, category)


	kda_avg = round((float(kills + assists) / (deaths+1)), 2)
	gpm_avg = gold_per_min / match_count
	xpm_avg = xp_per_min / match_count
	hero_damage_avg = hero_damage / match_count
	tower_damage_avg = tower_damage / match_count
	last_hits_avg = last_hits / match_count
	denies_avg = denies / match_count
	
	if match_count:
		hero_winrate = float(wins) / float(match_count)

	mmr = derive_mmr()

	return mmr, hero_winrate


with open('gamesdata.csv', 'wb') as csvfile:
	outfile = csv.writer(csvfile, delimiter=',')

	params = {"key": "ACABEB1FD8894A44B2A5AB4B79209C75", "game_mode": 22}
	r = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001", params=params).json()

	matches = r['result']['matches']

	for match in matches:
		team_radiant = []
		team_dire = []
		for player in match['players']:
			account_id = player['account_id']
			hero_id = player['hero_id']
			player_slot = player['player_slot']

			## Look up player history based on account_id

			## Guess MMR based on our algorithm
			## Calculate their recent winrate with that hero based on last 50 games
			mmr, hero_winrate = process_player(account_id, hero_id)

			

			if player_slot <= 4:
				team_radiant.append((hero_id, hero_winrate, mmr))
			else:
				team_dire.append((hero_id, hero_winrate, mmr))