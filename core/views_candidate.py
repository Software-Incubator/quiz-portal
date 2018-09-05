from django.shortcuts import render, redirect, reverse
from django.views import generic
from . import forms
from core.models import Category, Question, Instruction, Test, SelectedAnswer, Candidate, Algorithm, DesignQuestion
import itertools
from django.http import JsonResponse, Http404
import datetime as dt
from django.conf import settings
import requests
from django.contrib import messages
import time

a = []

def make_permutation(n, required_question, can_id):
    global a
    a = [x for x in range(1, n + 1)]
    a = list(itertools.combinations(a, required_question))
    if len(a)>10:
        a = a[0:10]
    return a[can_id%len(a)]


def random_question(n, can_id, ques_id):
    global a
    l = len(a)
    return a[can_id % l][ques_id % n]


class AlgorithmQuestionDisplay(generic.DetailView):
    template_name = 'candidate/algorithm_question.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.has_key("email"):
            return redirect('signup')
        return super(AlgorithmQuestionDisplay, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        email = request.session["email"]
        candidate = Candidate.objects.get(email=email)
        test_name = candidate.test_name
        test = Test.objects.get(test_name=test_name)
        duration = test.duration
        dif_time = (dt.datetime.utcnow() - candidate.time.replace(tzinfo=None)).total_seconds()
        remain_time = duration*60 - round(dif_time)
        context_dict = {"category_name": "algorithm"}
        context_dict["remain_time"] = remain_time
        try:
            total_question = Algorithm.objects.filter(test=test).count()
            if total_question:
                id = kwargs["id"]
                if int(id) not in range(1, total_question + 1):
                    return redirect(reverse('algorithm', kwargs={"id": 1}))
                context_dict["question_list_number"] = [int(x) for x in range(1, total_question+1)]
                context_dict["total_question"] = total_question
                context_dict["question"] = Algorithm.objects.filter(test=test)[id-1]
                context_dict["id"] = id
                context_dict["all_category"] = Category.objects.filter(test=test)

            else:
                message = "NO QUESTIONS IN THIS CATEGORY!"
                return render(request, 'candidate/error.html', {'message':message})

        except Category.DoesNotExist:
            pass
        return render(self.request, self.template_name, context_dict)


def category_name_to_number(all_category, all_category_count):
    category_dict = {}
    counter = 1
    for category in all_category:
        category_dict[category.category] = counter
        counter = counter + 1
    return category_dict


def category_number_to_name(all_category, all_category_count):
    category_dict = {}
    for i in range(1, all_category_count+1):
        category_dict[i] = all_category[i-1].category
    return category_dict


class QuestionByCategory(generic.DetailView):
    template_name = 'candidate/question_by_category.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.has_key("email"):
            return redirect('signup')
        return super(QuestionByCategory, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        print("start time", time.time())
        email = request.session["email"]
        candidate = Candidate.objects.get(email=email)
        name=candidate.name
        candidate_id = candidate.id
        test_name = candidate.test_name
        test = Test.objects.get(test_name=test_name)
        duration = test.duration
        dif_time = (dt.datetime.utcnow() - candidate.time.replace(tzinfo=None)).total_seconds()
        remain_time = duration*60 - round(dif_time)
        all_category = Category.objects.filter(test=test)
        all_category_count = all_category.count()
        category_name = kwargs["category_name"]
        context_dict = {'category_name': category_name,"name":name}
        category_dict_by_number =category_number_to_name(all_category, all_category_count)
        category_dict_by_name = category_name_to_number(all_category, all_category_count)

        try:
            category = Category.objects.get(category=category_name, test=test)
            total_question = Question.objects.filter(category=category).count()
            required_question = category.total_question_display
            if required_question > total_question:
                message = "More than required question select"
                return render(request, 'candidate/error.html', {'message': message})
            last_question = 0
            first_question = 0
            if total_question:
                email = request.session["email"]
                id = kwargs["id"]

                if id not in range(1, required_question + 1):
                    return redirect(reverse('category', kwargs={"category_name": category_name,
                                                                "id": 1 }))
                # if last question of current category
                if required_question==id:
                    last_question = 1
                    next_category = category_dict_by_number[(category_dict_by_name[category_name])%all_category_count + 1]
                    context_dict["next_category"] = next_category

                # if first question of current category
                if id==1:
                    first_question = 1
                    prev_category = category_dict_by_number[(category_dict_by_name[category_name]-2+all_category_count)%all_category_count + 1]

                    context_dict["prev_category"] = prev_category
                    prev_category_obj = Category.objects.get(test=test, category=prev_category)
                    context_dict["prev_category_last_ques"] = Question.objects.filter(category=prev_category_obj).count()

                make_permutation(total_question, required_question)
                which_question = random_question(required_question, int(candidate_id), id)
                question = Question.objects.filter(category=category)[which_question - 1]
                all_algo = Algorithm.objects.filter(test=test)
                algo_count = all_algo.count()
                context_dict["algo_count"] = algo_count
                context_dict["all_algo"] = all_algo
                all_design_ques = DesignQuestion.objects.filter(test=test)
                design_ques_count = all_design_ques.count()
                context_dict["all_design_ques"] = all_design_ques
                context_dict["design_ques_count"] = design_ques_count
                instruction = Instruction.objects.filter(test=test)
                context_dict["last_question"] = last_question
                context_dict["first_question"] = first_question
                context_dict["instruction"] = instruction
                context_dict["which_question"] = which_question
                context_dict["test_name"] = test_name
                context_dict["remain_time"] = remain_time
                context_dict['question'] = question
                context_dict["question_id"] = question.id
                context_dict['category'] = category
                context_dict["id"] = id
                context_dict["all_category"] = Category.objects.filter(test=test)
                status_dict = {}
                for i in range(1, required_question+1):
                    now_question = random_question(required_question, int(candidate_id), i)
                    per_question = Question.objects.filter(category=category)[now_question - 1]
                    try:
                        obj = SelectedAnswer.objects.get(email=candidate, question_text=per_question,)
                        status_dict[i] = obj.status

                    except:
                        obj = SelectedAnswer.objects.create(email=candidate, question_text=per_question, selected_choice=-1)
                        status_dict[i] = 1
                context_dict["status_dict"] = status_dict
            else:
                message = "NO QUESTIONS IN THIS CATEGORY!"
                return render(request, 'candidate/error.html', {'message':message})

            """
            status=1 (not attempted)
            status=2 (preview)
            status=3 (save)
            """
        except Category.DoesNotExist:
            pass
        print("end time", time.time())
        return render(self.request, self.template_name, context_dict)


class InstructionView(generic.ListView):
    """
    Instruction view
    """
    template_name = 'candidate/instructions.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.has_key("email"):
            return redirect('signup')
        return super(InstructionView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        email = request.session["email"]
        candidate = Candidate.objects.get(email=email)
        name=candidate.name
        test_name = candidate.test_name
        test = Test.objects.get(test_name=test_name)
        instruction = Instruction.objects.filter(test=test)

        try:
            category = Category.objects.filter(test=test)[0]
        except:
            message = "NO CATEGORY AVAILABLE RIGHT NOW!"
            return render(request, 'candidate/error.html', {'message': message})

        return render(request, self.template_name, {'instruction': instruction,
                                                    'category': category,
                                                    'test_name':test_name,
                                                    "name":name})


class CandidateRegistration(generic.ListView):
    """
    Candidate registration view
    """
    form_class = forms.CandidateRegistration
    template_name ='candidate/signup.html'

    def dispatch(self, request, *args, **kwargs):
        if request.session.has_key("email"):
            return redirect('instruction')
        return super(CandidateRegistration, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request,*args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            test_name = form.cleaned_data.get('test_name')
            candidate = Candidate.objects.get(name=name, email=email)
            if candidate:
                self.request.session['email'] = email
                try:
                    test = Test.objects.get(test_name=test_name)
                    time = test.duration
                    self.request.session.set_expiry(time*60)
                    #  question order for all category in session

                    question_seq = {}
                    categories = Category.objects.filter(test=test_name)
                    for category in categories:
                        total_question = Question.objects.filter(category=category).count()
                        required_question = category.total_question_display
                        question_seq[category.category] = make_permutation(total_question, required_question, candidate.id)
                    self.request.session['question_seq'] = question_seq
                    print("-->", question_seq)
                    print(request.session["question_seq"])
                except:
                    self.request.session.set_expiry(1)
                return redirect('instruction')
        return render(self.request, self.template_name, {'form': form})


class UserAnswerView(generic.ListView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            if not request.session.has_key("email"):
                data = {
                    "url": reverse('ending'),
                    "candidate_answer": -2
                }
                return JsonResponse(data)
            email = request.session["email"]
            candidate = Candidate.objects.get(email=email)
            option_number = request.GET["option_number"]
            question_id = request.GET["question_id"]
            email = request.session["email"]
            candidate = Candidate.objects.get(email=email)
            test_name = candidate.test_name
            test = Test.objects.get(test_name=test_name)
            question = Question.objects.get(id=int(question_id))
            try:
                object = SelectedAnswer.objects.get(email=candidate,
                                                    question_text=question
                                                    )
                object.selected_choice = int(option_number)
                object.save()
                print(option_number, "on")
            except:
                object = SelectedAnswer.objects.create(email=candidate,
                                                    question_text=question,
                                                    selected_choice=int(option_number)
                                                       )
            data = {
                "candidate_answer": object.selected_choice
            }
            return JsonResponse(data)
        else:
            raise Http404


class DefaultOption(generic.ListView):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            email = request.session["email"]
            candidate = Candidate.objects.get(email=email)

            question_id = request.GET["question_id"]
            question = Question.objects.get(id=int(question_id))
            candidate_answer = -1
            try:
                object = SelectedAnswer.objects.get(email=candidate,
                                                    question_text=question
                                                    )
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
            email = request.session["email"]
            candidate = Candidate.objects.get(email=email)
            question_id = request.GET["question_id"]
            status = int(request.GET["status"])
            question = Question.objects.get(id=int(question_id))

            try:
                object = SelectedAnswer.objects.get(email=candidate,
                                                    question_text=question
                                                    )
                if object.selected_choice==-1 and status == 3:
                    pass
                else:
                    object.status = status
                    object.save()
            except:
                if status == 2:
                    object = SelectedAnswer.objects.create(email=candidate,
                                                        question_text=question,
                                                        status=2,
                                                        selected_choice=-1
                                                           )
                    if object:
                        print(object)
                else:
                    pass

            data = {
                "status": status
            }
            return JsonResponse(data)
        else:
            raise Http404


def logout(request):
    try:
        del request.session['email']
    except:
        pass
    return render(request,'candidate/end.html')
