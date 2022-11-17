RESULT_FIELDS = ['position_number', 'driver_number', 'driver', 'constructor', 'engine_manufacturer', 
    'tyre_manufacturer'] 

RACE_RESULT_FIELDS = ['race_laps', 'race_time', 'race_time_penalty', 'race_interval', 'race_reason_retired',
    'race_points', 'race_grid_position_text', 'race_positions_gained']

QUALIFYING_RESULT_FIELDS = ['qualifying_q1', 'qualifying_q2', 'qualifying_q3', 'qualifying_laps']

GRAND_PRIX_FIELDS = ['race']

DRIVER_OF_THE_DAY_FIELDS = ['driver_of_the_day_percentage']

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