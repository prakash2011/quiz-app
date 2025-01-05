from django.shortcuts import render,redirect,get_object_or_404
from .forms import UserRegistrationForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
# from .models import questions
from django.contrib import messages
from django.urls import reverse
# Create your views here.

def index(request):
    feedbacks=CustomerFeddback.objects.all()
    return render(request,'surveys.html',{"feedbacks":feedbacks})

# @login_required
def Customer_feedback(request,id):
    feedback=CustomerFeddback.objects.get(id=id)
    session_key = request.session.session_key
    user_responses = CustomerResponse.objects.filter(feedback=feedback, session_key=session_key)
    if user_responses.exists():
        # messages.info(request, "You have already submitted your feedback.")
        return redirect('thank-you', id=feedback.id)
    if not session_key:
        request.session.create()  # Create a session if one does not exist
        session_key = request.session.session_key
    

    if request.method =='POST':
        for question in feedback.question.all():
            response_text=request.POST.get(f"response_{question.id}")
            selected_option_ids=request.POST.getlist(f"options_{question.id}")
            
            print(response_text)
            print(selected_option_ids)
            response=CustomerResponse.objects.create(
                feedback=feedback,
                question=question,
                response_text=response_text if question.question_type in ["Text","BigText"] else None,
                session_key=session_key
            )
            if selected_option_ids:
                selected_options=Options.objects.filter(id__in=selected_option_ids)
                response.selected_options.set(selected_options)
        messages.success(request, "Thank you for your feedback!")
        return redirect(reverse('thank-you', args=[feedback.id]))
    
       
    return render(request,'survey.html',{"questions":feedback.question.all()})
    
def thank_you(request,id):
    context = {"id": id}
    return render(request,'thank_you.html',context)

def register(request):
    if request.method =="POST":
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request,user)
            return redirect('index')
    else:
        form=UserRegistrationForm()
    return render(request,'registration/register.html',{'form':form})
def about(request):
    return render(request,'about.html')



def results_view(request, id):
    # Fetch the specific feedback instance
    feedback = get_object_or_404(CustomerFeddback, id=id)
    session_key = request.session.session_key

    # If the session key does not exist, no responses can be matched
    if not session_key:
        messages.error(request, "Session not found. Please participate in the survey first.")
        return redirect('index')

    # Get the questions associated with this feedback
    questions = feedback.question.all()

    # Prepare data to display
    questions_data = []
    for question in questions:
        options = question.options.all()
        questions_data.append({
            "question_text": question.question,
            "options": [{"option_name": option.option_name, "is_correct": option.is_correct} for option in options]
        })

    # Fetch customer responses for this feedback filtered by session key
    user_responses = CustomerResponse.objects.filter(feedback=feedback, session_key=session_key)

    response_data = []
    total_score = 0
    for response in user_responses:
        selected_options = [option.option_name for option in response.selected_options.all()]
        is_correct = all(option.is_correct for option in response.selected_options.all())
        if is_correct:
            total_score += 1
        response_data.append({
            "question": response.question.question,
            "selected_options": selected_options,
            "is_correct": is_correct,
        })

    # Pass total_score and response_data to the template
    return render(request, 'results.html', {
        "questions_data": questions_data,
        "response_data": response_data,
        "session_key": session_key,
        "total_score": total_score,
        "max_score": len(user_responses),
    })
