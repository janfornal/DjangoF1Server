import logging
from f1app.model_tables import CAR, COMMENT_MODEL, DRIVER_OPINION_MODEL, RACE_OPINION_MODEL, RACE_VIDEOS

logger = logging.getLogger('django')

class DatabaseRouter(object):
    administration_apps = [
        'admin', 
        'auth', 
        'contenttypes', 
        'sessions',
    ]
    
    f1_related = [
        COMMENT_MODEL,
        DRIVER_OPINION_MODEL,
        RACE_OPINION_MODEL,
        RACE_VIDEOS,
        CAR,
    ]
    
    f1_tables = [
        'circuit',
        'constructor',
        'constructor_previous_next_constructor',
        'constructor_standing',
        'continent',
        'country',
        'driver',
        'driver_family_relationship',
        'driver_of_the_day_result',
        'driver_standing',
        'engine_manufacturer',
        'entrant',
        'fastest_lap',
        'free_practice_1_result',
        'free_practice_2_result',
        'free_practice_3_result',
        'free_practice_4_result',
        'grand_prix',
        'pit_stop',
        'pre_qualifying_result',
        'qualifying_1_result',
        'qualifying_2_result',
        'qualifying_result',
        'race',
        'race_constructor_standing',
        'race_data',
        'race_driver_standing',
        'race_result',
        'season',
        'season_constructor_standing',
        'season_driver_standing',
        'season_entrant',
        'season_entrant_constructor',
        'season_entrant_driver',
        'season_entrant_tyre_manufacturer',
        'sprint_qualifying_result',
        'sprint_qualifying_starting_grid_position',
        'starting_grid_position',
        'tyre_manufacturer',
        'warming_up_result',
    ]

    def db_for_read(self, model, **hints):
        return 'default'         

    def db_for_write(self, model, **hints):
        # if model._meta.app_label in self.administration_apps:
            # return 'default'
        if model._meta.db_table not in DatabaseRouter.f1_tables:
            return 'default'

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True
        # dictionary = {
            # COMMENT_MODEL: 'default',
            # DRIVER_OPINION_MODEL: 'default',
            # RACE_OPINION_MODEL: 'default',
        # }
        # if model_name in dictionary.keys():
            # return db == dictionary[model_name]    
        # if app_label in self.administration_apps:
            # return db == 'default'
        # return False