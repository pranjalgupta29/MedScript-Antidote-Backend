from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from .models import User,Patient,Doctor,Reports,Treatment,Disease,Specialization,Symptom,QnA
from .forms import FileForm , send_to_doc_Form,Register_Doc,Register_Patient, LoginUserForm, RegisterUserForm, Forgot_email_form,Forgot_Password_Form, Prescription,Symptoms,QuestionForm, AnswerForm, AppointmentForm
from .utils import send_email,sort_lat
from django.contrib.sites.shortcuts import get_current_site

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .token import account_activation_token

from .decorators import patient_required, doctor_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
#from models import Disease
import pickle
import joblib
import json
import pandas as pd
import numpy as np
from collections import Counter
#from sklearn import preprocessing
from rest_framework.decorators import api_view
#from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.parsers import JSONParser

# Create your views here.

@login_required
@doctor_required
def Add_Appointment(request,nums):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if not form.is_valid():
            print("here")
            return HttpResponseRedirect(reverse("Treat",args=[nums]))
        
        print(form.data.get('Appointment'))
        tr = Treatment.objects.get(pk=nums)
        tr.Appointment = form.data.get('Appointment')
        tr.save()
        return HttpResponseRedirect(reverse("Treat",args=[nums]))
    return HttpResponseRedirect(reverse("Treat",args=[nums]))


@login_required()
def delete_Question(request,nums):
    Q = QnA.objects.get(id = nums)
    t = Q.Treatment
    print(t.id)
    if Q.Made_By != request.user:
        return HttpResponseRedirect(reverse("index"))
    
    Q.delete()
    return HttpResponseRedirect(reverse("Treat",args=[t.id]))
    

@login_required
def Add_Answer(request, nums, Q_id):
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if not form.is_valid():
            print("here")
            return HttpResponseRedirect(reverse("Treat", args=[nums]))

        print(form.data.get('Question'))
        tr = Treatment.objects.get(pk=nums)
        Q = QnA.objects.get(id=Q_id)
        Q.Answer = form.data.get('Answer')
        Q.Is_Answered = True
        Q.save()
        return HttpResponseRedirect(reverse("Treat", args=[nums]))
    return HttpResponseRedirect(reverse("Treat", args=[nums]))


@login_required
def Add_Question(request, nums):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if not form.is_valid():
            print("here")
            return HttpResponseRedirect(reverse("Treat", args=[nums]))

        print(form.data.get('Question'))
        tr = Treatment.objects.get(pk=nums)
        Q = QnA.objects.create(Made_By=request.user, Question=form.data.get('Question'), Treatment=tr)
        Q.save()
        return HttpResponseRedirect(reverse("Treat", args=[nums]))
    return HttpResponseRedirect(reverse("Treat", args=[nums]))


@login_required
@patient_required
def create_Treat(request):
    if request.method == "POST":
        f = Symptoms(request.POST)
        syms = f.data.getlist("SymptomList")
        syms = [int(x) for x in syms]
        idx = []
        df = pd.read_csv('Users/test.csv')
        for col in range(len(df.columns)):
            if col in syms:
                idx.append(1)
            else:
                idx.append(0)
        idx = np.array(idx)
        idx = np.reshape(idx, (1, 132))
        df1=pd.DataFrame(idx,columns=df.columns)
        df=df.append(df1)
        answer = mydisease(df).strip()
        dis = Disease.objects.get(Name=answer)
        tr = Treatment.objects.create(Patient=request.user.Patient, Disease=dis, is_new=True)
        for id in syms:
            s = Symptom.objects.get(pk=id)
            tr.SymptomList.add(s)
        tr.lat = f.data.get("lat")
        tr.lon = f.data.get("lon")
        tr.save()
        return HttpResponseRedirect(reverse("Doctor_list", args=[tr.id]))

    f = Symptoms()
    return render(request, "Users/Create_Treat.html", {
        "f": f,
    })


@login_required
@patient_required
def Add_doc(request, T_id, D_id):
    tr = Treatment.objects.get(pk=T_id)
    doc = Doctor.objects.get(pk=D_id)
    if tr.Patient != request.user.Patient or not tr.is_new:
        return HttpResponseRedirect(reverse("index"))
    tr.Doctor = doc
    tr.save()
    return HttpResponseRedirect(reverse("View_Treatment"))


@login_required
@patient_required
def Doctor_list(request, nums):
    tr = Treatment.objects.get(pk=nums)
    Docs = tr.Disease.Specialization.Doctors.all()
    Docs = sort_lat(Docs, (tr.lat, tr.lon))
    for doc in Docs:
        print(doc.Name)
    return render(request, "Users/Doctor_list.html", {
        "Docs": Docs,
        "tr": tr,
    })


