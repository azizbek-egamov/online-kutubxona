from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from dj_rest_auth import urls

schema_view = get_schema_view(
    openapi.Info(
        title="API hujjatlari",
        default_version='v10',
        description="Sizning API tavsifi",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(url="https://visualcoder.ru"),
        license=openapi.License(name="datatalim.uz", url="https://datatalim.uz"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)