from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login",views.login_view,name="login"),
    path("logout", views.logout_view, name="logout"),
    path("rform/<int:num>",views.rform,name="rform"),
    path("reg", views.reg, name="reg"),
    path("register", views.register, name="register"),
    path("registerD", views.register_Doctor, name="registerDoctor"),
    path("reports", views.showfile, name="reports"),
    path("View_Treatment",views.View_Treatment, name = "View_Treatment"),

    path('activate/<slug:uidb64>/<slug:token>',views.activate, name='activate'),
    path("send/<int:nums>",views.send,name="send"),
    path("NewTreat",views.view_new_treatments,name="NewTreat"),
    path("ActiveTreat",views.view_active_treatments,name="ActiveTreat"),
    path("Treat/<int:nums>",views.Treats,name="Treat"),
    path("Email_Forget",views.email_forgot,name="Email_Forget"),

    path('Forgot/<slug:uidb64>/<slug:token>',views.Forgot,name="Forgot"),

    path("Edit_profile",views.Edit_profile,name="Edit_profile"),
    path("Change_Password",views.Change_Password,name="Change_Password"),
    path("delete_Treatment/<int:nums>",views.delete_Treat,name="Delete_Treatment"),
    path("Complete_Treatment/<int:nums>",views.Complete_Treat,name="Complete_Treatment"),
    path("not_new/<int:nums>",views.not_new,name="not_new"),
    path("edit_Presc/<int:nums>",views.edit_Presc,name="edit_Presc"),
    path("Doctor_list/<int:nums>",views.Doctor_list,name="Doctor_list"),
    path("create_Treat",views.create_Treat,name="create_Treat"),
    path("Add_doc/<int:T_id>/<int:D_id>",views.Add_doc,name="Add_doc"),

    path("base",views.base, name = "base"),
     path("about",views.about, name = "about"),
    path("describe_prediction",views.describe_prediction, name = "describe_prediction"),
    path("describe_doctor",views.describe_doctor, name = "describe_doctor"),
    path("describe_report",views.describe_report, name = "describe_report"),
    path("describe_prescription",views.describe_prescription, name = "describe_prescription"),


    path("Add_Question/<int:nums>/",views.Add_Question,name="Add_Question"),
    path("Add_Answer/<int:nums>/<int:Q_id>",views.Add_Answer,name="Add_Answer"),
    path("delete_Question/<int:nums>/",views.delete_Question,name="delete_Question"),
    path("Add_Appointment/<int:nums>/",views.Add_Appointment,name="Add_Appointment"),
    path("delete_report/<int:nums>/",views.delete_report,name="delete_report"),
    

]