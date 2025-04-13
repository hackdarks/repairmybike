# from rest_framework import authentication
# from rest_framework import exceptions
# import jwt
# from django.conf import settings
# from .models import SupabaseUser
# from django.contrib.auth import get_user_model

# class SupabaseAuthentication(authentication.BaseAuthentication):
#     def authenticate(self, request):
#         auth_header = request.headers.get('Authorization')
#         if not auth_header:
#             return None

#         try:
#             # Remove 'Bearer ' prefix
#             token = auth_header.split(' ')[1]
#             # Decode the JWT token without verification since we trust Supabase
#             decoded_token = jwt.decode(token, options={"verify_signature": False})
            
#             # Get or create user
#             email = decoded_token.get('email')
#             supabase_id = decoded_token.get('sub')
            
#             if not email:
#                 raise exceptions.AuthenticationFailed('No email in token')

#             User = get_user_model()
            
#             try:
#                 user = User.objects.get(email=email)
#             except User.DoesNotExist:
#                 # Create new user
#                 username = email.split('@')[0]  # Use part before @ as username
#                 user = User.objects.create_user(
#                     username=username,
#                     email=email,
#                     supabase_id=supabase_id
#                 )

#             # Update supabase_id if it changed
#             if user.supabase_id != supabase_id:
#                 user.supabase_id = supabase_id
#                 user.save()

#             return (user, None)
#         except jwt.InvalidTokenError:
#             raise exceptions.AuthenticationFailed('Invalid token')
#         except Exception as e:
#             raise exceptions.AuthenticationFailed(str(e)) 


import requests
import jwt
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

SUPABASE_JWKS_URL = "https://ijdvwxnegbyqyjhysfqm.supabase.co/auth/v1/keys"

class SupabaseAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return None

        try:
            token = auth_header.split(" ")[1]

            # Fetch public keys from Supabase
            jwks = requests.get(SUPABASE_JWKS_URL).json()
            public_keys = {key["kid"]: jwt.algorithms.RSAAlgorithm.from_jwk(key) for key in jwks["keys"]}

            # Decode token with key verification
            headers = jwt.get_unverified_header(token)
            key = public_keys.get(headers["kid"])
            if not key:
                raise AuthenticationFailed("Invalid token key")

            decoded_token = jwt.decode(token, key=key, algorithms=["RS256"])

            email = decoded_token.get("email")
            supabase_id = decoded_token.get("sub")

            if not email:
                raise AuthenticationFailed("No email in token")

            User = get_user_model()
            user, _ = User.objects.get_or_create(email=email, defaults={"username": email.split("@")[0], "supabase_id": supabase_id})

            return (user, None)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expired")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")
