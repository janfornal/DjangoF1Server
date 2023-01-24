from datetime import datetime
from pathlib import Path
from typing import Union

from f1app.serializers import *
from f1app.models import *
from django.db import IntegrityError, transaction
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from time import perf_counter
import re
import pandas as pd
import numpy as np

from f1app.views import ConstructorPolePositionAPIView
from scripts.video_highlights import get_cleaned_video_data, get_race_highlights

BASE_DIR = Path(__file__).resolve().parents[7]   ### when running from shell

def serialize_with_abstraction_level():
    race = RaceData.objects.filter(race_id=1000)
    race_result_serializer = RaceResultSerializer(race, many=True)
    print(race_result_serializer.data[0])
    print(race_result_serializer.data[0].get('std_name'))

def serialize_constructor_model():
    driver_history = RaceData.objects.filter(constructor_id='red-bull', type='RACE_RESULT', position_number=1)
    serializer = ConstructorSerializer(driver_history,many=True)
    if len(driver_history) > 0:
        logger.info(serializer.data[0])

def delete_race_opinion_key_from_active_sessions():
    sessions = Session.objects.exclude(expire_date__lte=datetime.now())
    logged_in = [s.session_key for s in sessions if s.get_decoded().get('_auth_user_id')]
    for session_key in logged_in:
        s = SessionStore(session_key=session_key)
        del s['new_race_opinion']
        s.save()  

def print_session_dictionaries():
    sessions = Session.objects.exclude(expire_date__lte=datetime.now())
    for s in sessions:
        print(s.get_decoded())

def print_data_about_custom_user_from_username():
    user = User.objects.get(username = 'username2')
    print(user.__dict__)

def get_list_from_constructor_pole_position_api_view():
    api_view = ConstructorPolePositionAPIView()
    logger.iapi_view.get_queryset()

