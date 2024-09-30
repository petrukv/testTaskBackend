from django.urls import path
from .views import (
    EventListCreateView, 
    EventDetailView,
    LoginView,
    LogoutView,
    MyRegistrationsView,
    RegisterView, 
    RegistrationCreateView, 
    RegistrationCancelView,
    UserRegistrationsView,
    UserView
)

urlpatterns = [
    path('events/', EventListCreateView.as_view(), name='event-list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('register/', RegistrationCreateView.as_view(), name='register-event'),
    path('cancel/<str:manage_code>/', RegistrationCancelView.as_view(), name='cancel-registration'),
    path('signup/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('user-registrations/', UserRegistrationsView.as_view(), name='user-registrations'),
]
