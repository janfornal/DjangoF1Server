#!/bin/bash

sed -i "s/constructor_id = models.CharField(max_length=255, blank=True, null=True)/constructor = models.ForeignKey(Constructor, models.DO_NOTHING)/g" f1app/models.py
sed -i "s/engine_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)/engine_manufacturer = models.ForeignKey(EngineManufacturer, models.DO_NOTHING)/g" f1app/models.py
sed -i "s/tyre_manufacturer_id = models.CharField(max_length=255, blank=True, null=True)/tyre_manufacturer = models.ForeignKey(TyreManufacturer, models.DO_NOTHING)/g" f1app/models.py
sed -i "s/race_id = models.IntegerField(blank=True, null=True)/race = models.ForeignKey(Race, models.DO_NOTHING)/g" f1app/models.py
