from rest_framework.permissions import BasePermission
from django.conf import settings
import jwt

class HasValidSessionToken(BasePermission):
    def has_permission(self, request, view):
        session_token = request.COOKIES.get('sessionToken')
        if not session_token or not self.is_valid_token(session_token):
            return False
        return True
    def is_valid_token(self, token):
        return token == "your_valid_token_here"
