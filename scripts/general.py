from googleapiclient.discovery import build
import json
from urllib import request
from bs4 import BeautifulSoup

google_api_key = "AIzaSyCYWwkFENwTrTstBAzelZtoCK03V3arQu0"
google_cse_id = "c301728d33cd74777"
youtube_api_key = 'AIzaSyAL3SKKwwKoX7I_ZIyLtMSVuiRTHtGIzz8'
youtube = build('youtube', 'v3', developerKey=youtube_api_key)

wiki_prefix = 'https://en.wikipedia.org'

###### general utility

def get_and_print_response(request):
    response = request.execute()
    print(json.dumps(response, indent = 4))

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res

def open_page(link):
    try:
        webUrl = request.urlopen(link, timeout = 20)
    except Exception as e:
        print(e)
        return None
    soup = BeautifulSoup(webUrl.read(), 'html.parser') # Parsing content using beautifulsoup. Notice driver.page_source instead of page.content
    return soup

def find(element, tag = None, identifies = {}):
    return_element = element.find(tag, identifies) if tag else element.find(identifies)
    if return_element:
        return return_element
    else:
        raise Exception("%s does not have tag %s with identifies %s" % (element, tag, identifies))

def find_from_list(element, tag = None, list = []):
    for item in list:
        return_element = element.find(tag, {'id': item})
        if return_element:
            return return_element
    raise Exception("%s does not have tag %s with id identifier from list %s" % ("Element", tag, list))

def find_next(element, tag = None, identifies = {}):
    return_element = element.find_next(tag, identifies) if tag else element.find_next(identifies)
    if return_element:
        return return_element
    else:
        raise Exception("%s does not have tag %s with identifies %s" % ("Element", tag, identifies)) 

def find_all(element, tag = None, identifies = {}):
    return_element = element.find_all(tag, identifies) if tag else element.find_all(identifies)
    if return_element:
        return return_element
    else:
        raise Exception("%s does not have tag %s with identifies %s" % ("Element", tag, identifies)) 

def find_direct_all(element, tag = None, identifies = {}):
    return_element = element.find_all(tag, identifies, recursive=False) if tag else element.find_all(identifies, recursive=False)
    if return_element:
        return return_element
    else:
        raise Exception("%s not have tag %s with identifies %s" % ("Element", tag, identifies)) 