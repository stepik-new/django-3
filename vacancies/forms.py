from django.forms import ModelForm

from vacancies.models import Application, Company, Vacancy, Resume


class ApplicationForm(ModelForm):
    class Meta:
        model = Application
        fields = ['written_username', 'written_phone', 'written_cover_letter']


class MyCompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'location', 'logo', 'description', 'employee_count']


class MyVacancyForm(ModelForm):
    class Meta:
        model = Vacancy
        fields = ['title', 'skills', 'description', 'salary_min', 'salary_max']


class ResumeForm(ModelForm):
    class Meta:
        model = Resume
        fields = ['first_name', 'last_name', 'status', 'grade',
                  'portfolio', 'salary', 'experience', 'education']
