from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'reg.views.home', name='home'),
    # url(r'^reg/', include('reg.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'app.views.index', name='index'),
    url(r'^home$', 'app.views.home', name='home'),
    url(r'^login/$', 'app.views.user_login', name='login'),
    url(r'^login_user$', 'app.views.login_user', name='login_user'),
    url(r'^logout', 'app.views.user_logout', name='logout'),
    url(r'^buyer/register', 'app.views.user_register', name='buyer_register'),
    url(r'^add/user$', 'app.views.add_user'),
    url(r'^activate/(?P<verification_key>[0-9a-z]+)$', 'app.views.activate'),
    url(r'^registration/success$', 'app.views.registration_success',
        name='registration_success'),
    #password reset
    url(r'^password/reset$', 'app.views.password_reset',
        name='password_reset'),
    url(r'^password/reset/submit/email$',
        'app.views.password_reset_submit_email',
        name='password_reset_submit_email'),
    url(r'^password/reset/form/(?P<verification_key>[0-9a-z]+)$',
        'app.views.password_reset_form',
        name='password_reset_form'),
    url(r'^password/reset/submit/password$',
        'app.views.password_reset_submit_password',
        name='password_reset_submit_password'),
    # seller
    url(r'^seller/register$', 'app.views.seller_register',
        name='seller_register'),
    url(r'^seller/register/submit$', 'app.views.seller_register_submit',
        name='seller_register_submit'),
    # admin
    url(r'^admin/', include('administrator.urls')),
    #test url
    url(r'^test$', 'app.views.test', name='test'),
)
