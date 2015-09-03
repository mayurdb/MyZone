from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^key/$', views.index, name='index'),
	url(r'^loggedin/$', views.sign_in,name='sign_in'),
	url(r'^register/$',views.sign_up,name="sign_up"),
	url(r'^go_home/$',views.cprofile,name="child_profile"),
	url(r'^search_results/$',views.search,name="search"),
	url(r'^(?P<user_id>\d+)/home/$',views.send_friend_request,name="send_friend_request"),	
	url(r'^loggedout/$',views.logout_view,name="logout"),
	url(r'^view_requests/$',views.view_requests,name="view_requests"),	
	url(r'^(?P<decision>\d+)/(?P<frndreq_id>\d+)/home/$',views.make_friends,name="view_requests"),			
	url(r'^(?P<child_id>\d+)/update/$',views.update, name='update_profile'),
	url(r'^home_again/$',views.cprofile_update,name="update_child_profile"),
	url(r'^home/$',views.home,name="go_home"),		
	url(r'^friend_list/$',views.friend_list,name="go_home"),		
	]	