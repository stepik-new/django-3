from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.db.models import Q, Count
from django.http import Http404
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView
from django.urls import reverse

from vacancies.models import Specialty, Company, Vacancy, Resume
from vacancies.forms import ApplicationForm, MyCompanyForm, MyVacancyForm, ResumeForm


class MainView(View):
    def get(self, request, *args, **kwargs):
        specialties = Specialty.objects.all().annotate(vacancies_count=Count('vacancies'))
        companies = Company.objects.all().annotate(vacancies_count=Count('vacancies'))
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
        url_from = request.META.get('HTTP_REFERER', '')
        company = Company.objects.filter(id=company_id).first()
        if company is None:
            raise Http404
        context = {
            'company': company,
            'url_from': url_from
        }
        return render(request, 'vacancies/company.html', context)


class AllCompaniesView(View):
    def get(self, request, *args, **kwargs):
        companies = Company.objects.all()
        context = {
            'companies': companies
        }
        return render(request, 'vacancies/companies-all.html', context)


class VacancyView(View):
    def get(self, request, vacancy_id, *args, **kwargs):
        vacancy = Vacancy.objects.filter(id=vacancy_id).first()
        url_from = request.META.get('HTTP_REFERER', '')

        if vacancy is None:
            raise Http404
        context = {
            'vacancy': vacancy,
            'url_from': url_from
        }
        return render(request, 'vacancies/vacancy.html', context)


class ApplicationSendView(View):
    def post(self, request, vacancy_id, *args, **kwargs):
        vacancy = Vacancy.objects.filter(id=vacancy_id).first()
        if vacancy is None:
            raise Http404

        application_form = ApplicationForm(request.POST)
        if not application_form.is_valid():
            context = {
                'vacancy': vacancy,
                'error': 'Данные заполнены некорректно'
            }
            return render(request, 'vacancies/vacancy.html', context)

        current_user = request.user
        if current_user.is_authenticated:
            application = application_form.save(commit=False)
            application.vacancy = vacancy
            application.user = current_user
            application.save()
        return render(request, 'vacancies/sent.html', context={
            'vacancy_id': vacancy_id
        })


