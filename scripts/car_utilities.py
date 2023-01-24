import inspect
import re
import pandas as pd
import numpy as np
from general import open_page, find, find_next, find_from_list, find_all, find_direct_all, wiki_prefix

# functions returning links to wikipedia pages of formula 1 constructors

def get_current_constructors():
    mercedes_link = 'https://en.wikipedia.org/wiki/Mercedes-Benz_in_Formula_One'
    ferrari_link = 'https://en.wikipedia.org/wiki/Ferrari_Grand_Prix_results'
    mclaren_link = 'https://en.wikipedia.org/wiki/McLaren'
    williams_link = 'https://en.wikipedia.org/wiki/Williams_Grand_Prix_Engineering'
    aston_martin_link = 'https://en.wikipedia.org/wiki/Aston_Martin_in_Formula_One'
    alpine_link = 'https://en.wikipedia.org/wiki/Alpine_F1_Team'
    alphatauri_link = 'https://en.wikipedia.org/wiki/Scuderia_AlphaTauri'
    alfa_romeo_link = 'https://en.wikipedia.org/wiki/Alfa_Romeo_in_Formula_One'
    haas_link = 'https://en.wikipedia.org/wiki/Haas_F1_Team'
    red_bull_link = 'https://en.wikipedia.org/wiki/Red_Bull_Racing' 
    return [
        ('mercedes', mercedes_link),
        ('ferrari', ferrari_link),
        ('mclaren', mclaren_link),
        ('williams', williams_link),
        ('aston-martin', aston_martin_link),
        ('alpine', alpine_link),
        ('alphatauri', alphatauri_link),
        ('alfa-romeo', alfa_romeo_link),
        ('haas', haas_link),
        ('red-bull', red_bull_link),
    ]

def get_historic_constructors():
    constructors_result = []
    soup = open_page('https://en.wikipedia.org/wiki/List_of_Formula_One_constructors')
    historic_constructors_section = find(soup, "span", {'id': 'Former_constructors'}).parent
    table = find_next(historic_constructors_section, "table", {"class": "wikitable"})
    tbody = find(table, "tbody")
    for row in find_direct_all(tbody, "tr"):
        cells = find_direct_all(row)
        if len(cells) > 0:
            team_cell = cells[0]
            try:
                constructors_result.append((find(team_cell, 'a').contents[0], wiki_prefix + find(team_cell, 'a')['href']))
            except Exception as e:
                pass
    return constructors_result

# get all cars from given wikipedia page of formula 1 constructor
# TODO - get all cars from given year

def get_racing_record_table(url):
    def get_cars_from_table(table):
        list_of_results = []
        rows = find_all(table, "tr")
        try:
            title_row = next(filter(lambda item: re.search('(Year|Season)', str(item)), rows))
        except Exception as e:
            return 
        title_row = [str(x) for x in find_direct_all(title_row)]
        list_index = [i for i, item in enumerate(title_row) if re.search('(Car|Chassis)', item)]
        if len(list_index) == 0:
            return 
        car_index = list_index[0]
        for row in table.find_all("tr")[1:]:
            cells = find_direct_all(row)
            if len(cells) > car_index:
                car_cell = cells[car_index]
                try:
                    list_of_results.append(wiki_prefix + find(car_cell, 'a')['href'])
                except Exception as e:
                    pass
        return list_of_results
    soup = open_page(url)
    if soup is None: raise ValueError('Page with given url: %s does not exist!' % url)
    list_of_titles = ['Complete_Formula_One_results', 'Formula_One_results', 'Formula_One_World_Championship_results', 
        'Racing_results', 'Racing_record', 'Complete_World_Championship_results',
        'Complete_Formula_One_World_Championship_results', 'Championship_results',
        "Complete_Drivers'_World_Championship_results", 'Formula_One', 'Other', 'World_Championship_results']
    list_of_results = []
    racing_record_section = find_from_list(soup, "span", list_of_titles).parent
    cnt = 0
    for tag in racing_record_section.next_siblings:
        if tag.name == "h2":
            break
        elif tag.name == "h3":
            if cnt > 0: break
            cnt += 1
        elif tag.name == "table" and "wikitable" in tag['class']:
            list_of_results.append(get_cars_from_table(tag))
    return list_of_results

