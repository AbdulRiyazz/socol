from django.shortcuts import render,redirect
from app.models import Post, User 
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from app.models import account_profile

# Create your views here.
@login_required(login_url="signin")
def home (request):
    user_object=User.objects.get(username=request.user.username)
    user_profile=account_profile.objects.get(user=user_object)
    posts=Post.objects.all()
    
    return render(request,"index.html",{'user_profile':user_profile, 'posts':posts  })

@login_required(login_url="signin")
def user_bio (request):
    user_profile=account_profile.objects.get(user=request.user)
    if request.method=='POST':

        if request.FILES.get('image')==None:
            image=user_profile.profile_image
            bio=request.POST['bio']
            location=request.POST['location']

            user_profile.bio=bio
            user_profile.profile_image=image
            user_profile.location=location
            user_profile.save()


        if request.FILES.get('image')!=None:
            image=request.FILES.get('image')
            bio=request.POST['bio']
            location=request.POST['location']

            user_profile.bio=bio
            user_profile.profile_image=image
            user_profile.location=location
            user_profile.save()   
        return redirect(user_bio)     

    else:
        return render (request,"setting.html",{'user_profile':user_profile})

def sign_up (request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']

        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,"E-mail is already taken")
                return redirect ('sign_up')
            elif User.objects.filter(username=username).exists():
                messages.info(request,"username is already taken")
                return redirect ('signup')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()

            
                user_model=User.objects.get(username=username)
                profile=account_profile.objects.create(user=user_model,id_user=user_model.id)
                profile.save()
                return redirect('signin')

        else:
            messages.info(request,"password is not matching")
            return redirect ('signup') 
               
    else:
        return render(request,"signup.html")
    
def signin (request): 

    if request.method=="POST":
        username=request.POST['Username']
        password=request.POST['password']

        user =auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        
        else:
            messages.info(request,"user and password doesn't exist ")
            return redirect("signin")
        
    else:
        return render(request,"signin.html")

@login_required(login_url="signin")
def logout (request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url="signin")
def upload (request):
    if request.method =="POST":
        user=request.user.username
        image=request.FILES.get('image')
        caption=request.POST['caption'] 

        post=Post.objects.create(user=user,image=image,caption=caption)
        post.save()

        return redirect ('home')
    else:
        return redirect('home')
        