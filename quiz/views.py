from django.shortcuts import render
from django.http import JsonResponse
from .models import Messages,Chat,SearchTags,User,Course,Lesson,TestQuiz,TestQuestion,PassedTestQuiz,TestQuestionVariantResult,QuestionAnswerResult
# Create your views here.
"""Quiz,Question,VariantResult,PassedQuiz,QuestionAnswerResult,"""
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
import json
from .send_mail import send_email_for_course_subscription

def enter(request):

    print("hello")
   # print(request.session.get("semail"))
    return render(request, "login.html", {"user": str(request.session.get("semail"))})


def load_quiz(request):
    print(request.POST)
   # print(request.session.get("num"))
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
              #  request.session['semail'] =[ 'hrthrthrtirfan.sssit@gmail.com']
                return HttpResponseRedirect(reverse('enter'))

        else:

         #   request.session['semail'] = ['irfan.sssit@gmail.comhthrthrthr']
            return HttpResponseRedirect(reverse('enter'))

            #return render(request, "login.html",  {"user":user})


def load_quiz_info(request):
    print(request.POST["quiz_name"])

    response = Data.get(request.POST["quiz_name"])
    print(response)
    return JsonResponse(response,safe=False)


def create_quiz(request):

    return render(request, "test.html", {"quizes":[]})


def load_test_pass_info(request):


    return  render(request, "quiz.html")


def clear(request):
     print("hhhh")
     print(User.objects.all().count())
    # PassedQuiz.objects.all().delete()
    # Question.objects.all().delete()
   #  VariantResult.objects.all().delete()
    # Question.objects.all().delete()
    # PassedQuiz.objects.all().delete()
    # QuestionAnswerResult.objects.all().delete()

   #  Quiz.objects.all().delete()
   #  Document.objects.all().delete()
    # Lesson.objects.all().delete()
     #Course.objects.all().delete()
     #User.objects.all().delete()

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
    if request.GET and len(request.GET) == 3 and request.GET["tag"] != "Show all":

        i = Course.objects.none()
        save = []
        for it in it3.all():
            tag_ = SearchTags.objects.get(name = request.GET["tag"])
            if tag_ in it.search_tags.all():
                print(it.name +" " +it.description)
                tags = [t.name for t in it.search_tags.all()]
                save.append({
                    "name": it.name, "description": it.description,
                    "author": it.course_creator.name,
                    "course_id": it.id,
                    "date": it.created_on.strftime("%Y-%m-%d %H:%M:%S"),
                    "tags": tags
                })



        return JsonResponse({'courses': save})
    if request.GET and len(request.GET) == 2 and request.GET["title"] != "Show all":

        i = None
        for it in it3.all():
            if it.name == request.GET["title"]:
                print(it.name +" " +it.description)
                i = it

        tags = [t.name for t in i.search_tags.all()]
        save = [{
            "name": i.name, "description": i.description,
            "author": i.course_creator.name,
            "course_id": i.id,
            "date": i.created_on.strftime("%Y-%m-%d %H:%M:%S"),
            "tags": tags
        }]
        return JsonResponse({'courses': save})
    if request.GET:
        course =  it3.all()
        print(username)
        save = []
        tags_ = []
        for i in course:
            tags = [t.name for t in i.search_tags.all()]
            if len(tags) > 0:
                tags_.extend(tags)
            save.append({"name": i.name, "description": i.description,
                         "author": i.course_creator.name,
                         "course_id": i.id,
                         "date": i.created_on.strftime("%Y-%m-%d %H:%M:%S"),
                         "tags": tags
                         })
        return JsonResponse({'courses': save, "tags":tags_})

    return render(request, "possible-course-subsciptions.html",{"courses":it3.all(), "username":username})

