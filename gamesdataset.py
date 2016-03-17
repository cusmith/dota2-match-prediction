import numpy as np
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm

import csv
import requests

def derive_mmr(kda_avg, gpm_avg, xpm_avg, hero_damage_avg, tower_damage_avg, last_hits_avg, denies_avg):
	return -1

def process_player(account_id, hero_id, clf1, clf2, clf3):
	match_count = 0
	all_matches = 0
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
		return []

	for match in matches:
		# Get Match Details
		match_id = match["match_id"]
		params = {"key": "ACABEB1FD8894A44B2A5AB4B79209C75", "match_id": match_id}

		try:
			match_details = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001", params=params).json()
		except ValueError:
			continue

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
				all_matches += 1


	kda_avg = round((float(kills + assists) / (deaths+1)), 2)
	gpm_avg = gold_per_min / match_count
	xpm_avg = xp_per_min / match_count
	hero_damage_avg = hero_damage / match_count
	tower_damage_avg = tower_damage / match_count
	last_hits_avg = last_hits / match_count
	denies_avg = denies / match_count
	
	hero_winrate = float(-1.000)
	if match_count:
		hero_winrate = float(wins) / float(match_count)

	player_attributes = np.array([kda_avg, gpm_avg, xpm_avg, hero_damage_avg, tower_damage_avg, last_hits_avg, denies_avg], dtype='float32')
	player_attributes = player_attributes.reshape(1, -1)
	# Calculate custom mmr
	mmr = derive_mmr(kda_avg, gpm_avg, xpm_avg, hero_damage_avg, tower_damage_avg, last_hits_avg, denies_avg)

	# Calculate scikit benchmark mmr
	sk_mmr1 = clf1.predict(player_attributes)
	sk_mmr2 = clf2.predict(player_attributes)
	sk_mmr3 = clf3.predict(player_attributes)

	sk_mmr = float(-1.000)
	sk_mmr = float(sk_mmr1 + sk_mmr2 + sk_mmr3) / float(3)

	result = [mmr, sk_mmr, hero_winrate]
	return result


def main():
	# Train scikit classifiers
	with open('mmrdata.csv', 'rb') as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',')
		X_load = []
		y_load = []

		for row in csvreader:
			X_load.append(row[:7])
			# X_load.append(row[:-1])
			y_load.append(row[-1])

	X = np.array(X_load, dtype='float32')
	y = np.array(y_load, dtype='float32')

	data_train, data_test, target_train, target_test = cross_validation.train_test_split(X, y, test_size=0.1, random_state=0)

	# Random ForestClassifier
	clf1 = RandomForestClassifier(n_estimators=10, criterion='entropy')
	clf1.fit(data_train, target_train)

	# Multinomial NB
	clf2 = MultinomialNB()
	clf2.fit(data_train, target_train)

	# SVC
	clf3 = svm.SVC()
	clf3.fit(data_train, target_train)

	match_count = 1
	with open('gamesdata.csv', 'wb') as csvfile:
		outfile = csv.writer(csvfile, delimiter=',')

		params = {"key": "ACABEB1FD8894A44B2A5AB4B79209C75", "skill": 3, "game_mode": 22}
		r = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001", params=params).json()

		matches = r['result']['matches']

		for match in matches:
			invalid_player = False
			player_count = 1
			team_radiant = []
			team_dire = []
			for player in match['players']:
				if invalid_player:
					break
				account_id = player['account_id']
				hero_id = player['hero_id']
				player_slot = player['player_slot']

				## Look up player history based on account_id

				## Guess MMR based on our algorithm
				## Calculate their recent winrate with that hero based on last 50 games
				result = process_player(account_id, hero_id, clf1, clf2, clf3)
				if len(result) < 3:
					mmr = -1
					sk_mmr = -1
					hero_winrate = -1
					invalid_player = True
				else:
					mmr = result[0]
					sk_mmr = result[1]
					hero_winrate = result[2]
					print "Player %d/10 processed for match #%d. MMR: %d, sk_MMR:%.2f, Hero ID: %d, Hero Winrate:%.2f" % (player_count, match_count, mmr, sk_mmr, hero_id, hero_winrate)

				if player_slot <= 4:
					team_radiant.append((hero_id, hero_winrate, mmr, sk_mmr))
				else:
					team_dire.append((hero_id, hero_winrate, mmr, sk_mmr))

				player_count += 1

			params = {"key": "ACABEB1FD8894A44B2A5AB4B79209C75", "match_id": match["match_id"]}
			match_details = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001", params=params).json()
			radiant_win = match_details["result"]["radiant_win"]

			entry = []

			# Record Match details in CSV
			# format = [hero_ids_radiant x5, hero_ids_dire x5, hero_winrate_radiant x5, hero_winrate_dire x5, mmr_radiant x5, mmr_dire x5, sk_mmr_radiant x5, sk_mmr_dire x5, radiant_win?]
			for player in team_radiant:
				entry.append(player[0])

			for player in team_dire:
				entry.append(player[0])

			for player in team_radiant:
				entry.append(player[1])

			for player in team_dire:
				entry.append(player[1])

			for player in team_radiant:
				entry.append(player[2])

			for player in team_dire:
				entry.append(player[2])

			for player in team_radiant:
				entry.append(player[3])

			for player in team_dire:
				entry.append(player[3])

			if radiant_win:
				entry.append(1)
			else:
				entry.append(0)

			if invalid_player or len(entry) < 41:
				print "Could not find info for all 10 players.  Trying next match."
			else:
				print "Match complete: " + str(entry)
				outfile.writerow(entry)
			match_count += 1



if __name__ == "__main__":
    main()







