from collections import OrderedDict
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import RequestContext
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from f1app.field_options import *
from f1app.forms import CommentForm, CommentModel, DriverOpinionForm, RaceOpinionForm
from django.http.response import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.views.generic.edit import FormView
from f1app.utils import get_image_links
import json
from f1app.variables import NEW_RACE_OPINION
from rest_framework import permissions, views, status, generics
from rest_framework.response import Response
import logging

from f1app.serializers import ConstructorSerializer, DriverFamilyRelationshipSerializer, DriverOfTheDaySerializer, DriverSerializer, QualifyingResultSerializer, RaceOpinionModelSerializer, RaceResultSerializer, LoginSerializer, RaceSerializer, SeasonEntrantDriverSerializer
from f1app.models import Constructor, Driver, Race, RaceData, RaceOpinionModel, Season, SeasonEntrantDriver

logger = logging.getLogger("django")
# Create your views here.

def index(request):
    dictionary = {
        'Jajka': 1.79,
        'Bułki': 0.17,
        'Owsianka': 2.99,
        'Woda mineralna': 0.25,         
    }
    return render(request, 'template.html', {"dictionary": dictionary})

class GeneralRaceView(views.APIView):    
    permission_classes = (permissions.AllowAny,)
    def get(self, request, format=None):
        race = Race.objects.all()
        race_serializer=RaceSerializer(race,many=True)
        return JsonResponse(race_serializer.data,safe=False)

class CustomListAPIView(generics.ListAPIView):
    def get_serializer_context(self):
        return {}

    def list(self, request):
        return super(generics.ListAPIView, self).list(request)
    
    def get(self, request):
        return super(generics.ListAPIView, self).get(request)

class CustomListView(LoginRequiredMixin, ListView):
    login_url = "/" ### loginrequiredmixin
    template_name = "list_table.html" ### templateresponsemixin

    @classmethod
    def get_api_view_object(cls):
        pass

    def get_queryset(self): ### listapiview, według https://stackoverflow.com/questions/51169129/get-queryset-missing-1-required-positional-argument-request wystarczy listview
        api_view_object = self.__class__.get_api_view_object()
        api_view_object.setup(self.request, **self.kwargs)
        return api_view_object.list(self.request).data
    
    def get(self, request, *args):
        format = request.GET.get('format')
        if format == 'json':
            return JsonResponse(self.get_queryset(),safe=False)
        return super(ListView, self).get(request, *args)

class YearRaceAPIView(CustomListAPIView):
    serializer_class = RaceSerializer

    def get_queryset(self): 
        return Race.objects.filter(year=self.kwargs['year'])

class YearRaceView(ListView):
    login_url = "/"
    template_name = "year_race.html"
    allow_empty = False

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['year'] = self.kwargs['year']
        logger.info(data['year'])
        return data
    
    def get_queryset(self):
        race_list = Race.objects.filter(year=self.kwargs['year'])
        serializer = RaceSerializer(race_list, many=True)
        # opinion_list = RaceOpinionModel.objects.filter(user=self.request.user, race__in=race_list)
        # opinion_serializer = RaceOpinionModelSerializer(opinion_list, many=True)
        # combine_ordered_dicts(serializer.data, 'id', opinion_serializer.data, 'race')
        try: 
            return serializer.data
        except IndexError:
            raise Http404
        
    def get(self, request, year):
        request.session.get('years').insert(0, year)
        if len(request.session.get('years')) > 5:
            request.session.get('years').pop()
        request.session.modified = True
        format = request.GET.get('format')
        if format == 'json':
            return JsonResponse(self.get_queryset(),safe=False)
        return super(ListView, self).get(request, year)
        # if len(race) > 0:
            # return render(request, 'year_race.html', {'data': serializer.data})
        # return render(request, 'error_message.html')

class QualifyingResultAPIView(CustomListAPIView):
    serializer_class = QualifyingResultSerializer

    def get_serializer_context(self): ### listapiview
        return {
            'delete_fields': ['race'],
        }

    def get_queryset(self): ### listapiview, według https://stackoverflow.com/questions/51169129/get-queryset-missing-1-required-positional-argument-request wystarczy listview
        race = Race.objects.filter(year=self.kwargs['year'], round=self.kwargs['no'])
        values = race.values_list('id', flat=True)
        return RaceData.objects.filter(race_id__in=values, type='QUALIFYING_RESULT')

class RaceResultAPIView(CustomListAPIView):
    serializer_class = RaceResultSerializer

    def get_serializer_context(self): ### listapiview
        return {
            'delete_fields': ['race'],
            'add_fields': ['opinion']
        }

    def get_queryset(self): ### listapiview, według https://stackoverflow.com/questions/51169129/get-queryset-missing-1-required-positional-argument-request wystarczy listview
        race = Race.objects.filter(year=self.kwargs['year'], round=self.kwargs['no'])
        values = race.values_list('id', flat=True)
        return RaceData.objects.filter(race_id__in=values, type='RACE_RESULT')

