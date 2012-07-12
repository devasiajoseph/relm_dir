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
    url(r'^$', 'administrator.views.admin_dashboard', name='admin_dashboard'),
    url(r'^seller/request/list/(?P<list_type>[0-9A-Za-z\-]+)/(?P<page>[0-9]+)$',
        'administrator.views.seller_request_list',
        name='seller_request_list'),
    url(r'^seller/request/view/(?P<object_id>[0-9]+)$',
        'administrator.views.seller_request_view',
        name='seller_request_view'),
     url(r'^seller/request/decision$',
         'administrator.views.seller_request_decision',
         name='seller_request_decision'),
)