@login_required
@doctor_required
def edit_Presc(request, nums):
    Tr = Treatment.objects.get(pk=nums)
    if request.method == "POST":
        if request.user.Doctor == Tr.Doctor:
            form = Prescription(request.POST, instance=Tr)
            form.save()
        return HttpResponseRedirect(reverse("Treat", args=[nums]))

    if request.user.Doctor == Tr.Doctor:
        form = Prescription(instance=Tr)
        return render(request, "Users/presc.html", {
            "presc": form,
            "id": Tr.id
        })


def Change_Password(request):
    if request.method == "POST":
        form = Forgot_Password_Form(request.POST)
        if not form.is_valid() or form.data.get('password1') != form.data.get('password2'):
            return render(request, "Users/forgot.html", {
                "message": "Change Passsword",
                "form": form,
                "name": "Change Password",
                "alert": "Passwords Should Match"
            })
        else:
            request.user.set_password(form.data.get('password1'))
            request.user.save()
            login(request, request.user)
            # return HttpResponseRedirect(reverse("login"))
            return render(request, "Users/forgot.html", {
                "message": "Change Passsword",
                "form": form,
                "name": "Change Password",
                "alert": "Password Changed Succesfully"
            })

    form = Forgot_Password_Form()
    return render(request, "Users/forgot.html", {
        "message": "Change Passsword",
        "form": form,
        "name": "Change Password",
    })


@login_required
def Edit_profile(request):
    message = None
    if request.method == "POST":
        if request.user.is_patient:
            form = Register_Patient(data=request.POST, instance=request.user.Patient)
            form.save()

        else:
            form = Register_Doc(data=request.POST, instance=request.user.Doctor)
            form.save()

        message = "Profile Updated Succesfully"

    if request.user.is_patient:
        form = Register_Patient(instance=request.user.Patient)
    else:
        form = Register_Doc(instance=request.user.Doctor)

    return render(request, "Users/Edit.html", {
        "form": form,
        "message": message
    })


@login_required
@doctor_required
def view_active_treatments(request):
    Treatments = Treatment.objects.filter(Doctor=request.user.Doctor)
    t = []
    for tr in Treatments:
        if tr.is_active:
            t.append(tr)

    return render(request, 'Users/ActiveTreat.html', {
        'Treatments': t,
    })


@login_required
@doctor_required
def view_new_treatments(request):
    Treatments = Treatment.objects.filter(Doctor=request.user.Doctor)
    t = []
    for tr in Treatments:
        if tr.is_new:
            t.append(tr)

    return render(request, 'Users/NewTreat.html', {
        'Treatments': t
    })


@login_required
def Treats(request, nums):
    Q_Form = QuestionForm()
    A_Form = AnswerForm()
    Appoint_Form = AppointmentForm()
    Treat = Treatment.objects.get(pk=nums)
    if request.user.is_doctor:
        rep = request.user.Doctor.Reports.all()
        reports = []
        for r in rep:
            if r.Patient == Treat.Patient:
                reports.append(r)
        if Treat.Doctor != request.user.Doctor or Treat.is_completed or Treat.is_new:
            return HttpResponseRedirect(reverse("index"))

        return render(request, 'Users/Treatment.html',{
            'Treatment' : Treat,
            'files' : reports,
            'Q_Form' : Q_Form,
            "A_Form" : A_Form,
            "Appoint_Form" : Appoint_Form
        })
    else:
        rep = Treat.Doctor.Reports.all()
        reports = []
        for r in rep:
            if r.Patient == Treat.Patient:
                reports.append(r)
        # reports = Reports.objects.filter(Patient=request.user.Patient)
        if Treat.Patient != request.user.Patient or Treat.is_new:
            return HttpResponseRedirect(reverse("index"))

        return render(request, 'Users/Treatment.html',{
            'Treatment' : Treat,
            'files' : reports,
            'Q_Form' : Q_Form,
            "A_Form" : A_Form,
            "Appoint_Form" : Appoint_Form
        })


@login_required()
def delete_Treat(request, nums):
    t = Treatment.objects.get(pk=nums)
    print(nums)
    if t.Patient != request.user.Patient:
        return HttpResponseRedirect(reverse("View_Treatment"))

    t.delete()
    return HttpResponseRedirect(reverse("View_Treatment"))

@login_required()
def delete_report(request, nums):
    rep = Reports.objects.get(pk=nums)
    if rep.Patient != request.user.Patient:
        return HttpResponseRedirect(reverse("reports"))

    rep.delete()
    return HttpResponseRedirect(reverse("reports"))


@login_required()
def Complete_Treat(request, nums):
    if request.method == "POST":
        t = Treatment.objects.get(pk=nums)
        print(nums)
        if t.Doctor != request.user.Doctor:
            pass
        else:
            t.is_completed = True
            t.is_active = False
            t.save()

    return HttpResponseRedirect(reverse("ActiveTreat"))


