from django.db import models
from django.db.models import Avg, functions
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from f1app.model_tables import DRIVER_OPINION_MODEL, RACE_OPINION_MODEL

##### f1database


class Circuit(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, )
    full_name = models.CharField(max_length=255, )
    previous_names = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, )
    place_name = models.CharField(max_length=255, )
    country = models.ForeignKey('Country', models.DO_NOTHING)
    latitude = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    longitude = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    total_races_held = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'circuit'

class Constructor(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, )
    full_name = models.CharField(max_length=255, )
    country = models.ForeignKey('Country', models.DO_NOTHING)
    best_championship_position = models.IntegerField(blank=True, null=True)
    best_race_result = models.IntegerField(blank=True, null=True)
    best_starting_grid_position = models.IntegerField(blank=True, null=True)
    total_championship_wins = models.IntegerField()
    total_race_entries = models.IntegerField()
    total_race_starts = models.IntegerField()
    total_race_wins = models.IntegerField()
    total_1_and_2_finishes = models.IntegerField()
    total_race_laps = models.IntegerField()
    total_podiums = models.IntegerField()
    total_podium_races = models.IntegerField()
    total_championship_points = models.TextField()  # This field type is a guess.
    total_pole_positions = models.IntegerField()
    total_fastest_laps = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'constructor'

class ConstructorPreviousNextConstructor(models.Model):
    constructor = models.OneToOneField('Constructor', models.DO_NOTHING, primary_key=True, related_name='constructor')
    previous_next_constructor = models.ForeignKey('Constructor', models.DO_NOTHING)
    year_from = models.IntegerField()
    year_to = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'constructor_previous_next_constructor'

class ConstructorStanding(models.Model):
    year = models.OneToOneField('Season', models.DO_NOTHING, db_column='year', primary_key=True)
    round = models.IntegerField()
    position_display_order = models.IntegerField()
    position_number = models.IntegerField(blank=True, null=True)
    position_text = models.CharField(max_length=255, )
    constructor = models.ForeignKey('Constructor', models.DO_NOTHING)
    engine_manufacturer = models.ForeignKey('EngineManufacturer', models.DO_NOTHING)
    points = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'constructor_standing'

class Continent(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=255, unique=True)
    demonym = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'continent'

