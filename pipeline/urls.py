from django.urls import path, include
from pipeline.views import (dashboard, project_index, profile_detail,
                            ProjectSetup, SoftwareSetup)

app_name="pipeline"

urlpatterns= [
    path('accounts/', include("django.contrib.auth.urls")),
    path('', dashboard, name= "dashboard"),
    path('projects/', project_index, name= "project_index"),
    path('project-detail/<int:pk>/',  profile_detail, name= "profile_detail"),
    path('create-project/', ProjectSetup, name= "create_project"),
    path('project-specs/', SoftwareSetup, name= "project_specs"),
]