tuples = [(2021, 5), (2009, 8), (2012, 8), (2014, 10), (2011, 2), (2013, 15), (2022, 11), (2010, 10), (2020, 1), (2009, 2), (2011, 7), (2015, 10), (2007, 15), (2017, 1), (2011, 5), (2010, 6), (2014, 2), (2017, 2), (2017, 14), (2022, 15), (2008, 8), (2011, 8), (2011, 12), (2012, 8), (2011, 6), (2014, 
3), (2019, 11), (2021, 2), (2016, 11), (2020, 3), (2022, 2), (2019, 10), (2021, 9), (2015, 10), (2015, 2), (2013, 4), (2022, 1), (2016, 2), (2018, 4), (2016, 11), (2013, 6), (2017, 6), (2017, 10), (2013, 5), (2017, 1), (2008, 3), (2007, 10), (2014, 11), (2012, 5), (2021, 5), (2008, 15), (2018, 7), (2013, 9), (2017, 9), (2010, 2), (2014, 7), (2020, 9), (2018, 11), (2022, 12), (2013, 4), (2008, 5), (2022, 7), (2008, 6), (2009, 11), (2021, 14), (2016, 14), (2009, 6), (2013, 8), (2009, 15), (2011, 10), (2021, 5), (2013, 2), (2017, 4), (2007, 8), (2015, 5), (2020, 14), (2010, 14), (2012, 9), (2016, 3), (2011, 11), (2014, 8), (2011, 2), (2021, 1), (2014, 2), (2013, 6), (2013, 11), (2008, 7), (2017, 6), (2021, 15), (2019, 9), (2013, 5), (2018, 5), (2017, 15), (2009, 2), (2013, 10), (2008, 2), (2022, 3), (2021, 12), (2012, 15), (2020, 10), (2009, 6), (2019, 1), (2012, 8), (2010, 9), (2007, 15), (2016, 5), (2017, 10), (2019, 7), (2010, 7), (2014, 2), (2014, 8), (2022, 8), (2007, 1), (2009, 8), (2011, 7), (2020, 9), 
(2015, 4), (2019, 1), (2010, 8), (2013, 11), (2019, 5), (2009, 7), (2021, 5), (2015, 6), (2013, 9), (2008, 10), (2013, 15), (2013, 9), (2019, 10), (2018, 4), (2022, 8), (2017, 1), (2022, 15), (2020, 10), (2021, 1), (2020, 4), (2008, 2), (2021, 8), (2011, 8), (2008, 10), (2018, 4), (2016, 13), (2008, 14), (2014, 2), (2010, 13), (2022, 10), (2021, 1), (2020, 12), (2011, 2), (2015, 1), (2009, 7), (2011, 6), (2016, 4), (2021, 1), (2015, 3), (2009, 3), (2010, 8), (2016, 13), (2012, 8), (2014, 12), (2007, 10), (2015, 12), (2011, 14), (2011, 6), (2021, 5), (2022, 14), (2007, 4), (2008, 6), (2013, 11), (2007, 11), (2018, 4), (2021, 8), (2013, 8), (2012, 7), (2022, 11), (2014, 4), (2022, 6), (2015, 13), (2012, 1), (2017, 10), (2017, 15), (2018, 11), (2020, 7), (2015, 9), (2011, 6), (2009, 7), (2022, 3), (2019, 2), (2020, 1), (2019, 8), (2022, 13), (2020, 14), (2012, 1), (2019, 13), (2015, 9), (2015, 8), (2008, 5), (2011, 10), (2015, 9), (2017, 4), (2019, 2), (2009, 12), (2007, 2), (2021, 6), (2015, 8), (2022, 14), (2011, 6), (2013, 4), (2009, 11), (2008, 5), (2022, 1), (2021, 10), (2016, 13), (2013, 3), (2008, 2), (2019, 13), (2016, 14), (2018, 11), (2022, 12), (2019, 2), (2018, 4), (2007, 15), (2010, 12), (2008, 5), (2022, 5), (2018, 7), (2022, 14), (2015, 4), (2008, 15), (2012, 3), (2009, 9), (2016, 
12), (2015, 11), (2014, 14), (2007, 9), (2020, 7), (2019, 7), (2011, 13), (2017, 15), (2007, 1), (2020, 3), (2018, 6), (2020, 9), (2007, 6), (2011, 11), (2016, 7), (2019, 4), (2017, 12), (2007, 1), (2022, 4), (2007, 2), (2009, 15), (2014, 15), (2022, 1), (2021, 13), (2021, 14), (2018, 15), (2009, 1), (2007, 11), (2022, 14), (2021, 10), (2016, 8), (2014, 11), (2018, 8), (2016, 8), (2008, 1), (2017, 9), (2011, 11), (2021, 12), (2010, 15), (2022, 10), (2015, 15), (2020, 10), (2020, 12), (2020, 9), (2013, 11), (2019, 14), (2013, 14), (2016, 1), (2017, 13), (2012, 2), (2013, 12), (2021, 10), (2014, 10), (2021, 13), (2019, 2), (2008, 3), (2014, 12), (2011, 6), (2022, 8), (2014, 1), (2011, 13), (2007, 11), (2021, 5), (2019, 9), (2017, 9), (2017, 8), (2008, 4), (2022, 8), (2009, 14), (2010, 9), (2013, 9), (2007, 5), (2016, 3), (2007, 9), (2018, 5), (2022, 9), (2011, 9), (2012, 11), (2016, 4), (2014, 13), (2016, 6), (2014, 2), (2019, 11), (2014, 4), (2011, 13), (2019, 8), (2010, 8), (2019, 13), (2017, 14), (2016, 11), (2013, 13), (2011, 9), (2016, 15), (2020, 5), (2020, 15), (2013, 4), (2014, 10), (2019, 1), (2007, 1), (2009, 1), (2016, 4), (2011, 3), (2012, 
4), (2019, 11), (2017, 10), (2017, 15), (2010, 8), (2016, 5), (2019, 1), (2012, 2), (2022, 12), (2017, 7), (2008, 13), (2018, 14), (2022, 9), (2018, 11), (2019, 1), (2010, 8), (2016, 15), (2017, 5), (2017, 14), (2016, 5), (2021, 5), (2014, 1), (2011, 14), (2015, 12), (2009, 7), (2022, 3), (2007, 8), (2022, 14), (2017, 2), (2021, 3), (2014, 11), (2010, 12), (2012, 14), (2009, 8), (2013, 8), (2021, 5), (2013, 9), (2022, 2), (2020, 6), (2012, 14), (2021, 7), (2020, 15), (2008, 13), (2008, 6), (2015, 3), (2009, 1), (2020, 8), (2014, 13), (2019, 9), (2007, 4), (2019, 3), (2017, 1), 
(2021, 14), (2013, 1), (2019, 5), (2008, 4), (2020, 4), (2015, 15), (2013, 12), (2008, 6), (2012, 11), (2016, 9), (2018, 12), (2021, 12), (2018, 9), (2009, 2), (2011, 5), (2010, 1), (2007, 1), (2010, 4), (2021, 4), (2012, 15), (2008, 1), (2016, 12), (2007, 5), (2019, 7), (2010, 10), (2016, 7), (2021, 12), (2020, 8), (2009, 13), (2013, 2), (2007, 8), (2015, 4), (2007, 9), (2011, 6), (2014, 9), (2010, 9), (2021, 7), (2011, 8), (2010, 12), (2013, 14), (2015, 3), (2022, 9), (2013, 10), (2010, 1), (2010, 2), (2011, 14), (2013, 13), (2009, 8), (2010, 9), (2013, 7), (2020, 1), (2016, 
1), (2008, 14), (2010, 6), (2007, 13), (2011, 10), (2016, 5), (2019, 7), (2022, 7), (2021, 9), (2015, 7), (2009, 11), (2011, 4), (2020, 3), (2012, 10), (2008, 10), (2016, 11), (2007, 4), (2007, 8), (2016, 4), (2020, 5), (2011, 2), (2014, 10), (2010, 15), (2011, 15), (2009, 3), (2007, 1), (2022, 2), (2010, 8), (2008, 9), (2021, 3), (2016, 6), (2009, 7), (2012, 8), (2012, 15), (2018, 4), (2008, 1), (2014, 11), (2017, 5), (2018, 10), (2015, 6), (2008, 10), (2021, 13), (2011, 11), (2018, 10), (2022, 13), (2011, 12), (2021, 1), (2009, 12), (2016, 2), (2012, 2), (2017, 1), (2010, 8), (2020, 3), (2020, 10), (2021, 6), (2022, 9), (2014, 4), (2013, 6), (2015, 14), (2012, 7), (2010, 6), (2007, 7), (2020, 5), (2009, 7), (2016, 4), 
(2018, 2), (2012, 15), (2015, 2), (2016, 10), (2008, 8), (2013, 9), (2011, 14), (2012, 2), (2021, 5), (2017, 4), (2011, 5), (2012, 5), (2015, 10), (2020, 6), (2017, 3), (2013, 2), (2020, 10), (2020, 4), (2007, 6), (2010, 2), (2011, 14), (2015, 14), (2021, 13), (2021, 9), (2010, 5), (2013, 10), (2018, 5), (2009, 12), (2015, 14), (2017, 11), (2013, 10), (2012, 15), (2007, 9), (2007, 4), (2020, 8), (2012, 3), (2011, 8), (2015, 9), (2015, 1), (2019, 13), (2015, 5), (2010, 1), (2013, 14), (2019, 9), (2010, 1), (2017, 15), (2018, 9), (2011, 3), (2015, 13), (2007, 1), (2017, 12), (2011, 15), (2008, 8), (2007, 9), (2012, 5), (2010, 12), (2011, 4), (2012, 8), (2008, 4), (2019, 7), (2016, 6), (2021, 13), (2007, 6), (2010, 8), (2008, 1), (2020, 3), (2012, 11), (2022, 9), (2012, 9), (2019, 15), (2008, 2), (2016, 14), (2015, 13), (2022, 13), (2007, 11), (2010, 1), (2011, 14), 
(2016, 11), (2016, 15), (2019, 8), (2007, 11), (2010, 1), (2022, 8), (2019, 14), (2009, 9), (2008, 6), (2010, 9), (2016, 4), (2016, 6), (2009, 10), (2008, 2), (2013, 3), (2012, 10), (2013, 10), (2009, 10), (2011, 15), (2008, 11), (2017, 1), (2017, 7), (2022, 15), (2008, 5), (2011, 8), (2013, 5), (2016, 1), (2022, 1), (2009, 5), (2012, 8), (2022, 7), (2019, 15), (2011, 9), (2016, 11), (2014, 15), (2013, 7), (2013, 9), (2017, 9), (2016, 3), (2013, 9), (2015, 12), (2014, 13), (2012, 8), (2018, 14), (2013, 7), (2019, 3), (2015, 11), (2020, 14), (2011, 13), (2008, 7), (2012, 3), (2022, 4), (2012, 5), (2014, 13), (2014, 8), (2007, 8), (2008, 8), (2021, 8), (2019, 6), (2019, 1), (2013, 3), (2007, 4), (2013, 1), (2014, 4), (2022, 5), (2009, 9), (2017, 13), (2009, 10), (2010, 5), (2018, 7), (2017, 1), (2011, 10), (2014, 5), (2018, 15), (2014, 12), (2019, 5), (2016, 6), (2022, 8), (2007, 4), (2012, 15), (2020, 15), (2022, 13), (2020, 5), (2013, 5), (2019, 15), (2010, 7), (2016, 12), (2015, 10), (2015, 10), (2016, 5), (2022, 11), (2011, 2), (2022, 6), (2007, 4), (2014, 1), (2009, 14), (2012, 11), (2013, 6), (2013, 1), (2020, 3), (2018, 11), (2018, 10), (2015, 8), (2007, 5), (2008, 5), (2008, 15), (2016, 2), (2010, 11), (2014, 14), (2017, 4), (2021, 15), (2012, 9), (2017, 8), (2016, 10), (2015, 11), (2010, 8), (2017, 12), (2019, 3), (2012, 14), (2013, 8), (2017, 3), (2020, 2), (2015, 9), (2007, 2), (2012, 15), (2014, 6), (2008, 3), (2007, 13), (2022, 1), (2013, 14), (2015, 11), (2007, 3), (2018, 8), (2010, 11), (2009, 14), (2017, 10), (2017, 6), (2020, 7), (2010, 1), (2019, 13), (2016, 1), (2009, 9), (2019, 7), (2007, 9), (2008, 2), (2021, 14), (2021, 7), (2011, 13), (2017, 4), (2021, 8), (2008, 12), (2008, 4), (2007, 7), (2021, 7), (2009, 6), (2018, 11), (2013, 8), (2010, 10), (2010, 12), (2010, 2), (2017, 6), (2022, 15), (2012, 5), (2012, 14), (2018, 7), (2008, 13), (2007, 3), (2014, 14), (2008, 7), (2008, 9), (2015, 5), (2015, 6), (2010, 4), (2015, 7), (2015, 7), (2011, 11), (2020, 4), (2012, 7), (2016, 12), (2013, 13), (2012, 15), (2011, 11), (2020, 10), (2012, 5), (2012, 15), (2016, 1), (2009, 11), (2022, 6), (2014, 7), (2016, 2), (2014, 11), (2014, 9), (2011, 6), (2008, 5), (2010, 13), (2010, 8), (2022, 7), (2012, 13), (2013, 14), (2008, 7), (2014, 9), (2014, 1), (2012, 1), (2021, 13), (2011, 9), (2008, 9), (2008, 7), (2013, 7), (2007, 2), (2021, 2), (2009, 10), (2019, 4), (2022, 7), (2017, 9), (2022, 6), (2007, 12), (2014, 3), (2019, 12), (2022, 9), (2007, 3), (2007, 14), (2014, 10), (2012, 8), (2014, 11), (2011, 1), (2022, 15), (2022, 6), (2021, 14), (2022, 10), (2009, 12), (2007, 13), (2012, 10), (2017, 8), (2008, 11), (2015, 8), (2011, 9), (2017, 4), (2012, 5), (2022, 6), (2020, 8), (2018, 2), (2021, 7), (2018, 15), (2007, 4), (2016, 4), (2015, 4), (2016, 12), (2007, 7), (2013, 9), (2021, 7), (2010, 3), (2008, 1), (2012, 7), (2007, 12), (2009, 14), (2011, 8), (2017, 15), (2014, 7), (2011, 3), (2014, 12), (2021, 6), (2014, 9), (2007, 8), (2012, 3), (2013, 15), (2011, 15), (2020, 15), (2022, 8), (2011, 10), (2008, 
7), (2009, 5), (2015, 15), (2012, 2), (2018, 15), (2020, 7), (2008, 15), (2014, 12), (2019, 3), (2016, 9), (2008, 5), (2017, 13), (2014, 2), (2021, 13), (2010, 15), (2016, 2), (2007, 8), (2014, 11), (2017, 2), (2012, 2), (2010, 7), (2018, 13), (2020, 12), (2020, 13), (2017, 13), (2013, 9), (2019, 13), (2009, 13), (2014, 5), (2015, 11), (2014, 14), (2018, 5), (2014, 1), (2007, 7), (2011, 8), (2008, 9), (2012, 15), (2012, 14), (2022, 3), (2009, 7), (2022, 1), (2019, 4), (2007, 12), (2015, 12), (2009, 10), (2008, 14), (2016, 14), (2015, 7), (2019, 10), (2019, 6), (2011, 12), (2009, 4), (2012, 3), (2021, 1), (2007, 1), (2022, 9), (2021, 6), (2008, 1), (2011, 6), (2007, 14), (2017, 1), (2015, 3), (2007, 6), (2022, 2), (2009, 
3), (2011, 8), (2010, 15), (2008, 10), (2011, 2), (2015, 3), (2010, 13), (2022, 11), (2020, 12), (2010, 6), (2016, 5), (2007, 3), (2021, 5), (2010, 9), (2019, 1), (2013, 13), (2014, 14), (2015, 6), (2019, 4), (2015, 6), (2008, 13), (2020, 11), (2017, 3), (2014, 7), (2007, 6), (2017, 13), (2018, 7), (2017, 8), (2019, 2), (2012, 12), (2010, 8), (2009, 12), (2015, 4), (2008, 1), (2015, 3), (2021, 4), (2021, 13), (2007, 14), (2021, 12), (2012, 1), (2008, 11), (2021, 1), (2009, 2), (2018, 13), (2017, 12), (2013, 8), (2014, 14), (2017, 14), (2022, 15), (2007, 8), (2012, 12), (2010, 2), (2015, 9), (2012, 1), (2022, 8), (2017, 6), (2022, 1), (2019, 1), (2012, 15), (2022, 12), (2011, 2), (2007, 11), (2009, 5), (2011, 14), (2019, 
10), (2020, 1), (2018, 9), (2017, 2), (2020, 8), (2007, 7), (2010, 2), (2011, 13), (2008, 5), (2012, 12), (2014, 2), (2019, 2), (2015, 4), (2011, 
9), (2020, 3), (2015, 3), (2012, 3), (2020, 13), (2015, 1), (2017, 3), (2018, 10), (2008, 5), (2007, 12), (2022, 10), (2008, 5)]

