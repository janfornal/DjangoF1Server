import logging
from django.forms import ModelForm
from f1app.models import DriverOpinionModel, RaceOpinionModel
from f1app.utils import RACE_OPINION_MODEL_FIELDS

logger = logging.Logger("django")

# class ExampleForm(ModelForm):
    # class Meta:
        # model = ExampleModel
        # fields = '__all__'

class DriverOpinionForm(ModelForm):
    class Meta:
        model = DriverOpinionModel
        fields = ['driver', 'rate', 'extended_opinion']
    
    def __init__(self, *args, **kwargs):
        super(DriverOpinionForm, self).__init__(*args, **kwargs)
        self.fields['driver'].required = False 

class RaceOpinionForm(ModelForm):
    class Meta:
        model = RaceOpinionModel
        fields = RACE_OPINION_MODEL_FIELDS
    
    def __init__(self, *args, **kwargs):
        super(RaceOpinionForm, self).__init__(*args, **kwargs)
        for field in RACE_OPINION_MODEL_FIELDS:
            self.fields[field].required = False 