from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django_ajax.decorators import ajax
from django.utils import timezone
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
import urllib, string, random
import onetimepass as otp

"""
index view for the home page with login and registration
"""
def index(request):
    """Renders the home page."""
    if 'message' in request.session:
        message = request.session['message']
        del request.session['message']
    if 'error' in request.session:
        message = request.session['error']
        del request.session['error']

    assert isinstance(request, HttpRequest)

    key = ''.join(random.choice(string.ascii_uppercase) for _ in range(16))
    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
            'key': key,
            'qrcode_key': qrcode(key),
            'message': message if 'message' in locals() else "",
            'error': message if 'error' in locals() else "",
        })
    )


"""
contact us page, must login to see it
"""
@login_required
def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        context_instance = RequestContext(request,
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })
    )

"""
about us page, must login to see it
"""
@login_required
def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
    )

"""
login view
"""
def login_user(request):

    if request.method == 'POST':
        #logout(request)
        username = request.POST['username']
        password = request.POST['password']
        secureKey = request.POST['secureKey']

        user = authenticate(username=username, password=password, secureKey=secureKey)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('/about')

        request.session['message'] = 'your login data is not correct'
    return redirect('/')

"""
regestration view
"""
def register(request):

    if request.method == 'POST':
        from app.forms import UserForm

        user_form = UserForm(data=request.POST)

        if user_form.is_valid() :
            secureKey=request.POST['secureKey']
            my_secret=request.POST['key']
            if( otp.valid_totp(token=secureKey, secret=my_secret)==False ):
                request.session['message'] = 'the secure key is not correct please try again'
                return redirect("/")

            user = user_form.save()
            user.set_password(user.password)

            user.save()

            request.session['message'] = 'registration done please login'
            return redirect("/")
        else:
            request.session['error'] = user_form.errors
            return redirect("/")

"""
function to generate qr code using google api
"""
@stringfilter
def qrcode(value, alt=None):
    """
    Generate QR Code image from a string with the Google charts API
    http://code.google.com/intl/fr-FR/apis/chart/types.html#qrcodes
    Exemple usage --
    {{ my_string|qrcode:"my alt" }}
    <img src="http://chart.apis.google.com/chart?chs=150x150&amp;cht=qr&amp;chl=my_string&amp;choe=UTF-8" alt="my alt" />
    """
    url = conditional_escape("http://chart.apis.google.com/chart?%s" % \
            urllib.urlencode({'chs':'150x150', 'cht':'qr', 'chl':value, 'choe':'UTF-8'}))
    alt = conditional_escape(alt or value)
    
    return mark_safe(u"""<img class="qrcode" src="%s" width="150" height="150" alt="%s" />""" % (url, alt))