def driver_results():
    start = perf_counter()
    for item in tuples:
        rr = RaceResult.objects.get(driver = Driver.objects.get(id='lewis-hamilton'), year=item[0], round=item[1])
    stop = perf_counter()
    logger.info(stop - start)

def driver_results_2():
    start = perf_counter()
    for item in tuples:
        race = Race.objects.get(year=item[0], round=item[1])
        rr = RaceData.objects.get(driver = Driver.objects.get(id='lewis-hamilton'), race = race, type = 'RACE_RESULT')
    stop = perf_counter()
    logger.info(stop - start)

drivers = ['heikki-kovalainen',
'innes-ireland',
'jarno-trulli',
'jean-alesi',
'jean-pierre-beltoise',
'jim-rathmann',
'jimmy-bryan',
'jo-bonnier',
'jochen-mass',
'johnnie-parsons',
'lee-wallard',
'lorenzo-bandini',
'ludovico-scarfiotti',
'luigi-fagioli',
'luigi-musso',
'olivier-panis',
'pastor-maldonado',
'pat-flaherty',
'peter-gethin',
'piero-taruffi',
'pierre-gasly',
'richie-ginther',
'robert-kubica',
'rodger-ward',
'sam-hanks',
'troy-ruttman',
'vittorio-brambilla',
'bill-vukovich',
'elio-de-angelis',
'jean-pierre-jabouille',
'jo-siffert',
'jose-froilan-gonzalez',
'maurice-trintignant',
'patrick-depailler',
'patrick-tambay',
'pedro-rodriguez',
'peter-revson',
'wolfgang-von-trips',
'didier-pironi',
'giancarlo-fisichella',
'heinz-harald-frentzen',
'johnny-herbert',
'mike-hawthorn',
'peter-collins',
'phil-hill',
'thierry-boutsen',
'bruce-mclaren',
'dan-gurney',
'eddie-irvine',
'sergio-perez',
'charles-leclerc',
'clay-regazzoni',
'john-watson',
'keke-rosberg',
'michele-alboreto',
'nino-farina',
'gilles-villeneuve',
'jacques-laffite',
'jochen-rindt',
'john-surtees',
'ralf-schumacher',
'riccardo-patrese',
'tony-brooks',
'juan-pablo-montoya',
'rene-arnoux',
'daniel-ricciardo',
'denny-hulme',
'jacky-ickx',
'mark-webber',
'gerhard-berger',
'james-hunt',
'jody-scheckter',
'ronnie-peterson',
'valtteri-bottas',
'felipe-massa',
'jacques-villeneuve',
'rubens-barrichello',
'alan-jones',
'carlos-reutemann',
'mario-andretti',
'alberto-ascari',
'david-coulthard',
'emerson-fittipaldi',
'graham-hill',
'jack-brabham',
'jenson-button',
'stirling-moss',
'mika-hakkinen',
'kimi-raikkonen',
'damon-hill',
'nelson-piquet',
'nico-rosberg',
'juan-manuel-fangio',
'jim-clark',
'niki-lauda',
'jackie-stewart',
'nigel-mansell',
'fernando-alonso',
'max-verstappen',
'ayrton-senna',
'alain-prost',
'sebastian-vettel',
'michael-schumacher',
'lewis-hamilton']