class GrandPrixResultView(ListView):
    login_url = "/" ### loginrequiredmixin
    template_name = "race_result.html"
    context_object_name = "race_list"
    allow_empty = False

    def get_qualifying_queryset(self):
        api_view_object = QualifyingResultAPIView()
        api_view_object.setup(self.request, **self.kwargs)
        return api_view_object.list(self.request).data

    def get_context_data(self, **kwargs): ### multipleobjectmixin
        data = super().get_context_data(**kwargs)
        data['race'] = Race.get_race(self.kwargs['year'], self.kwargs['no'])
        data['qualifying_list'] = self.get_qualifying_queryset()
        data['image_urls'] = get_image_links(data['race'])  
        return data
    
    def get_queryset(self): ### listapiview, według https://stackoverflow.com/questions/51169129/get-queryset-missing-1-required-positional-argument-request wystarczy listview
        api_view_object = RaceResultAPIView()
        api_view_object.setup(self.request, **self.kwargs)
        return api_view_object.list(self.request).data

    def get(self, request, year, no):
        format = request.GET.get('format')
        if format == 'json':
            return JsonResponse(self.get_queryset(),safe=False)
        return super(ListView, self).get(request, year, no)

class ConstructorView(LoginRequiredMixin, DetailView):
    login_url = "/" 
    template_name = "constructor.html"
    allow_empty = False
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['list_of_extendables'] = ['total_pole_positions', 'total_race_wins']
        return data
    
    def get_object(self): ### listapiview, według https://stackoverflow.com/questions/51169129/get-queryset-missing-1-required-positional-argument-request wystarczy listview
        constructor = Constructor.objects.filter(id=self.kwargs['name'])
        serializer = ConstructorSerializer(constructor, many=True)
        try: 
            return serializer.data[0]
        except IndexError:
            raise Http404
        
    def get(self, request, name):
        return super(DetailView, self).get(request, name)    

class ConstructorPolePositionAPIView(CustomListAPIView):
    serializer_class = QualifyingResultSerializer

    def get_queryset(self): 
        return RaceData.objects.filter(constructor_id=self.kwargs['name'], type='QUALIFYING_RESULT', position_number=1)

class ConstructorPolePositionView(CustomListView):
    def get_api_view_object():
        return ConstructorPolePositionAPIView()
        
    def get(self, request, name):
        return super().get(request, name)    

class ConstructorWinAPIView(CustomListAPIView):
    serializer_class = RaceResultSerializer

    def get_queryset(self): 
        return RaceData.objects.filter(constructor_id=self.kwargs['name'], type='RACE_RESULT', position_number=1)

class ConstructorWinView(CustomListView):
    def get_api_view_object():
        return ConstructorWinAPIView()
        
    def get(self, request, name):
        return super().get(request, name)    

class DriverView(LoginRequiredMixin, DetailView):
    login_url = "/" 
    template_name = "driver.html"
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['list_of_extendables'] = ['total_pole_positions', 'total_race_starts', 'total_race_wins', 'total_driver_of_the_day']
        family_relations = Driver.family_relations(self.get_raw_object())
        data['family_relations'] = DriverFamilyRelationshipSerializer(family_relations, many=True).data if len(family_relations) > 0 else OrderedDict()
        history = SeasonEntrantDriver.team_history(self.get_raw_object())
        data['team_history'] = SeasonEntrantDriverSerializer(history, many=True).data
        data['results_visual'] = json.dumps(data['team_history'])
        return data
    
    def get_raw_object(self):
        try:
            return Driver.objects.filter(id=self.kwargs['name'])[0]
        except IndexError:
            raise Http404
    
    def get_object(self):
        serializer = DriverSerializer(self.get_raw_object())
        return serializer.data
        
    def get(self, request, name):
        return super(DetailView, self).get(request, name)    

class DriverPolePositionAPIView(CustomListAPIView):
    serializer_class = QualifyingResultSerializer

    def get_queryset(self): 
        return RaceData.objects.filter(driver_id=self.kwargs['name'], type='QUALIFYING_RESULT', position_number=1)

class DriverPolePositionView(CustomListView):
    def get_api_view_object():
        return DriverPolePositionAPIView()
        
    def get(self, request, name):
        return super().get(request, name)    

class DriverWinAPIView(CustomListAPIView):
    serializer_class = RaceResultSerializer

    def get_queryset(self): 
        return RaceData.objects.filter(driver_id=self.kwargs['name'], type='RACE_RESULT', position_number=1)

