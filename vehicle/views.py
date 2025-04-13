from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import VehicleType, Manufacturer, VehicleModel, UserVehicle
from .serializers import (
    VehicleTypeSerializer, ManufacturerSerializer, VehicleModelSerializer, UserVehicleSerializer
)

class VehicleTypeViewSet(viewsets.ModelViewSet):
    queryset = VehicleType.objects.all()
    serializer_class = VehicleTypeSerializer

class ManufacturerViewSet(viewsets.ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer

class VehicleModelViewSet(viewsets.ModelViewSet):
    queryset = VehicleModel.objects.all()
    serializer_class = VehicleModelSerializer

class UserVehicleViewSet(viewsets.ModelViewSet):
    queryset = UserVehicle.objects.all()
    serializer_class = UserVehicleSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["post"], url_path="create/(?P<vehicle_type_id>\d+)/(?P<manufacturer_id>\d+)/(?P<vehicle_model_id>\d+)")
    def create_from_params(self, request, vehicle_type_id, manufacturer_id, vehicle_model_id):
        vehicle_type = get_object_or_404(VehicleType, id=vehicle_type_id)
        manufacturer = get_object_or_404(Manufacturer, id=manufacturer_id)
        vehicle_model = get_object_or_404(VehicleModel, id=vehicle_model_id, vehicle_type=vehicle_type, manufacturer=manufacturer)

        data = {
            "user": request.user.id,
            "vehicle_type": vehicle_type.id,
            "manufacturer": manufacturer.id,
            "model": vehicle_model.id,
            "registration_number": request.data.get("registration_number"),
            "purchase_date": request.data.get("purchase_date")
        }

        serializer = UserVehicleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