def get_my_course_subscriptions(request,username):
    if request.GET and len(request.GET) == 3:

        rem = User.objects.get(name=username).course_subscriptions.get(name=request.GET["coursename"])
        User.objects.get(name=username).course_subscriptions.remove(rem)
        it = User.objects.get(name=username).course_subscriptions.all()
        save = []
        for i in it:
            tags = [t.name for t in i.search_tags.all()]
            print(i.course_creator.name)
            save.append({"name": i.name, "description": i.description,
                         "author": i.course_creator.name,
                         "course_id": i.id,
                         "date": i.created_on.strftime("%Y-%m-%d %H:%M:%S"),
                         "tags": tags
                         })

        course_creator_email = rem.course_creator.user_email
        import re

        print(course_creator_email)
        if course_creator_email != None and bool(
                    re.match("^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", course_creator_email)):
            import threading
            t = threading.Thread(target=send_email_for_course_subscription, args=(
                username, rem.name, 'Subscriber unsubscribed ):',username + " " + " unsubscribed from your course " + rem.name,
                              course_creator_email
            ), kwargs={})
            t.setDaemon(True)
            t.start()

              # send_email_for_course_subscription(username, rem.name, 'Subscriber unsubscribed ):',
               #                                    username + " " + " unsubscribed from your course " + rem.name,
                #                                   course_creator_email)'''
        return JsonResponse({'courses': save,"username":username})
    if request.GET:
        it = User.objects.get(name=username).course_subscriptions.all()
        save = []
        for i in it:
            tags = [t.name for t in i.search_tags.all()]
            save.append({"name": i.name, "description": i.description,
                         "author": i.course_creator.name,
                         "course_id": i.id,
                         "date": i.created_on.strftime("%Y-%m-%d %H:%M:%S"),
                         "tags": tags
                         })
        return JsonResponse({'courses': save, "username":username})
    it = User.objects.get(name=username).course_subscriptions

    return  render(request, "my-course-subsciptions.html",{"course_subsciptions":it.all(), "username":username})


def create_course_subscription(request,username,coursename):
    print(username +" "+coursename)
    course = Course.objects.get(name = coursename)
    User.objects.get(name=username).course_subscriptions.add(course)
    course_creator_email = course.course_creator.user_email
    import re
    if  course_creator_email != None and bool(re.match("^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$",course_creator_email)):
       # re.match("^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", course_creator_email)):
        import threading
        t = threading.Thread(target=send_email_for_course_subscription, args=(username, coursename,
            'New subscriber for the course congratulations',
                                         username + " " + " subscribed to your course " + coursename ,course_creator_email
        ), kwargs={})
        t.setDaemon(True)
        t.start()

       # send_email_for_course_subscription(username, coursename,  'New subscriber for the course congratulations',
          #                                 username + " " + " subscribed to your course " + coursename ,course_creator_email )
    return HttpResponseRedirect(reverse('get_my_course_subscriptions',args=(username,)))
#JsonResponse({}) #redirect('/possible-course-subscriptions/'+username) #render(request, "possible-course-subsciptions.html",{})

def delete_course_subscription(request,coursename, username):
    print(Course.objects.all().count())
    rem = User.objects.get(name=username).course_subscriptions.get(name = coursename)
    course_creator_email = rem.course_creator.user_email
    User.objects.get(name=username).course_subscriptions.remove(rem)
    print(Course.objects.all().count())
    print("haha")
    import re
    print()
    print(course_creator_email )
    if course_creator_email != None and bool(re.match("^.+@(\[?)[a-zA-Z0-9-.]+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$", course_creator_email)):
        send_email_for_course_subscription(username, coursename, 'Subscriber unsubscribed ):',
                                           username + " " + " unsubscribed from your course " + coursename,
                                           course_creator_email)
    #it = User.objects.get(name=username).course_subscriptions
    return redirect('/course-subscriptions/'+username) # render(request, "my-course-subsciptions.html",{"course_subsciptions":it.all(), "username":username})

