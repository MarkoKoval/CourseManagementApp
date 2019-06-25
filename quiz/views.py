from django.shortcuts import render
from django.http import JsonResponse
from .models import Quiz,Question,VariantResult,User,PassedQuiz,QuestionAnswerResult,Course,Lesson
# Create your views here.
from .quizes_data import *
import os
import ast
import json
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Document
from .forms import DocumentForm
from django.db.models import Q
from django.http.response import JsonResponse

def enter(request):

    print("hello")
    print(request.session.get("semail"))
    return render(request, "login.html", {"user": str(request.session.get("semail"))})


def load_quiz(request):
    print(request.POST)
    print(request.session.get("num"))
    return render(request, "quiz.html")


def enter_quiz_app(request):

    if request.method == "GET" and len(request.GET) == 3:
        user = User.objects.get(name = request.GET["user_name"])
        user.user_email = request.GET["user_email"]
        user.save()
        return JsonResponse({"email": user.user_email})
    print("dddd")
    print(request.POST)
    user = None
    created = None
    try:
        '''     user_email = request.POST["email"], '''
        user,created = User.objects.get_or_create(name=request.POST["nickname"],password=request.POST["password"],
                                             user_status = request.POST["status"])
    except Exception as E:
         print(E)
         return HttpResponseRedirect(reverse('enter'))
    print("ggg")

    print(created)
    print(user)
    if created:
        return render(request, "quiz.html", {"user": user})
    else:
        if user != None:
            if user.password == request.POST["password"]:
                print("zbs")
                return render(request, "quiz.html",  {"user":user})
            else:
                print("not zbs")

                temp = ["hihi"]
               # return render(request, "login.html")
                request.session['semail'] =[ 'hrthrthrtirfan.sssit@gmail.com']
                return HttpResponseRedirect(reverse('enter'))

        else:

            request.session['semail'] = ['irfan.sssit@gmail.comhthrthrthr']
            return HttpResponseRedirect(reverse('enter'))

            #return render(request, "login.html",  {"user":user})


def load_quiz_info(request):
    print(request.POST["quiz_name"])

    response = Data.get(request.POST["quiz_name"])
    print(response)
    return JsonResponse(response,safe=False)


def create_quiz(request):
    Quiz.objects.all().delete()
    Question.objects.all().delete()
    VariantResult.objects.all().delete()
    Data = {"beginner": [{
        'question': "•	Переживаєте за успіх в роботі?",
        'choices': ["сильно", "не дуже", "спокійний"],
        'correctAnswer': [5, 3, 2]
    },
        {
            'question': "•	Прагнете досягти швидко результату?",
            'choices': ["поступово", "якомога швидше", "дуже"],
            'correctAnswer': [2, 3, 5]
        },

        {
            'question': "•	Легко попадаєте в тупик при проблемах в роботі?",
            'choices': ["неодмінно", "поступово", "зрідка"],
            'correctAnswer': [5, 3, 2]
        },

        {
            'question': "•	Чи   потрібен чіткий алгоритм для вирішення задач?",
            'choices': ["так", "в окремих випадках", "не потрібен"],
            'correctAnswer': [5, 3, 2]
        },
    ]}
    try:
        quiz = Quiz(title="First Quiz")
        quiz.save()
        for item in Data["beginner"]:
            print(item["question"])
            question = Question(title=item["question"])
            question.save()
            for choice, score in zip(item["choices"], item["correctAnswer"]):
                print(choice+" " + str(score))
                vr = VariantResult(choice=choice, score=score)
                vr.save()
                question.variant_result_pair.add(vr)

            quiz.questions.add(question)
            quiz.save()
    except Exception as exp:
        print(exp)
    return render(request, "test.html", {"quizes": Quiz.objects.all()})


