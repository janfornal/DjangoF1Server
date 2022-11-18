from datetime import datetime
from f1app.serializers import *
from f1app.models import *
from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore

from f1app.views import ConstructorPolePositionAPIView

# Create your tests here.

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

print_session_dictionaries()