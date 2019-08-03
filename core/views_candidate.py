from django.shortcuts import render, redirect, reverse
from django.views import generic
from . import forms
from core.models import Category, Question, Instruction, Test,\
    SelectedAnswer, Candidate, Additional, AdditionalQuestion
import itertools
from django.http import JsonResponse, Http404
import datetime as dt
import random
from core.views_admin import CalculateMarks;
from core.models import Candidate, Instruction, Category, Test, Question, SelectedAnswer, Marks


class QuestionByCategory(generic.DetailView):
    template_name = 'candidate/question_by_category.html'

    def dispatch(self, request, *args, **kwargs):
        if "email" not in request.session or "test_name" not in request.session:
            return redirect('signup')
        # if "test_name" not in request.session:
        #     return redirect('get_test')
        return super(QuestionByCategory, self).dispatch(request, *args, **kwargs)

    def category_name_to_number(self, all_category):
        category_dict = {}
        counter = 1
        for category in all_category:
            category_dict[category.category] = counter
            counter = counter + 1
        return category_dict

    def category_number_to_name(self, all_category):
        category_dict = {}
        all_category_count = all_category.count()
        for i in range(1, all_category_count + 1):
            category_dict[i] = all_category[i - 1].category
        return category_dict

    def get(self, request, *args, **kwargs):
        """
        status=1 (not attempted)
        status=2 (preview)
        status=3 (save)
        """
        email = request.session["email"]
        candidate = Candidate.objects.get(email=email)
        test_name = candidate.test_name
        test = Test.objects.get(test_name=test_name)
        duration = test.duration
        dif_time = (dt.datetime.utcnow() - candidate.time.replace(tzinfo=None)).total_seconds()
        remain_time = duration*60 - round(dif_time) + 30
        all_category = Category.objects.filter(test=test)
        category_name = kwargs["category_name"]
        question_seq = request.session["question_seq"][category_name]
        context_dict = {'category_name': category_name, "candidate_name": candidate.name}
        category_dict_by_number = self.category_number_to_name(all_category)
        category_dict_by_name = self.category_name_to_number(all_category)
        category = Category.objects.get(category=category_name, test=test)
        total_question = Question.objects.filter(category=category).count()
        required_question = category.total_question_display
        last_question = 0
        first_question = 0
        if not total_question:
            message = "NO QUESTIONS IN THIS CATEGORY!"
            return render(request, 'candidate/error.html', {'message': message})

        id = kwargs["id"]
        if id not in range(1, required_question + 1):
            return redirect(reverse('category', kwargs={"category_name": category_name,
                                                            "id": 1}))
        # if last question of current category
        if required_question == id:
            last_question = 1
            next_category = category_dict_by_number[(category_dict_by_name[category_name])%all_category.count() + 1]
            context_dict["next_category"] = next_category

        # if first question of current category
        if id == 1:
            first_question = 1
            prev_category = category_dict_by_number[(category_dict_by_name[category_name]-2+all_category.count())%  all_category.count() + 1]
            context_dict["prev_category"] = prev_category
            prev_category_obj = Category.objects.get(test=test, category=prev_category)
            context_dict["prev_category_last_ques"] = Question.objects.filter(category=prev_category_obj).count()

        which_question = question_seq[id % required_question]
        question = Question.objects.get(pk=which_question)
        additional_objs = Additional.objects.filter(test_name=test, on_or_off=True)
        context_dict["additional_objs"] = additional_objs
        instruction = Instruction.objects.filter(test=test)
        context_dict["last_question"] = last_question
        context_dict["first_question"] = first_question
        context_dict["instruction"] = instruction
        context_dict["which_question"] = which_question
        context_dict["test_name"] = test_name
        context_dict["remain_time"] = remain_time
        context_dict['question'] = question
        context_dict['category'] = category
        context_dict["id"] = id
        context_dict["all_category"] = Category.objects.filter(test=test)
        status_dict = {}
        for i in range(1, required_question+1):
            question_number = question_seq[i%required_question]
            try:
                obj = SelectedAnswer.objects.get(email=candidate, question_text=question_number,)
                status_dict[i] = obj.status
            except:
                obj = SelectedAnswer.objects.create(email=candidate, question_text=question_number, selected_choice=-1)
                status_dict[i] = 1
        context_dict["status_dict"] = status_dict
        return render(self.request, self.template_name, context_dict)


