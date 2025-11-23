from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import logout, login
from .models import CustomUser, Staffs, Students, AdminHOD
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.views.generic import View
from User_app.forms import RegisterForm, Loginform
from django.contrib.auth import authenticate, login


# regiter view for three typee of user

class UserRegisterView(View):

    def get(self,request):

        form = RegisterForm()

        return render(request,'register.html',{'form':form})


    def post(self,request):
        
        form = RegisterForm()

        email = request.POST.get('email')
        password = request.POST.get('password1')
        username= request.POST.get('username')
        
    
        

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'User with this email already exists. Please login.')
            return render(request,'register.html',{'form':form})

        user_type = get_user_type_from_email(email)

        if user_type is None:
            messages.error(request, "Email must be like: 'john.student@college.com', 'rahul.staff@institute.edu' or 'principal.hod@university.org'")
            return render(request,'register.html',{'form':form})

        username = email.split('@')[0].split('.')[0]

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'User with this username already exists. Please choose a different email.')
            return render(request,'register.html',{'form':form})

        user = CustomUser()
        user.username = username
        user.email = email
        
        user.user_type = user_type
        user.set_password(password) 
        user.save()

        if user_type == CustomUser.STAFF:
            Staffs.objects.create(admin=user)
        elif user_type == CustomUser.STUDENT:
            Students.objects.create(admin=user)
        elif user_type == CustomUser.HOD:
            AdminHOD.objects.create(admin=user)

        messages.success(request, "Registration successful. Please log in.")
        return redirect('login')

# email verify with usertype 

def get_user_type_from_email(email):
        try:
            email_user_type = email.split('@')[0].split('.')[1]
            return CustomUser.EMAIL_TO_USER_TYPE_MAP[email_user_type]
        except:
            return None    
        


# login view for three typee of user

class LoginView(View):

    template_name = "login.html"

    def get (self,request):

        form = Loginform()

        return render (request,self.template_name,{'form':form})

    def post (self,request):

        form = Loginform(request.POST)

        if form.is_valid():

            print(form.cleaned_data)

            username = request.POST.get('username')

            password = request.POST.get('password')


            user = authenticate(request, username=username, password=password)

            

            if user is not None:
                login(request, user)

                # Redirect based on user type
                if user.user_type == CustomUser.HOD:
                    return redirect("hod_dashboard")
                elif user.user_type == CustomUser.STAFF:
                    return redirect("staff_dashboard")
                elif user.user_type == CustomUser.STUDENT:
                    return redirect("student_dashboard")
                
              

            else:

                messages.error(request, 'Invalid username or password.')
                return render(request, self.template_name, {
                    "form": form
                })

        return render(request, self.template_name, {"form": form})
    


# user_app/views.py 

from django.http import HttpResponse

class Hod_dashboard(View):

    def get(self,request):

        print('wellcome to hod dashboard')

        return HttpResponse("Welcome HOD Dashboard")


class Staff_dashboard(View):

    def get(self,request):

        return HttpResponse('Welcome Staff Dashboard')

class Student_dashboard(View):

    def get(self,request):

        return HttpResponse('Welcome Student Dashboard')




# logout View

class LogoutView(View):

    def get(self,request):

        logout(request)

        return render(request,'register.html')
    

# base View

class Baseview(View):

    def get (self, request):

        return render(request,'home.html')