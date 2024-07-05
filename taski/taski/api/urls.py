from django.urls import path, include

urlpatterns = [
    path('authentication/', include(('taski.authentication.urls', 'authentication'))),
    path('users/', include(('taski.users.urls', 'users'))),
    path('projects/', include(('taski.project.urls', 'projects'))),
    path('tasks/', include(('taski.task.urls', 'tasks'))),
    path('ws/', include(('taski.ws.urls', 'ws'))),
]