def wins_performance():
    start = perf_counter()
    for item in drivers:
        win_race = RaceData.objects.filter(driver=item, type='RACE_RESULT', position_number=1)
    stop = perf_counter()
    print(stop - start)

def wins_performance_2():
    start = perf_counter()
    for item in drivers:
        win_race = RaceResult.objects.filter(driver=item, position_number=1)
    stop = perf_counter()
    print(stop - start)

###### generic utilities

def get_object_from_model(model: models.base.ModelBase, params: dict):
    try:
        return model.objects.get(**params)
    except model.DoesNotExist:
        raise model.DoesNotExist(f"There does not exist object of type {model} with parameters: {params}") from None

def get_race(year: int, full_name: str) -> Race:
    season = get_object_from_model(Season, {'year': year})
    grand_prix = get_object_from_model(GrandPrix, {'full_name': full_name})
    return get_object_from_model(Race, {'year': season, 'grand_prix': grand_prix})

## works for any m2m field
def add_if_not_exist(feature, related_object):
    if feature.all().contains(related_object):
        return
    feature.add(related_object)

###### functionality for adding new objects to racevideos database

def add_link(link, full_name, year, thumbnail):
    race = get_race(year, full_name)
    RaceVideos.objects.get_or_create(race=race, link=link, thumbnail=thumbnail)