def load_test_pass_info(request):

    result = ast.literal_eval(request.POST["data"])
    quiz_name = result[0]
    print(quiz_name)
    user_name = result[1]
    print(user_name)
    questions = []

    exist_quiz_previously = True
    try:
        item = User.objects.get(name=user_name).passed_quizes.get(quiz_name=quiz_name)#.passed_quizes.all().get(quiz_name=quiz_name)
    except Exception as ex:
        print(ex)
        exist_quiz_previously = False
    print(exist_quiz_previously)
    for i in result[2:]:
        val = ast.literal_eval(i)
        questions.append(val)
        print(val)
    try:

        quiz =  User.objects.get(name=user_name).passed_quizes.get(quiz_name=quiz_name) if exist_quiz_previously else PassedQuiz(quiz_name=quiz_name)
        if not exist_quiz_previously:
            quiz.save()
        else:
            User.objects.get(name=user_name).passed_quizes.get(quiz_name=quiz_name).question_answer_result_pair.all().delete()
        #print("quiz")

        for item in questions:
            obj = QuestionAnswerResult(question=item["question"],answer=item["choices"],result=item["correctAnswer"])
            obj.save()
            #print("question")
            #print(dir(quiz))

            quiz.question_answer_result_pair.add(obj)
            quiz.save()
            #print("questionsss")

        User.objects.get(name=user_name).passed_quizes.add(quiz)
       # print("eerr")
    except Exception as ex:
        print(ex)
    return  render(request, "quiz.html")


def clear(request):
     print("hhhh")
     print(User.objects.all().count())
     Document.objects.all().delete()
     Lesson.objects.all().delete()
     Course.objects.all().delete()
     User.objects.all().delete()

    # PassedQuiz.objects.all().delete()
    # QuestionAnswerResult.objects.all().delete()

     return render(request, "quiz.html")


def statistic(request, username):
    obj = User.objects.get(name=username)
    print(obj.name)
    print(obj.password)

    js = dict()
    for quiz_ in obj.passed_quizes.all():
        print(quiz_.quiz_name)
        js[quiz_.quiz_name] = []
        for que in quiz_.question_answer_result_pair.all():
            js[quiz_.quiz_name].append({"question":que.question,
                                         "answer":que.answer,
                                        "result":que.result})
            print(que.question + " " + que.answer + " " + str(que.result))
    js = json.dumps(js)
    return render(request, "statistic.html", {"user":obj, "js":js})

def list(request):
    # Handle file upload
    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)
        form = DocumentForm(request.POST, request.FILES)
        print(1)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()
            print(2)
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('list'))
    else:
        form = DocumentForm() # A empty, unbound form
        print(3)
    print(4)
    #Document.objects.all().delete()

    # Load documents for the list page
    documents = Document.objects.all()


    # Render list page with the documents and the form
    return render(request, 'list.html', {'documents': documents, 'form': form})

""" it2 = User.objects.get(name=username).course_subscriptions
    it3 = None
    if it.count() != 0 and it2.count() != 0:
        it3 =   it.difference(it2)
    elif it.count() != 0 and it2.count() == 0:
        it3 = it
    elif it.count() == 0 and it2.count() != 0:
        it3 = it2"""
def get_possible_course_subscriptions(request,username):
    it = Course.objects.filter(~Q(course_creator__name = username))
    it2 = User.objects.get(name=username).course_subscriptions.all()
    it3 = Course.objects.none()
    print(type(it))
    print(type(it2))
    print(it.count())
    print(it2.count())
    if it.count() != 0 and it2.count() != 0:
        print(1)
        it3 = it.difference(it2)
    elif it.count() != 0:
        print(2)
        it3 = it
    elif it2.count() != 0:
        print(3)
        it3 = it2

    return render(request, "possible-course-subsciptions.html",{"courses":it3.all(), "username":username})

def get_my_course_subscriptions(request,username):
    it = User.objects.get(name=username).course_subscriptions

    return  render(request, "my-course-subsciptions.html",{"course_subsciptions":it.all(), "username":username})

def create_course_subscription(request,username,coursename):
    print(username +" "+coursename)
    User.objects.get(name=username).course_subscriptions.add(Course.objects.get(name = coursename))

    return redirect('/possible-course-subscriptions/'+username) #render(request, "possible-course-subsciptions.html",{})

def delete_course_subscription(request,coursename, username):
    print(Course.objects.all().count())
    rem = User.objects.get(name=username).course_subscriptions.get(name = coursename)
    User.objects.get(name=username).course_subscriptions.remove(rem)
    print(Course.objects.all().count())
    #it = User.objects.get(name=username).course_subscriptions
    return redirect('/course-subscriptions/'+username) # render(request, "my-course-subsciptions.html",{"course_subsciptions":it.all(), "username":username})

