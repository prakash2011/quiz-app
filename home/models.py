from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class questions(models.Model):
    QUESTION_CHOICES=(("Text","Text"),("BigText","BigText"),("Radio","Radio"),("Checkbox","Checkbox"))
    question=models.CharField(max_length=100)
    question_type=models.CharField(choices=QUESTION_CHOICES,max_length=50,default="Text")

    def __str__(self) -> str:
        return f"{self.question} {self.question_type}"

class Options(models.Model):
    question=models.ForeignKey(questions,related_name="options",on_delete=models.CASCADE)
    option_name=models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self) ->str:
        return f"{self.option_name} ({'Correct' if self.is_correct else 'Incorrect'}) for {self.question.question}"
        
class CustomerFeddback(models.Model):
    question=models.ManyToManyField(questions)
    feedback_name=models.CharField(max_length=100,blank=True)

    

class CustomerResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True) 
    feedback=models.ForeignKey(CustomerFeddback,on_delete=models.CASCADE)
    question=models.ForeignKey(questions,on_delete=models.CASCADE)
    response_text=models.TextField(null=True,blank=True)
    selected_options=models.ManyToManyField(Options,blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    

    def is_correct(self):
        # Fetch correct options for the question
        correct_options = set(self.question.options.filter(is_correct=True))
        # Compare with selected options
        selected_options = set(self.selected_options.all())
        return correct_options == selected_options

