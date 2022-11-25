from os import error
from bs4 import BeautifulSoup
import logging
import random
import urllib.request
import pandas as pd

logger = logging.getLogger('django')

INTERESTING_TAGS = ['start', 'Start', 'atmosphere', 'Podium', '(L to R)']

def function_explain(func):
    def inner(*args, **kwargs):
        logger.info(f"passed arguments to {func.__name__}: {args}, {kwargs}")
        func(*args, **kwargs)
    return inner

def function_return(func):
    def inner(*args, **kwargs):
        result = func(*args, **kwargs)
        logger.info(f"returned value from {func.__name__}: {result}")
        return result
    return inner

def open_page(link):
    try:
        webUrl = urllib.request.urlopen(link)
    except error:
        print(error)
        return None
    soup = BeautifulSoup(webUrl.read(), 'html.parser') # Parsing content using beautifulsoup. Notice driver.page_source instead of page.content
    return soup

def is_interesting(photo_figure):
    description_caption = photo_figure.find("figcaption", {"class": "wp-caption-text gallery-caption"})
    if description_caption and any(map(lambda pattern: pattern in description_caption.get_text(), INTERESTING_TAGS)):
        return True

def get_interesting_figure_list(soup):
    gallery_box = soup.find("div", {"id": "gallery-1"})
    photo_figures = gallery_box.findAll("figure", {"class": "gallery-item"})
    return (list)(filter(is_interesting, photo_figures))

def get_race_photo_list(photo_figures, max_amount = 5):
    figure_sample = random.sample(photo_figures, min(max_amount, len(photo_figures)))
    return_list = []
    for photo_figure in figure_sample:
        photo_link = photo_figure.find('a')['href']
        soup = open_page(photo_link)
        if soup is None: continue
        attachment = soup.find("div", {"class": "entry-attachment"})
        if attachment and attachment.find('img') and attachment.find('img').get('src'):
            return_list.append(attachment.find('img').get('src'))
    return return_list
            
def get_gallery_from_race(url_origin):
    soup = open_page(url_origin)
    if soup is None: return
    figure_list = get_interesting_figure_list(soup)
    return get_race_photo_list(figure_list)

def get_lowercase_hyphened_name(name):
    return name.lower().replace(' ', '-')

def get_image_links(race):
    race_date = race.date.strftime("%Y/%m/%d")
    full_name = get_lowercase_hyphened_name(race.grand_prix.full_name)
    url = "https://www.racefans.net/" + race_date + "/" + (str)(race.year.year) + "-" + full_name + "-in-pictures/"
    logger.info(url)
    return get_gallery_from_race(url)


### not used
def combine_ordered_dicts(first_dict, first_key, second_dict, second_key):
    lst1_df = pd.DataFrame(first_dict)
    lst2_df = pd.DataFrame(second_dict)
    lst2_df.rename(columns={second_key: first_key}, inplace=True)
    lst_concat_df = pd.concat([lst1_df, lst2_df])
    lst_grouped_res_df = lst_concat_df.groupby([first_key]).agg(sum)
    print(lst_grouped_res_df.reset_index().to_dict('records'))