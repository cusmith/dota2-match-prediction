#######################################################################################
#																					  #
#	This generates a dataset of player statistics and their predicted MMR category    #
#																					  #
#######################################################################################


import csv
import requests

def main():
	NORMAL_IDS = []
	HIGH_IDS = []
	VERY_HIGH_IDS = []

	# Get Match History for each Account
	with open('mmrdata.csv', 'wb') as csvfile:
		outfile = csv.writer(csvfile, delimiter=',')

		params = {"key": "ACABEB1FD8894A44B2A5AB4B79209C75", "skill": 1, "game_mode": 22}
		r = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001", params=params).json()

		for match in r["result"].get("matches", []):
			for player in match["players"]:
				try:
					if player["account_id"] not in NORMAL_IDS:
						NORMAL_IDS.append(player["account_id"])
				except KeyError:
					pass

		params = {"key": "ACABEB1FD8894A44B2A5AB4B79209C75", "skill": 2, "game_mode": 22}
		r = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001", params=params).json()

		for match in r["result"].get("matches", []):
			for player in match["players"]:
				try:
					if player["account_id"] not in HIGH_IDS:
						HIGH_IDS.append(player["account_id"])
				except KeyError:
					pass

		params = {"key": "ACABEB1FD8894A44B2A5AB4B79209C75", "skill": 3, "game_mode": 22}
		r = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001", params=params).json()

		for match in r["result"].get("matches", []):
			for player in match["players"]:
				try:
					if player["account_id"] not in VERY_HIGH_IDS:
						VERY_HIGH_IDS.append(player["account_id"])
				except KeyError:
					pass

		categories = [NORMAL_IDS, HIGH_IDS, VERY_HIGH_IDS]
		total_players = len(NORMAL_IDS) + len(HIGH_IDS) + len(VERY_HIGH_IDS)
		output_counter = 0

		for category, account_ids in enumerate(categories):


			for account_id in account_ids:
				output_counter += 1
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
				try:
					r = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001", params=params).json()
				except ValueError:
					continue

				matches = []
				try:
					matches = r["result"]["matches"]
				except KeyError:
					continue

				for match in matches:
					# Get Match Details
					try:
						match_id = match["match_id"]
					except KeyError:
						continue
					params = {"key": "ACABEB1FD8894A44B2A5AB4B79209C75", "match_id": match_id}

					try:
						match_details = requests.get("https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001", params=params).json()
					except ValueError:
						continue

					try:
						players = match_details["result"]["players"]
					except KeyError:
						continue

					# Get Player Stats from this match
					for player in players:
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

					# Did the player win? Radient_win + on_radiant = yes, Radiant_loss + not_on_radiant = yes
					if match_details["result"]["radiant_win"] == on_radiant:
						wins += 1	
					else:
						losses += 1

					match_count += 1
					# print "Match #%d recorded for account_id %d in category %d." % (match_count, account_id, category)
					if match_count >= 50:
						break

				kda_avg = round((float(kills + assists) / (deaths+1)), 2)
				gpm_avg = gold_per_min / match_count
				xpm_avg = xp_per_min / match_count
				hero_damage_avg = hero_damage / match_count
				tower_damage_avg = tower_damage / match_count
				last_hits_avg = last_hits / match_count
				denies_avg = denies / match_count

				entry = [kda_avg, gpm_avg, xpm_avg, hero_damage_avg, tower_damage_avg, last_hits_avg, denies_avg, match_count, category]
				
				print "Player %d/%d: %s" % (output_counter, total_players, str(entry))

				outfile.writerow(entry)

if __name__ == "__main__":
    main()