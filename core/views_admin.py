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
from core.models import Candidate, Instruction, Category, Test, Question, SelectedAnswer, Algorithm, Marks
import json
import itertools
import os
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
import datetime
from django.template.loader import render_to_string
from django.template import loader
import pdfkit
from io import BytesIO
import xhtml2pdf.pisa as pisa


def CalculateMarks(pk):

    cand = Candidate.objects.get(pk=pk)
    test = Test.objects.get(test_name=cand.test_name)
    cats = Category.objects.filter(test=test)
    selects = SelectedAnswer.objects.filter(email=cand)
    score = 0
    for select in selects:
        if select.question_text.negative == 1:
            if select.selected_choice == select.question_text.correct_choice:
                score += select.question_text.marks
            elif select.selected_choice == None or select.selected_choice <= 0 or select.selected_choice > 4:
                pass
            else:
                score -= select.question_text.negative_marks
        else:
            if select.selected_choice == select.question_text.correct_choice:
                score += select.question_text.marks
    Marks.objects.create(test_name=test, candidate=cand, marks=score)
    return 1



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
        return render(request, self.template_name, {'form': form})

    def post(self,request, *args, **kwargs):
        if request.POST['duration'] == '0':
            message = "Test duration cannot be zero"
            return render(request, 'admin/error.html', {'message': message})
        else:
            form = self.form_class(request.POST)
            if form.is_valid():
                Test.objects.create(test_name=request.POST['test_name'],
                                    duration=request.POST['duration'],
                                    on_or_off=request.POST['on_or_off'])
                return redirect('control_operation')
            else:
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
        test_id = 0
        test_id = request.GET['imgid']
        if test_id:
            dur = request.GET['dur']
            test = request.GET['test']
            if int(dur) < 1:
                message = "Duration cannot be 0 or less"
                return render(request, 'admin/error.html', {'message': message})
            else:
                Test.objects.filter(pk=test_id).update(duration=dur, test_name=test)
                return HttpResponse(img_id)


