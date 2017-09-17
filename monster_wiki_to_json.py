#! /usr/bin/env python3
# coding: utf-8


map_element = {
    't' : 'Thunder',
    'w' : 'Water',
    'f' : 'Fire',
    'n' : 'Nature',
    'm' : 'Magic',
    'mt': 'Metal',
    'l' : 'Light',
    'd' : 'Dark',
    'e' : 'Earth'
}


def main():
    from requests import get
    import bs4 as bs
    import json

    print("Getting monster-wiki Database")

    # Get Monsters Page HTML
    site_url = 'http://monster-wiki.com/monster/'
    response = get(site_url)

    # HTML Scrapping
    soup = bs.BeautifulSoup(response.text, 'html.parser')

    # Get Hash and Time to Request the Monster List
    raw = soup.findAll("div", {"id": "search_monster"})[0]
    hash = raw["data-hash"]
    data_time = raw["data-time"]

    # Request The Monster List
    base_url = 'http://monster-wiki.com/monster-api/'
    url = base_url + "h=" + hash + "&t=" + data_time + '&rarity=any&element=any'
    response = get(url)

    # Init output Dictionary
    monsters_data = {}

    # Progression Indicator Values
    monsters_count_total = len(response.json()['result'])
    monster_count = 0

    for monster in response.json()['result'] :

        monster_code = monster['code']

        monsters_data[monster_code] = {}

        # Monster Page Scrapping
        monster_url = site_url + monster_code
        monster_html = get(monster_url)
        soup =bs.BeautifulSoup(monster_html.text, 'html.parser')
        data = soup.findAll("input", {"id": "monster_level_stat"})

        # Get Monster Data
        data_levels = json.loads(data[0]['data-stats'])
        decode_data_levels = {}

        # Decode Data from 32 Base
        for key in data_levels :
            decode_data_levels[key] = []
            for value in data_levels[key]:
                decode_value = int(value, 32)
                decode_data_levels[key].append(decode_value)

        # Dump Data in Dictionary
        monsters_data[monster_code]['level_data'] = decode_data_levels
        raw_stamina = soup.findAll("span", {'class':'stats-value-stamina'})
        monsters_data[monster_code]['level_data']['stamina'] = raw_stamina[0].string
        monsters_data[monster_code]['is_vip'] = monster['is_vip']

        # Format Elements Names
        monsters_data[monster_code]['elements'] = monster['elements']
        for index, element in enumerate(monsters_data[monster_code]['elements']):
            monsters_data[monster_code]['elements'][index] = map_element[element]

        # Progression
        monster_count += 1
        progress = round(monster_count / monsters_count_total * 100, 2)
        print("Progress : {} %    ".format(str(progress)), end='\r')

    # Dump Database into File
    file_name = 'monster-wiki-db.json'
    print("Duming Database into file: " + path + file_name)
    with open(file_name, 'w') as out:
        json.dump(monsters_data, out)
    print('Done')

if __name__ == '__main__':
    main()
