import logging
import collections

from django.contrib.auth import authenticate
from django.db import models
from f1app.variables import PRETTY_FAMILY_NAMES, RACE_OPINION_MODEL_FIELDS
from rest_framework import serializers

from f1app.field_options import *
from f1app.models import Car, Constructor, Driver, DriverFamilyRelationship, DriverOfTheDayResult, QualifyingResult, Race, RaceOpinionModel, RaceResult, SeasonEntrantDriver

logger = logging.getLogger("django")

class BaseSerializer(serializers.Serializer):
    object_type = serializers.SerializerMethodField()
    std_name = serializers.SerializerMethodField()

    def get_object_type(self, obj):
        return obj.__class__.__name__

    def get_std_name(self, obj):
        if obj.__class__ == Race:
            return obj.official_name
        return getattr(obj, 'name', None)
    
class NestedSerializer(BaseSerializer):
    def to_representation(self, obj):
        base_representation = super().to_representation(obj)
        base_representation.update(BaseSerializer(obj).data)
        for key in base_representation.keys():
            value = getattr(obj, key, None)
            if issubclass(type(value), models.Model) and type(base_representation[key]) is collections.OrderedDict:
                base_representation[key].update(BaseSerializer(value).data)
        delete_fields = super().context.get('delete_fields')
        if delete_fields is not None:
            for key in delete_fields:
                del base_representation[key]
        add_fields = super().context.get('add_fields')
        if add_fields is not None:
            for key in add_fields:
                base_representation[key] = getattr(obj, key)
        return base_representation

class ShallowRaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = tuple(RACE_FIELDS)
  
class RaceSerializer(NestedSerializer, serializers.ModelSerializer):
    class Meta:
        model = Race 
        fields = tuple(RACE_FIELDS)
        depth = 1

class RaceOpinionModelSerializer(NestedSerializer, serializers.ModelSerializer):
    class Meta:
        model = RaceOpinionModel
        fields = tuple(RACE_OPINION_MODEL_FIELDS + ['race'])

### TODO - jakaś blokada żeby zawsze RESULT_FIELDS oraz ShallowRaceSerializer() były razem
class RaceResultSerializer(NestedSerializer, serializers.ModelSerializer):
    race = ShallowRaceSerializer()
    class Meta:
        model = RaceResult 
        fields = tuple(GRAND_PRIX_FIELDS + RESULT_FIELDS + RACE_RESULT_FIELDS)
        depth = 1
        
class ConstructorSerializer(NestedSerializer, serializers.ModelSerializer):
    class Meta:
        model = Constructor 
        fields = tuple(CONSTRUCTOR_FIELDS)
        depth = 1

class QualifyingResultSerializer(NestedSerializer, serializers.ModelSerializer):
    race = ShallowRaceSerializer()
    class Meta:
        model = QualifyingResult
        fields = tuple(GRAND_PRIX_FIELDS + RESULT_FIELDS + QUALIFYING_RESULT_FIELDS)
        depth = 1

class DriverOfTheDaySerializer(NestedSerializer, serializers.ModelSerializer):
    race = ShallowRaceSerializer()
    class Meta:
        model = DriverOfTheDayResult
        fields = tuple(GRAND_PRIX_FIELDS + RESULT_FIELDS + DRIVER_OF_THE_DAY_FIELDS)
        depth = 1

class DriverSerializer(NestedSerializer, serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = tuple(DRIVER_FIELDS)
        depth = 1

class SeasonEntrantDriverSerializer(NestedSerializer, serializers.ModelSerializer):
    class Meta:
        model = SeasonEntrantDriver
        fields = tuple(SEASON_ENTRANT_DRIVER_FIELDS)
        depth = 1
    
class DriverFamilyRelationshipSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    class Meta:
        model = DriverFamilyRelationship
        fields = tuple(FAMILY_RELATION_FIELDS)

    @staticmethod
    def get_type(obj: DriverFamilyRelationship):
        return PRETTY_FAMILY_NAMES[f'{obj.type}']

class CarSerializer(NestedSerializer, serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'
        depth = 1

class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')
        logger.info(f"Username: {username}, password: {password}")

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs