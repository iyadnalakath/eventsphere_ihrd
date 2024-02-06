from django.urls import path
from rest_framework_nested import routers
from . import views
from .views import PopularityViewSetList,LocationCreateAPIView

urlpatterns = [
    # path("popular/", PopularityViewSetList.as_view(), name="popular-product-list"),
    path('location/', LocationCreateAPIView.as_view(), name='location_create'),
    # path('location/', LocationView.as_view(), name='location'),
]

router = routers.DefaultRouter()
router.register("popular", views.PopularityViewSetList)
router.register("area", views.AreaViewSet)
# router.register('catagory',views.CatagoryViewSet)
router.register("subcatagory", views.SubCatagoryViewSet)
# router.register('event_team',views.EventTeamViewSet)
router.register("service", views.ServiceViewSet)
router.register("rating", views.RatingViewSet)
router.register("notification", views.NotificationViewSet)
router.register("enquiry", views.EnquiryViewSet)
router.register("inbox", views.InboxViewSet)
router.register("profile_pic", views.ProfileViewSet)
router.register("team_profile", views.TeamProfileViewSet)
# router.register('eventteamlistsubcatagory',views.EventManagementSubcategoryViewSet,basename='MyModel')


urlpatterns = router.urls + urlpatterns
