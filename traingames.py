import numpy as np
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
import csv
from random import randint


def evaluate_composition(hero_ids):
    
    hero_dict={'Razor': [u' Carry', u'Durable', u'Nuker', u'Pusher</p>\r\n\t\t\t\t\t<div class="c'], 'Legion_Commander': [u'Carry', u'Disabler', u'Initiator', u'Durable', u'Nuker</p>\r\n\t\t\t\t\t'], 'Undying': [u'Support', u'Durable', u'Disabler', u'Nuker</p>\r\n\t\t\t\t\t<div class'], 'Wraith_King': [u'Carry', u'Support', u'Durable', u'Disabler', u'Initiator</p>\r\n\t\t\t'], 'Juggernaut': [u'Carry', u'Pusher', u'Escape</p>\r\n\t\t\t\t\t<div class="centerColHR'], 'Ursa': [u'Carry', u'Jungler', u'Durable', u'Disabler</p>\r\n\t\t\t\t\t<div class'], 'Ancient_Apparition': [u' Support', u'Disabler', u'Nuker</p>\r\n\t\t\t\t\t<div class="centerC'], 'Bane': [u' Support', u'Disabler', u'Nuker', u'Durable</p>\r\n\t\t\t\t\t<div clas'], 'Pugna': [u' Nuker', u'Pusher</p>\r\n\t\t\t\t\t<div class="centerColHR"></div>'], 'Tinker': [u' Carry', u'Nuker', u'Pusher</p>\r\n\t\t\t\t\t<div class="centerColHR'], 'Terrorblade': [u'Carry', u'Pusher', u'Nuker</p>\r\n\t\t\t\t\t<div class="centerColHR"'], 'Omniknight': [u'Support', u'Durable', u'Nuker</p>\r\n\t\t\t\t\t<div class="centerCol'], 'Ogre_Magi': [u'Support', u'Nuker', u'Disabler', u'Durable', u'Initiator</p>\r\n\t\t\t'], 'Elder_Titan': [u'Initiator', u'Disabler', u'Nuker', u'Durable</p>\r\n\t\t\t\t\t<div cla'], 'Death_Prophet': [u' Carry', u'Pusher', u'Nuker', u'Disabler</p>\r\n\t\t\t\t\t<div class="'], 'Abaddon': [u'Support', u'Carry', u'Durable</p>\r\n\t\t\t\t\t<div class="centerCol'], 'Dark_Seer': [u'Initiator', u'Jungler', u'Escape', u'Disabler</p>\r\n\t\t\t\t\t<div cl'], 'Mirana': [u' Carry', u'Support', u'Escape', u'Nuker', u'Disabler</p>\r\n\t\t\t\t\t<d'], "Nature's_Prophet": [u' Carry', u'Jungler', u'Pusher', u'Escape', u'Nuker</p>\r\n\t\t\t\t\t<div'], 'Bristleback': [u'Carry', u'Durable', u'Initiator', u'Nuker</p>\r\n\t\t\t\t\t<div class='], 'Sand_King': [u'Initiator', u'Disabler', u'Nuker', u'Escape', u'Jungler</p>\r\n\t\t\t\t'], 'Troll_Warlord': [u' Carry', u'Pusher', u'Disabler', u'Durable</p>\r\n\t\t\t\t\t<div class'], 'Slardar': [u'Carry', u'Durable', u'Initiator', u'Disabler', u'Escape</p>\r\n\t\t\t\t'], 'Anti-Mage': [u'Carry', u'Escape', u'Nuker</p>\r\n\t\t\t\t\t<div class="centerColHR"'], 'Necrophos': [u' Carry', u'Nuker', u'Durable', u'Disabler</p>\r\n\t\t\t\t\t<div class='], 'Storm_Spirit': [u' Carry', u'Escape', u'Nuker', u'Initiator', u'Disabler</p>\r\n\t\t\t\t\t'], 'Medusa': [u' Carry', u'Disabler', u'Durable</p>\r\n\t\t\t\t\t<div class="centerC'], 'Ember_Spirit': [u'Carry', u'Escape', u'Nuker', u'Disabler', u'Initiator</p>\r\n\t\t\t\t\t<'], 'Queen_of_Pain': [u' Carry', u'Nuker', u'Escape</p>\r\n\t\t\t\t\t<div class="centerColHR'], 'Enchantress': [u' Support', u'Jungler', u'Pusher', u'Durable', u'Disabler</p>\r\n\t\t\t'], 'Tiny': [u'Carry', u'Nuker', u'Pusher', u'Initiator', u'Durable', u'Disabler</'], 'Riki': [u'Carry', u'Escape', u'Disabler</p>\r\n\t\t\t\t\t<div class="centerCol'], 'Invoker': [u' Carry', u'Nuker', u'Disabler', u'Escape', u'Pusher</p>\r\n\t\t\t\t\t<di'], 'Earth_Spirit': [u'Nuker', u'Escape', u'Disabler', u'Initiator', u'Durable</p>\r\n\t\t\t\t'], 'Sniper': [u' Carry', u'Nuker</p>\r\n\t\t\t\t\t<div class="centerColHR"></div>\r'], 'Witch_Doctor': [u' Support', u'Nuker', u'Disabler</p>\r\n\t\t\t\t\t<div class="centerC'], 'Leshrac': [u' Carry', u'Support', u'Nuker', u'Pusher', u'Disabler</p>\r\n\t\t\t\t\t<d'], 'Zeus': [u' Nuker</p>\r\n\t\t\t\t\t<div class="centerColHR"></div>\r\n\t\t\t\t\t\r\n'], 'Silencer': [u' Carry', u'Support', u'Disabler', u'Initiator', u'Nuker</p>\r\n\t\t\t\t'], 'Broodmother': [u'Carry', u'Pusher', u'Escape', u'Nuker</p>\r\n\t\t\t\t\t<div class="cen'], 'Enigma': [u' Disabler', u'Jungler', u'Initiator', u'Pusher</p>\r\n\t\t\t\t\t<div c'], 'Doom': [u'Carry', u'Disabler', u'Initiator', u'Durable', u'Nuker</p>\r\n\t\t\t\t\t'], 'Lina': [u' Support', u'Carry', u'Nuker', u'Disabler</p>\r\n\t\t\t\t\t<div class='], 'Spirit_Breaker': [u'Carry', u'Initiator', u'Disabler', u'Durable', u'Escape</p>\r\n\t\t\t\t'], 'Alchemist': [u'Carry', u'Support', u'Durable', u'Disabler', u'Initiator', u'Nuker<'], 'Batrider': [u' Initiator', u'Jungler', u'Disabler', u'Escape</p>\r\n\t\t\t\t\t<div c'], 'Brewmaster': [u'Carry', u'Initiator', u'Durable', u'Disabler', u'Nuker</p>\r\n\t\t\t\t\t'], 'Dragon_Knight': [u'Carry', u'Pusher', u'Durable', u'Disabler', u'Initiator', u'Nuker</'], 'Crystal_Maiden': [u' Support', u'Disabler', u'Nuker', u'Jungler</p>\r\n\t\t\t\t\t<div clas'], 'Drow_Ranger': [u' Carry', u'Disabler', u'Pusher</p>\r\n\t\t\t\t\t<div class="centerCo'], 'Techies': [u' Nuker', u'Disabler</p>\r\n\t\t\t\t\t<div class="centerColHR"></di'], 'Shadow_Demon': [u' Support', u'Disabler', u'Initiator', u'Nuker</p>\r\n\t\t\t\t\t<div cl'], 'Lifestealer': [u'Carry', u'Durable', u'Jungler', u'Escape', u'Disabler</p>\r\n\t\t\t\t\t<'], 'Gyrocopter': [u' Carry', u'Nuker', u'Disabler</p>\r\n\t\t\t\t\t<div class="centerCol'], 'Venomancer': [u' Support', u'Nuker', u'Initiator', u'Pusher', u'Disabler</p>\r\n\t\t\t'], 'Naga_Siren': [u'Carry', u'Support', u'Pusher', u'Disabler', u'Initiator', u'Escape<'], 'Treant_Protector': [u'Support', u'Initiator', u'Durable', u'Disabler', u'Escape</p>\r\n\t\t'], 'Morphling': [u' Carry', u'Escape', u'Durable', u'Nuker', u'Disabler</p>\r\n\t\t\t\t\t<d'], 'Lion': [u' Support', u'Disabler', u'Nuker', u'Initiator</p>\r\n\t\t\t\t\t<div cl'], 'Phantom_Lancer': [u'Carry', u'Escape', u'Pusher', u'Nuker</p>\r\n\t\t\t\t\t<div class="cen'], 'Dazzle': [u' Support', u'Nuker', u'Disabler</p>\r\n\t\t\t\t\t<div class="centerC'], 'Magnus': [u'Initiator', u'Disabler', u'Nuker', u'Escape</p>\r\n\t\t\t\t\t<div clas'], 'Axe': [u'Initiator', u'Durable', u'Disabler', u'Jungler</p>\r\n\t\t\t\t\t<div c'], 'Lone_Druid': [u' Carry', u'Pusher', u'Jungler', u'Durable</p>\r\n\t\t\t\t\t<div class='], 'Pudge': [u'Disabler', u'Initiator', u'Durable', u'Nuker</p>\r\n\t\t\t\t\t<div cla'], 'Centaur_Warrunner': [u'Durable', u'Initiator', u'Disabler', u'Nuker', u'Escape</p>\r\n\t\t\t\t'], 'Warlock': [u' Support', u'Initiator', u'Disabler</p>\r\n\t\t\t\t\t<div class="cen'], 'Skywrath_Mage': [u' Support', u'Nuker', u'Disabler</p>\r\n\t\t\t\t\t<div class="centerC'], 'Sven': [u'Carry', u'Disabler', u'Initiator', u'Durable', u'Nuker</p>\r\n\t\t\t\t\t'], 'Huskar': [u' Carry', u'Durable', u'Initiator</p>\r\n\t\t\t\t\t<div class="center'], 'Shadow_Shaman': [u' Support', u'Pusher', u'Disabler', u'Nuker', u'Initiator</p>\r\n\t\t\t'], 'Outworld_Devourer': [u' Carry', u'Nuker', u'Disabler</p>\r\n\t\t\t\t\t<div class="centerCol'], 'Clinkz': [u' Carry', u'Escape', u'Pusher</p>\r\n\t\t\t\t\t<div class="centerColH'], 'Keeper_of_the_Light': [u' Support', u'Nuker', u'Disabler', u'Jungler</p>\r\n\t\t\t\t\t<div clas'], 'Chaos_Knight': [u'Carry', u'Disabler', u'Durable', u'Pusher', u'Initiator</p>\r\n\t\t\t\t'], 'Clockwerk': [u'Initiator', u'Disabler', u'Durable', u'Nuker</p>\r\n\t\t\t\t\t<div cla'], 'Night_Stalker': [u'Carry', u'Initiator', u'Durable', u'Disabler', u'Nuker</p>\r\n\t\t\t\t\t'], 'Oracle': [u' Support', u'Nuker', u'Disabler', u'Escape</p>\r\n\t\t\t\t\t<div class'], 'Phantom_Assassin': [u'Carry', u'Escape</p>\r\n\t\t\t\t\t<div class="centerColHR"></div>\r'], 'Earthshaker': [u'Support', u'Initiator', u'Disabler', u'Nuker</p>\r\n\t\t\t\t\t<div cla'], 'Puck': [u' Initiator', u'Disabler', u'Escape', u'Nuker</p>\r\n\t\t\t\t\t<div cla'], 'Luna': [u' Carry', u'Nuker', u'Pusher</p>\r\n\t\t\t\t\t<div class="centerColHR'], 'Faceless_Void': [u'Carry', u'Initiator', u'Disabler', u'Escape', u'Durable</p>\r\n\t\t\t\t'], 'Shadow_Fiend': [u' Carry', u'Nuker</p>\r\n\t\t\t\t\t<div class="centerColHR"></div>\r'], 'Disruptor': [u' Support', u'Disabler', u'Nuker', u'Initiator</p>\r\n\t\t\t\t\t<div cl'], 'Timbersaw': [u'Nuker', u'Durable', u'Escape</p>\r\n\t\t\t\t\t<div class="centerColH'], 'Vengeful_Spirit': [u' Support', u'Initiator', u'Disabler', u'Nuker', u'Escape</p>\r\n\t\t\t'], 'Templar_Assassin': [u' Carry', u'Escape</p>\r\n\t\t\t\t\t<div class="centerColHR"></div>'], 'Winter_Wyvern': [u' Support', u'Disabler', u'Nuker</p>\r\n\t\t\t\t\t<div class="centerC'], 'Viper': [u' Carry', u'Durable', u'Initiator', u'Disabler</p>\r\n\t\t\t\t\t<div cl'], 'Tusk': [u'Initiator', u'Disabler', u'Nuker</p>\r\n\t\t\t\t\t<div class="center'], 'Lycan': [u'Carry', u'Pusher', u'Jungler', u'Durable', u'Escape</p>\r\n\t\t\t\t\t<di'], 'Phoenix': [u' Support', u'Nuker', u'Initiator', u'Escape', u'Disabler</p>\r\n\t\t\t'], 'Beastmaster': [u'Initiator', u'Disabler', u'Durable', u'Nuker</p>\r\n\t\t\t\t\t<div cla'], 'Bloodseeker': [u'Carry', u'Disabler', u'Jungler', u'Nuker', u'Initiator</p>\r\n\t\t\t\t\t'], 'Jakiro': [u' Support', u'Nuker', u'Pusher', u'Disabler</p>\r\n\t\t\t\t\t<div class'], 'Windranger': [u' Carry', u'Support', u'Disabler', u'Escape', u'Nuker</p>\r\n\t\t\t\t\t<d'], 'Meepo': [u'Carry', u'Escape', u'Nuker', u'Disabler', u'Initiator', u'Pusher</p'], 'Nyx_Assassin': [u'Disabler', u'Nuker', u'Initiator', u'Escape</p>\r\n\t\t\t\t\t<div clas'], 'Arc_Warden': [u' Carry', u'Escape', u'Nuker</p>\r\n\t\t\t\t\t<div class="centerColHR'], 'Spectre': [u'Carry', u'Durable', u'Escape</p>\r\n\t\t\t\t\t<div class="centerColH'], 'Kunkka': [u'Carry', u'Disabler', u'Initiator', u'Durable', u'Nuker</p>\r\n\t\t\t\t\t'], 'Slark': [u'Carry', u'Escape', u'Disabler', u'Nuker</p>\r\n\t\t\t\t\t<div class="c'], 'Weaver': [u' Carry', u'Escape</p>\r\n\t\t\t\t\t<div class="centerColHR"></div>'], 'Bounty_Hunter': [u'Escape', u'Nuker</p>\r\n\t\t\t\t\t<div class="centerColHR"></div>\r'], 'Lich': [u' Support', u'Nuker</p>\r\n\t\t\t\t\t<div class="centerColHR"></div'], 'Visage': [u' Support', u'Nuker', u'Durable', u'Disabler', u'Pusher</p>\r\n\t\t\t\t\t'], 'Tidehunter': [u'Initiator', u'Durable', u'Disabler', u'Nuker</p>\r\n\t\t\t\t\t<div cla'], 'Io': [u' Support', u'Escape', u'Nuker</p>\r\n\t\t\t\t\t<div class="centerCol'], 'Chen': [u' Support', u'Jungler', u'Pusher</p>\r\n\t\t\t\t\t<div class="centerC'], 'Rubick': [u' Support', u'Disabler', u'Nuker</p>\r\n\t\t\t\t\t<div class="centerC']}
    hero_mapping = {1: 'Anti-Mage', 2: 'Axe', 3: 'Bane', 4: 'Bloodseeker', 5: 'Crystal Maiden', 6: 'Drow Ranger', 7: 'Earthshaker', 8: 'Juggernaut', 9: 'Mirana', 10: 'Morphling', 11: 'Shadow Fiend', 12: 'Phantom Lancer', 13: 'Puck', 14: 'Pudge', 15: 'Razor', 16: 'Sand King', 17: 'Storm Spirit', 18: 'Sven', 19: 'Tiny', 20: 'Vengeful Spirit', 21: 'Windranger', 22: 'Zeus', 23: 'Kunkka', 25: 'Lina', 26: 'Lion', 27: 'Shadow Shaman', 28: 'Slardar', 29: 'Tidehunter', 30: 'Witch Doctor', 31: 'Lich', 32: 'Riki', 33: 'Enigma', 34: 'Tinker', 35: 'Sniper', 36: 'Necrophos', 37: 'Warlock', 38: 'Beastmaster', 39: 'Queen of Pain', 40: 'Venomancer', 41: 'Faceless Void', 42: 'Wraith King', 43: 'Death Prophet', 44: 'Phantom Assassin', 45: 'Pugna', 46: 'Templar Assassin', 47: 'Viper', 48: 'Luna', 49: 'Dragon Knight', 50: 'Dazzle', 51: 'Clockwerk', 52: 'Leshrac', 53: "Nature's Prophet", 54: 'Lifestealer', 55: 'Dark Seer', 56: 'Clinkz', 57: 'Omniknight', 58: 'Enchantress', 59: 'Huskar', 60: 'Night Stalker', 61: 'Broodmother', 62: 'Bounty Hunter', 63: 'Weaver', 64: 'Jakiro', 65: 'Batrider', 66: 'Chen', 67: 'Spectre', 68: 'Ancient Apparition', 69: 'Doom', 70: 'Ursa', 71: 'Spirit Breaker', 72: 'Gyrocopter', 73: 'Alchemist', 74: 'Invoker', 75: 'Silencer', 76: 'Outworld Devourer', 77: 'Lycan', 78: 'Brewmaster', 79: 'Shadow Demon', 80: 'Lone Druid', 81: 'Chaos Knight', 82: 'Meepo', 83: 'Treant Protector', 84: 'Ogre Magi', 85: 'Undying', 86: 'Rubick', 87: 'Disruptor', 88: 'Nyx Assassin', 89: 'Naga Siren', 90: 'Keeper of the Light', 91: 'Io', 92: 'Visage', 93: 'Slark', 94: 'Medusa', 95: 'Troll Warlord', 96: 'Centaur Warrunner', 97: 'Magnus', 98: 'Timbersaw', 99: 'Bristleback', 100: 'Tusk', 101: 'Skywrath Mage', 102: 'Abaddon', 103: 'Elder Titan', 104: 'Legion Commander', 105: 'Techies', 106: 'Ember Spirit', 107: 'Earth Spirit', 109: 'Terrorblade', 110: 'Phoenix', 111: 'Oracle', 112: 'Winter Wyvern', 113: 'Arc Warden'}
    highWinRate=["Omniknight","Spectre","Necrophos","Abaddon","Zeus","Ursa","Wraith King","Warlock","Undying"]

    radiantTeam = []
    direTeam = []
    hero_ids_radiant = hero_ids[0:5]
    hero_ids_dire = hero_ids[5:10]
    try:
        for hero in hero_ids_radiant:
            radiantTeam.append(hero_mapping[int(hero)].replace(" ", "_"))
    except KeyError:
        return 0


    try:
        for hero in hero_ids_dire:
            direTeam.append(hero_mapping[int(hero)].replace(" ", "_"))
    except KeyError:
        return 0


    dire=0
    rad=0

    DireSuppCount=0
    DireCarrCount=0
    DireJungCount=0
    DireNukCount=0
    DireDisCount=0
    DireInitCount=0

    for hero in direTeam:
        for s in hero_dict[hero]:
            if 'Disabler' in s :
                DireDisCount+=1
            if 'Support' in s:
                DireSuppCount+=1
            if 'Carry' in s:
                DireCarrCount+=1
            if 'Initiator' in s:
                DireInitCount+=1
            if 'Jungler' in s:
                DireJungCount+=1
            if 'Durable' in s:
                dire=dire+1
            if 'Nuker' in s:
                DireNukCount+=1

        if hero in highWinRate:
            dire+=2

    if DireInitCount>0:
        dire=dire+DireInitCount
    else:
        dire=dire-5

    if DireDisCount>0:
        dire=dire+DireDisCount
    else:
        dire=dire-5

    if DireSuppCount<=2 and DireSuppCount!=0:
        dire=dire+DireSuppCount
    elif DireSuppCount==0:
        dire=dire-5

    if DireCarrCount<=2 and DireCarrCount!=0:
        dire=dire+1
    else:
        dire= dire-(DireCarrCount-2)*1.5

    if DireJungCount>1:
        dire=dire-(DireJungCount-1)*2

    if DireNukCount>0:
        dire=dire+DireNukCount
    else:
        dire=dire-5

    RadSuppCount=0
    RadCarrCount=0
    RadJungCount=0
    RadNukCount=0
    RadDisCount=0
    RadInitCount=0

    for hero in radiantTeam:
        for s in hero_dict[hero]:
            if 'Disabler' in s :
                RadDisCount+=1
            if 'Support' in s:
                RadSuppCount+=1
            if 'Carry' in s:
                RadCarrCount+=1
            if 'Initiator' in s:
                RadInitCount+=1
            if 'Jungler' in s:
                RadJungCount+=1
            if 'Durable' in s:
                rad=rad+1
            if 'Nuker' in s:
                RadNukCount+=1

        if hero in highWinRate:
            rad+=2

    if RadInitCount>0:
        rad=rad+RadInitCount
    else:
        rad=rad-5

    if RadDisCount>0:
        rad=rad+RadDisCount
    else:
        rad=rad-5

    if RadSuppCount<=2 and RadSuppCount!=0:
        rad=rad+RadSuppCount
    elif RadSuppCount==0:
        rad=rad-5

    if RadCarrCount<=2 and RadCarrCount!=0:
        rad=rad+1
    else:
        rad= rad-(RadCarrCount-2)*1.5

    if RadJungCount>1:
        rad=rad-(RadJungCount-1)*2

    if RadNukCount>0:
        rad=rad+RadNukCount
    else:
        rad=rad-5

    result = float(rad - dire) / float(rad + dire)

    return result
    



