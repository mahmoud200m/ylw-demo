from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django_ajax.decorators import ajax
from django.utils import timezone

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
    return render(
        request,
        'app/index.html',
        context_instance = RequestContext(request,
        {
            'title':'Home Page',
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
            user = user_form.save()
            user.set_password(user.password)

            import string, random
            key = ''.join(random.choice(string.ascii_uppercase) for _ in range(16))
            user.set_key(key)

            user.save()

            import qrcode
            from Pillow import Image
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data('Some data')
            qr.make(fit=True)

            img = qr.make_image()

            import sys
            print >> sys.stderr, '\n\n\n'+img+'\n\n\n'

            request.session['message'] = 'registration done please login <br /> your security code is: '+key
            return redirect("/")
        else:
            request.session['error'] = user_form.errors
            return redirect("/")