class InstructionView(generic.ListView):
    """
    Instruction view
    """
    template_name = 'candidate/instructions.html'

    def dispatch(self, request, *args, **kwargs):
        if "email" not in request.session or "test_name" not in request.session:
            return redirect('signup')
        candidate = Candidate.objects.filter(email=request.session["email"])
        if not candidate:
            for key in list(request.session.keys()):
                del request.session[key]
            return redirect('signup')
        candidate = Candidate.objects.filter(email=request.session["email"])
        if not candidate:
            for key in list(request.session.keys()):
                del request.session[key]
            return redirect('get_test')
        return super(InstructionView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        email = request.session["email"]
        candidate = Candidate.objects.get(email=email)
        name = candidate.name
        test_name = candidate.test_name
        test = Test.objects.get(test_name=test_name)
        instruction = Instruction.objects.filter(test=test)

        try:
            category = Category.objects.filter(test=test)[0]
        except IndexError:
            message = "NO CATEGORY AVAILABLE RIGHT NOW!"
            return render(request, 'candidate/error.html', {'message': message})

        return render(request, self.template_name, {'instruction': instruction,
                                                    'category': category,
                                                    'test_name': test_name,
                                                    "name": name})


class CandidateRegistration(generic.ListView):
    """
    Candidate registration.js view
    """
    form_class = forms.CandidateRegistration
    template_name = 'candidate/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if "email" in request.session:
            return redirect('instruction')
        # if "test_name" not in request.session:
        #     return redirect('get_test')
        return super(CandidateRegistration, self).dispatch(request, *args, **kwargs)

    def default_result(self, question_seq, candidate):
        selected_answer = []
        for question in question_seq:
            selected_answer.append(SelectedAnswer(email=candidate, question_text=question, selected_choice=-1))
        SelectedAnswer.objects.bulk_create(selected_answer)

    def get(self, request, *args, **kwargs):
        form = self.form_class
        test_name_on = Test.objects.filter(on_or_off=True)[0]
        print(test_name_on.test_name)
        self.request.session['test_name'] = test_name_on.test_name
        test_obj = Test.objects.get(test_name=test_name_on.test_name)
        return render(request, self.template_name, {'form': form, 'test_obj': test_obj})

    def post(self, request,*args, **kwargs):
        form = self.form_class(self.request.POST)
        test_name = self.request.session["test_name"]
        test_obj = Test.objects.get(test_name=test_name)
        if form.is_valid():
            form_obj = form.save(commit=False)
            form_obj.test_name = test_name
            form_obj.save()
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            candidate = Candidate.objects.get(name=name, email=email,)
            if candidate:
                self.request.session['email'] = email
                test = Test.objects.get(test_name=test_name)
                time = test.duration
                self.request.session.set_expiry(time*60)
                #  question order for all category in session

                question_seq = []
                session_seq = {}
                categories = Category.objects.filter(test=test)
                for category in categories:
                    total_question = list(Question.objects.filter(category=category))
                    required_question = category.total_question_display
                    if required_question > len(total_question):
                        message = "More than required question select"
                        return render(request, 'candidate/error.html', {'message': message})
                    random.shuffle(total_question)
                    student_questions = total_question[:required_question]
                    student_questions_pk = [ques.pk for ques in student_questions]
                    question_seq += student_questions
                    session_seq[category.category] = student_questions_pk
                self.request.session['question_seq'] = session_seq
                self.default_result(question_seq, candidate)
                return redirect('instruction')
        return render(request, self.template_name, {'form': form, 'test_obj': test_obj})


class GetTestView(generic.ListView):
    template_name = 'candidate/get_test.html'
    form_class = forms.GetTestNameForm

    def dispatch(self, request, *args, **kwargs):
        if "email" in request.session:
            return redirect('instruction')

        return super(GetTestView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            test_name = form.cleaned_data.get('test_name')
            if 'test_name' in request.session:
                del request.session['test_name']
            self.request.session['test_name'] = test_name
            return redirect('signup')
        return render(self.request, self.template_name, {'form': form})


# class UserAnswerView(generic.ListView):
#
#     def get(self, request, *args, **kwargs):
#         if request.is_ajax():
#             if "email" not in request.session:
#                 data = {
#                     "url": reverse('ending'),
#                     "candidate_answer": -2
#                 }
#                 return JsonResponse(data)
#             email = request.session["email"]
#             candidate = Candidate.objects.get(email=email)
#             option_number = request.GET["option_number"]
#             question_id = request.GET["question_id"]
#             test_name = candidate.test_name
#             question = Question.objects.get(id=int(question_id))
#             try:
#                 object = SelectedAnswer.objects.get(email=candidate, question_text=question)
#                 object.selected_choice = int(option_number)
#                 object.save()
#             except:
#                 object = SelectedAnswer.objects.create(email=candidate,
#                                                     question_text=question,
#                                                     selected_choice=int(option_number)
#                                                        )
#             data = {
#                 "candidate_answer": object.selected_choice
#             }
#             return JsonResponse(data)
#         else:
#             raise Http404


class DefaultOption(generic.ListView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            email = request.session["email"]
            candidate = Candidate.objects.get(email=email)
            question_id = request.GET["question_id"]
            question = Question.objects.get(id=int(question_id))
            candidate_answer = -1
            try:
                object = SelectedAnswer.objects.get(email=candidate, question_text=question)
                candidate_answer = object.selected_choice
            except:
                pass
            data = {
                "candidate_answer": candidate_answer
            }
            return JsonResponse(data)
        else:
            raise Http404


class SaveStatus(generic.ListView):

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            if "email" not in request.session:
                data = {
                    "url": reverse('ending'),
                    "candidate_answer": -2
                }
                return JsonResponse(data)
            email = request.session["email"]
            candidate = Candidate.objects.get(email=email)
            question_id = request.GET["question_id"]
            status = int(request.GET["status"])
            option_number = request.GET["option_number"]
            question = Question.objects.get(id=int(question_id))
            if status != 1:
                try:
                    object = SelectedAnswer.objects.get(email=candidate,
                                                    question_text=question
                                                    )
                # if object.selected_choice == -1 and status == 3:
                #     pass
                # else:
                    object.status = status
                    object.selected_choice = int(option_number)
                    object.save()

                except:
                    object = SelectedAnswer.objects.create(email=candidate,
                                                        question_text=question,
                                                        status=status,
                                                        selected_choice=int(option_number)
                                                           )

            data = {
                "status": status,
                "candidate_answer": object.selected_choice
            }
            return JsonResponse(data)
        else:
            raise Http404


def logout(request):
    tests = Test.objects.all()
    if len(tests) != 0:
        cands = Candidate.objects.filter(test_name=tests[0]).order_by("-time")
        for cand in cands:
            try:
                Marks.objects.get(test_name=tests[0], candidate=cand)
            except:
                CalculateMarks(cand.pk)
    for key in list(request.session.keys()):
        del request.session[key]
    return render(request, 'candidate/end.html')
