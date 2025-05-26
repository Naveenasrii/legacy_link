from django.shortcuts import render, redirect
from django.contrib import messages
from .firebase_config import db
from django.http import JsonResponse
import json
import tempfile
from firebase_admin import storage  # if you're using Firebase Storage
import uuid
import os
from firebase_admin import firestore
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required
def login_page(request):
    return render(request, 'home.html') 

def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        users_ref = db.collection('users')
        query = users_ref.where('email', '==', email).where('password', '==', password).stream()
        user = next(query, None)

        if user:
            user_data = user.to_dict()
            uid = user.id  # Firebase document ID is usually the UID
            request.session['user_email'] = email
            messages.success(request, 'Login Successful')
            return redirect('dash')  # or another name for your dashboard page if it's different
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login_page')



def home(request):
    return render(request, 'dash.html') 

def signup_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('signup_page')

        users_ref = db.collection('users')
        existing_users = users_ref.where('email', '==', email).stream()

        if next(existing_users, None):
            messages.error(request, 'User already exists')
            return redirect('signup_page')
       
        users_ref.add({
            'name': name,
            'email': email,
            'username': username,
            'password': password
        })

        messages.success(request, 'Signup Successful. Please login.')
        return redirect('login_page')
    else:
        return redirect('signup_page')


def alumni_login_page(request):
    return render(request, 'alumni_login.html')


