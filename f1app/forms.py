import logging
from django.forms import ModelForm
from f1app.models import DriverOpinionModel, RaceOpinionModel

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
        fields = ['championship_rate', 'chaos_rate', 'racing_rate', 'strategy_rate']