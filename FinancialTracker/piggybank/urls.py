from dj_rest_auth.views import LoginView
from django.urls import include, path
from . import views


urlpatterns=[
    path('login', LoginView.as_view(),name='login'),
    path('api/auth/', include('dj_rest_auth.urls')),  # Handles login and logout
    path('api/auth/registration', include('dj_rest_auth.registration.urls')),  # Handles signup
    path('add-category', views.AddCategory, name="Add Category"),
    path('make-transaction', views.AddTransactions, name="Add Transaction"),
    path('future-transaction', views.AddFutureTransaction, name="Add Future Transaction"),
    path('add-budget', views.add_budget, name="Add Budget"),
    path('edit-budget', views.edit_budget, name="Edit Budget"),
    path('get-profile', views.get_profile, name="Get Profile"),
    
    
    path('user-profile', views.CreateProfile, name="Create Profile")
]