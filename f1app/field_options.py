RESULT_FIELDS = ['position_number', 'driver_number', 'driver', 'constructor', 'engine_manufacturer', 
    'tyre_manufacturer'] 

RACE_RESULT_FIELDS = ['laps', 'time', 'time_penalty', 'interval', 'reason_retired',
    'points', 'grid_position_text', 'positions_gained']

QUALIFYING_RESULT_FIELDS = ['q1', 'q2', 'q3', 'laps']

GRAND_PRIX_FIELDS = ['race']

DRIVER_OF_THE_DAY_FIELDS = ['percentage']

DRIVER_FIELDS = ['id', 'name', 'first_name', 'last_name', 'full_name', 'abbreviation', 'permanent_number', 
    'gender', 'date_of_birth', 'date_of_death', 'place_of_birth', 'country_of_birth_country', 
    'nationality_country', 'second_nationality_country', 'best_championship_position', 'best_race_result', 
    'best_starting_grid_position', 'total_championship_wins', 'total_race_entries', 'total_race_starts', 
    'total_race_wins', 'total_race_laps', 'total_podiums', 'total_points', 'total_championship_points', 
    'total_pole_positions', 'total_fastest_laps', 'total_driver_of_the_day']

CONSTRUCTOR_FIELDS = ['id', 'name', 'full_name', 'country', 'best_championship_position', 'best_race_result', 
    'best_starting_grid_position', 'total_championship_wins', 'total_race_entries', 'total_race_starts', 
    'total_race_wins', 'total_1_and_2_finishes', 'total_race_laps', 'total_podiums', 'total_podium_races', 
    'total_championship_points', 'total_pole_positions', 'total_fastest_laps']

RACE_FIELDS = ['id', 'year_id', 'round', 'date', 'grand_prix', 'official_name', 'qualifying_format',
    'circuit', 'circuit_type', 'course_length', 'laps', 'distance', 'scheduled_laps', 'scheduled_distance']

SEASON_ENTRANT_DRIVER_FIELDS = [
    'id', 'year', 'constructor', 'rounds_text', 'results'
]

FAMILY_RELATION_FIELDS = [
    'driver', 'type'
]