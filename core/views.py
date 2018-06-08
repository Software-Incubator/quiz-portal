from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.views import generic, View
from . import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render_to_response
from django.template import RequestContext
from .models import Candidate, Instruction, Category, Test, Question


class AdminAuth(generic.ListView):
    form_class = forms.AdminLoginForm
    template_name = 'core/admin_login.html'
    model = User

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('control_operation')
        return super(AdminAuth, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args):
        form = self.form_class
        return render(request, self.template_name, {"form": form})

    def post(self, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(self.request, user)
                return redirect("control_operation")
            else:
                messages.error(self.request, "Invalid user. Please enter a valid username")
                return redirect("admin_auth")


class ControlOperation(View):
    template_name = 'core/control.html'

    def get(self, request):
        return render(request, self.template_name)
        

# @user_passes_test(lambda u: u.is_superuser)
class TestName(View):
    form_class = forms.TestForm
    template_name = 'core/test.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            Test.objects.get(pk=1)
        except:
            Test.objects.create(test_name='', duration = 0)

        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(EditTestName, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        Tname = Test.objects.get(pk=1)
        return render(request,  self.template_name, {'form': form, 'Tname':Tname,})

    def post(self,request):
        Tname = Test.objects.get(pk=1)
        form = self.form_class(request.POST)
        if form.is_valid():
            Test.objects.filter(pk=1).update(test_name=request.POST['test_name'],
             duration=request.POST['duration'])
            return redirect('admin_auth')
        else:
            form = self.form_class
        return render(request, 'core/signup.html', {'form': form})


# class StartTest(generic.ListView):
#     template_name = 'core/start_test.html'
#
#     def dispatch(self, request, *args, **kwargs):
#         if not request.session.has_key("email"):
#             return redirect('signup')
#         return super(StartTest, self).dispatch(request, *args, **kwargs)
#
#     def get(self, request, *args, **kwargs):
#         category = Category.objects.all()
#         return render(request, self.template_name,{'category': category})

def index(request):
    context = RequestContext(request)
    category_list = Category.objects.all()
    context_dict = {'categories': category_list}
    for category in category_list:
        category.url = category.name.replace(' ', '_')
    return render_to_response('core/start_test.html', context_dict, context)


def category(request, category_name_url):
    context = RequestContext(request)
    category_name = category_name_url.replace('_', ' ')
    context_dict = {'category_name': category_name}

    try:
        category = Category.objects.get(name=category_name)
        questions = Question.objects.filter(category=category)
        context_dict['questions'] = questions
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass
    return render_to_response('core/question_by_category.html', context_dict, context)





# class QuestionByCategory(generic.DetailView):
#     model = Category
#     template_name = 'core/question_by_category.html'
#     context_object_name = 'category'
#
#     def dispatch(self, request, *args, **kwargs):
#         if not request.session.has_key("email"):
#             return redirect('signup')
#         return super(QuestionByCategory, self).dispatch(request, *args, **kwargs)
#
#     def get_object(self, queryset=None):
#         return get_object_or_404(Category, category=self.kwargs['category'])
#
#     def get_context_data(self, **kwargs):
#         context = super(QuestionByCategory, self).get_context_data(**kwargs)
#         context['questions'] = Question.objects.filter(category=self.get_object())
#         return context




class InstructionView(generic.ListView):
    template_name = 'core/instructions.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.has_key("email"):
            return redirect('signup')
        return super(InstructionView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        instruction = Instruction.objects.all()
        return render(request, self.template_name, {'instruction': instruction})


class CandidateRegistration(generic.ListView):
    form_class = forms.CandidateRegistration
    template_name = 'core/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if request.session.has_key("email"):
            return redirect('home')
        return super(CandidateRegistration, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            candidate = Candidate.objects.get(name=name, email=email)
            if candidate:
                self.request.session['email'] = email
                self.request.session['name'] = name
                return redirect('home')
        return render(self.request, self.template_name, {'form':form })


def logout(request):
    try:
        del request.session['email']
        del request.session['name']
    except:
        pass
    return redirect('signup')