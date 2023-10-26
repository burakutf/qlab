from rest_framework.routers import DefaultRouter
from django.urls import path
from .auth import views as auth
from .company import views as company
from .accounts import views as accounts
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
    accounts.UserViewSet,
)
router.register(
    'group',
    accounts.GroupViewSet,
)
router.register(
    'permission',
    accounts.PermissionViewSet,
)
router.register(
    'minimal/user',
    accounts.MinimalUserViewSet,
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
    'proposal/draft',
    company.ProposalDraftViewSet,
)

router.register(
    'notification',
    company.NotificationView,
)
urlpatterns = [
    path('login/', auth.LoginView.as_view(), name='login'),
    path('profile/me/', accounts.ProfileView.as_view(), name='profile'),
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
