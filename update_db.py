from datetime import datetime

from data import jobs, companies, specialties
from vacancies.models import Specialty, Company, Vacancy

IMG_100x60 = 'https://place-hold.it/100x60'


def update_companies():
    Company.objects.all().delete()
    for company in companies:
        Company.objects.create(
            name=company['title'],
            logo=IMG_100x60
        )


def update_specialties():
    Specialty.objects.all().delete()
    for specialty in specialties:
        Specialty.objects.create(
            code=specialty['code'],
            title=specialty['title'],
            picture=IMG_100x60
        )


def update_vacancies():
    Vacancy.objects.all().delete()
    for vacancy in jobs:
        published_at = datetime.strptime(vacancy['posted'], '%Y-%m-%d')
        Vacancy.objects.create(
            title=vacancy['title'],
            specialty=Specialty.objects.get(code=vacancy['cat']),
            company=Company.objects.get(name=vacancy['company']),
            salary_min=vacancy['salary_from'],
            salary_max=vacancy['salary_to'],
            description=vacancy['desc'],
            published_at=published_at
        )


update_companies()
update_specialties()
update_vacancies()
