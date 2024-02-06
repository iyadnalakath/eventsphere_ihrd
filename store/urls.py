from django.urls import path
from rest_framework_nested import routers
from . import views
from .views import PopularityViewSetList,LocationCreateAPIView

urlpatterns = [
    path('location/', LocationCreateAPIView.as_view(), name='location_create'),
    
]

router = routers.DefaultRouter()
router.register("popular", views.PopularityViewSetList)
router.register("area", views.AreaViewSet)
router.register("subcatagory", views.SubCatagoryViewSet)
router.register("service", views.ServiceViewSet)
router.register("rating", views.RatingViewSet)
router.register("notification", views.NotificationViewSet)
router.register("enquiry", views.EnquiryViewSet)
router.register("inbox", views.InboxViewSet)
router.register("profile_pic", views.ProfileViewSet)
router.register("team_profile", views.TeamProfileViewSet)



urlpatterns = router.urls + urlpatterns
