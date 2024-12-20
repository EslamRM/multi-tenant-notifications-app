import logging
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from tenants.models import Tenant
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(self, user):
        # Generate the default token
        token = super().get_token(user)

        request = self.context["request"]
        if request:
            domain = request.META['HTTP_HOST'].split(':')[0]
            tenant = Tenant.objects.filter(domains__domain=domain).first()
            if tenant:
                # Add tenant information to the token payload
                token["tenant_domain"] = domain
                token["tenant"] = tenant.schema_name
            else:
                logger.error(f"No tenant found for domain: {domain}")
        else:
            logger.error("Request context is not available to extract the domain.")

        return token


class TenantAwareTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=200)
