from django.urls import path, include

urlpatterns = [
    path('authentication/', include(('taski.authentication.urls', 'authentication'))),
    path('users/', include(('taski.users.urls', 'users'))),
]
