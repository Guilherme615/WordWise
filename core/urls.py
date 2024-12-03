from django.urls import path
from .views import WordCreate, WordUpdate, WordDelete, RequestCreate, RequestUpdate, RequestDelete, RequestList
from .views import WordList, UserWordList
from .views import IndexView
from django.contrib.auth import views as auth_views
from .views import UserCreate
from .views import word_create
from . import views
from .views import admin_page
from django.contrib import admin
from django.urls import path
from .views import register_user
urlpatterns = [
    path('login', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register', UserCreate.as_view(), name='register'),
    path('add/word', WordCreate.as_view(), name='add-word'),
    path('edit/word/<int:pk>', WordUpdate.as_view(), name='edit-word'),
    path('delete/word/<int:pk>', WordDelete.as_view(), name='delete-word'),
    path('list/words', WordList.as_view(), name='list-words'),
    path('', UserWordList.as_view(), name='inicio'),
    
    path('js/add', word_create, name='js-add'),

    path('request/word/', RequestCreate.as_view(), name='request-word'),
    path('edit/request/<int:pk>/', RequestUpdate.as_view(), name='edit-request'),
    path('delete/request/<int:pk>/', RequestDelete.as_view(), name='delete-request'),
    path('list/requests', RequestList.as_view(), name='list-requests'),

    path('admin_page/', admin_page, name='admin_page'),

    path('register/', register_user, name='register'),

    path('admin/', admin.site.urls),
    path('register/', register_user, name='register'),
]