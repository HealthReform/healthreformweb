from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'root.views.home', name='home'),
    url(r'^$', 'root.views.main', name='main'),
    url(r'account/', 'root.views.account', name='account'),
    url(r'account1/', 'root.views.account', name='account1'),
    url(r'logout/', 'root.views.logout', name='logout'),
    # url(r'^blog/', include('blog.urls')),
    url(r'dashboard/', 'root.views.dashboard', name='dashboard'),
    url(r'surgery/', 'root.views.surgery', name='surgery'),
    url(r'outpatient/', 'root.views.outpatient', name='outpatient'),
    url(r'patient/', 'root.views.patient', name='patient'),
    url(r'rank/', 'root.views.rank', name='rank'),
     url(r'performanceanalysis/', 'root.views.correlation', name='correlation'),
    url(r'^admin/', include(admin.site.urls)),
)  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
