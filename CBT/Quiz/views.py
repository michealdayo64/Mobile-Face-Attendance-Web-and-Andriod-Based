from django.shortcuts import render
from .models import Aquiz
from questions.models import Questions, Answer
from results.models import Result
from django.http import JsonResponse
# Create your views here.

def quizListView(request):
    quiz_data = Aquiz.objects.all()
    return render(request, 'quizes/main.html', {'quiz_data': quiz_data})

def quizDetailView(request, pk):
    quiz = Aquiz.objects.get(pk = pk)
    return render(request, 'quizes/quiz.html', {'quiz': quiz})

def quiz_data_view(request, pk):
    quiz = Aquiz.objects.get(pk = pk)
    questions = []
    
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        questions.append({str(q): answers})
    print(questions)
    return JsonResponse({
        'data': questions,
        'time': quiz.time
    })

def save_quiz_view(request, pk):
    #print(request.POST)
    if request.is_ajax():
        data = request.POST
        data_ = dict(data.lists())
        #print(data_)
        questions = []
        data_.pop('csrfmiddlewaretoken')
        #print(data_)
        #print(type(data))
        for k in data_.keys():
            print('key: ', k)
            question = Questions.objects.get(text = k)
            questions.append(question)
        print(questions)

        user = request.user
        quiz = Aquiz.objects.get(pk = pk)

        score = 0
        multiplier = 100 / quiz.number_of_quesstions
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)
            print(a_selected)
            if a_selected != "":
                question_answers = Answer.objects.filter(question = q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text
                results.append({str(q): {'correct_answer': correct_answer, 'answered': a_selected}})
            else:
                results.append({str(q): 'Not answered'})
        score_ = score * multiplier
        Result.objects.create(quiz = quiz, user = user, score = score_)
        if score_ >= quiz.required_score_to_pass:
            return JsonResponse({"Passed": True, "score": score_, "results": results})
        else:    
            return JsonResponse({
        'passed': False, 
        "score": score_, 
        "results": results
    })

    