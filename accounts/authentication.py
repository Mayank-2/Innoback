from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from rest_framework import exceptions
from django.middleware.csrf import CsrfViewMiddleware, get_token


class CustomAuthentication(JWTAuthentication):

    def dummy_get_response(request):  # pragma: no cover
        return None

    def enforce_csrf(self, request):
        # print("running CSRF check")
        """
        Enforce CSRF validation
        """
        check = CsrfViewMiddleware(self.dummy_get_response)
    # populates request.META['CSRF_COOKIE'], which is used in process_view()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})

        if reason:
            # Log the CSRF failure reason for debugging
            print(f"CSRF Check Failed: {reason}")
        # CSRF failed, bail with explicit error message
            raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)
        else:
            print("CSRF Check Passed")
           

    def authenticate(self, request):
        
        raw_token = request.COOKIES.get(
            settings.SIMPLE_JWT['AUTH_COOKIE']) or None

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        user = self.get_user(validated_token)
        self.enforce_csrf(request)

        return (user, validated_token)
