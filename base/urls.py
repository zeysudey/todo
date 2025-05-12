from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views 
from .views import (
    CustomLoginView,
    RegisterPage,
    TaskList,
    TaskDetail,
    TaskCreate,
    TaskUpdate,
    DeleteView,
    TaskReorder,
)


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', DeleteView.as_view(), name='task-delete'),
    path('task-reorder/', TaskReorder.as_view(), name='task-reorder'),
    path('update-user-info/', views.update_user_info, name='update_user_info'),
    path('change-password/', views.change_password_modal, name='change_password'), 
    path('toggle_language/', views.toggle_language, name='toggle_language'),
]
