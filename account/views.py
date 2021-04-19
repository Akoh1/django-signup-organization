from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .models import AccountUser, WorkPlace
from .forms import AdminUserForm, SingleUserForm, AccountAuthenticationForm
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError, EmailMultiAlternatives, EmailMessage
from django.conf import settings
from django.template.loader import get_template
from django.urls import reverse
# Create your views here.



def signup(request):
    context = {}
    
    if request.method == 'POST':
        adminform = AdminUserForm(request.POST or None)
        if adminform.is_valid():

            adminform.save()
            email = adminform.cleaned_data.get('email')
            raw_password = adminform.cleaned_data.get('password1')
            if email:
                htmly = get_template('account/activate_email.html')
                subject = "Test Activation email"
                d = {
                    'site_url': settings.DOMAIN_URL,
                    'email': email,
                    'url': reverse('account:activate', kwargs={"email":email})
                }
        
                from_email = settings.EMAIL_HOST_USER
                # from_email = 'akohsamuel018@gmail.com'
                html_content = htmly.render(d)   
                msg = EmailMessage(subject, html_content, from_email, [email])
                msg.content_subtype = "html" 
                try:
                    
                    msg.send()
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                messages.success(request, "An Activation email has been sent to your address, check your email to activate!")
                return redirect('account:sent-email')
            return redirect('account:activate-email', email=email)
       
        else:
            context['adminform'] = adminform
         
    else:
        adminform = AdminUserForm()
        context['adminform'] = adminform

     
    return render(request, 'account/signup.html', context)

def signup_workplace(request, workplace, email):
    workplace_id = get_object_or_404(WorkPlace, name=workplace)
    context = {'workplace': workplace_id.name,
               'email': email}

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if first_name and last_name and username and password1 and password2:
            if password1 != password2:
                messages.error(request, "Password do not match")
                return render(request, 'account/signup_workplace.html', context)
            
            AccountUser.objects.create(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                workplace_id = workplace_id,
                password = make_password(password1),
                is_staff = True,
                is_active = True
                # password2 = make_password(password2),
            )
            # account = authenticate(email=account_user.email, password=account_user.password)
            # login(request, account)
            messages.success(request, "You have successfully signed up to this workplace!")
            return redirect('account:login')
                
    
    return render(request, 'account/signup_workplace.html', context)

def login_view(request):
    context = {}
    user = request.user

    if user.is_authenticated:

        if user.workplace_id:
            return redirect('account:index', workplace=user.workplace_id)
        else:
            return redirect('account:single-index')

    if request.method == 'POST':
        form = AccountAuthenticationForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)

            if user and user.workplace_id:
                login(request, user)
                return redirect('account:index', workplace=user.workplace_id)
            elif user and not user.workplace_id:
                login(request, user)
                return redirect('account:single-index')
    else:
        form = AccountAuthenticationForm()

    context['form'] = form

    return render(request, 'account/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('account:login')

@login_required
def index(request, workplace):
    workplace = request.user.workplace_id.name
    return render(request, 'account/welcome.html', {'workplace':workplace})



def manage_users(request):
    return render(request, 'project/single_user_index.html')

def activate_email(request, email):
    user = get_object_or_404(AccountUser, email=email)
    context = {
        'site_url': settings.DOMAIN_URL,
        'user': user,
        'url': reverse('account:activate', kwargs={"email":user.email})
    }
    return render(request, 'account/activate_email.html', context)

def activate(request, email):
    # print(email)
    user = get_object_or_404(AccountUser, email=email)
    if user.is_active is False:
        user.is_active = True
        user.save()
        messages.info(request, "Your account has been activated!")
        return redirect('account:login')
    else:
        messages.info(request, "Your account has been activated already")
        return redirect('account:login')

def sent_mail(request):
    return render(request, 'account/sent_email.html')

@login_required
def invite_users(request, workplace):
    workplace_id = request.user.workplace_id.name
    if request.method == 'POST':
        get_emails = request.POST.get('emails')
        emails = get_emails.split()
        print(emails)
        from_email = request.user.email
        subject = "{} is inviting you to join its workplace".format(workplace_id)
        htmly = get_template('account/invite.html')
        
        for i in range(len(emails)):
            email = emails[i]
            print(email)
            d = {
                    'site_url': settings.DOMAIN_URL,
                    'email': email,
                    'url': reverse('account:signup-workplace', kwargs={"workplace":workplace_id,
                    'email':email})
                }
            html_content = htmly.render(d)
            msg = EmailMessage(subject, html_content, from_email, [email])
            msg.content_subtype = "html" 
            msg.send()
            messages.success(request, "You have sent an invite to {}!".format(email))
        messages.success(request, "Your invite email has been sent to the following users")
        return redirect('account:invite-users', workplace=workplace_id)
    return render(request, 'account/add_user_form.html')
 