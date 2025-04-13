from django.shortcuts import render
import json 
# Create your views here.
import jwt
from django.conf import settings
from django.http import JsonResponse
from supabase import create_client
from django.views.decorators.csrf import csrf_exempt

SUPABASE_URL = "https://ijdvwxnegbyqyjhysfqm.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlqZHZ3eG5lZ2J5cXlqaHlzZnFtIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0MzE1Mzc0NSwiZXhwIjoyMDU4NzI5NzQ1fQ.8rpikjMONHUs_Htfd_AgIfKk7l0TGHwssL0VJlYvO_Q"
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# @csrf_exempt
# def auth_callback(request):
#     token = request.GET.get("token")
#     if not token:
#         return JsonResponse({"error": "Token missing"}, status=400)
    
#     try:
#         decoded_token = jwt.decode(token, options={"verify_signature": False})
#         user_email = decoded_token.get("email")
        
#         # Supabase se user ka data fetch karna
#         response = supabase.auth.get_user(jwt=token)
#         if response.get("error"):
#             return JsonResponse({"error": "Invalid token"}, status=400)
        
#         user_data = response["user"]
        
#         return JsonResponse({
#             "email": user_email,
#             "supabase_user": user_data
#         })
    
#     except jwt.ExpiredSignatureError:
#         return JsonResponse({"error": "Token expired"}, status=401)
#     except jwt.InvalidTokenError:
#         return JsonResponse({"error": "Invalid token"}, status=401)



@csrf_exempt
def auth_callback(request):
    token = request.GET.get("token")
    if not token:
        return JsonResponse({"error": "Token missing"}, status=400)

    try:
        response = supabase.auth.get_user(jwt=token)
        if response.get("error"):
            return JsonResponse({"error": "Invalid token"}, status=400)

        user_data = response["user"]
        email = user_data["email"]

        # Sync user with Django DB
        user, created = SupabaseUser.objects.get_or_create(email=email, defaults={"username": email.split("@")[0]})
        return JsonResponse({"email": email, "supabase_user": user_data})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


from django.shortcuts import render
@csrf_exempt
def complete_profile(request):
    return render(request, "complete_profile.html")



from django.shortcuts import redirect
from django.http import JsonResponse
from .models import UserProfile

# def save_profile(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         name = request.POST.get("name")
#         username = request.POST.get("username")
#         address = request.POST.get("address")
#         vehicle_name = request.POST.get("vehicle_name")
#         vehicle_type = request.POST.get("vehicle_type")
#         manufacturer = request.POST.get("manufacturer")
#         profile_photo = request.FILES.get("profile_photo")

#         user_profile, created = UserProfile.objects.get_or_create(email=email)
#         user_profile.name = name
#         user_profile.username = username
#         user_profile.address = address
#         user_profile.vehicle_name = vehicle_name
#         user_profile.vehicle_type = vehicle_type
#         user_profile.manufacturer = manufacturer
#         if profile_photo:
#             user_profile.profile_photo = profile_photo
#         user_profile.save()
        
#         return JsonResponse({"message": "Profile updated successfully!"})


# from django.http import JsonResponse
# @csrf_exempt
# def save_profile(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             email = data.get("email")
#             name = data.get("name")
#             username = data.get("username")
#             address = data.get("address")
#             vehicle_name = data.get("vehicle_name")
#             vehicle_type = data.get("vehicle_type")
#             manufacturer = data.get("manufacturer")

#             if not email:
#                 return JsonResponse({"error": "Email is required"}, status=400)

#             user_profile, created = UserProfile.objects.get_or_create(email=email)
#             user_profile.name = name
#             user_profile.username = username
#             user_profile.address = address
#             user_profile.vehicle_name = vehicle_name
#             user_profile.vehicle_type = vehicle_type
#             user_profile.manufacturer = manufacturer
#             user_profile.save()

#             return JsonResponse({"message": "Profile updated successfully!"})
#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON format"}, status=400)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)
#     return JsonResponse({"error": "Invalid request method"}, status=405)


from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserProfile
from .serializers import UserProfileSerializer

class SaveProfileView(APIView):
    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)




@csrf_exempt
def set_session(request):
    token = request.GET.get("token")
    if token:
        request.session["auth_token"] = token
        return JsonResponse({"message": "Session set successfully!"})
    return JsonResponse({"error": "Token missing"}, status=400)




@csrf_exempt
def get_user_data(request):
    token = request.session.get("auth_token")
    if not token:
        return JsonResponse({"error": "User not authenticated"}, status=401)
    
    response = supabase.auth.get_user(jwt=token)
    return JsonResponse(response["user"])




@csrf_exempt
def supabase_auth(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            supabase_token = data.get("token")
            if not supabase_token:
                return JsonResponse({"error": "Token required"}, status=400)

            # Verify token with Supabase API
            headers = {"Authorization": f"Bearer {supabase_token}"}
            response = requests.get(f"{SUPABASE_URL}/auth/v1/user", headers=headers)
            if response.status_code != 200:
                return JsonResponse({"error": "Invalid token"}, status=401)

            user_data = response.json()
            email = user_data.get("email")
            uid = user_data.get("id")
            if not email or not uid:
                return JsonResponse({"error": "Invalid user data"}, status=400)

            # Store in PostgreSQL (Django Users model)
            user, created = SupabaseUser.objects.get_or_create(
                email=email, defaults={"username": email.split("@")[0]}
            )

            # Save user profile data
            user_profile, created = UserProfile.objects.get_or_create(
                email=email, defaults={"name": email.split("@")[0], "username": email.split("@")[0]}
            )

            return JsonResponse({"message": "Authenticated", "user_id": user.id})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request"}, status=400)