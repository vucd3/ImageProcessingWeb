from django.urls import path
from api import views


urlpatterns = [
    path('signup/', views.sign_up),
    path('login/', views.log_in),
    path('logout/', views.log_out),
    path('upload/', views.upload_image),
    path('process_image/', views.image_processing),
    path('perform_process/', views.perform_process, name='perform_process'), 
    path('save_infor/', views.save_infor, name = 'save_infor'),
    path('history/', views.history)
]