@login_required()
def not_new(request, nums):
    if request.method == "POST":
        t = Treatment.objects.get(pk=nums)
        print(nums)
        if t.Doctor != request.user.Doctor:
            pass
        else:
            t.is_new = False
            if "Accept" in request.POST:
                t.is_active = True
            t.save()

    return HttpResponseRedirect(reverse("NewTreat"))


@login_required()
@patient_required
def View_Treatment(request):
    Treatments = Treatment.objects.filter(Patient=request.user.Patient)

    active = []
    new = []
    rejected = []
    completed = []

    for t in Treatments:
        if t.is_active:
            active.append(t)
        elif t.is_new:
            new.append(t)
        elif t.is_completed:
            completed.append(t)
        else:
            rejected.append(t)
    return render(request, 'Users/Treat.html', {
        'active': active,
        'new': new,
        'rejected': rejected,
        "completed": completed
    })


@login_required()
@patient_required
@require_http_methods(["POST"])
def send(request, nums):
    if request.method == "POST":
        files = Reports.objects.get(pk=nums)
        if files.Patient != request.user.Patient:
            return HttpResponseRedirect(reverse("index"))
        docs = request.POST.getlist(f'file_{nums}')

        for id in docs:
            if all(int(id) != doc.id for doc in files.Doctors.all()):
                d = Doctor.objects.get(pk=id)
                files.Doctors.add(d)

        for doc in files.Doctors.all():
            if str(doc.id) not in docs:
                d = Doctor.objects.get(pk=doc.id)
                files.Doctors.remove(d)
        messages.success(request, 'Changed sharing access Successfully')
        return HttpResponseRedirect(reverse("reports"))


@login_required()
@patient_required
def showfile(request):
    form = FileForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save(request.user)  # replace by patient

    lastfile = Reports.objects.filter(Patient=request.user.Patient)

    send_form = send_to_doc_Form(request.user.Patient)

    context = None
    if lastfile:
        context = {
            'form': form,
            'lastfile': lastfile,
            'Send': send_form
        }

    if not context:
        context = {
            'form': form,
            'Send': send_form
        }

    return render(request, 'Users/files.html', context)


def rform(request, num):
    if (num == 1):
        form = Register_Patient()
    else:
        form = Register_Doc()

    return render(request, 'Users/form.html', {
        "form": form
    })


def index(request):
    return render(request, "Users/index.html", )


def email_forgot(request):
    if request.method == "POST":
        form = Forgot_email_form(request.POST)
        email = form.data.get("email").lower()
        u = User.objects.filter(email=email).first()

        if u is not None:
            current_site = get_current_site(request)
            send_email(current_site, u, mess="reset your Password", link="Forgot", subj="Reset Password")
            logout(request)
            return render(request, "Users/confirmation.html", {
                "message": "Change you password by email sent ",
                "u": u,
            })
        else:
            return render(request, "Users/forgot.html", {
                "message": "Forgot Password",
                "form": form,
                "name": "Send Email",
                "error": "Email Doesnot Exists"
            })

    form = Forgot_email_form()
    return render(request, "Users/forgot.html", {
        "message": "Forgot Password",
        "form": form,
        "name": "Send Email"
    })


