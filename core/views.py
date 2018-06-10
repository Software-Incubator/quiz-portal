from django.shortcuts import render, redirect, reverse
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
from .models import Candidate
from core.models import Category, Question, Instruction, Test, SelectedAnswer
import json
import itertools
import os
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
import datetime
from xhtml2pdf import pisa


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
        

class TestName(View):
    form_class = forms.TestForm
    template_name = 'core/test.html'

    def dispatch(self, request, *args, **kwargs):
        
        if (Test.objects.all()).count() == 0:
            Test.objects.create(test_name='', duration = 0)

        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(TestName, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        Tname = Test.objects.latest('test_name')
        return render(request,  self.template_name, {'form': form, 'Tname':Tname,})

    def post(self,request):
        Tname = Test.objects.latest('test_name')
        form = self.form_class(request.POST)
        if form.is_valid():
            Test.objects.filter(pk=Tname.pk).update(test_name=request.POST['test_name'],
             duration=request.POST['duration'])
            return redirect('admin_auth')
        else:
            form = self.form_class
        return render(request, 'core/signup.html', {'form': form})


class StartTest(generic.ListView):
    template_name = 'core/start_test.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.has_key("email"):
            return redirect('signup')
        return super(StartTest, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        category_list = Category.objects.all()
        context_dict = {'categories': category_list}
        return render(request, self.template_name, context_dict)


def random_question(n, can_id, ques_id):
    a = [x for x in range(1, n+1)]
    a = list(itertools.permutations(a))
    print(n, can_id, ques_id)
    print(a)
    l = len(a)
    return a[can_id % l][ques_id % n]


class QuestionByCategory(generic.DetailView):
    template_name = 'core/question_by_category.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.has_key("email"):
            return redirect('signup')
        return super(QuestionByCategory, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        category_name = kwargs["category_name"]
        context_dict = {'category_name': category_name}

        try:
            category = Category.objects.get(category=category_name)
            total_question = Question.objects.filter(category=category).count()
            email = request.session["email"]
            id = kwargs["id"]

            if id not in range(1,total_question+1):
                return redirect(reverse('category', kwargs={"category_name": category_name,
                                                     "id": 1}))
            candidate_id = Candidate.objects.get(email=email).id
            which_question = random_question(total_question, int(candidate_id), id)
            print("which question -> ", which_question)
            question = Question.objects.filter(category=category)[which_question-1]
            context_dict["which_question"] = which_question
            context_dict['question'] = question
            context_dict['category'] = category
        except Category.DoesNotExist:
            pass
        return render(self.request, self.template_name, context_dict)


class InstructionView(generic.ListView):
    template_name = 'core/instructions.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.has_key("email"):
            return redirect('signup')
        return super(InstructionView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        instruction = Instruction.objects.all()
        return render(request, self.template_name, {'instruction': instruction})



class AddQuestionView(View):
    form_class = forms.QuestionForm
    template_name = 'core/addquestion.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(AddQuestionView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request,  self.template_name, {'form': form})

    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            c = Category.objects.get(category = (dict(request.POST)['category'])[0])
            num = len(Question.objects.filter(category = c))+1
            if (dict(request.POST)['choice1'])[0] != (dict(request.POST)['choice2'])[0] != (dict(request.POST)['choice3'])[0] != (dict(request.POST)['choice4'])[0]:
                Question.objects.create(category = c, question_number = num,
                    question_text = (dict(request.POST)['question_text'])[0],choice1 = (dict(request.POST)['choice1'])[0],
                    choice2 = (dict(request.POST)['choice2'])[0], choice3 = (dict(request.POST)['choice3'])[0],
                    choice4 = (dict(request.POST)['choice4'])[0], correct_choice = (dict(request.POST)['correct_choice'])[0] )
                return redirect('admin_auth')
            else:
                return HttpResponse("Choices cannot be same")
        else:
            form = self.form_class()
        return render(request, self.template_name, {'form': form})


class AddCategoryView(View):
    form_class = forms.CategoryForm
    template_name = 'core/addcategory.html'

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(AddCategoryView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        if (Test.objects.all()).count() == 0:
            return redirect('Test name')
        else:
            cats = Category.objects.all()
            form = self.form_class()
            return render(request,  self.template_name, {'form': form, 'cats':cats})

    def post(self,request):
        (dict(request.POST))['category'][0] = ((dict(request.POST))['category'][0]).lower()
        form = self.form_class(request.POST)
        cats = Category.objects.all()
        if (Category.objects.filter(category=((dict(request.POST))['category'][0]).lower())).count() > 0:
            return HttpResponse('ALL READY EXIST')
        else:
            if form.is_valid():
                form.save()
                return redirect('admin_auth')
            else:
                form = self.form_class()
            return render(request, self.template_name, {'form': form, 'cats':cats})


class editcategory(View):

    def get(self,request):
        img_id = 0
        img_id = request.GET['imgid']

        if img_id:
            d = dict()
            name = request.GET['name']
            Category.objects.filter(pk=img_id).update(category=name)
            c = Category.objects.get(pk=img_id)
            d['name'] = c.category
            x = json.dumps(d)
            return HttpResponse(x)

class ShowQuestionsView(View):
    template_name = 'core/showquestion.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(ShowQuestionsView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        ques = Question.objects.all()
        return render(request,  self.template_name, {'ques':ques})

class ShowCandidateListView(View):
    template_name = 'core/candidatelist.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(ShowCandidateListView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        cands = Candidate.objects.all()
        return render(request,  self.template_name, {'cands':cands})


class ViewResultView(View):
    template_name = 'core/result.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(ViewResultView, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        l1=[]
        overall_total = 0
        overall_correct = 0
        cand = Candidate.objects.get(pk=pk)
        cats = Category.objects.all()
        selects = SelectedAnswer.objects.filter(email = cand)
        if len(selects) != 0:
            for cat in cats:
                total = 0
                correct = 0
                l=[]
                l.append(cat.category)
                percent = 0.0
                for select in selects:
                    if cat.category == select.question_text.category.category:
                        total = total + 1
                        overall_total = overall_total + 1
                        if select.question_text.correct_choice == select.selected_choice:
                            correct = correct + 1
                            overall_correct = overall_correct + 1
                l.append(total)
                l.append(correct)
                if total == 0:
                    percent = 0.0
                else:
                    percent =(correct/float(total))*100
                l.append(percent)
                l1.extend([l])
            total = 0
            correct = 0
            l=[]
            percent = 0.0
            if overall_total == 0:
                percent = 0.0
            else:
                percent = (overall_correct/float(overall_total))*100
                l.append("Total")
            l.append(overall_total)
            l.append(overall_correct)
            l.append(percent)
            l1.extend([l])
        return render(request,  self.template_name, {'selects':selects, 'cats':cats, 'cand':cand, 'l':l1})

    def post(self, request, pk):
        l1=[]
        data = {}
        overall_total = 0
        overall_correct = 0
        cand = Candidate.objects.get(pk=pk)
        cats = Category.objects.all()
        selects = SelectedAnswer.objects.filter(email = cand)
        if len(selects) != 0:
            for cat in cats:
                total = 0
                correct = 0
                l=[]
                l.append(cat.category)
                percent = 0.0
                for select in selects:
                    if cat.category == select.question_text.category.category:
                        total = total + 1
                        overall_total = overall_total + 1
                        if select.question_text.correct_choice == select.selected_choice:
                            correct = correct + 1
                            overall_correct = overall_correct + 1
                l.append(total)
                l.append(correct)
                if total == 0:
                    percent = 0.0
                else:
                    percent =(correct/float(total))*100
                l.append(percent)
                l1.extend([l])
            total = 0
            correct = 0
            l=[]
            percent = 0.0
            if overall_total == 0:
                percent = 0.0
            else:
                percent = (overall_correct/float(overall_total))*100
                l.append("Total")
            l.append(overall_total)
            l.append(overall_correct)
            l.append(percent)
            l1.extend([l])
            try:
                os.mkdir(os.path.join('core', 'media'))
            except:
                pass
            data = {'selects':selects, 'cats':cats, 'cand':cand, 'l':l1}
            template = get_template(self.template_name)
            html  = template.render(data)
            print(cand.name)
            st1 = str(cand.name) +" - " + str(cand.email) + ".pdf"
            file = open('core/' + 'media/' + st1, "w+b")
            pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file,
                    encoding='utf-8')
            file.seek(0)
            pdf = file.read()
            file.close()
        return render(request,  self.template_name, {'selects':selects, 'cats':cats, 'cand':cand, 'l':l1})



class EditQuestionView(View):
    form_class = forms.QuestionForm
    template_name = 'core/editquestion.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(EditQuestionView, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        question = Question.objects.get(pk=pk)
        print(question)
        form = self.form_class()
        return render(request,  self.template_name, {'form': form, 'question':question})

    def post(self,request, pk):
        question = Question.objects.get(pk=pk)
        num = question.question_number
        form = self.form_class(request.POST)
        if form.is_valid():
            if int((dict(request.POST)['correct_choice'])[0]) > 4:
                return HttpResponse("Not a valid choice")
            else:
                if (dict(request.POST)['choice1'])[0] != (dict(request.POST)['choice2'])[0] != (dict(request.POST)['choice3'])[0] != (dict(request.POST)['choice4'])[0]:
                    c = Category.objects.get(category = (dict(request.POST)['category'])[0])
                    Question.objects.filter(pk=pk).update(category = c,  question_number = num,
                        question_text = (dict(request.POST)['question_text'])[0], choice1 = (dict(request.POST)['choice1'])[0],
                        choice2 = (dict(request.POST)['choice2'])[0], choice3 = (dict(request.POST)['choice3'])[0],
                        choice4 = (dict(request.POST)['choice4'])[0], correct_choice = (dict(request.POST)['correct_choice'])[0] )
                    return redirect('admin_auth')
                else:
                    return HttpResponse("Choices cannot be same")
        else:
            form = self.form_class()
        return render(request, self.template_name, {'form': form, 'question':question})

class DeleteQuestionView(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(DeleteQuestionView, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        Question.objects.filter(pk=pk).delete()
        return redirect('control_operation')


class DeleteCategoryView(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(DeleteCategoryView, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        Category.objects.filter(pk=pk).delete()
        return redirect('control_operation')

@login_required
def instruction(request):
    form = forms.CandidateRegistration(None)
    name = form.cleaned_data.get('name')
    return render('core/instructions.html',{'name': name})


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


class AdminInstructionView(View):
    form_class = forms.InstructionForm
    template_name = 'core/instruction.html'

    def dispatch(self, request, *args, **kwargs):
        if len(Instruction.objects.all()) == 0:
            Instruction.objects.create(instruction='')

        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(AdminInstructionView, self).dispatch(request, *args, **kwargs)

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


def logout(request):
    try:
        del request.session['email']
        del request.session['name']
    except:
        pass
    return redirect('signup')