from django.db import models


class Vacancy(models.Model):
    title = models.CharField(max_length=128)
    specialty = models.ForeignKey('vacancies.Specialty',
                                  on_delete=models.CASCADE,
                                  related_name='vacancies')
    company = models.ForeignKey('vacancies.Company',
                                on_delete=models.CASCADE,
                                related_name='vacancies')
    skills = models.CharField(max_length=1024)
    description = models.TextField()
    salary_min = models.FloatField()
    salary_max = models.FloatField()
    published_at = models.DateTimeField()


class Company(models.Model):
    name = models.CharField(max_length=128)
    location = models.CharField(max_length=128, default='')
    logo = models.CharField(max_length=1024, default='')
    description = models.TextField(default='')
    employee_count = models.IntegerField(default=0)


class Specialty(models.Model):
    code = models.CharField(max_length=64)
    title = models.CharField(max_length=128)
    picture = models.CharField(max_length=1024, default='')