def get_my_created_courses(request,username):

    if request.method == 'GET' and len(request.GET) == 1:
        print(username)
        course = Course.objects.filter(course_creator__name= username).all()
        print(username)
        save = []
        for i in course:

            tags = [t.name for t in i.search_tags.all()]
            save.append({"name":i.name,"description":i.description,
                         "author":username,
                         "course_id":i.id,
                         "date": i.created_on.strftime("%Y-%m-%d %H:%M:%S"),
                         "tags": tags
                         })
        return JsonResponse({'courses': save})
    if request.method == 'GET' and len(request.GET) == 2:

        course = Course.objects.get(name = request.GET["course_name"])
        course.delete()
        course = Course.objects.filter(course_creator__name= username).all()

        print(username)
        save = []
        for i in course:
            tags = [t.name for t in i.search_tags.all()]
            save.append({"name":i.name,"description":i.description,
                         "author":username,
                         "course_id":i.id,
                         "date":i.created_on.strftime("%Y-%m-%d %H:%M:%S"),
                         "tags": tags
                         })
        return JsonResponse({'courses': save })
    print("get_my_created_courses")
    i = Course.objects.filter(course_creator__name = username)

    """,{"my_courses":Course.objects.get(name=username)}"""
    return render(request, "my-created-courses.html", {"my_courses":i})

def create_course(request,username):
    if request.POST:
        print(request.POST)
        s = request.POST["course_name"]
        description = request.POST["description"]
        cat = request.POST["tags"].split(",")
        categories = [i for i in cat if i]

        print(type(categories))
        print(categories)

        try:
            course, created  =  Course.objects.get_or_create(name = s, course_creator = User.objects.get(name=username), description = description)
            if len(categories) > 0:
                for tag in categories:
                    categorie, created = SearchTags.objects.get_or_create(name=tag)

                    course.search_tags.add(categorie)
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

def show_course_lessons(request,coursename,username):
    course = Course.objects.get(name = coursename)
    lessons = Lesson.objects.filter(course = course ).all()
    return render(request,"show_course_lessons.html",{"username":username,"lessons": lessons, "coursename":coursename})

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
    print("hahaTR")

    if request.GET and len(request.GET) == 1:
        test_course = Course.objects.get(name=coursename)
        test_lesson = Lesson.objects.get(name=lessonname, course=test_course)
        quiz, created = TestQuiz.objects.get_or_create(belong_to_lesson=test_lesson)
        if not created:
            return JsonResponse({"test_in_json": quiz.quiz_in_json})
        else:
            quiz.quiz_in_json= '{"test_name": "", "test_author": "", "test_questions": [{"question": "", "answers": [{"1": ""}, {"2": ""}], "correct_answer": ""},{"question": "", "answers": [{"1": ""}, {"2": ""}], "correct_answer": ""}]}';

            quiz.save()
            return JsonResponse({"test_in_json":  quiz.quiz_in_json})
    if request.GET and len(request.GET) == 2:
      #  {"test_name": "fewfe", "test_author": "",
        # "test_questions": [{"question": "", "answers": [{"1": ""}, {"2": ""}], "correct_answer": ""},
         #                   {"question": "", "answers": [{"1": ""}, {"2": ""}], "correct_answer": ""}]}

        obj = json.loads(request.GET["test_in_json"])
        test_course = Course.objects.get(name = coursename)
        test_lesson = Lesson.objects.get(name=lessonname,course=test_course)
        quiz,created = TestQuiz.objects.get_or_create(belong_to_lesson = test_lesson)

        quiz.title = obj["test_name"]
        quiz.quiz_in_json = request.GET["test_in_json"]
        quiz.save()
        TestQuestion.objects.filter(belong_to_quiz = quiz).delete()
        PassedTestQuiz.objects.filter(test_quiz = quiz).delete()
        return JsonResponse({});

    return render(request, "create_tests_for_lesson.html", {"coursename": coursename,
                                                       "lessonname":  lessonname})