def pass_video_urls_to_db(source: Union[str, list]):
    dataframe = get_cleaned_video_data(source)
    dataframe.apply(lambda row: add_link(row['link'], row['full_name'], row['year'], row['thumbnail']), axis=1)

def get_and_pass_video_urls(playlists_id: list):
    highlights = get_race_highlights(playlists_id)
    pass_video_urls_to_db(highlights)

###### functionality for adding new objects to car/car-constructor database

def check_car_integrity(series, instance):
    old_tuple = (series['Id'], series['Car'], series['Photo'], series['Debut'], series['Races'], series['Wins'], series['Poles'], series['F/Laps'])
    new_tuple = (instance.id, instance.name, instance.photo, instance.debut, instance.races, instance.wins, instance.poles, instance.fastest_laps)
    if old_tuple != new_tuple: 
        raise IntegrityError("Provided instance {} does not agree with existing instance {}".format(old_tuple, new_tuple))

def replace_debut_str_with_race_object(series):
    year = (int)(series['Debut'].split()[0])
    full_name = ' '.join(series['Debut'].split()[1:])
    series['Debut'] = get_race(year, full_name)

def add_car(series):
    constructor_object = Constructor.objects.get(id=series['Constructor'])
    series = series.replace({np.nan: None})
    if series['Debut']:
        replace_debut_str_with_race_object(series)
    else: series['Debut'] = None
    existing_instances = Car.objects.filter(id = series['Id'])
    if len(existing_instances) > 0:
        instance = existing_instances[0]
        check_car_integrity(series, instance)
        add_if_not_exist(instance.constructor, constructor_object)
    else:
        instance, created = Car.objects.get_or_create(id = series['Id'], name=series['Car'], 
            photo=series['Photo'], debut=series['Debut'], races=series['Races'], wins=series['Wins'],
            poles=series['Poles'], fastest_laps=series['F/Laps'])
        add_if_not_exist(instance.constructor, constructor_object)

@transaction.atomic
def pass_cars_to_db():
    frame = pd.read_csv(BASE_DIR.joinpath("tyrrell.csv"))
    frame['Id'] = frame['Car'].map(lambda s: s.lower())
    frame.apply(lambda row: add_car(row), axis = 1)

pass_cars_to_db()