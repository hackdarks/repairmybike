from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile
from django.shortcuts import get_object_or_404

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def profile_view(request, email):
    # Get the email from the authenticated user
    user_email = request.user.email
    
    # Verify that the requested email matches the user's email
    if user_email != email:
        return Response(
            {"error": "You can only access your own profile"},
            status=status.HTTP_403_FORBIDDEN
        )

    try:
        # Try to get existing profile
        profile = UserProfile.objects.get(email=email)
    except UserProfile.DoesNotExist:
        # If profile doesn't exist, create new one with default values
        profile = UserProfile.objects.create(
            email=email,
            name=email.split('@')[0],  # Use email prefix as default name
            username=email.split('@')[0],  # Use email prefix as default username
            address='',
            vehicle_name='',
            vehicle_type='',
            manufacturer=''
        )

    if request.method == 'GET':
        data = {
            'email': profile.email,
            'name': profile.name,
            'username': profile.username,
            'address': profile.address,
            'vehicle_name': profile.vehicle_name,
            'vehicle_type': profile.vehicle_type,
            'manufacturer': profile.manufacturer,
            'profile_photo': profile.profile_photo.url if profile.profile_photo else None
        }
        return Response(data)
    
    elif request.method == 'POST':
        try:
            # Update profile fields
            profile.name = request.data.get('name', profile.name)
            profile.username = request.data.get('username', profile.username)
            profile.address = request.data.get('address', profile.address)
            profile.vehicle_name = request.data.get('vehicle_name', profile.vehicle_name)
            profile.vehicle_type = request.data.get('vehicle_type', profile.vehicle_type)
            profile.manufacturer = request.data.get('manufacturer', profile.manufacturer)
            
            profile.save()
            
            data = {
                'email': profile.email,
                'name': profile.name,
                'username': profile.username,
                'address': profile.address,
                'vehicle_name': profile.vehicle_name,
                'vehicle_type': profile.vehicle_type,
                'manufacturer': profile.manufacturer,
                'profile_photo': profile.profile_photo.url if profile.profile_photo else None
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            ) 