def pass_tests_forlesson(request,coursename,lessonname,username):
    print("ffa")
    if request.GET and len(request.GET) == 1:
        test_course = Course.objects.get(name=coursename)
        test_lesson = Lesson.objects.get(name=lessonname, course=test_course)
        try:
            quiz = TestQuiz.objects.get(belong_to_lesson = test_lesson)
            if quiz:
                user = User.objects.get(name=username)
                PassedTest,created = PassedTestQuiz.objects.get_or_create(test_quiz = quiz,test_quiz_user =user)
                if PassedTest.test_quiz_pass_attempt != 0:
                    print(1)
                    return JsonResponse({"passed": "yes","available":"yes"})
                else:

                    return JsonResponse({"test_in_json":quiz.quiz_in_json,
                                         "passed": "no","available":"yes"})
            else:
                print(3)
                return JsonResponse({"test_in_json": "0","passed": "no","available":"no"})
        except Exception as e:
            print(e)
            return JsonResponse({"test_in_json":"0","passed": "no", "available":"no"})
        #on quiz pass
    try:
        print(request.GET["testResult"])
    except Exception as e:
        print(e)
    if request.GET and len(request.GET) == 3:
        print("ffew")
        test_course = Course.objects.get(name=coursename)
        test_lesson = Lesson.objects.get(name=lessonname, course=test_course)
        quiz = TestQuiz.objects.get(belong_to_lesson=test_lesson)
        user = User.objects.get(name=username)

        passed_test, created = PassedTestQuiz.objects.get_or_create(test_quiz_user=user,
                                                                    test_quiz=quiz)
        i = 0
        info = json.loads(request.GET["testResult"])
        for question in json.loads(quiz.quiz_in_json)["test_questions"]:
            QuestionAnswer = QuestionAnswerResult.objects.create(belong_to_quiz = passed_test)
            QuestionAnswer.question = question["question"]
            print(request.GET.keys())
            QuestionAnswer.answer = info["answers"][i]

            i+= 1
            QuestionAnswer.save()
        passed_test.test_quiz_pass_attempt = passed_test.test_quiz_pass_attempt + 1
        passed_test.save()
        return JsonResponse({})
    if request.GET and len(request.GET) == 2:

        test_course = Course.objects.get(name=coursename)
        test_lesson = Lesson.objects.get(name=lessonname, course=test_course)
        quiz = TestQuiz.objects.get(belong_to_lesson=test_lesson)
        user = User.objects.get(name=username)

        passed_test,created = PassedTestQuiz.objects.get_or_create(test_quiz_user=user,
                                             test_quiz = quiz)
        if not created:
            quiz_in_json = json.loads(quiz.quiz_in_json)
            user = User.objects.get(name=username)
            PassedQuiz = PassedTestQuiz.objects.get(test_quiz=quiz, test_quiz_user=user)
            save = []
            print(quiz_in_json)
            for question in quiz_in_json["test_questions"]:
                question_answer = QuestionAnswerResult.objects.get(belong_to_quiz = PassedQuiz,question = question["question"] )

                save.append({
                    "quiz_user": username,
                    "question":question["question"] ,
                    "answer": question_answer.answer,
                    "correct_answer": question['answers'][question["correct_answer"]-1][str(question["correct_answer"])],
                    "correct":question_answer.answer == question['answers'][question["correct_answer"]-1][str(question["correct_answer"])]
                })
            return JsonResponse({"status":"You have passed the quiz already", "test_passing": save, "quiz_name":quiz.title})


    print("hahf")
    return render(request,"pass_test.html", {})

def pass_test(request,coursename,lessonname):

    return render(request, "pass_test.html", {})

def show_chat(request,coursename,username):
    #select chat per coursename
    course = Course.objects.get(name=coursename)


    chat,created = Chat.objects.get_or_create(course = course)

    if request.GET and len(request.GET) == 3:
        # "messages": messages,

        message = Messages.objects.create(author=username,belong_to_chat=chat,text=request.GET["save"])
        save = []

        for message in Messages.objects.filter(belong_to_chat=chat).all():
            save.append({"text": message.text, "date": message.created_on.strftime("%Y-%m-%d %H:%M:%S"), "author": message.author,
                         "iamAuthor": message.author == username})
        return JsonResponse({"messages": save, "coursename": coursename, "username": username})

    messages = Messages.objects.filter(belong_to_chat = chat)

    if request.GET and len(request.GET) == 2:
       # "messages": messages,
        save = []
        for message in messages.all():
            save.append({"text":message.text, "date":message.created_on.strftime("%Y-%m-%d %H:%M:%S") , "author": message.author,
                         "iamAuthor": message.author == username})
        return JsonResponse({"messages":save,"coursename": coursename, "username": username})

    return render(request,"shat.html",{})

def about(request):
    return render(request, "about.html", {})