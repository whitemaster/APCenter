from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.defaults import *
from adminmanager.views import *
from adminmanager.models import *
from django.views.generic import list_detail
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

#В файле урл не принято взаимодействовать с базой данных. 
csv_info = {
    "queryset" : CSVBox.objects.all(),
	"template_name": "usermodule.html",
}

csv_info0 = {
    "queryset" : CSVBox.objects.all(),
	"template_name": "usermodule.html",
}

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'APCenter.views.home', name='home'),
    # url(r'^APCenter/', include('APCenter.foo.urls')),
	(r'^$', main),
	(r'^register/$', registration),
	(r'^register/response/$', register_response),
	(r'^user/$', usercenter),
	(r'^user/editor/', addto),
	(r'^user/output/', some_view),
	(r'^user/view/', list_detail.object_list, csv_info),
	(r'^user/generate/', generate),
	(r'^user/logout/$', logout),
	(r'^tester/$', reg_test),
	(r'^user/edit/$', delete_row),
	(r'^user/update/$', update_row),
	(r'^user/base/$', output_csvbox),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
