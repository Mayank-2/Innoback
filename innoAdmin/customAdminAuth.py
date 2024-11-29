from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from rest_framework.authentication import CSRFCheck
from django.middleware.csrf import CsrfViewMiddleware, get_token

from rest_framework import exceptions


class CustomAdminAuthentication(JWTAuthentication):
    def dummy_get_response(request):
        return None

    def enforce_csrf(self, request):
        """
        Enforce CSRF validation
        """
        check = CSRFCheck(self.dummy_get_response)
        check.process_request(request)
        reason = check.process_view(request, None, (), {})

        if reason:
            raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)

    def authenticate(self, request):

        raw_token = request.COOKIES.get(
            settings.SIMPLE_JWT['Admin_AUTH_COOKIES']) or None

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        user = self.get_user(validated_token)
        self.enforce_csrf(request)
        if user.is_admin:
            return (user, validated_token)
        else:
            return None
