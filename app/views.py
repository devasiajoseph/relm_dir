# Create your views here.
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.db import transaction
from app.forms import CreateUserForm, LoginForm, PasswordEmailForm,\
PasswordEmailForm, SellerRequestForm, SellerSignUpForm
from app.models import UserProfile, Country, SellerRequest
from app.utilities import reply_object, create_key
import simplejson
import datetime


def index(request):
    return render_to_response("index.html",
                              context_instance=RequestContext(request))


def home(request):
    """
    Home page after logging in
    """
    if request.user.is_authenticated():
        return render_to_response("home.html",
                                  context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('login'))


def user_register(request):
    """
    Registration page
    """
    form = CreateUserForm()
    return render_to_response(
        "register.html",
        context_instance=RequestContext(request, {"user_form": form}))


def add_user(request):
    """
    Registration request handler
    """
    response = reply_object()
    form = CreateUserForm(request.POST)
    if form.is_valid():
        response = form.save_user()
        response["success_page"] = reverse('registration_success')
    else:
        response["code"] = settings.APP_CODE["FORM ERROR"]
        response["errors"] = form.errors
    return HttpResponse(simplejson.dumps(response))


def registration_success(request):
    return render_to_response('registration_success.html',
                              context_instance=RequestContext(request,
                {"activation_email": settings.EMAIL_VERIFICATION_REQUIRED}))


def user_login(request):
    """
    Login page
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    form = LoginForm(request=request)
    return render_to_response("login.html",
            context_instance=RequestContext(request,
                {"login_form": form}))


def login_user(request):
    """
    Login request handler
    """
    response = reply_object()
    form = LoginForm(request.POST, request=request)

    if form.is_valid():
        response["code"] = settings.APP_CODE["LOGIN"]
        response["next_view"] = reverse('home')
    else:
        response["code"] = settings.APP_CODE["FORM ERROR"]
        response["errors"] = form.errors

    return HttpResponse(simplejson.dumps(response))


def user_logout(request):
    """
    Logout request
    """
    # Logout function flushes all sessions.Save session variables to a local
    # variable for reuse
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def activate(request, verification_key):
    """
    New account activation function
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    user_profile = get_object_or_404(UserProfile,
                                     verification_key=verification_key)
    naive_date = user_profile.key_expires.replace(tzinfo=None)
    if naive_date < datetime.datetime.today():
        return render_to_response('expired.html',
                                  context_instance=RequestContext(request))
    user_account = user_profile.user
    user_account.is_active = True
    user_account.save()
    #remove activation key once account is activated
    user_profile.verification_key = ""
    user_profile.save()
    return render_to_response('activated.html',
                              context_instance=RequestContext(request))


def password_reset(request):
    """
    Password reset step1
    """
    reset_form = PasswordEmailForm()

    return render_to_response('password_reset.html',
                                  context_instance=RequestContext(
            request, {"reset_form": reset_form}))


def password_reset_submit_email(request):
    response = reply_object()
    form = PasswordEmailForm(request.POST)
    if form.is_valid():
        response = form.send_reset_link()
    else:
        response["code"] = settings.APP_CODE["FORM ERROR"]
        response["errors"] = form.errors

    return HttpResponse(simplejson.dumps(response))


def password_reset_form(request, verification_key):
    """
    Password reset form
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    user_profile = get_object_or_404(UserProfile,
                                     verification_key=verification_key)
    naive_date = user_profile.key_expires.replace(tzinfo=None)
    if naive_date < datetime.datetime.today():
        return render_to_response('expired.html',
                                  context_instance=RequestContext(request))

    user_account = user_profile.user
    temp_password = create_key(user_account.username, 2)
    user_account.set_password(temp_password)
    user_account.save()
    user = authenticate(username=user_account.username, password=temp_password)
    if user is not None:
        if user.is_active:
            login(request, user)
        else:
            return HttpResponse("This account is inactive.")
    #remove reset key
    user_profile.verification_key = ""
    user_profile.save()
    reset_form = PasswordResetForm()
    return render_to_response('password_reset_form.html',
                              context_instance=RequestContext(
            request, {"reset_form": reset_form}))


def password_reset_submit_password(request):
    response = reply_object()
    form = PasswordResetForm(request.POST, request=request)
    if form.is_valid():
        response = form.save_new_password()
        response["code"] = settings.APP_CODE["CALLBACK"]
        response["redirect"] = reverse('home')
    else:
        response["code"] = settings.APP_CODE["FORM ERROR"]
        response["errors"] = form.errors

    return HttpResponse(simplejson.dumps(response))


def seller_register(request):
    default_country = Country.objects.get(name="Vietnam")
    form = SellerRequestForm(initial={"country": default_country.id})
    return render_to_response(
        "seller/registration_request.html",
        context_instance=RequestContext(request,
                                        {"form": form}))


def seller_register_submit(request):
    response = reply_object()
    form = SellerRequestForm(request.POST)
    if form.is_valid():
        form.save_seller_request()
        response["code"] = settings.APP_CODE["CALLBACK"]
    else:
        response["code"] = settings.APP_CODE["FORM ERROR"]
        response["errors"] = form.errors

    return HttpResponse(simplejson.dumps(response))


def seller_signup(request, approval_key):
    seller_request = get_object_or_404(
        SellerRequest,
        approval_key=approval_key,
        status=settings.SELLER_REQUEST_STATUS["APPROVED"])
    naive_date = seller_request.key_expires.replace(tzinfo=None)
    if naive_date < datetime.datetime.today():
        return render_to_response('expired.html',
                                  context_instance=RequestContext(request))

    form = SellerSignUpForm()
    return render_to_response('seller/seller_signup.html',
                              context_instance=RequestContext(
            request, {"form": form,
                      "seller_request": seller_request}))


@transaction.commit_on_success
def seller_signup_submit(request):
    response = reply_object()
    form = SellerSignUpForm(request.POST)
    if form.is_valid():
        response = form.save_user()
    else:
        response["code"] = settings.APP_CODE["FORM ERROR"]
        response["errors"] = form.errors

    return HttpResponse(simplejson.dumps(response))
