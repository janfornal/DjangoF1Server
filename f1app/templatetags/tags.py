from django import template
from f1app.variables import CURRENT_YEAR, META_FIELDS
from django_project_2 import settings
import collections
import logging
import re
import os
from bs4 import BeautifulSoup
import urllib.request
from f1app.models import Driver, SeasonEntrantConstructor, SeasonEntrantDriver
from f1app.serializers import SeasonEntrantDriverSerializer
from rest_framework import utils

register = template.Library()
logger = logging.getLogger('django')

@register.filter
def get_fields(model):
    return model._meta.get_fields()

@register.filter
def id_name(field_name):
    field_list = field_name.split() 
    field_list = (list)(map(lambda s: s.lower(), field_list))
    return '-'.join(field_list)

@register.filter
def pretty_name(field_name):
    field_list = re.split('-|_', field_name) 
    field_list = (list)(map(lambda s: s.capitalize(), field_list))
    return ' '.join(field_list)

@register.filter
def upper_underscore(field_name):
    field_list = re.split('-|_', field_name)
    field_list = (list)(map(lambda s: s.capitalize(), field_list))
    return '_'.join(field_list)

@register.filter
def column_names(data):
    if(type(data) == utils.serializer_helpers.ReturnList):
        return (list)(data[0].keys())
    if(type(data) == collections.OrderedDict):
        return (list)(data.keys())
    raise TypeError("Allowed argument types are: " + utils.serializer_helpers.ReturnList + " and " + collections.OrderedDict)

@register.filter
def get_photo(object):
    local_path = os.path.join(settings.BASE_DIR, 'static/f1app/img/%s.jpg' % object)
    if os.path.isfile(local_path):
        return "/static/f1app/img/%s.jpg" % object
    else:
        path_to_follow = 'https://en.wikipedia.org/wiki/%s' % object
        webUrl = urllib.request.urlopen(path_to_follow)
        soup = BeautifulSoup(webUrl.read(), 'html.parser')
        box_list = soup.findAll("td", {"class": "infobox-image"})
        for box in box_list:
            return "https:%s" % box.find('img')['src']

@register.filter
def get_range(a):
    return range(1, a+1)

@register.filter
def item(dictionary, key):
    return get_item(dictionary, key)

@register.filter
def get_item(dictionary, key):
    if dictionary.__class__ in [collections.OrderedDict, dict, utils.serializer_helpers.ReturnDict]:
        return dictionary.get(key)
    return None

@register.filter
def is_ordered_dict(field):
    return field.__class__ == collections.OrderedDict

@register.filter
def is_meta_field(field):
    return field in META_FIELDS

@register.filter
def is_relation(field):
    return field.is_relation

#### TODO nieserializowane !!!!!
@register.simple_tag()
def current_drivers():
    return SeasonEntrantDriver.driver_from_season(CURRENT_YEAR)

#### TODO nieserializowane !!!!!
@register.simple_tag()
def current_constructors():
    return SeasonEntrantConstructor.constructor_from_season(CURRENT_YEAR)

@register.simple_tag()
def last_years():
    return range(CURRENT_YEAR, CURRENT_YEAR - 20, -1)
