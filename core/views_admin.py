from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from django.views import generic, View
from . import forms
from django.contrib import messages
from django.contrib.auth.models import User
from core.models import Candidate, Instruction, Category, Test, Question, SelectedAnswer, Marks

import json


def CalculateMarks(pk):

    cand = Candidate.objects.get(pk=pk)
    test = Test.objects.get(test_name=cand.test_name)
    cats = Category.objects.filter(test=test)
    selects = SelectedAnswer.objects.filter(email=cand)
    score = 0
    for select in selects:
        if select.question_text.negative:
            if select.selected_choice == select.question_text.correct_choice:
                score += select.question_text.marks
            elif select.selected_choice == None or select.selected_choice <= 0 or select.selected_choice > 4:
                pass
            else:
                score -= select.question_text.negative_marks
        else:
            if select.selected_choice == select.question_text.correct_choice:
                score += select.question_text.marks
    # percentage = (score/total_marks)*100
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

        return render(request, self.template_name, {'form':form})


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

    def post(self, request, *args, **kwargs):
        if request.POST['duration'] == '0':
            message = "Test duration cannot be zero"
            return render(request, 'admin/error.html', {'message': message})
        else:
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save()
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
                response = {'res': test_id}
                return HttpResponse(json.dumps(response), content_type='application/json')


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
        test = Test.objects.get(pk=pk)
        candidate_list = Candidate.objects.filter(test_name=test)
        for candidate in candidate_list:
            Candidate.objects.get(name=candidate.name).delete()
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
            if request.POST['choice1'] != request.POST['choice2'] != request.POST['choice3'] != request.POST['choice4']:
                form.save()
                return redirect('control_operation')
            else:
                message = "Choices cannot be same"
                return render(self.request, self.template_name, {'form': form, 'messages': message})
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
        form = self.form_class(instance=question)
        return render(request, self.template_name, {'form': form, 'que': question})

    def post(self, request, pk, *args, **kwargs):
        question = Question.objects.get(pk=pk)
        form = self.form_class(request.POST, instance=question)
        if form.is_valid():
            if request.POST['choice1'] != request.POST['choice2'] != request.POST['choice3'] != request.POST['choice4']:
                form.save()
                return redirect('Show_Category')
            else:
                message = "Choices cannot be same"
                return render(self.request, self.template_name, {'form': form, 'question': question, 'messages': message})
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
            category_list=[]
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
        ques = Question.objects.filter(category_id=cat.id)
        return render(request, self.template_name, {'ques': ques, 'cat': cat})


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
            return render(request, self.template_name, {'form': form, 'cats': cats, 'tests': tests})

    def post(self, request, *args, **kwargs):
        (dict(request.POST))['category'][0] = ((dict(request.POST))['category'][0]).lower()
        form = self.form_class(request.POST)
        cats = Category.objects.all()
        tests = Test.objects.all()
        if (Category.objects.filter(test=request.POST['test'], category=((dict(request.POST))['category'][0]).lower())).count() > 0:
            message = 'ALL READY EXIST'
            return render(request, 'admin/error.html', {'message': message})
        else:
            if form.is_valid():
                form.save()
                return redirect('Add_Category')
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
            response = {'name':Tname.test_name}
            return HttpResponse(json.dumps(response), content_type='application/json')


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
        if len(tests) != 0:
            cands = Candidate.objects.filter(test_name=tests[0]).order_by("-time")
            # for cand in cands:
            #     try:
            #         Marks.objects.get(test_name=tests[0], candidate=cand)
            #     except:
            #         CalculateMarks(cand.pk)
            return render(request, self.template_name, {'cands': cands, 'form': form, 'test': tests[0]})
        else:
            message = 'No Test Present'
            return render(request, 'admin/error.html', {'message': message})

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            test = form.cleaned_data.get('test_name')
            tests = Test.objects.get(test_name=test)
            cands = Candidate.objects.filter(test_name=test).order_by("-time")
            for cand in cands:
                try:
                    Marks.objects.get(test_name=test, candidate=cand)
                except:
                    CalculateMarks(cand.pk)
            return render(request, self.template_name, {'cands': cands, 'form':form, 'test':test})
        else:
            return redirect('Show_Candidates')


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
            form.save()
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
        form = self.form_class(instance=inst)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk, *args, **kwargs):
        inst = Instruction.objects.get(pk=pk)
        form = self.form_class(request.POST, instance=inst)
        if form.is_valid():
            form.save()
            return redirect('control_operation')
        else:
            return render(self.request, self.template_name, {'form': form})


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


def error404(request, exception):
    message = 'Error 404 \n Page not found'
    return render(request, 'admin/error.html', {'message': message})


def error400(request, exception):
    message = 'Error 400 \n Bad Request'
    return render(request, 'admin/error.html', {'message': message})


def error403(request, exception):
    message = 'Error 403 \n Permission Denied'
    return render(request, 'admin/error.html', {'message': message})


def error500(request):
    message = 'Error 500 \n Server Error'
    return render(request, 'admin/error.html', {'message': message})

