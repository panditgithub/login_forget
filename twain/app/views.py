from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import *
from .forms import *
import random
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate, logout
from django.views.generic.edit import DeleteView
from django.contrib import messages
from .task import *
from .ipaddress import get_client_ip
from django.shortcuts import render, redirect,HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test
from .decorators import *
import datetime
from django.db.models import Q
from django.core.paginator import Paginator ,EmptyPage, PageNotAnInteger
from .filters import *
# from .models import *
def loan(request):
    user=User.objects.get(pk=request.user.id)
    return render (request,'loan.html')


def user_register(request):

    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
    
        password = request.POST['password_original']
        type = request.POST['radio']
        password_confirm = request.POST['password_confirm']
        if password == password_confirm:
            if User.objects.filter(username1 = username).exists() or User.objects.filter(email = email).exists():
     
                error_message=''
                email_error=('','Email is taken.')[User.objects.filter(email = email).exists():]
                username_error=('','Username is taken.')[User.objects.filter(username1 = username).exists():]
                error_message = email_error + username_error
                messages.success(request, error_message)
                return redirect('register')
     
            else:
                if type == 'costomer':
                    user = User.objects.create_user(email = email,username1 =username, password = password)
                    user.is_costomer = True
                    user.save()
                    otp = random.randint(100000, 999999)
                    otpmodel = OTPModel(user=user, otp=otp)
                    otpmodel.save()
                    send_otp_with_celery.delay(email,otp)
                    subject = "OTP Verification From Digibuddies"
                    message = f"Your OTP for Account Verification in Digibuddies is {otp}"
                    send_mail(subject, message, 'b9c043482eca45', [email], fail_silently=False)
                    return redirect('verify')
                elif type == 'dealer':
                    user = User.objects.create_user(email = email, username1 =username, password = password)
                    user.is_dealer = True
                    user.save()
                    otp = random.randint(100000, 999999)
                    otpmodel = OTPModel(user=user, otp=otp)
                    otpmodel.save()
                    send_otp_with_celery.delay(email,otp)
                    subject = "OTP Verification From Digibuddies"
                    message = f"Your OTP for Account Verification in Digibuddies is {otp}"
                    
     
                    send_mail(subject, message, 'b9c043482eca45', [email], fail_silently=False)
                    return redirect('verify')
                
                else:
                    pass
                return redirect('register')
        else:
            messages.info(request, 'password is not a match')
            return redirect ('register')
                
                
        
    else:
        # messages.info(request, 'password is not a match')
        return render(request, 'mainapp/signup.html')
    
@profile_required
def client_home(request):
    user = User.objects.get(pk=request.user.id)
            
    profile_type = 'dealer'
    dealer = DealerProfileModel.objects.get(user=user.id)
    today=datetime.datetime.now().date()
    
    try:
        posted_jobs = PostjobModel.objects.filter(Q(dealer=dealer) & Q(deadline__gte = today))
        try:
            completed_jobs=PostjobModel.objects.filter(dealer=dealer,is_completed=True)
        except:
            completed_jobs=""

    except:
        posted_jobs = None
    page_num = request.GET.get('page1', 1)
    paginator = Paginator(posted_jobs,3)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.page_num)
    
    try:
        in_progress=BidAmountModel.objects.filter(job__in=posted_jobs,is_accepted=True,job__is_completed=False)
        print(in_progress)
    except:
        in_progress={}
    unassigned={}
    try:
        is_bidded=BidAmountModel.objects.filter(job__in=posted_jobs,is_accepted=True).values('job_id')
        print(is_bidded)
        unassigned=PostjobModel.objects.exclude(id__in=is_bidded).filter(dealer=dealer)
        print(unassigned)


    except:
        unassigned={}
    
    try: 
        rejected=BidAmountModel.objects.filter(job__in=posted_jobs,is_rejected=True)
    except:
        rejected={}

    return render(request, 'mainapp/client_home.html', {
        'completed_jobs':completed_jobs,
        'in_progress':in_progress,
        'profile_type': profile_type,
        'seller':dealer,
        'posted_jobs':posted_jobs,
        'unassigned':unassigned,
        'rejected':rejected,
        'page_obj':page_obj
        }
    )

def index(request):

    ip=get_client_ip(request)
    print(ip)
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)
         
        # dashboard for seller or client
        if user.is_dealer:
            return redirect("client_home")
            
           
        elif user.is_costomer:
            return redirect('home')
       
            

        else:
            return redirect('profiletype')
    category = []
    categories = JobCategoryModel.objects.all()
    for i in categories:
        print(i)
        post = PostjobModel.objects.filter(category_type = i)
        no_of_jobs = post.count()
        category.append({'cat':i, 'post':no_of_jobs})
    print (category)
    context = {
        'costomer': CostomerProfileModel.objects.all(),
    'dealer':DealerProfileModel.objects.all(),
    'categories': categories,
    'category':category,
    'skills' : SkillModel.objects.all(),   
    'jobs' : PostjobModel.objects.all()
    }
    return render(request, 'mainapp/new_index.html', context= context)


