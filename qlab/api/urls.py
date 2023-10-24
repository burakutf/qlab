from rest_framework.routers import DefaultRouter
from django.urls import path
from .auth import views as auth
from .company import views as company
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import IsAuthenticated


app_name = 'api'

router = DefaultRouter()

schema_view = get_schema_view(
    openapi.Info(
        title='Snippets API',
        default_version='v1',
    ),
    public=True,
    permission_classes=(IsAuthenticated,),
)
router.register(
    'users',
    company.UserViewSet,
)
router.register(
    'companys',
    company.CompanyViewSet,
)
router.register(
    'vehicles',
    company.VehicleViewSet,
)

router.register(
    'minimal/user',
    company.MinimalUserViewSet,
)
router.register(
    'quality/method',
    company.QualityMethodViewSet,
)
router.register(
    'method/parameters',
    company.MethodParametersViewSet,
)
router.register(
    'devices',
    company.LabDeviceViewSet,
)
router.register(
    'notification',
    company.NotificationView,
)

urlpatterns = [
    path('login/', auth.LoginView.as_view(), name='login'),
    path('profile/me/', company.ProfileView.as_view(), name='profile'),
    path(
        'proposal/', company.ProposalListCreateView.as_view(), name='proposal'
    ),
    path(
        'proposal/<int:pk>/',
        company.ProposalRetrieveUpdateView.as_view(),
        name='proposal-detail',
    ),
    path('swagger<format>/', schema_view.without_ui(), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger'), name='schema-swagger-ui'),
] + router.urls
