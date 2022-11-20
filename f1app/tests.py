from django.test import TestCase
from f1app.models import *
from django.contrib.auth.models import User

# Create your tests here.

class ChampionshipRateTest(TestCase):
    def setUp(self):
        pass
        # self.user = User.objects.create_user(username='testing', password='testing')
        # season = Season.objects.create(year=2020)
        # continent = Continent.objects.create(id='europe', code='EU', name='Europe', demonym='European')
        # country = Country.objects.create(id='austria', alpha2_code='AT', alpha3_code='AUT', name='Austria', demonym='Austrian', continent=continent)
        # grandprix = GrandPrix.objects.create(id='austria', name='Austria', full_name='Austrian Grand Prix', short_name='Austrian GP', country=country, total_race_held='35')
        # circuit = Circuit(id='spielberg', name='Red Bull Ring', full_name='Red Bull Ring', previous_names='Österreichring,A1-Ring', type='RACE', place_name='Spielberg', country=country, latitude='47.219722', longitude='14.764722', total_races_held='36')
        # self.race = Race.objects.create(year=season, round=1, date='2020-07-05', grand_prix=grandprix, official_name='Formula 1 Rolex Grosser Preis von Österreich 2020', qualifying_format='KNOCKOUT', circuit=circuit, circuit_type='RACE', course_length=4.3179999999999996163, laps=71, distance=306.45199999999999818)
        # self.opinion = RaceOpinionModel(user=self.user, race=self.race, championship_rate=5, chaos_rate=5, racing_rate=5, strategy_rate=5)
    
    def test_championship_rate_function(self):
        user = User.objects.get(username='username2')
        race = Race.objects.get(id=1019)
        opinion = RaceOpinionModel.objects.get(user=user, race=race)
        self.assertTrue(Race.get_championship_rate(race, user), opinion.championship_rate)