def alumni_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        alumni_ref = db.collection('alumni')
        query = alumni_ref.where('email', '==', email).where('password', '==', password).stream()
        alumni = next(query, None)

        if alumni:
            request.session['alumni_email'] = email  # ✅ Set session key for alumni
            messages.success(request, 'Login successful')
            return redirect('alumni_dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('alumni_login_page')

def alumni_signup_page(request):
    return render(request, 'alumni_signup.html')


def alumni_signup(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('alumni_signup_page')

        alumni_ref = db.collection('alumni')
        query = alumni_ref.where('email', '==', email).stream()

        if next(query, None):
            messages.error(request, 'Alumni already exists')
            return redirect('alumni_signup_page')

        alumni_ref.add({
            'name': name,
            'email': email,
            'password': password
        })
        messages.success(request, 'Signup successful! Please login.')
        return redirect('alumni_login_page')



def home(request):
    return render(request, 'home.html') 

def dashboard(request):
    email = request.session.get('user_email')
    user_data = None
    user_id = None

    if email:
        users_ref = db.collection('users')
        query = users_ref.where('email', '==', email).stream()
        user_doc = next(query, None)
        if user_doc:
            user_data = user_doc.to_dict()
            user_id = user_doc.id  # Firebase document ID

    return render(request, 'dash.html', {
        'user': {'id': user_id, 'email': email, **(user_data or {})},
    })
def login_page(request):
    return render(request, 'login.html')

def alumni_login_page(request):
    return render(request, 'alumni_login.html')

def profile_page(request):
    return render(request, 'profile.html')
def alumni_profile_view(request):
    return render(request, 'alumniprof.html')
def job_opportunities(request):
    jobs_ref = db.collection('job_postings').order_by('postedAt', direction=firestore.Query.DESCENDING).stream()
    jobs = []

    for job_doc in jobs_ref:
        job_data = job_doc.to_dict()
        jobs.append(job_data)

    return render(request, 'jobopp.html', {'jobs': jobs})

def alumni_jobboard(request):
    return render(request, 'alumni_jobboard.html')

def user_profile(request, user_id):
    user_ref = db.collection('users').document(user_id)
    user_doc = user_ref.get()
    if user_doc.exists:
        user_data = user_doc.to_dict()
        return render(request, 'accounts/profile/profile.html', {'user_id': user_id})
    else:
        return HttpResponse("User not found", status=404)


def save_profile(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = request.session.get('user_email')  # <-- Correct way to get user email

            if not email:
                return JsonResponse({'error': 'User not logged in'}, status=401)

            users_ref = db.collection('users')
            query = users_ref.where('email', '==', email).stream()
            user_doc = next(query, None)

            if user_doc:
                user_ref = users_ref.document(user_doc.id)
                user_ref.update({
                    'name': data.get('name', ''),
                    'gradYear': data.get('gradYear', ''),
                    'department': data.get('department', ''),
                    'linkedin': data.get('linkedin', '')
                })
                return JsonResponse({'message': 'Profile updated successfully'})
            else:
                return JsonResponse({'error': 'User not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_profile(request):
    if request.method == 'GET':
        email = request.session.get('user_email')  # Use session-stored logged-in user's email
        if not email:
            return JsonResponse({'error': 'User not logged in'}, status=401)

        users_ref = db.collection('users')
        query = users_ref.where('email', '==', email).stream()
        user_doc = next(query, None)

        if user_doc:
            profile_data = user_doc.to_dict()
            return JsonResponse({'profile': profile_data})
        else:
            return JsonResponse({'profile': None})
    return JsonResponse({'error': 'Invalid request'}, status=400)
def get_alumni_profile(request):
    if request.method == 'GET':
        email = request.session.get('alumni_email')
        if not email:
            return JsonResponse({'error': 'Alumni not logged in'}, status=401)

        alumni_ref = db.collection('alumni')
        query = alumni_ref.where('email', '==', email).stream()
        alumni_doc = next(query, None)

        if alumni_doc:
            profile_data = alumni_doc.to_dict()
            return JsonResponse({'profile': profile_data})
        else:
            return JsonResponse({'profile': None})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def save_alumni_profile(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = request.session.get('alumni_email')

            if not email:
                return JsonResponse({'error': 'Alumni not logged in'}, status=401)

            alumni_ref = db.collection('alumni')
            query = alumni_ref.where('email', '==', email).stream()
            alumni_doc = next(query, None)

            if alumni_doc:
                alumni_ref.document(alumni_doc.id).update({
    'name': data.get('name', ''),
    'batch': data.get('batch', ''),
    'job_title': data.get('job_title', ''),
    'industry': data.get('industry', ''),
    'company': data.get('company', ''),
    'location': data.get('location', ''),
    'skills': data.get('skills', ''),
    'email': data.get('email', ''),
    'linkedin': data.get('linkedin', ''),
    'website': data.get('website', '')
})
                return JsonResponse({'message': 'Profile updated successfully'})
            else:
                return JsonResponse({'error': 'Alumni not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def post_job(request):
    if request.method == 'POST':
        title = request.POST.get('jobTitle')
        company = request.POST.get('companyName')
        location = request.POST.get('location')
        experience = int(request.POST.get('experience'))
        description = request.POST.get('jobDescription')

        job_data = {
            'title': title,
            'company': company,
            'location': location,
            'experience': experience,
            'description': description,
            'postedAt': firestore.SERVER_TIMESTAMP
        }

        try:
            # Add the job data to Firestore's job_postings collection
            db.collection('job_postings').add(job_data)
            messages.success(request, "✅ Job posted successfully!")
        except Exception as e:
            messages.error(request, f"❌ Failed to post job: {str(e)}")

        return redirect('alumni_jobboard')

    return redirect('alumni_jobboard')
def alumni_network_view(request):
    return render(request, 'alumni_network.html')
def alumni_mentorship(request):
    return render(request, 'alumni_mentorship.html')
def logout_view(request):
    logout(request)
    return redirect('homepage') 



def search_alumni(request):
    if request.method == "GET":
        alumni_ref = db.collection('alumni')
        docs = alumni_ref.stream()

        alumni_data = []
        for doc in docs:
            data = doc.to_dict()
            alumni_data.append({
                'name': data.get('name'),
                'industry': data.get('industry'),
                'batch': data.get('batch'),
                'image_url': data.get('image_url', '')  # optional field
            })

        return JsonResponse({'alumni': alumni_data})
def homepage(request):
    return render(request, 'homepage.html')  # Assuming the file is inside 'homepage' folder under templates


def ask_question(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        if question:
            db.collection('questions').add({
                'text': question,
                'createdAt': firestore.SERVER_TIMESTAMP
            })
        return redirect('ask_question')

    # Fetch questions and their answers
    questions_ref = db.collection('questions').order_by('createdAt', direction=firestore.Query.DESCENDING)
    questions = []

    for doc in questions_ref.stream():
        q = doc.to_dict()
        q['id'] = doc.id
        q['answers'] = [a.to_dict() for a in db.collection('questions').document(doc.id).collection('answers').order_by('createdAt').stream()]
        questions.append(q)

    return render(request, 'ask_question.html', {'questions': questions})


def answer_question(request, question_id):
    if request.method == 'POST':
        answer = request.POST.get('answer')
        if answer:
            db.collection('questions').document(question_id).collection('answers').add({
                'text': answer,
                'createdAt': firestore.SERVER_TIMESTAMP
            })
    return redirect('ask_question')



def applyme(request):
    return render(request, 'applyme.html') 
def about_page(request):
    return render(request, "about.html")

def contact_page(request):
    return render(request, "contact.html")


def submit_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        data = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message
        }

       
        db.collection('contact_messages').add(data)

        
        success_message = "Thank you! Your message has been received."
        return render(request, 'contact.html', {'success_message': success_message})

    return render(request, 'contact.html')
def search(request):
    return render(request, 'search.html')

def student_chat_view(request):
    alumni_id = request.GET.get('alumniId')
    # Use alumni_id in context or for logic
    return render(request, 'student_chat.html', {'alumni_id': alumni_id})

def alumni_chat_view(request):
    # Extract alumni username from session or URL or set default
    # This should be set dynamically for production use
    logged_in_alumni_username = "alumni2"  # example username
    alumni_chat_id = f"naveenasri_{logged_in_alumni_username}".lower()

    return render(request, "alumni_chat.html", {
        "logged_in_alumni_chat_id": alumni_chat_id
    })


def psg_college_view(request):
    return render(request, 'psg_college.html')
def alumni_dashboard(request):
    chat_id = request.session.get('alumni_email')
    return render(request, 'alumnidash.html', {'logged_in_alumni_chat_id': chat_id})

def messages_view(request):
    chat_id = request.session.get('alumni_email')
    return render(request, "messages.html", {"logged_in_alumni_chat_id": chat_id})

def alumni_announcements_view(request):
    return render(request, 'alumni_announcements.html')
def alumni_meetup_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        batch = request.POST.get('batch')
        contact = request.POST.get('contact')

        if name and email and batch and contact:
            try:
                db.collection('meetup_registrations').add({
                    'name': name,
                    'email': email,
                    'batch': batch,
                    'contact': contact,
                    'timestamp': firestore.SERVER_TIMESTAMP
                })
                messages.success(request, 'Registration submitted successfully!')
                return redirect('alumni_meetup_register')  # or another page like 'meetup_success'
            except Exception as e:
                messages.error(request, f'Error: {e}')
        else:
            messages.error(request, 'Please fill in all the required fields.')

    return render(request, 'alumni_meetup_register.html')
def mylswamy(request):
    return render(request, 'mylswamy.html')

def shiv(request):
    return render(request, 'shiv.html')

def pandia(request):
    return render(request, 'pandia.html')
def password_reset_page(request):
    return render(request, 'password_reset.html')

def forgot_password_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            # Send a password reset email using Firebase Authentication
            auth.send_password_reset_email(email)
            messages.success(request, "Password reset email sent. Please check your inbox.")
        except auth.UserNotFoundError:
            messages.error(request, "User with this email does not exist.")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
    return render(request, 'password_reset.html')

def password_reset_page(request):
    return render(request, 'password_reset.html')
def alumni_awards_view(request):
    return render(request, 'alumni_awards.html')

def announcements_view(request):
    return render(request, 'announcements.html')
def add_announcement_view(request):
    return render(request, 'add_announcement.html')
def reply_to_student(request):
    student_name = request.GET.get('student', '')
    return render(request, 'reply.html', {'student_name': student_name})
def ask_question(request):
    if request.method == 'POST' and 'question' in request.POST:
        question = request.POST.get('question')
        name = request.POST.get('name')
        year = request.POST.get('year')
        if question and name and year:
            db.collection('questions').add({
                'text': question,
                'name': name,
                'year': year,
                'createdAt': firestore.SERVER_TIMESTAMP
            })
        return redirect('ask_question')

    questions_ref = db.collection('questions').order_by('createdAt', direction=firestore.Query.DESCENDING)
    questions = []

    for doc in questions_ref.stream():
        q = doc.to_dict()
        q['id'] = doc.id
        q['editing'] = False
        q['answers'] = []

        answers_ref = db.collection('questions').document(doc.id).collection('answers').order_by('createdAt')
        for ans in answers_ref.stream():
            a = ans.to_dict()
            a['id'] = ans.id
            a['editing'] = False
            q['answers'].append(a)

        questions.append(q)

    return render(request, 'ask_question.html', {'questions': questions})

def answer_question(request, qid):
    if request.method == 'POST':
        answer = request.POST.get('answer')
        name = request.POST.get('name')
        year = request.POST.get('year')
        if answer and name and year:
            db.collection('questions').document(qid).collection('answers').add({
                'text': answer,
                'name': name,
                'year': year,
                'createdAt': firestore.SERVER_TIMESTAMP
            })
    return redirect('ask_question')

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from firebase_admin import firestore
from .firebase_config import db  # Adjust as needed if your Firebase config is named differently

def ask_question(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        name = request.POST.get('name')
        year = request.POST.get('year')
        if question and name and year:
            db.collection('questions').add({
                'text': question,
                'name': name,
                'year': year,
                'createdAt': firestore.SERVER_TIMESTAMP
            })
        return redirect('ask_question')

    # Fetch questions and answers
    questions_ref = db.collection('questions').order_by('createdAt', direction=firestore.Query.DESCENDING)
    questions = []

    for doc in questions_ref.stream():
        q = doc.to_dict()
        q['id'] = doc.id
        q['editing'] = False
        q['answers'] = []

        answers_ref = db.collection('questions').document(doc.id).collection('answers').order_by('createdAt')
        for ans in answers_ref.stream():
            a = ans.to_dict()
            a['id'] = ans.id
            a['editing'] = False
            q['answers'].append(a)

        questions.append(q)

    return render(request, 'ask_question.html', {'questions': questions})


def answer_question(request, question_id):
    if request.method == 'POST':
        answer = request.POST.get('answer')
        name = request.POST.get('name')
        year = request.POST.get('year')
        if answer and name and year:
            db.collection('questions').document(question_id).collection('answers').add({
                'text': answer,
                'name': name,
                'year': year,
                'createdAt': firestore.SERVER_TIMESTAMP
            })
    return redirect('ask_question')


def edit_question(request, qid):
    doc_ref = db.collection('questions').document(qid)
    if request.method == 'POST':
        if 'edit' in request.POST:
            # Load page with this question in edit mode
            questions_ref = db.collection('questions').order_by('createdAt', direction=firestore.Query.DESCENDING)
            questions = []

            for doc in questions_ref.stream():
                q = doc.to_dict()
                q['id'] = doc.id
                q['editing'] = (doc.id == qid)
                q['answers'] = []

                answers_ref = db.collection('questions').document(doc.id).collection('answers').order_by('createdAt')
                for ans in answers_ref.stream():
                    a = ans.to_dict()
                    a['id'] = ans.id
                    a['editing'] = False
                    q['answers'].append(a)

                questions.append(q)

            return render(request, 'ask_question.html', {'questions': questions})

        else:
            new_text = request.POST.get('question')
            if new_text:
                doc_ref.update({'text': new_text})

    return redirect('ask_question')


def delete_question(request, qid):
    if request.method == 'POST':
        answers_ref = db.collection('questions').document(qid).collection('answers')
        for ans in answers_ref.stream():
            ans.reference.delete()
        db.collection('questions').document(qid).delete()
    return redirect('ask_question')


def edit_answer(request, qid, aid):
    ans_ref = db.collection('questions').document(qid).collection('answers').document(aid)
    if request.method == 'POST':
        if 'edit' in request.POST:
            questions_ref = db.collection('questions').order_by('createdAt', direction=firestore.Query.DESCENDING)
            questions = []

            for doc in questions_ref.stream():
                q = doc.to_dict()
                q['id'] = doc.id
                q['editing'] = False
                q['answers'] = []

                answers_ref = db.collection('questions').document(doc.id).collection('answers').order_by('createdAt')
                for ans in answers_ref.stream():
                    a = ans.to_dict()
                    a['id'] = ans.id
                    a['editing'] = (doc.id == qid and ans.id == aid)
                    q['answers'].append(a)

                questions.append(q)

            return render(request, 'ask_question.html', {'questions': questions})

        else:
            new_text = request.POST.get('answer')
            if new_text:
                ans_ref.update({'text': new_text})

    return redirect('ask_question')


def delete_answer(request, qid, aid):
    if request.method == 'POST':
        db.collection('questions').document(qid).collection('answers').document(aid).delete()
    return redirect('ask_question')