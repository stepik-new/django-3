from django.http import Http404
from django.shortcuts import render
from django.views import View

from vacancies.models import Specialty, Company, Vacancy


class MainView(View):
    def get(self, request, *args, **kwargs):
        specialties = Specialty.objects.all()
        companies = Company.objects.all()
        context = {
            'specialties': specialties,
            'companies': companies,
        }
        return render(request, 'index.html', context)


class VacanciesView(View):
    def get(self, request, *args, **kwargs):
        vacancies = Vacancy.objects.all()
        context = {
            'vacancies': vacancies,
        }
        return render(request, 'vacancies/vacancies-all.html', context)


class VacanciesCatView(View):
    def get(self, request, category, *args, **kwargs):
        specialty = Specialty.objects.filter(code=category).first()
        if specialty is None:
            raise Http404
        context = {
            'specialty': specialty
        }
        return render(request, 'vacancies/vacancies-category.html', context)


class CompaniesView(View):
    def get(self, request, company_id, *args, **kwargs):
        company = Company.objects.filter(id=company_id).first()
        if company is None:
            raise Http404
        context = {
            'company': company
        }
        return render(request, 'vacancies/company.html', context)


class VacancyView(View):
    def get(self, request, vacancy_id, *args, **kwargs):
        vacancy = Vacancy.objects.filter(id=vacancy_id).first()
        if vacancy is None:
            raise Http404
        context = {
            'vacancy': vacancy
        }
        return render(request, 'vacancies/vacancy.html', context)
