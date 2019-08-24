# 2019 Emir Erbasan (humanova)
# MIT License, see LICENSE for more details

import codecs
import json

import requests
from bs4 import BeautifulSoup


def GetVictimsInventory(kills):

    victim_item_list = []
    for url in kills:

        kill_id = url.rsplit('/', 1)[-1]
        url = f"https://gameinfo.albiononline.com/api/gameinfo/events/{kill_id}"

        data = None
        try:
            r = requests.get(url)
            data = r.json()
        except Exception as e:
            print(f"Error while getting/parsing url : {url}...")
            print(e)

        player = data['Victim']['Name']
        main_hand = data['Victim']['Equipment']['MainHand']['Type']
        head = data['Victim']['Equipment']['Head']['Type']
        armor = data['Victim']['Equipment']['Armor']['Type']
        shoes = data['Victim']['Equipment']['Shoes']['Type']
        #bag = data['Victim']['Equipment']['Bag']['Type']
        #cape = data['Victim']['Equipment']['Cape']['Type']
        #mount = data['Victim']['Equipment']['Mount']['Type']

        if not data['Victim']['Equipment']['OffHand'] == None:
            off_hand = data['Victim']['Equipment']['OffHand']['Type']
        else:
            off_hand = "None"

        victim_items = {'Player': player,
                        'MainHand': main_hand,
                        'OffHand': off_hand,
                        'Head': head,
                        'Armor': armor,
                        'Shoes': shoes}

        victim_item_list.append(victim_items)

    return victim_item_list


def GetTotalItems(victim_inventories):

    total_items = {}
    for inv in victim_inventories:
        for key, value in inv.items():
            if key == 'Player' or value == 'None':
                continue
            if value in total_items.keys():
                total_items[value] += 1
            else:
                total_items[value] = 1
    total_items = sorted(total_items.items(), key=lambda x: x[1], reverse=True)
    return total_items


def GetItemPrice(item_name, count):

    url = f"https://www.albion-online-data.com/api/v2/stats/prices/{item_name}?locations=Caerleon"

    try:
        r = requests.get(url)
        data = r.json()
    except Exception as e:
        print(f"Error while getting/parsing url : {url}...")
        print(e)

    price = int(data[0]['sell_price_min'])
    return price * count