def Forgot(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        if request.method == "POST":
            form = Forgot_Password_Form(request.POST)
            if not form.is_valid() or form.data.get('password1') != form.data.get('password2'):
                return render(request, "Users/forgot.html", {
                    "message": "Change Passsword",
                    "form": form,
                    "name": "Change Password",
                    "error": "Password Should Match"
                })
            else:
                user.set_password(form.data.get('password1'))
                user.save()
                return HttpResponseRedirect(reverse("login"))

        else:
            form = Forgot_Password_Form()
        return render(request, "Users/forgot.html", {
            "message": "Change Passsword",
            "form": form,
            "name": "Change Password",
        })
    else:
        return render(request, "Users/confirmation.html", {
            "message": "Link is invalid!"
        })


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        log = LoginUserForm(request.POST)
        email = log.data.get("email").lower()
        password = log.data.get("password")
        user = authenticate(request, email=email, password=password)
    
        # Check if authentication successful
        if user is not None:
            if not user.is_active:
                logout(request)
                return render(request, "Users/login.html", {
                    "message": "Please confirm your email address to complete the registration",
                    "next": request.POST["next"],
                    "login": log
                })
            login(request, user)
            link = request.POST["next"]
            if link != "None":
                return HttpResponseRedirect(link)
            return HttpResponseRedirect(reverse("base"))
        else:
            return render(request, "Users/login.html", {
                "message": "Invalid username and/or password.",
                "next": request.POST["next"],
                "login": log
            })
    else:
        log = LoginUserForm()
        if "next" in request.GET:
            url = request.GET["next"]
        else:
            url = None
        return render(request, "Users/login.html", {
            "next": url,
            "login": log,
        })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def reg(request):
    reg = RegisterUserForm()
    form = Register_Patient()
    return render(request, "Users/registerDoctor.html", {
        "register": reg,
        "form": form,
    })


def register(request):
    if request.method == "POST":
        reg = RegisterUserForm(request.POST)
        email = reg.data.get("email").lower()
        form = Register_Patient(request.POST)
        # Ensure password matches confirmation
        password = reg.data.get("password1")
        confirmation = reg.data.get("password2")
        if not reg.is_valid() or password != confirmation:
            return render(request, "Users/registerDoctor.html", {
                "message": "Passwords must match.",
                "form": form,
                "register": reg
            })
        if not form.is_valid():
            return render(request, "Users/registerDoctor.html", {
                "form": form,
                "register": reg,
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, password, is_active=False,
                                            is_patient=True)  ### change is active to false
            user.save()
            p = form.save(commit=False)
            p.user = user
            p.save()
            current_site = get_current_site(request)
            send_email(current_site, user, p.Name)
            logout(request)
            return render(request, "Users/confirmation.html", {
                "message": "Confirm your email",
                "u": user,
            })
        except IntegrityError:
            return render(request, "Users/registerDoctor.html", {
                "message": "Username already taken.",
                "form": form,
                "register": reg
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))


def register_Doctor(request):
    if request.method == "POST":
        form = Register_Doc(request.POST)
        reg = RegisterUserForm(request.POST)
        if not reg.is_valid():
            print("h")
            return render(request, "Users/registerDoctor.html", {
                "form": form,
                "d": True,
                "register": reg
            })
        email = reg.data.get("email").lower()
        # Ensure password matches confirmation
        password = reg.data.get("password1")
        confirmation = reg.data.get("password2")
        if password != confirmation:
            return render(request, "Users/registerDoctor.html", {
                "message": "Passwords must match.",
                "form": form,
                "d": True,
                "register": reg
            })
        if not form.is_valid():
            print("h11")
            return render(request, "Users/registerDoctor.html", {
                "form": form,
                "d": True,
                "register": reg
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email, password, is_active=False,
                                            is_doctor=True)  ### change is active to false
            user.save()
            d = form.save(commit=False)
            d.user = user
            d.save()
            current_site = get_current_site(request)
            send_email(current_site, user, d.Name)
            logout(request)
            return render(request, "Users/confirmation.html", {
                "message": "Confirm your email",
                "u": user,
            })
        except IntegrityError:
            return render(request, "Users/registerDoctor.html", {
                "message": "Username already taken.",
                "form": form,
                "d": True,
                "register": reg
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    return HttpResponseRedirect(reverse("index"))


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        # return redirect('home')
        return render(request, "Users/confirmation.html", {
            "message": "Thank you for your email confirmation. Now you can login your account."
        })
    else:
        return render(request, "Users/confirmation.html",{
                "message" : "Activation link is invalid!" 
            })
    

def base(request):
    return render(request,'Users/base.html')

def about(request):
    return render(request,'Users/about.html')

def describe_prediction(request):
    return render(request,'Users/describe_prediction.html')

def describe_doctor(request):
    return render(request,'Users/describe_doctor.html')

def describe_report(request):
    return render(request,'Users/describe_report.html')

def describe_prescription(request):
    return render(request,'Users/describe_prescription.html')


# @api_view(["POST"])
def mydisease(df):
    try:
        y_pred=[]
        # print("1")
        mdl_mnb = joblib.load('Users/disease_mnb.pkl')
        # print("2")
        mdl_log = joblib.load('Users/disease_log.pkl')
        # print("3")
        mdl_ran = joblib.load('Users/disease_ran.pkl')
        # # print("4")
        mdl_dt = joblib.load('Users/disease_dt.pkl')
        # print("5")
        p1=mdl_mnb.predict(df.iloc[:, :132])
        p2=mdl_log.predict(df.iloc[:, :132])
        p3=mdl_ran.predict(df.iloc[:, :132])
        p4=mdl_dt.predict(df.iloc[:, :132])
        y_pred.append(p1[0])
        y_pred.append(p2[0])
        y_pred.append(p3[0])
        y_pred.append(p4[0])
        c=Counter(y_pred)
        max=0
        idx=0
        c=c.most_common()
        for itr in c:
            if itr[1]>max:
                max=itr[1]
                idx=itr[0]
        if (max==2 and len(c)==2) or max==1:
            print(idx)
            return(p4[0])
        else:
            return idx
    except ValueError as e:
        print(e)
        return Response(e.args[0], status.HTTP_400_BAD_REQUEST)