def main():
    with open('gamesdata.csv', 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')

        david_set = []
        sk_set = []
        for row in csvreader:

            hero_ids = row[0:10]
            hero_winrates = row[10:20]
            david_mmr = row[20:30]
            sk_mmr = row[30:40]

            composition_result = evaluate_composition(hero_ids)

            david_entry = []
            sk_entry = []
            # for winrate in hero_winrates:
            #     david_entry.append(winrate)   
            #     sk_entry.append(winrate)

            # for mmr in david_mmr:
            #     david_entry.append(mmr)
            # for mmr in sk_mmr:
            #     sk_entry.append(mmr)

            david_entry.append(composition_result)
            sk_entry.append(composition_result)

            david_entry.append(row[-1])
            sk_entry.append(row[-1])

            david_set.append(david_entry)
            sk_set.append(sk_entry)


    print "\n\n Results Including Composition Evaluation \n\n"
    X_load = []
    y_load = []

    for entry in david_set:
        X_load.append(entry[:-1])
        y_load.append(entry[-1])

    X = np.array(X_load, dtype='float32')
    y = np.array(y_load, dtype='float32')

    kf = cross_validation.KFold(len(X_load), n_folds=10, shuffle=True)

    rfc_score = 0
    svc_score = 0
    for train_index, test_index in kf:
        data_train, data_test = X[train_index], X[test_index]
        target_train, target_test = y[train_index], y[test_index]

    # Random ForestClassifier
        clf = RandomForestClassifier(n_estimators=10, criterion='entropy')
        clf = clf.fit(data_train, target_train)
        score = clf.score(data_test, target_test)
        rfc_score += score
        
        # SVC
        clf = svm.SVC()
        clf.fit(data_train, target_train)
        score = clf.score(data_test, target_test)
        svc_score += score

        
    print "David RFC Score: " + str(float(rfc_score) / 10)
    print "David SVC Score: " + str(float(svc_score) / 10)

    X_load = []
    y_load = []
    for entry in sk_set:
        X_load.append(entry[:-1])
        y_load.append(entry[-1])

    X = np.array(X_load, dtype='float32')
    y = np.array(y_load, dtype='float32')

    kf = cross_validation.KFold(len(X_load), n_folds=10, shuffle=True)

    rfc_score = 0
    svc_score = 0
    for train_index, test_index in kf:
        data_train, data_test = X[train_index], X[test_index]
        target_train, target_test = y[train_index], y[test_index]

    # Random ForestClassifier
        clf = RandomForestClassifier(n_estimators=10, criterion='entropy')
        clf = clf.fit(data_train, target_train)
        score = clf.score(data_test, target_test)
        rfc_score += score
        
        # SVC
        clf = svm.SVC()
        clf.fit(data_train, target_train)
        score = clf.score(data_test, target_test)
        svc_score += score

        
    print "SK RFC Score: " + str(float(rfc_score) / 10)
    print "SK SVC Score: " + str(float(svc_score) / 10)


    print "\n\n Results Excluding Composition Evalution\n\n"
    X_load = []
    y_load = []
    for entry in david_set:
        X_load.append(entry[:-2])
        y_load.append(entry[-1])

    X = np.array(X_load, dtype='float32')
    y = np.array(y_load, dtype='float32')

    kf = cross_validation.KFold(len(X_load), n_folds=10, shuffle=True)

    rfc_score = 0
    svc_score = 0
    for train_index, test_index in kf:
        data_train, data_test = X[train_index], X[test_index]
        target_train, target_test = y[train_index], y[test_index]

    # Random ForestClassifier
        clf = RandomForestClassifier(n_estimators=10, criterion='entropy')
        clf = clf.fit(data_train, target_train)
        score = clf.score(data_test, target_test)
        rfc_score += score
        
        # SVC
        clf = svm.SVC()
        clf.fit(data_train, target_train)
        score = clf.score(data_test, target_test)
        svc_score += score

        
    print "David RFC Score: " + str(float(rfc_score) / 10)
    print "David SVC Score: " + str(float(svc_score) / 10)


    X_load = []
    y_load = []
    for entry in sk_set:
        X_load.append(entry[:-2])
        y_load.append(entry[-1])

    X = np.array(X_load, dtype='float32')
    y = np.array(y_load, dtype='float32')

    kf = cross_validation.KFold(len(X_load), n_folds=10, shuffle=True)

    rfc_score = 0
    svc_score = 0
    for train_index, test_index in kf:
        data_train, data_test = X[train_index], X[test_index]
        target_train, target_test = y[train_index], y[test_index]

    # Random ForestClassifier
        clf = RandomForestClassifier(n_estimators=10, criterion='entropy')
        clf = clf.fit(data_train, target_train)
        score = clf.score(data_test, target_test)
        rfc_score += score
        
        # SVC
        clf = svm.SVC()
        clf.fit(data_train, target_train)
        score = clf.score(data_test, target_test)
        svc_score += score

        
    print "SK RFC Score: " + str(float(rfc_score) / 10)
    print "SK SVC Score: " + str(float(svc_score) / 10)

if __name__ == "__main__":
    main()