class Country(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    alpha2_code = models.CharField(max_length=2, unique=True)
    alpha3_code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=255, unique=True)
    demonym = models.CharField(max_length=255, blank=True, null=True)
    continent = models.ForeignKey('Continent', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'country'

class Driver(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, )
    first_name = models.CharField(max_length=255, )
    last_name = models.CharField(max_length=255, )
    full_name = models.CharField(max_length=255, )
    abbreviation = models.CharField(max_length=3, )
    permanent_number = models.CharField(max_length=2, blank=True, null=True)
    gender = models.CharField(max_length=255, )
    date_of_birth = models.DateField()
    date_of_death = models.DateField(blank=True, null=True)
    place_of_birth = models.CharField(max_length=255, )
    country_of_birth_country = models.ForeignKey('Country', models.DO_NOTHING, related_name='birth')
    nationality_country = models.ForeignKey('Country', models.DO_NOTHING, related_name="nationality")
    second_nationality_country = models.ForeignKey('Country', models.DO_NOTHING, blank=True, null=True)
    best_championship_position = models.IntegerField(blank=True, null=True)
    best_race_result = models.IntegerField(blank=True, null=True)
    best_starting_grid_position = models.IntegerField(blank=True, null=True)
    total_championship_wins = models.IntegerField()
    total_race_entries = models.IntegerField()
    total_race_starts = models.IntegerField()
    total_race_wins = models.IntegerField()
    total_race_laps = models.IntegerField()
    total_podiums = models.IntegerField()
    total_points = models.TextField()  # This field type is a guess.
    total_championship_points = models.TextField()  # This field type is a guess.
    total_pole_positions = models.IntegerField()
    total_fastest_laps = models.IntegerField()
    total_driver_of_the_day = models.IntegerField()
    
    class Meta:
        managed = False
        db_table = 'driver'

class DriverFamilyRelationship(models.Model):
    driver = models.OneToOneField('Driver', models.DO_NOTHING, primary_key=True, related_name='first_driver')
    other_driver = models.ForeignKey('Driver', models.DO_NOTHING)
    type = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'driver_family_relationship'

class DriverOfTheDayResult(models.Model):
    race_id = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    round = models.IntegerField(blank=True, null=True)
    position_display_order = models.IntegerField(blank=True, null=True)
    position_number = models.IntegerField(blank=True, null=True)
    position_text = models.CharField(max_length=255, blank=True, null=True)
    driver_number = models.CharField(max_length=255, blank=True, null=True)
    driver_id = models.CharField(max_length=255, blank=True, null=True)
    constructor_id = models.CharField(max_length=255, blank=True, null=True)
    engine_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    tyre_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    percentage = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'driver_of_the_day_result'

class DriverStanding(models.Model):
    year = models.OneToOneField('Season', models.DO_NOTHING, db_column='year', primary_key=True)
    round = models.IntegerField()
    position_display_order = models.IntegerField()
    position_number = models.IntegerField(blank=True, null=True)
    position_text = models.CharField(max_length=255, )
    driver = models.ForeignKey('Driver', models.DO_NOTHING)
    points = models.TextField()  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'driver_standing'

class EngineManufacturer(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, )
    country = models.ForeignKey('Country', models.DO_NOTHING)
    best_championship_position = models.IntegerField(blank=True, null=True)
    best_race_result = models.IntegerField(blank=True, null=True)
    best_starting_grid_position = models.IntegerField(blank=True, null=True)
    total_championship_wins = models.IntegerField()
    total_race_entries = models.IntegerField()
    total_race_starts = models.IntegerField()
    total_race_wins = models.IntegerField()
    total_race_laps = models.IntegerField()
    total_podiums = models.IntegerField()
    total_podium_races = models.IntegerField()
    total_championship_points = models.TextField()  # This field type is a guess.
    total_pole_positions = models.IntegerField()
    total_fastest_laps = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'engine_manufacturer'

class Entrant(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, )

    class Meta:
        managed = False
        db_table = 'entrant'

class FastestLap(models.Model):
    race_id = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    round = models.IntegerField(blank=True, null=True)
    position_display_order = models.IntegerField(blank=True, null=True)
    position_number = models.IntegerField(blank=True, null=True)
    position_text = models.CharField(max_length=255, blank=True, null=True)
    driver_number = models.CharField(max_length=255, blank=True, null=True)
    driver_id = models.CharField(max_length=255, blank=True, null=True)
    constructor_id = models.CharField(max_length=255, blank=True, null=True)
    engine_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    tyre_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    lap = models.IntegerField(blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    time_millis = models.IntegerField(blank=True, null=True)
    gap = models.CharField(max_length=255, blank=True, null=True)
    gap_millis = models.IntegerField(blank=True, null=True)
    interval = models.CharField(max_length=255, blank=True, null=True)
    interval_millis = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'fastest_lap'

class FreePractice1Result(models.Model):
    race_id = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    round = models.IntegerField(blank=True, null=True)
    position_display_order = models.IntegerField(blank=True, null=True)
    position_number = models.IntegerField(blank=True, null=True)
    position_text = models.CharField(max_length=255, blank=True, null=True)
    driver_number = models.CharField(max_length=255, blank=True, null=True)
    driver_id = models.CharField(max_length=255, blank=True, null=True)
    constructor_id = models.CharField(max_length=255, blank=True, null=True)
    engine_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    tyre_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    time_millis = models.IntegerField(blank=True, null=True)
    gap = models.CharField(max_length=255, blank=True, null=True)
    gap_millis = models.IntegerField(blank=True, null=True)
    interval = models.CharField(max_length=255, blank=True, null=True)
    interval_millis = models.IntegerField(blank=True, null=True)
    laps = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'free_practice_1_result'

class FreePractice2Result(models.Model):
    race_id = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    round = models.IntegerField(blank=True, null=True)
    position_display_order = models.IntegerField(blank=True, null=True)
    position_number = models.IntegerField(blank=True, null=True)
    position_text = models.CharField(max_length=255, blank=True, null=True)
    driver_number = models.CharField(max_length=255, blank=True, null=True)
    driver_id = models.CharField(max_length=255, blank=True, null=True)
    constructor_id = models.CharField(max_length=255, blank=True, null=True)
    engine_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    tyre_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    time_millis = models.IntegerField(blank=True, null=True)
    gap = models.CharField(max_length=255, blank=True, null=True)
    gap_millis = models.IntegerField(blank=True, null=True)
    interval = models.CharField(max_length=255, blank=True, null=True)
    interval_millis = models.IntegerField(blank=True, null=True)
    laps = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'free_practice_2_result'

class FreePractice3Result(models.Model):
    race_id = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    round = models.IntegerField(blank=True, null=True)
    position_display_order = models.IntegerField(blank=True, null=True)
    position_number = models.IntegerField(blank=True, null=True)
    position_text = models.CharField(max_length=255, blank=True, null=True)
    driver_number = models.CharField(max_length=255, blank=True, null=True)
    driver_id = models.CharField(max_length=255, blank=True, null=True)
    constructor_id = models.CharField(max_length=255, blank=True, null=True)
    engine_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    tyre_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    time_millis = models.IntegerField(blank=True, null=True)
    gap = models.CharField(max_length=255, blank=True, null=True)
    gap_millis = models.IntegerField(blank=True, null=True)
    interval = models.CharField(max_length=255, blank=True, null=True)
    interval_millis = models.IntegerField(blank=True, null=True)
    laps = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'free_practice_3_result'

class FreePractice4Result(models.Model):
    race_id = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    round = models.IntegerField(blank=True, null=True)
    position_display_order = models.IntegerField(blank=True, null=True)
    position_number = models.IntegerField(blank=True, null=True)
    position_text = models.CharField(max_length=255, blank=True, null=True)
    driver_number = models.CharField(max_length=255, blank=True, null=True)
    driver_id = models.CharField(max_length=255, blank=True, null=True)
    constructor_id = models.CharField(max_length=255, blank=True, null=True)
    engine_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    tyre_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    time_millis = models.IntegerField(blank=True, null=True)
    gap = models.CharField(max_length=255, blank=True, null=True)
    gap_millis = models.IntegerField(blank=True, null=True)
    interval = models.CharField(max_length=255, blank=True, null=True)
    interval_millis = models.IntegerField(blank=True, null=True)
    laps = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'free_practice_4_result'

class GrandPrix(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, )
    full_name = models.CharField(max_length=255, )
    short_name = models.CharField(max_length=255, )
    country = models.ForeignKey('Country', models.DO_NOTHING, blank=True, null=True)
    total_races_held = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'grand_prix'

class PitStop(models.Model):
    race_id = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    round = models.IntegerField(blank=True, null=True)
    position_display_order = models.IntegerField(blank=True, null=True)
    position_number = models.IntegerField(blank=True, null=True)
    position_text = models.CharField(max_length=255, blank=True, null=True)
    driver_number = models.CharField(max_length=255, blank=True, null=True)
    driver_id = models.CharField(max_length=255, blank=True, null=True)
    constructor_id = models.CharField(max_length=255, blank=True, null=True)
    engine_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    tyre_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    stop = models.IntegerField(blank=True, null=True)
    lap = models.IntegerField(blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    time_millis = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'pit_stop'

class PreQualifyingResult(models.Model):
    race_id = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    round = models.IntegerField(blank=True, null=True)
    position_display_order = models.IntegerField(blank=True, null=True)
    position_number = models.IntegerField(blank=True, null=True)
    position_text = models.CharField(max_length=255, blank=True, null=True)
    driver_number = models.CharField(max_length=255, blank=True, null=True)
    driver_id = models.CharField(max_length=255, blank=True, null=True)
    constructor_id = models.CharField(max_length=255, blank=True, null=True)
    engine_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    tyre_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    time_millis = models.IntegerField(blank=True, null=True)
    gap = models.CharField(max_length=255, blank=True, null=True)
    gap_millis = models.IntegerField(blank=True, null=True)
    interval = models.CharField(max_length=255, blank=True, null=True)
    interval_millis = models.IntegerField(blank=True, null=True)
    laps = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'pre_qualifying_result'

class Qualifying1Result(models.Model):
    race_id = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    round = models.IntegerField(blank=True, null=True)
    position_display_order = models.IntegerField(blank=True, null=True)
    position_number = models.IntegerField(blank=True, null=True)
    position_text = models.CharField(max_length=255, blank=True, null=True)
    driver_number = models.CharField(max_length=255, blank=True, null=True)
    driver_id = models.CharField(max_length=255, blank=True, null=True)
    constructor_id = models.CharField(max_length=255, blank=True, null=True)
    engine_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    tyre_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    time_millis = models.IntegerField(blank=True, null=True)
    gap = models.CharField(max_length=255, blank=True, null=True)
    gap_millis = models.IntegerField(blank=True, null=True)
    interval = models.CharField(max_length=255, blank=True, null=True)
    interval_millis = models.IntegerField(blank=True, null=True)
    laps = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'qualifying_1_result'

class Qualifying2Result(models.Model):
    race_id = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    round = models.IntegerField(blank=True, null=True)
    position_display_order = models.IntegerField(blank=True, null=True)
    position_number = models.IntegerField(blank=True, null=True)
    position_text = models.CharField(max_length=255, blank=True, null=True)
    driver_number = models.CharField(max_length=255, blank=True, null=True)
    driver_id = models.CharField(max_length=255, blank=True, null=True)
    constructor_id = models.CharField(max_length=255, blank=True, null=True)
    engine_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    tyre_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    time_millis = models.IntegerField(blank=True, null=True)
    gap = models.CharField(max_length=255, blank=True, null=True)
    gap_millis = models.IntegerField(blank=True, null=True)
    interval = models.CharField(max_length=255, blank=True, null=True)
    interval_millis = models.IntegerField(blank=True, null=True)
    laps = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'qualifying_2_result'

class QualifyingResult(models.Model):
    race_id = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    round = models.IntegerField(blank=True, null=True)
    position_display_order = models.IntegerField(blank=True, null=True)
    position_number = models.IntegerField(blank=True, null=True)
    position_text = models.CharField(max_length=255, blank=True, null=True)
    driver_number = models.CharField(max_length=255, blank=True, null=True)
    driver_id = models.CharField(max_length=255, blank=True, null=True)
    constructor_id = models.CharField(max_length=255, blank=True, null=True)
    engine_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    tyre_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    time_millis = models.IntegerField(blank=True, null=True)
    q1 = models.CharField(max_length=255, blank=True, null=True)
    q1_millis = models.IntegerField(blank=True, null=True)
    q2 = models.CharField(max_length=255, blank=True, null=True)
    q2_millis = models.IntegerField(blank=True, null=True)
    q3 = models.CharField(max_length=255, blank=True, null=True)
    q3_millis = models.IntegerField(blank=True, null=True)
    gap = models.CharField(max_length=255, blank=True, null=True)
    gap_millis = models.IntegerField(blank=True, null=True)
    interval = models.CharField(max_length=255, blank=True, null=True)
    interval_millis = models.IntegerField(blank=True, null=True)
    laps = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'qualifying_result'

class Race(models.Model):
    year = models.ForeignKey('Season', models.DO_NOTHING, db_column='year')
    round = models.IntegerField()
    date = models.DateField()
    grand_prix = models.ForeignKey(GrandPrix, models.DO_NOTHING)
    official_name = models.CharField(max_length=255, )
    qualifying_format = models.CharField(max_length=255, )
    circuit = models.ForeignKey('Circuit', models.DO_NOTHING)
    circuit_type = models.CharField(max_length=255, )
    course_length = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    laps = models.IntegerField(blank=True, null=True)
    distance = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    scheduled_laps = models.IntegerField(blank=True, null=True)
    scheduled_distance = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float

    def is_rated(self, user):
        races = RaceOpinionModel.objects.filter(race=self, user=user)
        return len(races) > 0

    def get_championship_rate(self, user):
        rate = RaceOpinionModel.objects.get(race=self, user=user)
        return rate.championship_rate
    
    @classmethod
    def get_race(cls, year, round):
        races = Race.objects.filter(year=year, round=round)
        return races[0] if len(races) > 0 else None

    class Meta:
        managed = False
        db_table = 'race'

class RaceConstructorStanding(models.Model):
    year = models.IntegerField(blank=True, null=True)
    round = models.IntegerField(blank=True, null=True)
    position_display_order = models.IntegerField(blank=True, null=True)
    position_number = models.IntegerField(blank=True, null=True)
    position_text = models.CharField(max_length=255, blank=True, null=True)
    constructor_id = models.CharField(max_length=255, blank=True, null=True)
    engine_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    points = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'race_constructor_standing'

class RaceData(models.Model):
    race = models.OneToOneField('Race', models.DO_NOTHING, primary_key=True)
    type = models.CharField(max_length=255, )
    position_display_order = models.IntegerField()
    position_number = models.IntegerField(blank=True, null=True)
    position_text = models.CharField(max_length=255, blank=True, null=True)
    driver_number = models.CharField(max_length=255, )
    driver = models.ForeignKey(Driver, models.DO_NOTHING)
    constructor = models.ForeignKey(Constructor, models.DO_NOTHING)
    engine_manufacturer = models.ForeignKey(EngineManufacturer, models.DO_NOTHING)
    tyre_manufacturer = models.ForeignKey('TyreManufacturer', models.DO_NOTHING)
    practice_time = models.CharField(max_length=255, blank=True, null=True)
    practice_time_millis = models.IntegerField(blank=True, null=True)
    practice_gap = models.CharField(max_length=255, blank=True, null=True)
    practice_gap_millis = models.IntegerField(blank=True, null=True)
    practice_interval = models.CharField(max_length=255, blank=True, null=True)
    practice_interval_millis = models.IntegerField(blank=True, null=True)
    practice_laps = models.IntegerField(blank=True, null=True)
    qualifying_time = models.CharField(max_length=255, blank=True, null=True)
    qualifying_time_millis = models.IntegerField(blank=True, null=True)
    qualifying_q1 = models.CharField(max_length=255, blank=True, null=True)
    qualifying_q1_millis = models.IntegerField(blank=True, null=True)
    qualifying_q2 = models.CharField(max_length=255, blank=True, null=True)
    qualifying_q2_millis = models.IntegerField(blank=True, null=True)
    qualifying_q3 = models.CharField(max_length=255, blank=True, null=True)
    qualifying_q3_millis = models.IntegerField(blank=True, null=True)
    qualifying_gap = models.CharField(max_length=255, blank=True, null=True)
    qualifying_gap_millis = models.IntegerField(blank=True, null=True)
    qualifying_interval = models.CharField(max_length=255, blank=True, null=True)
    qualifying_interval_millis = models.IntegerField(blank=True, null=True)
    qualifying_laps = models.IntegerField(blank=True, null=True)
    starting_grid_position_grid_penalty = models.CharField(max_length=255, blank=True, null=True)
    starting_grid_position_grid_penalty_positions = models.IntegerField(blank=True, null=True)
    starting_grid_position_time = models.CharField(max_length=255, blank=True, null=True)
    starting_grid_position_time_millis = models.IntegerField(blank=True, null=True)
    race_shared_car = models.BooleanField(blank=True, null=True)
    race_laps = models.IntegerField(blank=True, null=True)
    race_time = models.CharField(max_length=255, blank=True, null=True)
    race_time_millis = models.IntegerField(blank=True, null=True)
    race_time_penalty = models.CharField(max_length=255, blank=True, null=True)
    race_time_penalty_millis = models.IntegerField(blank=True, null=True)
    race_gap = models.CharField(max_length=255, blank=True, null=True)
    race_gap_millis = models.IntegerField(blank=True, null=True)
    race_gap_laps = models.IntegerField(blank=True, null=True)
    race_interval = models.CharField(max_length=255, blank=True, null=True)
    race_interval_millis = models.IntegerField(blank=True, null=True)
    race_reason_retired = models.CharField(max_length=255, blank=True, null=True)
    race_points = models.TextField(blank=True, null=True)  # This field type is a guess.
    race_grid_position_number = models.IntegerField(blank=True, null=True)
    race_grid_position_text = models.CharField(max_length=255, blank=True, null=True)
    race_positions_gained = models.IntegerField(blank=True, null=True)
    race_pit_stops = models.IntegerField(blank=True, null=True)
    race_fastest_lap = models.BooleanField(blank=True, null=True)
    race_driver_of_the_day = models.BooleanField(blank=True, null=True)
    fastest_lap_lap = models.IntegerField(blank=True, null=True)
    fastest_lap_time = models.CharField(max_length=255, blank=True, null=True)
    fastest_lap_time_millis = models.IntegerField(blank=True, null=True)
    fastest_lap_gap = models.CharField(max_length=255, blank=True, null=True)
    fastest_lap_gap_millis = models.IntegerField(blank=True, null=True)
    fastest_lap_interval = models.CharField(max_length=255, blank=True, null=True)
    fastest_lap_interval_millis = models.IntegerField(blank=True, null=True)
    pit_stop_stop = models.IntegerField(blank=True, null=True)
    pit_stop_lap = models.IntegerField(blank=True, null=True)
    pit_stop_time = models.CharField(max_length=255, blank=True, null=True)
    pit_stop_time_millis = models.IntegerField(blank=True, null=True)
    driver_of_the_day_percentage = models.TextField(blank=True, null=True)  # This field type is a guess.
    
    @property
    def opinion(self):
        performance_data = DriverOpinionModel.objects.filter(driver_id=self.driver, race_id=self.race)
        return performance_data.aggregate(opinion = functions.Coalesce(Avg('rate'), 0.0))['opinion']
    
    class Meta:
        managed = False
        db_table = 'race_data'

class RaceDriverStanding(models.Model):
    year = models.IntegerField(blank=True, null=True)
    round = models.IntegerField(blank=True, null=True)
    position_display_order = models.IntegerField(blank=True, null=True)
    position_number = models.IntegerField(blank=True, null=True)
    position_text = models.CharField(max_length=255, blank=True, null=True)
    driver_id = models.CharField(max_length=255, blank=True, null=True)
    points = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'race_driver_standing'

class RaceResult(models.Model):
    race_id = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    round = models.IntegerField(blank=True, null=True)
    position_display_order = models.IntegerField(blank=True, null=True)
    position_number = models.IntegerField(blank=True, null=True)
    position_text = models.CharField(max_length=255, blank=True, null=True)
    driver_number = models.CharField(max_length=255, blank=True, null=True)
    driver_id = models.CharField(max_length=255, blank=True, null=True)
    constructor_id = models.CharField(max_length=255, blank=True, null=True)
    engine_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    tyre_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    shared_car = models.BooleanField(blank=True, null=True)
    laps = models.IntegerField(blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    time_millis = models.IntegerField(blank=True, null=True)
    time_penalty = models.CharField(max_length=255, blank=True, null=True)
    time_penalty_millis = models.IntegerField(blank=True, null=True)
    gap = models.CharField(max_length=255, blank=True, null=True)
    gap_millis = models.IntegerField(blank=True, null=True)
    gap_laps = models.IntegerField(blank=True, null=True)
    interval = models.CharField(max_length=255, blank=True, null=True)
    interval_millis = models.IntegerField(blank=True, null=True)
    reason_retired = models.CharField(max_length=255, blank=True, null=True)
    points = models.TextField(blank=True, null=True)  # This field type is a guess.
    grid_position_number = models.IntegerField(blank=True, null=True)
    grid_position_text = models.CharField(max_length=255, blank=True, null=True)
    positions_gained = models.IntegerField(blank=True, null=True)
    pit_stops = models.IntegerField(blank=True, null=True)
    fastest_lap = models.BooleanField(blank=True, null=True)
    driver_of_the_day = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'race_result'

class Season(models.Model):
    year = models.AutoField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'season'

class SeasonConstructorStanding(models.Model):
    year = models.IntegerField(blank=True, null=True)
    position_display_order = models.IntegerField(blank=True, null=True)
    position_number = models.IntegerField(blank=True, null=True)
    position_text = models.CharField(max_length=255, blank=True, null=True)
    constructor_id = models.CharField(max_length=255, blank=True, null=True)
    engine_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    points = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'season_constructor_standing'

class SeasonDriverStanding(models.Model):
    year = models.IntegerField(blank=True, null=True)
    position_display_order = models.IntegerField(blank=True, null=True)
    position_number = models.IntegerField(blank=True, null=True)
    position_text = models.CharField(max_length=255, blank=True, null=True)
    driver_id = models.CharField(max_length=255, blank=True, null=True)
    points = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'season_driver_standing'

class SeasonEntrant(models.Model):
    year = models.OneToOneField('Season', models.DO_NOTHING, db_column='year', primary_key=True)
    entrant = models.ForeignKey('Entrant', models.DO_NOTHING)
    country = models.ForeignKey('Country', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'season_entrant'

class SeasonEntrantConstructor(models.Model):
    year = models.OneToOneField('Season', models.DO_NOTHING, db_column='year', primary_key=True)
    entrant = models.ForeignKey('Entrant', models.DO_NOTHING)
    constructor = models.ForeignKey('Constructor', models.DO_NOTHING)
    engine_manufacturer = models.ForeignKey('EngineManufacturer', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'season_entrant_constructor'

class SeasonEntrantDriver(models.Model):
    year = models.OneToOneField('Season', models.DO_NOTHING, db_column='year', primary_key=True)
    entrant = models.ForeignKey('Entrant', models.DO_NOTHING)
    constructor = models.ForeignKey('Constructor', models.DO_NOTHING)
    engine_manufacturer = models.ForeignKey('EngineManufacturer', models.DO_NOTHING)
    driver = models.ForeignKey('Driver', models.DO_NOTHING)
    rounds = models.CharField(max_length=255, blank=True, null=True)
    rounds_text = models.CharField(max_length=255, blank=True, null=True)
    test_driver = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'season_entrant_driver'

class SeasonEntrantTyreManufacturer(models.Model):
    year = models.OneToOneField('Season', models.DO_NOTHING, db_column='year', primary_key=True)
    entrant = models.ForeignKey('Entrant', models.DO_NOTHING)
    constructor = models.ForeignKey('Constructor', models.DO_NOTHING)
    engine_manufacturer = models.ForeignKey('EngineManufacturer', models.DO_NOTHING)
    tyre_manufacturer = models.ForeignKey('TyreManufacturer', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'season_entrant_tyre_manufacturer'

class SprintQualifyingResult(models.Model):
    race_id = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    round = models.IntegerField(blank=True, null=True)
    position_display_order = models.IntegerField(blank=True, null=True)
    position_number = models.IntegerField(blank=True, null=True)
    position_text = models.CharField(max_length=255, blank=True, null=True)
    driver_number = models.CharField(max_length=255, blank=True, null=True)
    driver_id = models.CharField(max_length=255, blank=True, null=True)
    constructor_id = models.CharField(max_length=255, blank=True, null=True)
    engine_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    tyre_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    laps = models.IntegerField(blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    time_millis = models.IntegerField(blank=True, null=True)
    time_penalty = models.CharField(max_length=255, blank=True, null=True)
    time_penalty_millis = models.IntegerField(blank=True, null=True)
    gap = models.CharField(max_length=255, blank=True, null=True)
    gap_millis = models.IntegerField(blank=True, null=True)
    gap_laps = models.IntegerField(blank=True, null=True)
    interval = models.CharField(max_length=255, blank=True, null=True)
    interval_millis = models.IntegerField(blank=True, null=True)
    reason_retired = models.CharField(max_length=255, blank=True, null=True)
    points = models.TextField(blank=True, null=True)  # This field type is a guess.
    grid_position_number = models.IntegerField(blank=True, null=True)
    grid_position_text = models.CharField(max_length=255, blank=True, null=True)
    positions_gained = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'sprint_qualifying_result'

class SprintQualifyingStartingGridPosition(models.Model):
    race_id = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    round = models.IntegerField(blank=True, null=True)
    position_display_order = models.IntegerField(blank=True, null=True)
    position_number = models.IntegerField(blank=True, null=True)
    position_text = models.CharField(max_length=255, blank=True, null=True)
    driver_number = models.CharField(max_length=255, blank=True, null=True)
    driver_id = models.CharField(max_length=255, blank=True, null=True)
    constructor_id = models.CharField(max_length=255, blank=True, null=True)
    engine_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    tyre_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    grid_penalty = models.CharField(max_length=255, blank=True, null=True)
    grid_penalty_positions = models.IntegerField(blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    time_millis = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'sprint_qualifying_starting_grid_position'

class StartingGridPosition(models.Model):
    race_id = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    round = models.IntegerField(blank=True, null=True)
    position_display_order = models.IntegerField(blank=True, null=True)
    position_number = models.IntegerField(blank=True, null=True)
    position_text = models.CharField(max_length=255, blank=True, null=True)
    driver_number = models.CharField(max_length=255, blank=True, null=True)
    driver_id = models.CharField(max_length=255, blank=True, null=True)
    constructor_id = models.CharField(max_length=255, blank=True, null=True)
    engine_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    tyre_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    grid_penalty = models.CharField(max_length=255, blank=True, null=True)
    grid_penalty_positions = models.IntegerField(blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    time_millis = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'starting_grid_position'

class TyreManufacturer(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    name = models.CharField(max_length=255, )
    country = models.ForeignKey('Country', models.DO_NOTHING)
    best_race_result = models.IntegerField(blank=True, null=True)
    best_starting_grid_position = models.IntegerField(blank=True, null=True)
    total_race_entries = models.IntegerField()
    total_race_starts = models.IntegerField()
    total_race_wins = models.IntegerField()
    total_race_laps = models.IntegerField()
    total_podiums = models.IntegerField()
    total_podium_races = models.IntegerField()
    total_pole_positions = models.IntegerField()
    total_fastest_laps = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tyre_manufacturer'

class WarmingUpResult(models.Model):
    race_id = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    round = models.IntegerField(blank=True, null=True)
    position_display_order = models.IntegerField(blank=True, null=True)
    position_number = models.IntegerField(blank=True, null=True)
    position_text = models.CharField(max_length=255, blank=True, null=True)
    driver_number = models.CharField(max_length=255, blank=True, null=True)
    driver_id = models.CharField(max_length=255, blank=True, null=True)
    constructor_id = models.CharField(max_length=255, blank=True, null=True)
    engine_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    tyre_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    time_millis = models.IntegerField(blank=True, null=True)
    gap = models.CharField(max_length=255, blank=True, null=True)
    gap_millis = models.IntegerField(blank=True, null=True)
    interval = models.CharField(max_length=255, blank=True, null=True)
    interval_millis = models.IntegerField(blank=True, null=True)
    laps = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False  # Created from a view. Don't remove.
        db_table = 'warming_up_result'

##### opinions

class DriverOpinionModel(models.Model):
    id = models.IntegerField(primary_key=True)
    race = models.ForeignKey(Race, models.CASCADE)
    driver = models.ForeignKey(Driver, models.CASCADE)
    rate = models.IntegerField()
    extended_opinion = models.TextField()
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check = models.Q(rate__gte=1) & models.Q(rate__lte=10), 
                name = 'rate_from_1_to_10',
            ),
        ]
        db_table = DRIVER_OPINION_MODEL

class RaceOpinionModel(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, models.CASCADE)
    race = models.ForeignKey(Race, models.CASCADE)
    championship_rate = models.IntegerField(null=True)
    chaos_rate = models.IntegerField(null=True)
    racing_rate = models.IntegerField(null=True)
    strategy_rate = models.IntegerField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'race'], name='unique_race_opinion'
            )
        ]
        db_table = RACE_OPINION_MODEL

##### testing 

# class ExampleModel(models.Model):
    # first_name = models.CharField(max_length=255)
    # last_name = models.CharField(max_length=255)
    # city = models.CharField(max_length=255)
    # def validator(x):
        # if x >= 1 and x <= 100:
            # return x
        # else:
            # raise ValidationError("Wrong state!")
    # state = models.IntegerField(validators=[validator])
    # class Meta:
        # db_table = 'tab_1'