class MyCompanyView(View):
    def get(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_authenticated:
            return HttpResponseRedirect('/login')

        user_company = Company.objects.filter(owner=current_user).first()
        if user_company is None:
            return render(request, 'vacancies/company-create.html')

        context = {
            'company': user_company,
            'form_action': 'update_company'
        }
        return render(request, 'vacancies/company-edit.html', context=context)

    def post(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_authenticated:
            return HttpResponseRedirect('/login')

        user_company = Company.objects.filter(owner=current_user).first()
        company_form = MyCompanyForm(request.POST, request.FILES)
        form_action = request.POST['form_action']

        if not company_form.is_valid():
            message = {
                'type': 'alert-danger',
                'text': 'Вы ввели некорректные данные'
            }
            context = {
                'form_action': form_action,
                'message': message,
                'company': user_company
            }
            return render(request, 'vacancies/company-edit.html', context=context)

        if form_action == 'add_company':
            company = company_form.save(commit=False)
            if 'logo' in request.FILES:
                company.logo = request.FILES['logo']
            company.owner = current_user
            company.save()
            message = {
                'type': 'alert-success',
                'text': 'Компания успешно добавлена!'
            }
            user_company = Company.objects.filter(owner=current_user).first()
            context = {
                'message': message,
                'company': user_company,
                'form_action': 'update_company'
            }
            return render(request, 'vacancies/company-edit.html', context=context)

        user_company.name = request.POST['name']
        user_company.location = request.POST['location']
        if 'logo' in request.FILES:
            user_company.logo = request.FILES['logo']
        user_company.description = request.POST['description']
        user_company.employee_count = request.POST['employee_count']
        user_company.save()
        message = {
            'type': 'alert-info',
            'text': 'Информация о компании изменена!'
        }
        context = {
            'message': message,
            'company': user_company,
            'form_action': 'update_company'
        }
        return render(request, 'vacancies/company-edit.html', context=context)


class AddMyCompanyView(View):
    def get(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_authenticated:
            return HttpResponseRedirect('/login')

        user_company = Company.objects.filter(owner=current_user).first()
        if user_company is None:
            return render(request, 'vacancies/company-edit.html', {
                'form_action': 'add_company'
            })
        return HttpResponseRedirect(reverse('my-company'))
        # return HttpResponseRedirect('/mycompany/')


class MyVacanciesView(View):
    def get(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_authenticated:
            return HttpResponseRedirect('/login')
        company = Company.objects.filter(owner=request.user).first()
        vacancies = Vacancy.objects.filter(company=company).\
            annotate(application_count=Count('applications'))
        context = {
            'vacancies': vacancies
        }
        return render(request, 'vacancies/vacancy-list.html', context)


class MyVacancyView(View):
    def get(self, request, vacancy_id, *args, **kwargs):
        current_user = request.user
        if not current_user.is_authenticated:
            return HttpResponseRedirect('/login')

        vacancy = get_object_or_404(Vacancy, id=vacancy_id)
        specialties = Specialty.objects.all()
        context = {
            'vacancy': vacancy,
            'specialties': specialties
        }
        return render(request, 'vacancies/vacancy-edit.html', context)

    def post(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_authenticated:
            return HttpResponseRedirect('/login')

        vacancy = get_object_or_404(Vacancy, id=request.POST['vacancy_id'])
        vacancy_form = MyVacancyForm(request.POST)
        specialty = get_object_or_404(Specialty, id=request.POST['specialty_id'])

        if not vacancy_form.is_valid():
            message = {
                'type': 'alert-danger',
                'text': 'Вы ввели некорректные данные'
            }
            context = {
                'message': message,
            }
            return render(request, 'vacancies/vacancy-edit.html', context)

        vacancy.title = request.POST['title']
        vacancy.skills = request.POST['skills']
        vacancy.description = request.POST['description']
        vacancy.salary_min = request.POST['salary_min']
        vacancy.salary_max = request.POST['salary_max']
        vacancy.specialty = specialty
        vacancy.save()
        message = {
            'type': 'alert-info',
            'text': 'Информация о вакансии изменена!'
        }
        context = {
            'message': message,
            'vacancy': vacancy,
        }
        return render(request, 'vacancies/vacancy-edit.html', context=context)


class AddMyVacancyView(View):
    def get(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_authenticated:
            return HttpResponseRedirect('/login')

        specialties = Specialty.objects.all()
        context = {
            'form_action': 'add_vacancy',
            'specialties': specialties
        }
        return render(request, 'vacancies/vacancy-edit.html', context)

    def post(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_authenticated:
            return HttpResponseRedirect('/login')

        vacancy_form = MyVacancyForm(request.POST)
        company = get_object_or_404(Company, owner=current_user)
        specialty = get_object_or_404(Specialty, id=request.POST['specialty_id'])

        if not vacancy_form.is_valid():
            message = {
                'type': 'alert-danger',
                'text': 'Вы ввели некорректные данные'
            }
            context = {
                'form_action': 'add_vacancy',
                'message': message,
            }
            return render(request, 'vacancies/vacancy-edit.html', context)

        vacancy = vacancy_form.save(commit=False)
        vacancy.company = company
        vacancy.specialty = specialty
        vacancy.save()
        message = {
            'type': 'alert-success',
            'text': 'Вакансия успешно добавлена!'
        }
        context = {
            'message': message,
            'vacancy': vacancy,
        }
        return render(request, 'vacancies/vacancy-edit.html', context=context)


class CustomLoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return render(request, 'vacancies/login.html', context={})

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect("/")
        else:
            return render(request, 'vacancies/login.html', context={
                'username': username,
            })


class CustomLogoutView(LogoutView):
    pass


class RegisterView(CreateView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return render(request, 'vacancies/register.html', context={})

    def post(self, request, *args, **kwargs):
        errors = {}
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        is_username_exists = bool(
            User.objects.filter(username=username).first()
        )

        if not is_username_exists:
            User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            return render(request, 'vacancies/login.html', context={
                'message': 'Регистрация прошла успешно'
            })

        errors['username'] = 'Пользователь с таким логином уже существует'
        context = {
            'errors': errors
        }
        return render(request, 'vacancies/register.html', context=context)


class AboutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'vacancies/about.html', {})


class SearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('s')
        if not query:
            HttpResponseRedirect('/')

        vacancies = Vacancy.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        context = {
            'vacancies': vacancies,
            'query': query
        }
        return render(request, 'vacancies/search.html', context=context)


class ResumeView(View):
    def get(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_authenticated:
            return HttpResponseRedirect('/login')

        resume = Resume.objects.filter(user=current_user).first()
        if not resume:
            return render(request, 'vacancies/resume-create.html')

        statuses, grades = Resume.STATUSES, Resume.GRADES
        specialties = Specialty.objects.all()
        context = {
            'resume': resume,
            'statuses': statuses,
            'grades': grades,
            'specialties': specialties
        }
        return render(request, 'vacancies/resume-edit.html', context)

    def post(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_authenticated:
            return HttpResponseRedirect('/login')

        resume = Resume.objects.filter(user=current_user).first()
        if resume.user != current_user:
            raise Http404

        statuses, grades = Resume.STATUSES, Resume.GRADES
        specialties = Specialty.objects.all()
        context = {
            'statuses': statuses,
            'grades': grades,
            'specialties': specialties,
        }
        resume_form = ResumeForm(request.POST)
        if not resume_form.is_valid():
            message = {
                'type': 'alert-danger',
                'text': 'Вы ввели некорректные данные'
            }
        else:
            message = {
                'type': 'alert-info',
                'text': 'Данные резюме обновлены'
            }

        specialty_id = request.POST['specialty_id']
        specialty = get_object_or_404(Specialty, id=specialty_id)
        resume.specialty = specialty
        resume.user = current_user
        resume.first_name = request.POST['first_name']
        resume.last_name = request.POST['last_name']
        resume.status = request.POST['status']
        resume.grade = request.POST['grade']
        resume.portfolio = request.POST['portfolio']
        resume.salary = request.POST['salary']
        resume.education = request.POST['education']
        resume.experience = request.POST['experience']
        resume.save()

        context['message'] = message
        context['resume'] = resume
        return render(request, 'vacancies/resume-edit.html', context)


class AddResumeView(View):
    def get(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_authenticated:
            return HttpResponseRedirect('/login')

        resume = Resume.objects.filter(user=current_user).first()
        statuses, grades = Resume.STATUSES, Resume.GRADES
        specialties = Specialty.objects.all()
        context = {
            'statuses': statuses,
            'grades': grades,
            'specialties': specialties
        }
        if resume:
            context['resume'] = resume
        else:
            context['form_action'] = 'add_resume'
        return render(request, 'vacancies/resume-edit.html', context=context)

    def post(self, request, *args, **kwargs):
        current_user = request.user
        if not current_user.is_authenticated:
            return HttpResponseRedirect('/login')

        if Resume.objects.filter(user=current_user).first():
            return HttpResponseRedirect('/resume')

        resume_form = ResumeForm(request.POST)
        statuses, grades = Resume.STATUSES, Resume.GRADES
        specialties = Specialty.objects.all()
        context = {
            'statuses': statuses,
            'grades': grades,
            'specialties': specialties,
        }
        if not resume_form.is_valid():
            message = {
                'type': 'alert-danger',
                'text': 'Вы ввели некорректные данные'
            }
            context['form_action'] = 'add_resume'

        specialty_id = request.POST['specialty_id']
        specialty = get_object_or_404(Specialty, id=specialty_id)
        resume = resume_form.save(commit=False)
        resume.specialty = specialty
        resume.user = current_user
        resume.save()

        message = {
            'type': 'alert-success',
            'text': 'Резюме успешно добавлено!'
        }
        context['message'] = message
        context['resume'] = resume
        return render(request, 'vacancies/resume-edit.html', context)

