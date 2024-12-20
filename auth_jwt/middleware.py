import logging
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import get_user_model
from tenants.models import Tenant
from django_tenants.utils import schema_context

logger = logging.getLogger(__name__)

User = get_user_model()


@database_sync_to_async
def get_user_from_token(token):
    try:
        decoded_token = UntypedToken(token)
        user_id = decoded_token["user_id"]
        domain = decoded_token.get("tenant_domain", None)
        if not domain:
            logger.error("Tenant domain is missing in the token")
            return AnonymousUser()

        tenant = Tenant.objects.filter(domains__domain=domain).first()

        if not tenant:
            logger.error(f"No tenant found for domain: {domain}")
            return AnonymousUser()

        with schema_context(tenant.schema_name):
            user = User.objects.get(id=user_id)
            logger.info(f"User {user} found for token")
            return user
    except (InvalidToken, TokenError, User.DoesNotExist) as e:
        logger.error(f"Error decoding token or retrieving user: {str(e)}")
        return AnonymousUser()


class JWTAuthMiddleware:
    """Custom middleware for JWT authentication in WebSocket connections."""

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"].decode()
        token = dict(x.split("=") for x in query_string.split("&")).get("token", None)
        if token:
            scope["user"] = await get_user_from_token(token)
        else:
            scope["user"] = AnonymousUser()
        return await self.inner(scope, receive, send)