class DriverWinView(CustomListView):
    def get_api_view_object():
        return DriverWinAPIView()
        
    def get(self, request, name):
        return super().get(request, name)    

class DriverRaceAPIView(CustomListAPIView):
    serializer_class = RaceResultSerializer

    def get_queryset(self): 
        return RaceData.objects.filter(driver_id=self.kwargs['name'], type='RACE_RESULT')

class DriverRaceView(CustomListView):
    def get_api_view_object():
        return DriverRaceAPIView()
        
    def get(self, request, name):
        return super().get(request, name)    

class DriverOfTheDayAPIView(CustomListAPIView):
    serializer_class = DriverOfTheDaySerializer

    def get_queryset(self): 
        return RaceData.objects.filter(driver_id=self.kwargs['name'], type='DRIVER_OF_THE_DAY_RESULT', position_number=1)

class DriverOfTheDayView(CustomListView):
    def get_api_view_object():
        return DriverOfTheDayAPIView()
        
    def get(self, request, name):
        return super().get(request, name)    

class TerminalLoginView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)
    def post(self, request, format=None):
        serializer = LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        logger.info(serializer.validated_data)
        user = serializer.validated_data['user']
        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)

class DriverOpinionFormView(FormView):
    form_class = DriverOpinionForm
    template_name = 'driver_opinion.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        race_instance = Race.objects.filter(year=self.kwargs["year"], round=self.kwargs["no"])
        race_result_data = RaceData.objects.filter(race_id=race_instance[0].id, type="RACE_RESULT")
        data['race_name'] = race_instance[0].official_name
        data['drivers'] = race_result_data.values("driver").distinct()
        if self.kwargs.get('name'):
            data['driver'] = Driver.objects.filter(id=self.kwargs["name"])[0].id
        return data

    def get_success_url(self):
        year = self.kwargs['year']
        no = self.kwargs['no']
        return f'/f1app/race/{year}/{no}/'

    def post(self, request, year, no, name=None):
        form = DriverOpinionForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.race = Race.objects.filter(year=year, round=no)[0]
            if name:
                post.driver = Driver.objects.filter(id=name)[0]
            post.save()
            return redirect(self.get_success_url())
        return HttpResponseRedirect(request.path_info)

class RaceOpinionFormView(FormView):
    form_class = RaceOpinionForm
    template_name = 'race_opinion.html'

    def get(self, request, year):
        try: 
            valid_year = Season.objects.get(year = year)
        except Season.DoesNotExist:
            raise Http404
        year = (str)(year)
        round = 1
        if request.session.get(NEW_RACE_OPINION) is None:
            request.session[NEW_RACE_OPINION] = {}
            request.session[NEW_RACE_OPINION][year] = round
            request.session.modified = True
        if request.session.get(NEW_RACE_OPINION).get(year) is None:
            request.session[NEW_RACE_OPINION][year] = round
            request.session.modified = True
        return super(FormView, self).get(request, year)
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        year = (str)(self.kwargs['year'])
        round = self.request.session[NEW_RACE_OPINION][year]
        race_instance = Race.get_race((int)(year), round)
        data['race'] = race_instance
        data['fields'] = RaceOpinionFormView.form_class._meta.fields
        opinion = RaceOpinionModel.objects.filter(user = self.request.user, race = race_instance).first()
        data['opinion'] = RaceOpinionModelSerializer(opinion).data
        data['comment_form'] = CommentForm()
        return data

    def get_success_url(self, year):
        no_of_races = len(Race.objects.filter(year=(int)(year)))
        if self.request.session.get(NEW_RACE_OPINION).get(year) < 1 or self.request.session.get(NEW_RACE_OPINION).get(year) > no_of_races:
            del self.request.session[NEW_RACE_OPINION][year]
            self.request.session.modified = True
        round = self.request.session.get(NEW_RACE_OPINION).get(year)
        if round is None:
            return f'/f1app/race/{year}/'
        else: 
            return f'/f1app/opinion/{year}/' 
    
    def post_comment(self, request, year, round):
        form = CommentForm(request.POST)
        if form.is_valid():
            CommentModel.objects.create(
                user = request.user, race = Race.get_race((int)(year), round),
                comment_body = form.cleaned_data['comment_body']
            )
        return redirect(self.get_success_url(year))

    def post_rates(self, request, year, round):
        form = RaceOpinionForm(request.POST)
        if form.is_valid():
            RaceOpinionModel.objects.update_or_create(
                user = request.user, race = Race.get_race((int)(year), round),
                defaults = form.cleaned_data
            )
        if request.method=='POST' and 'previous' in request.POST:
            request.session[NEW_RACE_OPINION][year] = round - 1
        if request.method=='POST' and 'next' in request.POST:
            request.session[NEW_RACE_OPINION][year] = round + 1
        request.session.modified = True
        return redirect(self.get_success_url(year))

    def post(self, request, year):
        year = (str)(year)
        round = request.session[NEW_RACE_OPINION][year]
        if 'submit-comment' in request.POST:
            return self.post_comment(request, year, round)
        else:
            return self.post_rates(request, year, round)
    