def get_racing_record_table_quickly(url):
    soup = open_page(url)
    content_section = find(soup, "div", {"class": "mw-content-ltr"})
    li_tags = find_all(content_section, "li")
    list_of_results = []
    for item in li_tags:
        list_of_results.append(wiki_prefix + find(item, "a").get('href'))
    return list_of_results

def car_list_scraper(list_of_constructors):
    return_list = []
    for item in list_of_constructors:
        id, url = item
        for item in get_racing_record_table_quickly(url):
            return_list.append((id, item))
    return return_list

###### scraping information about particular car

def get_page_title(soup, raise_exception = False):
    try:
        return find(soup, "span", {"class": "mw-page-title-main"}).get_text()
    except Exception as e:
        if raise_exception: raise e

def get_side_section_from_soup(soup, raise_exception = False):
    try:
        return find(soup, "table", {"class": "infobox"})
    except Exception as e:
        if raise_exception: raise e 
    
def get_photo_from_side_section(section, raise_exception = False):
    def get_actual_photo(url):
        soup = open_page(url)
        div_link = find(soup, "div", {"class": "fullImageLink", "id": "file"})
        return "https:" + find(div_link, "a").get('href')
    try: 
        url = wiki_prefix + find(find(section, "td", {"class": "infobox-image"}), 'a').get('href')
        return get_actual_photo(url)
    except (AttributeError, Exception) as e: 
        if raise_exception: raise e

def get_debut_from_side_section(section, raise_exception = False):
    try: 
        return find(section.find("th", string=re.compile("Debut")).parent, 'a').get('title')
    except (AttributeError, Exception) as e: 
        if raise_exception: raise e

def get_stat_table_from_side_section(section, raise_exception = False):
    try: 
        return find(section, "table", {"class": "wikitable"})
    except (AttributeError, Exception) as e:
        if raise_exception: raise e

def extract_stat_table_info(stat_table):
    events = []
    numbers = []
    for table_row in find_all(stat_table, "tr"):
        for column in find_all(table_row, ["th", "td"]):
            if column.name == "th":
                events.append(column.get_text())
            else:
                numbers.append((int)(column.get_text()))
    return dict(zip(events, numbers))

def car_scraper(row):
    url = row['Url']
    soup = open_page(url)
    row['Car'] = get_page_title(soup)
    section = get_side_section_from_soup(soup)
    if section is None: return row
    row['Photo'] = get_photo_from_side_section(section)
    row['Debut'] = get_debut_from_side_section(section)
    stat_table = get_stat_table_from_side_section(section)
    if stat_table is None: return row 
    try: 
        table_info = extract_stat_table_info(stat_table) 
        for key, value in table_info.items():
            if key in row.index.to_list():
                row[key] = value
    except (AttributeError, Exception): 
        pass
    return row
    
def collect_car_data(frame: pd.DataFrame) -> pd.DataFrame:
    old_column_names = ['Constructor', 'Url']
    new_column_names = old_column_names + ['Photo', 'Debut', 'Races', 'Wins', 'Poles', 'F/Laps', 'Car']
    if list(frame.columns) != old_column_names:
        raise ValueError('Wrong format of %s argument in %s' % (frame.__class__.__name__, inspect.currentframe().f_code.co_name))
    frame = frame.reindex(columns=new_column_names)
    frame = frame.apply(lambda row: car_scraper(row), axis = 1)
    return frame

tyrrell_list = car_list_scraper([('tyrrell', 'https://en.wikipedia.org/wiki/Category:Tyrrell_Formula_One_cars')])
frame = pd.DataFrame(tyrrell_list, columns=['Constructor', 'Url'])
collect_car_data(frame).to_csv('tmp/tyrrell.csv')