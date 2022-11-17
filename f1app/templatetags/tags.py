from django import template
import collections
import logging
import re
from f1app.utils import META_FIELDS
from rest_framework import utils

from f1app.models import Driver, Constructor

register = template.Library()
logger = logging.getLogger('django')

@register.filter(name='get_fields')
def get_fields(model):
    return model._meta.get_fields()

@register.filter(name='id_name')
def id_name(field_name):
    field_list = field_name.split() 
    field_list = (list)(map(lambda s: s.lower(), field_list))
    return '-'.join(field_list)

@register.filter
def pretty_name(field_name):
    field_list = re.split('-|_', field_name) 
    field_list = (list)(map(lambda s: s.capitalize(), field_list))
    return ' '.join(field_list)

@register.filter(name='upper_underscore')
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
def get_item(dictionary, key):
    if(dictionary.__class__ == collections.OrderedDict):
        return dictionary.get(key)
    return None

@register.filter
def is_ordered_dict(field):
    return field.__class__ == collections.OrderedDict

@register.filter
def is_meta_field(field):
    return field in META_FIELDS

@register.filter
def is_driver(field):
    return field.related_model == Driver

@register.filter
def is_constructor(field):
    return field.related_model == Constructor

@register.filter
def is_relation(field):
    return field.is_relation
