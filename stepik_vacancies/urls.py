from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from vacancies.views import MainView, CustomLoginView, CustomLogoutView, RegisterView
from vacancies.views import (
    VacanciesView, VacanciesCatView, VacancyView, CompaniesView,
    ApplicationSendView, MyCompanyView, MyVacanciesView, MyVacancyView,
    AddMyCompanyView, AllCompaniesView, AboutView, AddMyVacancyView
)

urlpatterns = [
    path('', MainView.as_view()),
    path('admin/', admin.site.urls),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('about', AboutView.as_view(), name='about'),

    path('vacancies/', VacanciesView.as_view(), name='all-vacancies'),
    path('vacancies/cat/<str:category>/', VacanciesCatView.as_view(), name='cat-vacancies'),
    path('vacancies/<int:vacancy_id>/', VacancyView.as_view(), name='vacancy'),
    path('vacancies/<vacancy_id>/send/', ApplicationSendView.as_view(), name='send-application'),
    path('companies/', AllCompaniesView.as_view(), name='companies'),
    path('companies/<int:company_id>/', CompaniesView.as_view(), name='company'),

    path('mycompany/', MyCompanyView.as_view(), name='my-company'),
    path('mycompany/add/', AddMyCompanyView.as_view(), name='add-my-company'),
    path('mycompany/vacancies/', MyVacanciesView.as_view(), name='my-vacancies'),
    path('mycompany/vacancies/<vacancy_id>/', MyVacancyView.as_view(), name='edit-vacancy'),
    path('mycompany/vacancies/add/', AddMyVacancyView.as_view(), name='add-vacancy'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
