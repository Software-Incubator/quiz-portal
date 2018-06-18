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
from core.models import Candidate, Instruction, Category, Test, Question, SelectedAnswer
import json
import itertools
import os
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
import datetime
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from django.template import loader
# from my_project.snippets.template import render_block_to_string 
from django.template import loader


class AdminAuth(generic.ListView):
    form_class = forms.AdminLoginForm
    template_name = 'admin/admin_login.html'
    model = User

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return redirect('control_operation')
        return super(AdminAuth, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(self.request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(self.request, user)
                return redirect("control_operation")
            else:
                messages.error(self.request, "Invalid username or password.Please enter valid credentials.")
                return redirect("admin_auth")

        return render(request,self.template_name, {'form':form})


class ControlOperation(View):
    template_name = 'admin/control.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(ControlOperation, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(self.request, self.template_name)


class TestName(View):
    form_class = forms.TestForm
    template_name = 'admin/test.html'

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(TestName, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        # Tname = Test.objects.latest('test_name')
        return render(request, self.template_name, {'form': form})

    def post(self,request, *args, **kwargs):
        if request.POST['duration'] == '0':
            message = "Test duration cannot be zero"
            return render(request, 'admin/error.html', {'message': message})
        else:
            if (Test.objects.filter(test_name=request.POST['test_name'])).count() > 0:
                message = "No two test can have same name"
                return render(request, 'admin/error.html', {'message': message})
            else:
                form = self.form_class(request.POST)
                if form.is_valid():
                    Test.objects.create(test_name=request.POST['test_name'],
                     duration=request.POST['duration'], on_or_off=request.POST['on_or_off'])
                    return redirect('control_operation')
                else:
                    messages.error(self.request, "Data not valid.")
                    form = self.form_class
                    return render(self.request, self.template_name, {'form': form})

class ShowTestView(View):
    template_name = 'admin/edittestname.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(ShowTestView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        tests = Test.objects.all()
        return render(request, self.template_name, {'tests':tests})

class EditTest(View):
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(EditTest, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        img_id = 0
        img_id = request.GET['imgid']
        if img_id:
            dur = request.GET['dur']
            test = request.GET['test']
            if int(dur) < 1:
                message = "Duration cannot be 0 or less"
                return render(request, 'admin/error.html', {'message': message})
            else:
                Test.objects.filter(pk=img_id).update(duration=dur, test_name=test)
                return HttpResponse(img_id)

class ToggleTestStatus(View):
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(ToggleTestStatus, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        if pk:
            test = Test.objects.get(pk=pk)
            if test.on_or_off == True:
                Test.objects.filter(pk=pk).update(on_or_off=False)
            else:
                Test.objects.filter(pk=pk).update(on_or_off=True)
            return redirect('See_Test')


class DeleteTest(View):
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(DeleteTest, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        Test.objects.filter(pk=pk).delete()
        return redirect('control_operation')


class AddQuestionView(View):
    form_class = forms.QuestionForm
    template_name = 'admin/addquestion.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(AddQuestionView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if (Test.objects.all()).count() == 0:
            message = "No test present"
            return render(request, 'admin/error.html', {'message': message})
        else:
            if (Category.objects.all()).count() == 0:
                message = "No category present"
                return render(request, 'admin/error.html', {'message': message})
            else:            
                form = self.form_class()
                return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            c = Category.objects.get(category=(dict(request.POST)['category'])[0])
            num = len(Question.objects.filter(category=c)) + 1
            if (dict(request.POST)['choice1'])[0] != (dict(request.POST)['choice2'])[0] != (dict(request.POST)['choice3'])[0] != (dict(request.POST)['choice4'])[0]:
                Question.objects.create(category=c, question_number=num,
                                        question_text=(dict(request.POST)['question_text'])[0],
                                        choice1=(dict(request.POST)['choice1'])[0],
                                        choice2=(dict(request.POST)['choice2'])[0],
                                        choice3=(dict(request.POST)['choice3'])[0],
                                        choice4=(dict(request.POST)['choice4'])[0],
                                        correct_choice=(dict(request.POST)['correct_choice'])[0])
                return redirect('control_operation')
            else:
                message = "Choices cannot be same"
                return render(request, 'admin/error.html', {'message': message})
        else:
            messages.error(self.request, "Invalid data.")
            form = self.form_class()
            return render(self.request, self.template_name, {'form': form})

class EditQuestionView(View):
    form_class = forms.QuestionForm
    template_name = 'admin/editquestion.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(EditQuestionView, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        question = Question.objects.get(pk=pk)
        form = self.form_class()
        (dict(form.__dict__['fields'])['question_text']).initial = question.question_text
        (dict(form.__dict__['fields'])['category']).initial = question.category
        (dict(form.__dict__['fields'])['choice1']).initial = question.choice1
        (dict(form.__dict__['fields'])['choice2']).initial = question.choice2
        (dict(form.__dict__['fields'])['choice3']).initial = question.choice3
        (dict(form.__dict__['fields'])['choice4']).initial = question.choice4
        (dict(form.__dict__['fields'])['correct_choice']).initial = question.correct_choice
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk, *args, **kwargs):
        question = Question.objects.get(pk=pk)
        num = question.question_number
        form = self.form_class(request.POST)
        if form.is_valid():
            if (dict(request.POST)['choice1'])[0] != (dict(request.POST)['choice2'])[0] != (dict(request.POST)['choice3'])[0] != (dict(request.POST)['choice4'])[0]:
                c = Category.objects.get(category = (dict(request.POST)['category'])[0])
                Question.objects.filter(pk=pk).update(category = c,  question_number = num,
                    question_text = (dict(request.POST)['question_text'])[0], choice1 = (dict(request.POST)['choice1'])[0],
                    choice2 = (dict(request.POST)['choice2'])[0], choice3 = (dict(request.POST)['choice3'])[0],
                    choice4 = (dict(request.POST)['choice4'])[0], correct_choice = (dict(request.POST)['correct_choice'])[0] )
                return redirect('admin_auth')
            else:
                message = "Choices cannot be same"
                return render(request, 'admin/error.html', {'message': message})
        else:
            messages.error(self.request, "Invalid data.")
            form = self.form_class()
            return render(self.request, self.template_name, {'form': form, 'question': question})

class ShowQuestionsView(View):
    template_name = 'admin/showquestion.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(ShowQuestionsView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        tests = Test.objects.all()
        cats = Category.objects.all()
        ques = Question.objects.all()
        return render(request, self.template_name, {'ques': ques, 'cats':cats, 'tests':tests})

class DeleteQuestionView(View):
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(DeleteQuestionView, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        Question.objects.filter(pk=pk).delete()
        return redirect('control_operation')

class AddCategoryView(View):
    form_class = forms.CategoryForm
    template_name = 'admin/addcategory.html'

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(AddCategoryView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if (Test.objects.all()).count() == 0 or (Test.objects.latest('test_name')).test_name == '':
            return redirect('Test_name')
        else:
            tests = Test.objects.all()
            cats = Category.objects.all()
            form = self.form_class()
            return render(request, self.template_name, {'form': form, 'cats': cats, 'tests':tests})

    def post(self, request, *args, **kwargs):
        (dict(request.POST))['category'][0] = ((dict(request.POST))['category'][0]).lower()
        form = self.form_class(request.POST)
        cats = Category.objects.all()
        tests = Test.objects.all()
        if (Category.objects.filter(category=((dict(request.POST))['category'][0]).lower())).count() > 0:
            message = 'ALL READY EXIST'
            return render(request, 'admin/error.html', {'message': message})
        else:
            if form.is_valid():
                Tname = Test.objects.get(test_name=(dict(request.POST)['test_name'])[0])
                Category.objects.create(category=(dict(request.POST)['category'])[0], test=Tname)
                return redirect('control_operation')
            else:
                messages.error(self.request, "Invalid data.")
                form = self.form_class()
                return render(self.request, self.template_name, {'form': form, 'cats': cats, 'tests':tests})

class Editcategory(View):
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(Editcategory, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        img_id = 0
        img_id = request.GET['imgid']
        if img_id:
            name = request.GET['name']
            test = request.GET['test']
            Tname = Test.objects.get(test_name=test)
            Category.objects.filter(pk=img_id).update(category=name, test=Tname)
            return HttpResponse(Tname.test_name)


class DeleteCategoryView(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(DeleteCategoryView, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        Category.objects.filter(pk=pk).delete()
        return redirect('control_operation')


class ShowCandidateListView(View):
    form_class = forms.ChooseTestForm
    template_name = 'admin/candidatelist.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(ShowCandidateListView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        tests = Test.objects.all()
        cands = Candidate.objects.filter(test_name=tests[0])
        return render(request, self.template_name, {'cands': cands, 'form':form, 'test':tests[0]})

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST)
        tests = Test.objects.all()
        if form.is_valid():
            test = form.cleaned_data.get('test_name')
            cands = Candidate.objects.filter(test_name=test)
            return render(request, self.template_name, {'cands': cands, 'form':form, 'test':test})
        else:
            cands = Candidate.objects.filter(test_name=tests[0])
            return render(request, self.template_name, {'cands': cands, 'form':form, 'test':tests[0]})


class ViewResultView(View):
    template_name = 'admin/result.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(ViewResultView, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        l1 = []
        overall_total = 0
        overall_correct = 0
        cand = Candidate.objects.get(pk=pk)
        cats = Category.objects.all()
        selects = SelectedAnswer.objects.filter(email=cand)
        # test = Test.objects.get(on_or_off=True)
        if len(selects) != 0:
            for cat in cats:
                total = 0
                correct = 0
                l = []
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
                    percent = (correct / float(total)) * 100
                l.append(percent)
                l1.extend([l])
            total = 0
            correct = 0
            l = []
            percent = 0.0
            if overall_total == 0:
                percent = 0.0
            else:
                percent = (overall_correct / float(overall_total)) * 100
                l.append("Total")
            l.append(overall_total)
            l.append(overall_correct)
            l.append(percent)
            l1.extend([l])
        return render(request, self.template_name, {'selects': selects, 'cats': cats, 'cand': cand, 'l': l1})

    def post(self, request, pk, *args, **kwargs):
        l1 = []
        data = {}
        overall_total = 0
        overall_correct = 0
        cand = Candidate.objects.get(pk=pk)
        cats = Category.objects.all()
        selects = SelectedAnswer.objects.filter(email=cand)
        # test = Test.objects.get(on_or_off=True)
        if len(selects) != 0:
            for cat in cats:
                total = 0
                correct = 0
                l = []
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
                    percent = (correct / float(total)) * 100
                l.append(percent)
                l1.extend([l])
            total = 0
            correct = 0
            l = []
            percent = 0.0
            if overall_total == 0:
                percent = 0.0
            else:
                percent = (overall_correct / float(overall_total)) * 100
                l.append("Total")
            l.append(overall_total)
            l.append(overall_correct)
            l.append(percent)
            l1.extend([l])
            try:
                os.mkdir(os.path.join('core', 'media'))
            except:
                pass
            data = {'selects': selects, 'cats': cats, 'cand': cand, 'l': l1}
            template = get_template(self.template_name)
            html = template.render(data)
            print(cand.name)
            st1 = str(cand.name) + " - " + str(cand.email) + ".pdf"
            file = open('core/' + 'media/' + st1, "w+b")
            pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file,
                                        encoding='utf-8')
            file.seek(0)
            pdf = file.read()
            file.close()
        return render(self.request, self.template_name, {'selects': selects, 'cats': cats, 'cand': cand, 'l': l1})



class AdminInstructionView(View):
    form_class = forms.InstructionForm
    template_name = 'admin/instruction.html'

    def dispatch(self, request, *args, **kwargs):
        if (Test.objects.all()).count() == 0:
            return redirect('Test_name')

        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(AdminInstructionView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            Tname = Test.objects.get(test_name=(dict(request.POST)['test_name'])[0])
            if (Instruction.objects.filter(test=Tname)).count() > 0:
                message = "Instruction for this test already exits"
                return render(request, 'admin/error.html', {'message': message})
            else:
                Instruction.objects.create(instruction=(dict(request.POST)['instruction'])[0], test=Tname)
                return redirect('admin_auth')
        else:
            messages.error(self.request, "Invalid data.")
            form = self.form_class()
            return render(self.request, self.template_name, {'form': form})

class EditInstructionView(View):
    form_class = forms.InstructionForm
    template_name = 'admin/editinstruction.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(EditInstructionView, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        inst = Instruction.objects.get(pk=pk)
        form = self.form_class()
        (dict(form.__dict__['fields'])['instruction']).initial = inst.instruction
        (dict(form.__dict__['fields'])['test_name']).initial = inst.test
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk, *args, **kwargs):
        question = Instruction.objects.get(pk=pk)
        form = self.form_class(request.POST)
        if form.is_valid():
            Tname = Test.objects.get(test_name=(dict(request.POST)['test_name'])[0])
            if (Instruction.objects.filter(test=Tname)).count() > 0 and question.test.test_name != (dict(request.POST)['test_name'])[0]:
                message = "Instruction for this test already exits"
                return render(request, 'admin/error.html', {'message': message})
            else:
                Instruction.objects.filter(pk=pk).delete()
                Instruction.objects.create(instruction=(dict(request.POST)['instruction'])[0], test=Tname)
                return redirect('control_operation')
        else:
            messages.error(self.request, "Invalid data.")
            form = self.form_class()
            return render(self.request, self.template_name, {'form': form, 'question': question})

class ShowInstructionView(View):
    template_name = 'admin/showInstructions.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(ShowInstructionView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        insts = Instruction.objects.all()
        return render(request, self.template_name, {'insts':insts})

class DeleteInstructionView(View):
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(DeleteInstructionView, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        Instruction.objects.filter(pk=pk).delete()
        return redirect('control_operation')


def error404(request):
    message = 'Error 404 \n Page not found'
    return render(request, 'admin/error.html', {'message':message})


def error400(request):
    message = 'Error 400 \n Bad Request'
    return render(request, 'admin/error.html', {'message':message})


def error403(request):
    message = 'Error 403 \n Permission Denied'
    return render(request, 'admin/error.html', {'message':message})


def error500(request):
    message = 'Error 500 \n Server Error'
    return render(request, 'admin/error.html', {'message':message})