def get_my_created_courses(request,username):

    if request.method == 'GET' and len(request.GET) == 1:
        print(username)
        course = Course.objects.filter(course_creator__name= username).all()
        print(username)
        save = []
        for i in course:
            save.append({"name":i.name,"description":i.description,
                         "author":username,
                         "course_id":i.id,
                         "date": i.created_on.strftime("%Y-%m-%d %H:%M:%S")
                         })
        return JsonResponse({'courses': save})
    if request.method == 'GET' and len(request.GET) == 2:

        course = Course.objects.get(name = request.GET["course_name"])
        course.delete()
        course = Course.objects.filter(course_creator__name= username).all()

        print(username)
        save = []
        for i in course:
            save.append({"name":i.name,"description":i.description,
                         "author":username,
                         "course_id":i.id,
                         "date":i.created_on.strftime("%Y-%m-%d %H:%M:%S")
                         })
        return JsonResponse({'courses': save})
    print("get_my_created_courses")
    i = Course.objects.filter(course_creator__name = username)

    """,{"my_courses":Course.objects.get(name=username)}"""
    return render(request, "my-created-courses.html", {"my_courses":i})

def create_course(request,username):
    if request.POST:
        print(request.POST)
        s = request.POST["course_name"]
        description = request.POST["description"]
        print(s)
        print(request.POST)
        try:
            course, created  =  Course.objects.get_or_create(name = s, course_creator = User.objects.get(name=username), description = description)
        except Exception as e:
            return render(request, "create-course.html", {"user": username,
                                                          "created": True})
        course.save()
        print(Course.objects.all().count())

        return  redirect('/created-courses/'+username)

    return render(request, "create-course.html",{"user":username,
                                                 "created": False})

def delete_course(request,id):
    return   HttpResponseRedirect(reverse("get_my_created_courses", args=("markor",))) #get_my_created_courses(request,"markor")

def update_course(request,id):
    return render(request, "my-created-courses.html",{})

def edit_course_content(request,coursename):
    print("haha")
    print(request.GET.get('title'))
    for i in request.GET:
        print(i +" "+request.GET[i])
    print(len(request.GET))
    print(coursename)
    if len(request.GET) == 2:
        course = Course.objects.get(name=coursename)
        lessons = Lesson.objects.filter(course=course)
        print(len(lessons))
        save = []
        for i in lessons.all():
            save.append(
                {
                    "title": i.name,
                    "description": i.description
                }
            )
            print(i.name + " " + i.description)
        print(save)
        return JsonResponse({'lessons': save})

    if len(request.GET) == 3:#
        course = Course.objects.get(name = coursename)
        lesson, created = Lesson.objects.get_or_create(name = request.GET['title'],
                                                    description=request.GET['description'],
                                                       course = course)
        print(request)
        lessons = Lesson.objects.filter(course = course)
        print(len(lessons))
        save = []
        for i in lessons.all():
            save.append(
                {
                    "title": i.name,
                    "description": i.description
                }
            )
            print(i.name +" "+i.description)
        print(save)
        return JsonResponse({'lessons':save})
    if len(request.GET) == 4:#
        course = Course.objects.get(name=coursename)
        instance = Lesson.objects.get(name = request.GET['title'],course = course)
        instance.delete()
        lessons = Lesson.objects.filter(course=course)
        print(len(lessons))
        save = []
        for i in lessons.all():
            save.append(
                {
                    "title": i.name,
                    "description": i.description
                }
            )
            print(i.name + " " + i.description)
        print(save)
        return JsonResponse({'lessons': save})
    if len(request.GET) == 5:
        course = Course.objects.get(name=coursename)

        obj = Lesson.objects.get(course=course,name = request.GET["title"])
        obj.name = request.GET["new_title"]
        obj.description = request.GET["new_description"]
        obj.save()
        lessons = Lesson.objects.filter(course=course)
        print(len(lessons))
        save =[]
        for i in lessons.all():
            save.append(
                {
                    "title": i.name,
                    "description": i.description
                }
            )
            print(i.name + " " + i.description)
        print(save)
        return JsonResponse({'lessons': save})

    print("haha")
    print("ffwe")
    item = Course.objects.get(name = coursename)
    return render(request, "edit-created-courses-content.html", {"course":item})

