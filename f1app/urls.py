from django.urls import path
from f1app import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path('', views.index, name='index'),
    path('race/',views.GeneralRaceView.as_view()),
    path('race/<int:year>/',views.YearRaceView.as_view()),
    path('race/<int:year>/<int:no>/',views.RaceResultView.as_view()),
    path('constructor/<str:name>/',views.ConstructorView.as_view()),
    path('constructor/<str:name>/total_pole_positions/',views.ConstructorPolePositionView.as_view()),
    path('constructor/<str:name>/total_race_wins/',views.ConstructorWinView.as_view()),
    path('driver/<str:name>/',views.DriverView.as_view()),
    path('driver/<str:name>/total_pole_positions/',views.DriverPolePositionView.as_view()),
    path('driver/<str:name>/total_race_starts/',views.DriverRaceView.as_view()),
    path('driver/<str:name>/total_race_wins/',views.DriverWinView.as_view()),
    path('driver/<str:name>/total_driver_of_the_day/',views.DriverOfTheDayView.as_view()),
    # path('form/',views.FormExampleView.as_view()),
    path('opinion/check_rate/', views.check_rate),
    path('opinion/<int:year>/', views.RaceOpinionFormView.as_view()),
    path('opinion/<int:year>/<int:no>/', views.DriverOpinionFormView.as_view()),
    path('opinion/<int:year>/<int:no>/<str:name>/', views.DriverOpinionFormView.as_view()),

    # re_path(r'^department$',views.departmentApi),
    # re_path(r'^department/([0-9]+)$',views.departmentApi),

    # re_path(r'^employee$',views.employeeApi),
    # re_path(r'^employee/([0-9]+)$',views.employeeApi),

    # re_path(r'^employee/savefile',views.SaveFile)
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
