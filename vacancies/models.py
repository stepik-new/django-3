from django.db import models
from django.contrib.auth.models import User

from stepik_vacancies.settings import (MEDIA_COMPANY_IMAGE_DIR,
                                       MEDIA_SPECIALITY_IMAGE_DIR)


class Vacancy(models.Model):
    title = models.CharField(max_length=128)
    specialty = models.ForeignKey('vacancies.Specialty',
                                  on_delete=models.CASCADE,
                                  related_name='vacancies')
    company = models.ForeignKey('vacancies.Company',
                                on_delete=models.CASCADE,
                                related_name='vacancies')
    skills = models.CharField(max_length=1024, blank=True)
    description = models.TextField()
    salary_min = models.FloatField()
    salary_max = models.FloatField()
    published_at = models.DateTimeField(auto_now_add=True)


class Company(models.Model):
    name = models.CharField(max_length=128)
    location = models.CharField(max_length=128, default='', blank=True)
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR,
                             default=None,
                             blank=True)
    description = models.TextField(default='', blank=True)
    employee_count = models.IntegerField(default=0)
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='companies',
                              default=None,
                              null=True,
                              blank=True)


class Specialty(models.Model):
    code = models.CharField(max_length=64)
    title = models.CharField(max_length=128)
    picture = models.ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR,
                                default=None)


class Application(models.Model):
    written_username = models.CharField(max_length=128)
    written_phone = models.CharField(max_length=32)
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey('vacancies.Vacancy',
                                related_name='applications',
                                on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             related_name='applications',
                             on_delete=models.CASCADE,
                             default=None)


class Resume(models.Model):
    STATUSES = ['Не ищу работу', 'Рассматриваю предложения', 'Ищу работу']
    GRADES = ['Стажер', 'Джуниор', 'Миддл', 'Синьор', 'Лид']

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='resume',
    )
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    status = models.CharField(max_length=128)
    grade = models.CharField(max_length=128)
    portfolio = models.CharField(max_length=128)
    salary = models.IntegerField(default=0)
    specialty = models.ForeignKey(
        'vacancies.Specialty',
        on_delete=models.CASCADE,
        related_name='resumes'
    )
    education = models.TextField(max_length=10000)
    experience = models.TextField(max_length=10000)
