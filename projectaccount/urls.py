from django.urls import path
from rest_framework_nested import routers
from .views import (
    LoginView,
    RegisterCustomerView,
    RegisterEventTeamView,
    ListUsersView,
    EventManagementUsersView,
    
)
from . import views
from .views import LogoutView


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("register/", RegisterCustomerView.as_view(), name="register"),
    path("event_team_register/", RegisterEventTeamView.as_view(), name="register"),
    # path("userslist/", ListUsersView.as_view(), name="list_users"),
    # path('users/<int:pk>/', SingleUserView.as_view(), name='user_detail'),
    # path(
    #     "event_management_users/",
    #     EventManagementUsersView.as_view(),
    #     name="event_management_users",
    # ),
]


router = routers.DefaultRouter()
router.register("userslist", views.SingleUserView),
router.register("event_management_users", views.EventManagementUsersView)
# router.register('eventteamlistsubcatagory',views.EventManagementSubcategoryViewSet,basename='MyModel')


urlpatterns = router.urls + urlpatterns