# class FormExampleView(views.APIView):
    # permission_classes = (permissions.AllowAny,)
    # def get(self, request, format=None):
        # return render(request, 'form_example.html')
    
    # def post(self, request, format=None):
        # form = ExampleForm(request.POST)
        # if form.is_valid():
            # form.save()
            # return HttpResponse("Your data is successfully saved")
        # else:
            # return HttpResponse("Validation error!")

"""
Page not found Error 404
"""
def page_not_found(request, exception):
    response = render('404.html', context_instance=RequestContext(request))
    response.status_code = 404
    return response

def check_rate(request):
    rate = request.GET.get('rate')
    rate = int(rate)
    data = {
       'valid_rate': rate >= 1 and rate <= 10
    }
    return JsonResponse(data)                    
    
# class LoginView(views.APIView):
    # def post(self, request, format=None):
        # form = AuthenticationForm(request, data=request.POST)
        # if form.is_valid():
            # username = form.cleaned_data.get('username')
            # password = form.cleaned_data.get('password')
            # user = authenticate(username=username, password=password)
            # if user is not None:
                # login(request, user)
                # return redirect("main:homepage")
            # else:
                # logger.error(request,"Invalid username or password.")
        # else:
            # logger.error(request,"Invalid username or password.")
        

# @csrf_exempt
# def driverApi(request,id=0):
    # if request.method=='GET':
        # race = Race.objects.all()
        # retrieval = request.path.split('/')[3] if len(request.path.split('/')) > 3 else ''
        # if retrieval != '':
            # race = race.filter(year=(int)(retrieval))
        # race_serializer=RaceSerializer(race,many=True)
        # return JsonResponse(race_serializer.data,safe=False)

# @csrf_exempt
# def departmentApi(request,id=0):
#     if request.method=='GET':
#         departments = Departments.objects.all()
#         departments_serializer=DepartmentSerializer(departments,many=True)
#         return JsonResponse(departments_serializer.data,safe=False)
#     elif request.method=='POST':
#         department_data=JSONParser().parse(request)
#         departments_serializer=DepartmentSerializer(data=department_data)
#         if departments_serializer.is_valid():
#             departments_serializer.save()
#             return JsonResponse("Added Successfully",safe=False)
#         return JsonResponse("Failed to Add",safe=False)
#     elif request.method=='PUT':
#         department_data=JSONParser().parse(request)
#         department=Departments.objects.get(DepartmentId=department_data['DepartmentId'])
#         departments_serializer=DepartmentSerializer(department,data=department_data)
#         if departments_serializer.is_valid():
#             departments_serializer.save()
#             return JsonResponse("Updated Successfully",safe=False)
#         return JsonResponse("Failed to Update")
#     elif request.method=='DELETE':
#         department=Departments.objects.get(DepartmentId=id)
#         department.delete()
#         return JsonResponse("Deleted Successfully",safe=False)

# @csrf_exempt
# def employeeApi(request,id=0):
#     if request.method=='GET':
#         employees = Employees.objects.all()
#         employees_serializer=EmployeeSerializer(employees,many=True)
#         return JsonResponse(employees_serializer.data,safe=False)
#     elif request.method=='POST':
#         employee_data=JSONParser().parse(request)
#         employees_serializer=EmployeeSerializer(data=employee_data)
#         if employees_serializer.is_valid():
#             employees_serializer.save()
#             return JsonResponse("Added Successfully",safe=False)
#         return JsonResponse("Failed to Add",safe=False)
#     elif request.method=='PUT':
#         employee_data=JSONParser().parse(request)
#         employee=Employees.objects.get(EmployeeId=employee_data['EmployeeId'])
#         employees_serializer=EmployeeSerializer(employee,data=employee_data)
#         if employees_serializer.is_valid():
#             employees_serializer.save()
#             return JsonResponse("Updated Successfully",safe=False)
#         return JsonResponse("Failed to Update")
#     elif request.method=='DELETE':
#         employee=Employees.objects.get(EmployeeId=id)
#         employee.delete()
#         return JsonResponse("Deleted Successfully",safe=False)

# @csrf_exempt
# def SaveFile(request):
#     file=request.FILES['file']
#     file_name=default_storage.save(file.name,file)
#     return JsonResponse(file_name,safe=False)