"""-----------this function is only for testing if status of page is successful or not-----------"""

def success_func(request):
    # user = User.objects.get()
    return render (request, 'mainapp/success.html')


"""-----------view for sending the otp to the mail and verify it-----------"""

def verify_email(request):
    
    if request.method == 'POST':
        otp = request.POST['otp']
        otpuser = OTPModel.objects.filter(otp=otp).first()
        
        if otpuser is not None:
            user = User.objects.get(pk=otpuser.user.id)
            user.is_verified = True
            user.save()
            otpuser.delete()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            # if user.is_dealer:
            #     return redirect('selleradd')
            # elif user.is_costomer:
            #     return redirect('buyeradd')
            if user.is_dealer:
                return redirect('login')
            elif user.is_costomer:
                return redirect('login')
        else:
            messages.error(request,'OTP is incorrect.')
            return render(request, 'mainapp/otp_verification.html')
    return render(request, 'mainapp/otp_verification.html')

def Login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        try:
            user = User.objects.get(username1=username)
        except:
            try:
                user = User.objects.get(email=username)
            except:
                user=None

        
        if user is not None:
            if user.check_password(password):
            
                if user.is_verified:
                    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                    if not(user.is_dealer or user.is_costomer):
                        return redirect('profiletype')
                    return redirect('/')
                else:
                    userotp = OTPModel.objects.filter(user=user)
                    if userotp:
                        userotp.delete()
                    otp = random.randint(100000, 999999)
                    otpmodel = OTPModel(user=user, otp=otp)
                    otpmodel.save()
                    send_otp_with_celery.delay(username,otp)
                    return redirect('verify')
            else:
                messages.error(request,'Please check your username and password')
        else:
            error = 'Please Check your email/password'
            return render(request, 'mainapp/signin.html', {'error': error})
    # if seller is  None:
    #             return redirect('register')

    return render(request, 'mainapp/signin.html')

def signout(request):
    logout(request)
    return redirect('login')

def forgetpassword(request):

    if request.method=="POST":
        username = request.POST.get("username")
        try:
            user = User.objects.get(email=username)
        except:
            user=""
        if user:
            otp = random.randint(100000, 999999)
            otpmodel = OTPModel(user=user, otp=otp)
            otpmodel.save()
            send_otp_with_celery.delay(username,otp)
            subject = "OTP Verification From Digibuddies"
            message = f"Your OTP for Account Verification in Digibuddies is {otp}"
            send_mail(subject, message, 'b9c043482eca45', [username], fail_silently=False)
            print("pass")
            return render(request,'mainapp/verification.html',{'user':user})
    
        else:
            print("fail")
            messages.error(request,"email Doesn't match")
    
    return render(request,'mainapp/forget.html')

def verify_forget_email(request):
    
    if request.method == 'POST':
        otp = request.POST['otp']
        user = request.POST['user']
        otpuser = OTPModel.objects.filter(otp=otp).first()
        print(otpuser)
        
        if otpuser is not None:
            otpuser.delete()
            return render(request,"mainapp/reset-password.html",{'user':user})
        else:
            print("fail")
    return render(request, 'mainapp/verification.html')

def resetnewpassword(request):
    if request.method == 'POST':
        password = request.POST.get("password")
        password1 = request.POST.get("password1")
        user=request.POST.get('user')
        usern=User.objects.get(email=user)
        print(usern)
        if password==password1:
            usern.set_password(password1)
            usern.save()
            return render(request,"mainapp/set-new-password.html")
        else:
            messages.error("password doesn't match")
        
           
    return render(request,'mainapp/reset-password.html',)



"""-----------view for registering the user as a buyer or freelancer-----------"""

