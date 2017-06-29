from django.conf.urls import url
from django.urls import reverse
from . import views

urlpatterns = [
				url(r'^home/$',views.index,name='index'),
				url(r'^$',views.Login,name='login'),
				url(r'^signup/$',views.Signup,name='signup'),
				url(r'^logout/$',views.Logout,name='logout'),
				url(r'^add_bill/(?P<id>\d+)/$',views.add_bill,name='add_bill'),
				url(r'^mtom/transaction/$',views.mtom_transaction, name='mtom_transaction'),
				url(r'^member/home/$',views.member_report,name='member_report'),
				url(r'^groupcreation/',views.group_creation,name='group_creation'),
				url(r'^settings/$',views.settings,name='settings'),
				url(r'^grpreport/(?P<id>\d+)/$',views.group_report, name='group_report'), 
			]