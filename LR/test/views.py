from pyexpat.errors import messages
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from test.form import CustomUserCreationForm
from django.contrib import messages   

# from .utils import generate_otp, send_otp_email
from .models import CustomUser

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str  # Update the import statement
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import send_mail


def verification_pending(request):
    return render(request, 'verification_pending.html') 

def verification_email(request):
    return render(request, 'verification_email.html') 

def verification_failed(request):
    return render(request, 'verification_failed.html') 

def home(request):
    # Your view logic here
    return render(request, 'login.html')

def index(request):
    # Your view logic here
    # For example, fetching data from a databa

    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print('username',username)
        print('password',password)
        user = authenticate(request, username=username, password=password)
        print('user',user)
        if user is not None:
           
           auth_login(request, user)
           print('Successfully logged in')
           print('User:', user)  # Print user information for debugging
           return redirect('index')
        else:
         messages.error(request, 'Wrong username or password.')

    return render(request, 'login.html', {'messages': messages.get_messages(request)})

def signup(request):
    error_message = ""

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Check if the username is valid
           username = form.cleaned_data['username']
           if len(username) <= 1:
            form.add_error('username', 'Username must be longer than one character.')
           else:
                user = form.save(commit=False)
                user.is_active = False  # User is not active until email is verified
                user.save()

                # Generate email verification token
                token = default_token_generator.make_token(user)

                # Send verification email
                current_site = get_current_site(request)
                verification_link = f"http://{current_site.domain}/verify/{urlsafe_base64_encode(force_bytes(user.pk))}/{token}/"
                subject = 'Activate Your Account'
                message = render_to_string('verification_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'verification_link': verification_link,  # Pass the verification link to the template
                })
                send_mail(subject, message, 'pbhujel115@gmail.com', [user.email])

                return redirect('verification_pending')  # Show a page indicating verification is pending
        else:
            # Get form errors and display them in the error_message
            error_message = "\n".join([f"{field}: {', '.join(errors)}" for field, errors in form.errors.items()])
            print(form.errors)  # Print form errors
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'signup.html', {'form': form, 'error_message': error_message})

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user)  # Use the correct login function from django.contrib.auth
        
        # Add a success message
        messages.success(request, 'Email verified')
        
        return redirect('login')  # Redirect to the login page
    else:
        return render(request, 'verification_failed.html')
        
    # def signup(request):
#     error_message = ""

#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             # Check if the passwords match
#             if form.cleaned_data['password1'] == form.cleaned_data['password2']:
#                 user = form.save()  # Save the user data to the database
#                 auth_login(request, user)  # Automatically log in the user
#                 return redirect('login')  # Redirect to the dashboard or profile page
#             else:
#                 error_message = "Passwords do not match."
#         else:
#             print(form.errors)  # Print form errors
#     else:
#         form = CustomUserCreationForm()
    
#     return render(request, 'signup.html', {'form': form, 'error_message': error_message})





# def send_otp(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         user = CustomUser.objects.get(email=email)
#         otp = generate_otp()
#         user.otp = otp  # Save OTP to user model field
#         user.save()
#         send_otp_email(user, otp)
#         return redirect('verify_otp')

#     return render(request, 'send_otp.html')

# def verify_otp(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         otp_entered = request.POST.get('otp')
#         user = CustomUser.objects.get(email=email)
#         if otp_entered == user.otp:
#             user.password_correct = True
#             user.save()
#             return redirect('login')
    
#     return render(request, 'verify_otp.html')