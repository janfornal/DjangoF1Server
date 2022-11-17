from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponse, redirect, render
from f1app.field_options import *
from f1app.forms import DriverOpinionForm, RaceOpinionForm
from django.http.response import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.views.generic.edit import FormView
from f1app.utils import RACE_OPINION
from rest_framework import permissions, views, status
from rest_framework.response import Response
import logging
import os

from f1app.serializers import ConstructorSerializer, DriverOfTheDaySerializer, DriverSerializer, QualifyingResultSerializer, RaceResultSerializer, LoginSerializer, RaceSerializer
from f1app.models import Constructor, Driver, Race, RaceData

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

class YearRaceView(LoginRequiredMixin, views.APIView):
    login_url = "/"
    def get(self, request, year):
        request.session.get('years').insert(0, year)
        logger.info(request.session.get('years'))
        if len(request.session.get('years')) > 5:
            request.session.get('years').pop()
        request.session.modified = True
        race = Race.objects.filter(year=year)
        serializer = RaceSerializer(race,many=True)
        if len(race) > 0:
            return render(request, 'year_race.html', {'data': serializer.data})
        return render(request, 'error_message.html')

class RaceResultView(LoginRequiredMixin, views.APIView):
    login_url = "/"
    def get(self, request, year, no):
        context = {
            'delete_fields': ['race'],
            'add_fields': ['opinion']
        }
        race = Race.objects.filter(year=year, round=no)
        values = race.values_list('id', flat=True)
        race_data = RaceData.objects.filter(race_id__in=values, type='RACE_RESULT')
        serializer = RaceResultSerializer(race_data, many=True, context=context)
        if len(race_data) > 0 and len(race) > 0:
            return render(request, 'race_result.html', {"data": serializer.data, 'race': race[0]})        
        return render(request, 'error_message.html')

class ConstructorView(views.APIView):
    login_url = "/"
    def get(self, request, name):
        constructor = Constructor.objects.filter(id=name)
        serializer = ConstructorSerializer(constructor, many=True)
        if len(constructor) > 0:
            return render(request, 'constructor.html', {"data": serializer.data[0],
                "list_of_extendables": ['total_pole_positions', 'total_race_wins']}) 
        return render(request, 'error_message.html')

class ConstructorPolePositionView(views.APIView):
    login_url = "/"
    def get(self, request, name):
        driver_history = RaceData.objects.filter(constructor_id=name, type='QUALIFYING_RESULT', position_number=1)
        serializer = QualifyingResultSerializer(driver_history,many=True)
        if len(driver_history) > 0:
            return render(request, 'race_table.html', {"data": serializer.data})
        return render(request, 'error_message.html')

class ConstructorWinView(views.APIView):
    login_url = "/"
    def get(self, request, name):
        driver_history = RaceData.objects.filter(constructor_id=name, type='RACE_RESULT', position_number=1)
        serializer = RaceResultSerializer(driver_history,many=True)
        if len(driver_history) > 0:
            return render(request, 'race_table.html', {"data": serializer.data})
        return render(request, 'error_message.html')

class DriverView(views.APIView):
    login_url = "/"
    def get(self, request, name):
        driver = Driver.objects.filter(id=name)
        serializer = DriverSerializer(driver,many=True)
        if len(driver) > 0:
            return render(request, 'driver.html', {"data": serializer.data[0],
                "list_of_extendables": ['total_pole_positions', 'total_race_starts', 'total_race_wins', 'total_driver_of_the_day']})
        return render(request, 'error_message.html')

class DriverPolePositionView(views.APIView):
    login_url = "/"
    def get(self, request, name):
        driver_history = RaceData.objects.filter(driver_id=name, type='QUALIFYING_RESULT', position_number=1)
        serializer = QualifyingResultSerializer(driver_history,many=True)
        if len(driver_history) > 0:
            return render(request, 'race_table.html', {"data": serializer.data})
        return render(request, 'error_message.html')

class DriverWinView(views.APIView):
    login_url = "/"
    def get(self, request, name):
        driver_history = RaceData.objects.filter(driver_id=name, type='RACE_RESULT', position_number=1)
        serializer = RaceResultSerializer(driver_history,many=True)
        if len(driver_history) > 0:
            return render(request, 'race_table.html', {"data": serializer.data})
        return render(request, 'error_message.html')

class DriverRaceView(views.APIView):
    login_url = "/"
    def get(self, request, name):
        driver_history = RaceData.objects.filter(driver_id=name, type='RACE_RESULT')
        serializer = RaceResultSerializer(driver_history,many=True)
        if len(driver_history) > 0:
            return render(request, 'race_table.html', {"data": serializer.data})
        return render(request, 'error_message.html')

class DriverOfTheDayView(views.APIView):
    login_url = "/"
    def get(self, request, name):
        driver_history = RaceData.objects.filter(driver_id=name, type='DRIVER_OF_THE_DAY_RESULT', position_number=1)
        serializer = DriverOfTheDaySerializer(driver_history,many=True)
        if len(driver_history) > 0:
            return render(request, 'race_table.html', {"data": serializer.data})
        return render(request, 'error_message.html')

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
        round = 0
        if self.request.session.get(RACE_OPINION) is None:
            self.request.session[RACE_OPINION] = {
                "year": year, 
                "round": round
            }
            self.set_next_race()
        if self.request.session.get(RACE_OPINION) is None:
            return redirect(self.get_success_url(year))
        return super(FormView, self).get(request, year)
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        opinion_dict = self.request.session[RACE_OPINION]
        logger.info(opinion_dict)
        race_instance = Race.get_race(opinion_dict['year'], opinion_dict['round'])
        data['race_name'] = race_instance.official_name
        data['fields'] = RaceOpinionFormView.form_class._meta.fields
        return data

    def get_success_url(self, year):
        opinion_dict = self.request.session.get(RACE_OPINION)
        if opinion_dict is None:
            return f'/f1app/race/{year}/'
        else: 
            return f'/f1app/opinion/{year}/' 

    def set_next_race(self):
        opinion_dict = self.request.session.get(RACE_OPINION)
        no_of_races = len(Race.objects.filter(year=opinion_dict['year']))
        for i in range(1, no_of_races + 2):
            opinion_dict['round'] = i
            if no_of_races < opinion_dict['round']:
                del self.request.session[RACE_OPINION]
                return 
            race = Race.get_race(opinion_dict['year'], opinion_dict['round'])
            if race.is_rated(self.request.user) is False:
                break
        self.request.session[RACE_OPINION] = opinion_dict 
        self.request.session.modified = True
    
    def post(self, request, year):
        form = RaceOpinionForm(request.POST)
        opinion_dict = self.request.session[RACE_OPINION]
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.race = Race.get_race(year=opinion_dict['year'], round=opinion_dict['round'])
            try:
                post.full_clean(exclude=['id'])
                post.save()
            except ValidationError:
                pass
            self.set_next_race()
            return redirect(self.get_success_url(year))
        else: return redirect(self.get_success_url(year))
    
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
