from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gettingstarted.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'app.views.index', name='index'),
    url(r'^contact', 'app.views.contact', name='contact'),
    url(r'^about', 'app.views.about', name='about'),
    url(r'^login', 'app.views.login_user', name='login'),
    url(r'^register', 'app.views.register', name='register'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/',}, name='logout'),

    url(r'^accounts/login', 'app.views.index', name='login'),
)
