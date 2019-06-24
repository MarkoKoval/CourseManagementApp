from django.db import models

# Create your models here.


class Quiz(models.Model):
        title = models.CharField(max_length=64,  default="no title yet")
        questions = models.ManyToManyField('Question', blank=True, related_name='posts')


class Question(models.Model):
        title = models.CharField(max_length=64,  default="no title yet")
        variant_result_pair = models.ManyToManyField('VariantResult', blank=True, related_name='posts')


class VariantResult(models.Model):
        choice = models.CharField(max_length=64,  default="no title yet")
        score = models.IntegerField()


class QuestionAnswerResult(models.Model):
        question =  models.CharField(max_length=64,  default="no question yet")
        answer = models.CharField(max_length=64,  default="no question yet")
        result = models.IntegerField()


class PassedQuiz(models.Model):
        quiz_name = models.CharField(max_length=64,  default="no name yet")
        question_answer_result_pair = models.ManyToManyField('QuestionAnswerResult', blank=True, related_name='question_answer_result')


class User(models.Model):
        name = models.CharField(max_length=64,  default="no name yet", unique=True)
        password = models.CharField(max_length=64,  default="no password yet")
        user_email =   models.CharField(max_length=64,  null=True, blank=True ,unique=True)
        user_status =  models.CharField(max_length=15,  null=True, blank=True)
        #is_varified_to_be_course_creator = models.BooleanField(default=False)
        passed_quizes = models.ManyToManyField('PassedQuiz', blank=True, related_name='passed_quizes')
        course_subscriptions = models.ManyToManyField('Course', blank=True, related_name='course_subscriptions')




class SearchTags(models.Model):
        name = models.CharField(max_length=64, default="no name yet", unique=True)



class Course(models.Model):
        name = models.CharField(max_length=64, unique=True)
        search_tags = models.ManyToManyField('SearchTags', blank=True, related_name='search_tags')
        description = models.CharField(max_length=500,  null=True, blank=True)
        course_creator = models.ForeignKey(User, on_delete=models.CASCADE)
        created_on = models.DateTimeField(auto_now_add=True)
        updated_on = models.DateTimeField(auto_now=True)



class Lesson(models.Model):
        name = models.CharField(max_length=64)
        description = models.CharField(max_length=500, null=True, blank=True)
        course = models.ForeignKey(Course, on_delete=models.CASCADE)
        created_on = models.DateTimeField(auto_now_add=True)
        updated_on = models.DateTimeField(auto_now=True)

        class Meta:
                unique_together = ("name", "course")

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    belong_to_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE,null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