@login_required
def buyer_form_view(request):
    # user = User.objects.get(pk=request.user.id)
    # buyer = BuyerProfileModel.objects.get(user=user)
    
    if request.method == 'POST':
        
        if request.user.is_authenticated:
            form =CostomerForm(request.POST, request.FILES)    
            if form.is_valid():
                profile_desc = form.cleaned_data['profile_desc']
                #linkedin_profile = form.cleaned_data['linkedin_profile']
                #github_profile = form.cleaned_data['github_profile']
                profile_picture = form.cleaned_data['profile_picture']
                resume = form.cleaned_data['resume']
                city = form.cleaned_data['city']
                state = form.cleaned_data['state']
                category = form.cleaned_data['category']
                country = form.cleaned_data['country']
                gender = request.POST['gender']
                #skills = request.POST.getlist('skills')
                long_description = form.cleaned_data['long_description']
                user = request.user
                buyer = CostomerProfileModel(user=user, category = category, profile_desc=profile_desc, 
                city=city, state=state, country=country, profile_picture=profile_picture, resume=resume, gender=gender, long_description=long_description)
                buyer.save()
                user_data = User.objects.get(pk=request.user.id)
                #user.is_buyer = True
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                user_data.first_name = first_name
                user_data.last_name = last_name
                user_data.save()
                return redirect('index')
            else:
                print(form.errors)
            
    
    else:
        form = CostomerForm()
    return render(request, 'freelancer/freelancer_form.html', {'form': form })

@login_required
# @profile_required
#rewite seller_form_view with cleaner code and remove commented code
#if request is not post return the form so taht user can fill it
# #if request is post then check if user is authenticated
# #if user is authenticated then get the form data and save it
# #if user is not authenticated then redirect to login page
def seller_form_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = User.objects.get(pk=request.user.id)
            try:
                seller = DealerProfileModel.objects.get(user=user)
           
                form = DealerForm(request.POST, request.FILES, instance=seller)
            except:
                seller = None
                form = DealerForm(request.POST, request.FILES)
                print(request.POST)
            if form.is_valid():
                ab = form.save(commit=False)
                user.first_name = request.POST.get('first_name')
                user.last_name = request.POST.get('last_name')
                user.save()
                ab.user = user
                ab.save()
                return redirect('index')
        else:
            return redirect('login')
    else:
        form = DealerForm()
    return render(request, 'client/client_form.html', {'form':form})

@login_required
@seller_role_required
def post_job_view(request):
    user = User.objects.get(pk=request.user.id)
    dealer = DealerProfileModel.objects.get(user=user)
    form = PostJobForm(request.POST, request.FILES)
    print(request.POST)
    print(request.FILES)  
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.id)
        dealer = DealerProfileModel.objects.get(user=user)
        title=request.POST['job_title']
        short_desc=request.POST['short_desc']
        skill_list=request.POST.getlist('skill_type')
        job_ki_type=request.POST['job_type']
        job = JobTypeModel.objects.get(job_type_title = job_ki_type)
        print(job)
        category_type=request.POST['category_type']
        cat = JobCategoryModel.objects.get(id=category_type)
        print(cat)
        deadline=request.POST['deadline']
        amount=request.POST['askamount']
        amount_2=request.POST['askamount_2']
        long_desc=request.POST['full_desc']
        try:
            file_upload=request.FILES['file_upload']
        except:
            file_upload={}
        
        job = PostjobModel(dealer = dealer, job_title=title, short_desc=short_desc, job_type=job, 
                        category_type=cat, deadline=deadline, askamount=amount, askamount_2=amount_2,
                        file_upload=file_upload, full_desc=long_desc )
        job.save()
        skill_type_obj = SkillModel.objects.filter(skill_title__in=skill_list)
        job.skills.set(skill_type_obj)
        job.save()
        messages.success(request, "Your Profile has been Updated Successfully.")
        # return to home page 
        # 
        return redirect('index')
       
        
    else:
        form = PostJobForm()
    skill_type = SkillModel.objects.all()
    job_t = JobTypeModel.objects.all()
    return render(request, 'client/Post_A_Job.html', {'form':form, 'skill_type':skill_type, 'job':job_t,
                                                      'seller':dealer})



@profile_required
def product_filters(request):
    user = User.objects.get(pk=request.user.id)
    costomer = CostomerProfileModel.objects.get(user=user)
    today = datetime.datetime.now().date()
    # myt = PostjobModel.objects.filter(is_completed=False)
    complete=BidAmountModel.objects.filter(is_accepted=True).values('job_id')
    print(complete)
    myt=PostjobModel.objects.filter(is_completed=False,deadline__gte=today).exclude(id__in=complete)
    val=PostjobModel.objects.filter(is_completed=False).exclude(id__in=complete).values("id")
    print(val)
    
    page_num = request.GET.get('page', 1)
    paginator = Paginator(myt,4)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.page_num)
    abc = alljobfilter(request.GET,queryset=myt)
    hours = JobTypeModel.objects.all()
    allskill = SkillModel.objects.all()     
    prodo = abc.qs
    
    return render(request,'freelancer/freelancerhome.html',{'formfilter':myt,'prodo':prodo,
                                                  'abc':abc,
                                                  'hours':hours,'allskill':allskill,
                                                  'buyer':costomer,'complete':complete,
                                                  'page_obj':page_obj})
    