def edit_lesson_content(request,coursename,lessonname,username):
    name = username

    if request.method == 'POST':

        print(request.POST)
        print(request.FILES)
        form = DocumentForm(request.POST, request.FILES)
        print(1)
        if form.is_valid():
            print(request.FILES['docfile'])
            course = Course.objects.get(name = coursename)
            lesson = Lesson.objects.get(name = lessonname,course = course)
            newdoc = Document(docfile = request.FILES['docfile'],belong_to_lesson=lesson )
            newdoc.save()
            print(2)

            course = Course.objects.get(name=coursename)
            lesson = Lesson.objects.get(name=lessonname, course=course)
            documents = Document.objects.filter(belong_to_lesson=lesson)

            save = []
            for doc in documents:
                save.append({"url": doc.docfile.url,
                             "name": doc.docfile.name})
            return JsonResponse({'documents': save})
            # Redirect to the document list after POST
           # return HttpResponseRedirect(reverse('tyy'))
    elif username[len(username)-1] == '_':
        name = username[:-1]
        print(2)
        form = DocumentForm()
        return HttpResponseRedirect(reverse("tyy", args=(coursename, lessonname, name,)))
    else:

        form = DocumentForm() # A empty, unbound form
        print(3)
    print(4)

    if request.method == 'GET' and len(request.GET) == 3:
       # documents = Document.objects.all()
        course = Course.objects.get(name=coursename)
        print("course")
        lesson = Lesson.objects.get(name=lessonname, course=course)
        print("lesson")
        documents = Document.objects.filter(belong_to_lesson=lesson).all()
        save = []
        for doc in documents:
            save.append({ "url":  doc.docfile.url,
                    "name": doc.docfile.name })
        return JsonResponse({'documents': save})

    if request.method == 'GET' and len(request.GET) == 4:

        course = Course.objects.get(name = coursename)
        lesson = Lesson.objects.get(name = lessonname, course=course)
        print(request.GET['url'] +"  "+request.GET['name'] )

        document = Document.objects.filter( belong_to_lesson=lesson,docfile =request.GET['name']).all()
        print("ffe")
        print(len(document))
        for i in document:
            print(i.docfile.name + " "+i.docfile.url)
            print(i.docfile)
        document = Document.objects.get(docfile =request.GET['name'],belong_to_lesson = lesson)
        document.delete()

        documents = Document.objects.filter(belong_to_lesson = lesson)
        save = []
        for doc in documents:
            save.append({ "url":  doc.docfile.url,
                    "name": doc.docfile.name })
        return JsonResponse({'documents': save})
    #Document.objects.all().delete()

    # Load documents for the list page
    course = Course.objects.get(name = coursename)
    print("course")
    lesson = Lesson.objects.get(name = lessonname, course = course)
    print("lesson")
    documents = Document.objects.filter(belong_to_lesson = lesson).all()
    print("documents")
    print(len(documents))
    docum = Document.objects.all()
    print(len(docum))
    # Render list page with the documents and the form
    #return render(request, 'list.html', {'documents': documents, 'form': form})

    print(name)
    return render(request, "edit-lesson-content.html", {"coursename": coursename,
                                                                 "lessonname":lessonname,
                                                                 "username":name,
                                                        'documents': documents, 'form': form })

def delete_lesson_content(request,coursename,lessonname,username,media,doc,year,day,month,name):
    print("haha")
    return HttpResponseRedirect(reverse("tyy",args=(coursename,lessonname,username,))) #redirect('update/course-content-of/'+coursename+'/lesson/'+lessonname+'/created-by/'+username)

def show_course_lessons(request,coursename):
    course = Course.objects.get(name = coursename)
    lessons = Lesson.objects.filter(course = course ).all()
    return render(request,"show_course_lessons.html",{"lessons": lessons, "coursename":coursename})

def show_lesson_files_(request,coursename,lessonname):
    course = Course.objects.get(name=coursename)
    lessons = Lesson.objects.filter(course=course).all()
    files = []
    for it in lessons:
        docs = Document.objects.filter(belong_to_lesson=it ).all()
        for doc in docs:
            files.append({
                "url":doc.docfile.url,
                "name":doc.docfile.name
            })
    print(files)
    return  render(request, "show_lesson_files_.html",{"files":files})

def create_course_tests_for_lesson(request,coursename, lessonname):
    return render(request, "create_tests_for_lesson.html", {"coursename": coursename,
                                                       "lessonname":  lessonname})

def pass_test(request,coursename,lessonname):
    return render(request, "pass_test.html", {})