class ToggleTestStatus(View):
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(ToggleTestStatus, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        if pk:
            test = Test.objects.get(pk=pk)
            if test.on_or_off:
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
        return redirect('See_Test')


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
            category = Category.objects.get(category=(dict(request.POST)['category'])[0])
            if (dict(request.POST)['choice1'])[0] != (dict(request.POST)['choice2'])[0] != (dict(request.POST)['choice3'])[0] != (dict(request.POST)['choice4'])[0]:
                Question.objects.create(category=category,
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
        (dict(form.__dict__['fields'])['category']).initial = question.category.category
        (dict(form.__dict__['fields'])['category']).show_hidden_initial = True
        (dict(form.__dict__['fields'])['choice1']).initial = question.choice1
        (dict(form.__dict__['fields'])['choice2']).initial = question.choice2
        (dict(form.__dict__['fields'])['choice3']).initial = question.choice3
        (dict(form.__dict__['fields'])['choice4']).initial = question.choice4
        (dict(form.__dict__['fields'])['correct_choice']).initial = question.correct_choice
        return render(request, self.template_name, {'form': form, 'que':question})

    def post(self, request, pk, *args, **kwargs):
        question = Question.objects.get(pk=pk)
        form = self.form_class(request.POST)
        if form.is_valid():
            if (dict(request.POST)['choice1'])[0] != (dict(request.POST)['choice2'])[0] != (dict(request.POST)['choice3'])[0] != (dict(request.POST)['choice4'])[0]:
                c = Category.objects.get(category = (dict(request.POST)['category'])[0])
                Question.objects.filter(pk=pk).update(category = c,
                    question_text = (dict(request.POST)['question_text'])[0], choice1 = (dict(request.POST)['choice1'])[0],
                    choice2 = (dict(request.POST)['choice2'])[0], choice3 = (dict(request.POST)['choice3'])[0],
                    choice4 = (dict(request.POST)['choice4'])[0], correct_choice = (dict(request.POST)['correct_choice'])[0] )
                return redirect('Show_Category')
            else:
                message = "Choices cannot be same"
                return render(request, 'admin/error.html', {'message': message})
        else:
            return render(self.request, self.template_name, {'form': form, 'question': question})


class ShowCategoryView(View):
    template_name = 'admin/showcategory.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(ShowCategoryView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        test_list_with_category = []
        tests = Test.objects.all()
        for test in tests:
            category_list = []
            category_list.append(test)
            cats = Category.objects.filter(test=test)
            category_list.append(cats)
            test_list_with_category.extend([category_list])
        return render(request, self.template_name, {'test_list': test_list_with_category})

class ShowQuestionsView(View):
    template_name = 'admin/showquestions.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(ShowQuestionsView, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        cat = Category.objects.get(pk=pk)
        ques = Question.objects.filter(category=cat)
        return render(request, self.template_name, {'ques':ques, 'cat':cat})


class DeleteQuestionView(View):
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(DeleteQuestionView, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        Question.objects.filter(pk=pk).delete()
        return redirect('Show_Category')

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
                c = Category.objects.create(category=(dict(request.POST)['category'])[0], test=Tname, 
                                        total_question_display = (dict(request.POST)['number_of_questions'])[0])
                return redirect('control_operation')
            else:
                return render(self.request, self.template_name, {'form': form, 'cats': cats, 'tests':tests})


class Editcategory(View):
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(Editcategory, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        category_id = 0
        category_id = request.GET['imgid']
        if category_id:
            name = request.GET['name']
            test = request.GET['test']
            num = request.GET['num']
            Tname = Test.objects.get(test_name=test)
            Category.objects.filter(pk=category_id).update(category=name, test=Tname, total_question_display=int(num))
            return HttpResponse(Tname.test_name)


class DeleteCategoryView(View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(DeleteCategoryView, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        Category.objects.filter(pk=pk).delete()
        return redirect('Add_Category')


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
        cands = Candidate.objects.filter(test_name=tests[0]).order_by("-time")
        if tests[0].negative == 1:
            for cand in cands:
                try:
                    Marks.objects.get(test_name=tests[0], candidate=cand)
                except:
                    CalculateMarks(cand.pk)
        return render(request, self.template_name, {'cands': cands, 'form':form, 'test':tests[0]})

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST)
        tests = Test.objects.all()
        if form.is_valid():
            test = form.cleaned_data.get('test_name')
            cands = Candidate.objects.filter(test_name=test).order_by("-time")
            if tests[0].negative == 1:
                for cand in cands:
                    try:
                        Marks.objects.get(test_name=test, candidate=cand)
                    except:
                        CalculateMarks(cand.pk)
            return render(request, self.template_name, {'cands': cands, 'form':form, 'test':test})
        else:
            cands = Candidate.objects.filter(test_name=tests[0]).order_by("-time")
            return render(request, self.template_name, {'cands': cands, 'form':form, 'test':tests[0]})

class DeleteResultView(View):
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(DeleteResultView, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        Candidate.objects.filter(pk=pk).delete()
        return redirect('Show_Candidates')

class ViewResultView(View):
    template_name = 'admin/result.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(ViewResultView, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        categorywise_marks = []
        overall_total = 0
        overall_correct = 0
        cand = Candidate.objects.get(pk=pk)
        test = Test.objects.get(test_name=cand.test_name)
        cats = Category.objects.filter(test=test)
        selects = SelectedAnswer.objects.filter(email=cand) 
        if len(selects) != 0:
            for cat in cats:
                total = 0
                correct = 0
                sub_list_for_marks = []
                sub_list_for_marks.append(cat.category)
                percent = 0.0
                for select in selects:
                    if cat.category == select.question_text.category.category:
                        total = total + 1
                        overall_total = overall_total + 1
                        if select.question_text.correct_choice == select.selected_choice:
                            correct = correct + 1
                            overall_correct = overall_correct + 1
                sub_list_for_marks.append(total)
                sub_list_for_marks.append(correct)
                if total == 0:
                    percent = 0.0
                else:
                    percent = (correct / float(total)) * 100
                sub_list_for_marks.append(percent)
                categorywise_marks.extend([sub_list_for_marks])
            total = 0
            correct = 0
            sub_list_for_marks = []
            percent = 0.0
            if overall_total == 0:
                percent = 0.0
            else:
                percent = (overall_correct / float(overall_total)) * 100
                sub_list_for_marks.append("Total")
            sub_list_for_marks.append(overall_total)
            sub_list_for_marks.append(overall_correct)
            sub_list_for_marks.append(percent)
            categorywise_marks.extend([sub_list_for_marks])
        return render(request, self.template_name, {'selects': selects, 'cats': cats, 'cand': cand, 'categorywise_marks': categorywise_marks})
        

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
            return render(self.request, self.template_name, {'form': form, 'question': question})


class ShowInstructionView(View):
    template_name = 'admin/showInstructions.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(ShowInstructionView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        insts = Instruction.objects.all()
        return render(request, self.template_name, {'insts': insts})


class DeleteInstructionView(View):
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(DeleteInstructionView, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        Instruction.objects.filter(pk=pk).delete()
        return redirect('Show_Instruction')


class AddAlgorithmView(View):
    form_class = forms.AlgorithmForm
    template_name = 'admin/addalgorithm.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(AddAlgorithmView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if Test.objects.all().count() == 0:
            message = "No test present"
            return render(request, 'admin/error.html', {'message': message})
        all_algo = Algorithm.objects.all()
        all_test = Test.objects.all()
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'all_algo': all_algo, 'all_test': all_test})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            test = Test.objects.get(test_name=(dict(request.POST)['test_name'])[0])
            # try:
            #     c = Category.objects.get(category='algorithm', test=test)
            # except:
            #     c = Category.objects.create(test=test, category='algorithm', total_question_display=2)
            Algorithm.objects.create(test=test, question_text=(dict(request.POST)['question_text'])[0])
            return redirect('control_operation')
        else:
            return render(self.request, self.template_name, {'form': form})


class EditAlgorithmView(View):
    form_class = forms.AlgorithmForm
    template_name = 'admin/editalgorithm.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(EditAlgorithmView, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        algo = Algorithm.objects.get(pk=pk)
        form = self.form_class()
        (dict(form.__dict__['fields'])['question_text']).initial = algo.question_text
        (dict(form.__dict__['fields'])['test_name']).initial = algo.test
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            Tname = Test.objects.get(test_name=(dict(request.POST)['test_name'])[0])
            Algorithm.objects.filter(pk=pk).update(test = Tname,
                    question_text = (dict(request.POST)['question_text'])[0])
            return redirect('control_operation')
        else:
            return render(self.request, self.template_name, {'form': form, 'question': question})


class DeleteAlgorithmView(View):
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('admin_auth')
        return super(DeleteAlgorithmView, self).dispatch(request, *args, **kwargs)

    def get(self, request, pk, *args, **kwargs):
        Algorithm.objects.filter(pk=pk).delete()
        return redirect('Add_Algorithm')



def error404(request):
    message = 'Error 404 \n Page not found'
    return render(request, 'admin/error.html', {'message': message})


def error400(request):
    message = 'Error 400 \n Bad Request'
    return render(request, 'admin/error.html', {'message': message})


def error403(request):
    message = 'Error 403 \n Permission Denied'
    return render(request, 'admin/error.html', {'message': message})


def error500(request):
    message = 'Error 500 \n Server Error'
    return render(request, 'admin/error.html', {'message': message})

