from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.views.generic import ListView, DetailView, FormView, TemplateView
from django.views import View
from . import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from core.models import Category, Question, Instruction, Test


class AdminAuth(ListView):
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
            username = form.cleaned_data.get('username', '')
            password = form.cleaned_data.get('password', '')
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
        return super(TestName, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        Tname = Test.objects.get(pk=1)
        print(Tname)
        return render(request,  self.template_name, {'form': form, 'Tname':Tname,})

    def post(self,request):
        Tname = Test.objects.get(pk=1)
        form = self.form_class(request.POST)
        print(dict(request.POST))
        if form.is_valid():
            Test.objects.filter(pk=1).update(test_name=request.POST['test_name'],
             duration=request.POST['duration'])
            return redirect('admin_auth')
        else:
            form = self.form_class()
        return render(request, self.template_name, {'form': form, 'Tname':Tname,})

class InstructionView(View):
    form_class = forms.InstructionForm
    template_name = 'core/instruction.html'

    def dispatch(self, request, *args, **kwargs):
        if len(Instruction.objects.all()) == 0:
            Instruction.objects.create(instruction='')

        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(InstructionView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        Iname = Instruction.objects.latest('instruction')
        return render(request,  self.template_name, {'form': form, 'Iname':Iname.instruction,})

    def post(self,request):
        Iname = Instruction.objects.latest('instruction')
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_auth')
        else:
            form = self.form_class()
        return render(request, self.template_name, {'form': form, 'Iname':Iname,})


# class signup(View):
#     form_class = SignUpPage

#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return redirect('newsfeed')
#         return super(signup, self).dispatch(request, *args, **kwargs)

#     def get(self, request):
#         form = self.form_class()
#         return render(request, 'learn/signup.html', {'form': form})

#     def post(self,request):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             User.objects.filter(email=email).count()
#             # if count is greater than zero it means this email id already exist
#             if email and User.objects.filter(email=email).count() > 0:
#                 messages.error(request, 'this email-id already register', extra_tags='alert')
#             else:
#                 user = form.save(commit=False)
#                 user.is_active = False
#                 user.save()
#                 # get_current_site used to get the url of current page
#                 current_site = get_current_site(request)
#                 subject = 'Activate Your phoics Account'
#                 # subject with email is send
#                 message = render_to_string('learn/account_activation_email.html', {
#                     'user': user,
#                     'domain': current_site.domain,
#                     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                     'token': account_activation_token.make_token(user),
#                 })
#                 from_mail = EMAIL_HOST_USER
#                 to_mail = [user.email]
#                 # fail_silently "false", then if error in sending email it will raise -
#                 # smtplib.SMTPException, SMTPServerDisconnected, SMTPDataError,etc.
#                 send_mail(subject, message, from_mail, to_mail, fail_silently=False)
#                 return render(request, 'learn/email_sent.html')

#         else:
#             form = SignUpPage()
#         return render(request, 'learn/signup.html', {'form': form})
