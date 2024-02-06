from django.urls import path
from rest_framework_nested import routers
from .views import (
    LoginView,
    RegisterCustomerView,
    RegisterEventTeamView,

)
from . import views
from .views import LogoutView


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("register/", RegisterCustomerView.as_view(), name="register"),
    path("event_team_register/", RegisterEventTeamView.as_view(), name="register"),
]


router = routers.DefaultRouter()
router.register("userslist", views.SingleUserView),
router.register("event_management_users", views.EventManagementUsersView)

urlpatterns = router.urls + urlpatterns
