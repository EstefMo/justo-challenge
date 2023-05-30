from apps.hit_management.models import Hitman, Hit
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .constants import (
    HITMAN_MANAGER_NOT_FOUND_ERROR,
    ERROR_PERMISSION_DENIED,
    LOGOUT_SUCCESS_MESSAGE,
)
from .models import Hit, Manager
from .serializers import (
    HitmanSerializer,
    LoginSerializer,
    HitSerializer,
    ManagerSerializer,
)


class LoginView(APIView):

    def post(self, request):
        login_serializer = LoginSerializer(data=request.data)
        login_serializer.is_valid(raise_exception=True)

        user = login_serializer.validated_data["user"]
        login(request=request, user=user)
        user_obj = User.objects.get(email=user)
        hitman = Hitman.objects.get(user_id=user_obj.id)

        if user_obj.is_superuser:
            user_type = "boss"
        elif user_obj.is_staff:
            user_type = "manager"
        else:
            user_type = "hitman"

        request.session["user_type"] = user_type
        request.session["hitman_id"] = hitman.id

        return Response(login_serializer.data)


class LogoutView(APIView):

    def post(self, request):
        logout(request)
        return Response(LOGOUT_SUCCESS_MESSAGE, status=status.HTTP_200_OK)


class HitmanView(APIView):

    def post(self, request):
        hitman_serializer = HitmanSerializer(data=request.data)
        if hitman_serializer.is_valid():
            hitman = hitman_serializer.create(
                request.data, validated_data=hitman_serializer.validated_data
            )
            return HitmanDetailView.get(self, request=request, hitman_id=hitman.id)
        return Response(
            data=hitman_serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request):
        try:
            if request.user.is_superuser:
                hitmans = Hitman.objects.all().exclude(user_id=request.user.id)
            else:
                hitman = Hitman.objects.get(user=request.user)
                manager = Manager.objects.get(user=hitman)
                hitmans = manager.lackeys.all()
            hitman_serializer = HitmanSerializer(hitmans, many=True)
            return Response(hitman_serializer.data)
        except:
            return Response(
                HITMAN_MANAGER_NOT_FOUND_ERROR, status=status.HTTP_404_NOT_FOUND
            )


class HitmanDetailView(APIView):

    def get(self, request, hitman_id):
        hitman = get_object_or_404(Hitman, id=hitman_id)
        hitman_serializer = HitmanSerializer(hitman)
        return Response(hitman_serializer.data, status=status.HTTP_200_OK)

    def put(self, request, hitman_id):
        hitman = get_object_or_404(Hitman, id=hitman_id)
        hitman_serializer = HitmanSerializer(hitman, data=request.data)
        if hitman_serializer.is_valid():
            first_name = request.data.get("first_name", None)
            if first_name is not None:
                hitman_serializer.update_first_name(first_name, hitman_id)
            hitman_serializer.save()
            hitman_serializer.save()
            return Response(hitman_serializer.data)
        return Response(hitman_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HitView(APIView):

    def post(self, request):
        hitman = get_object_or_404(Hitman, user=request.user)
        assignee_id = request.data.get("assignee", "0")
        hitmans = False

        if request.user.is_superuser:
            hitmans = Hitman.objects.all()
        elif assignee_id != 0:
            manager = get_object_or_404(Manager, user=hitman)
            hitmans = manager.lackeys.filter(id=assignee_id).exists()

        if assignee_id == 0:
            del request.data["assignee"]

        hit_serializer = HitSerializer(data=request.data)
        if hit_serializer.is_valid():
            hit_serializer.save()
            return Response(hit_serializer.data)
        return Response(hit_serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST) if assignee_id == "0" or hitmans else Response(
            ERROR_PERMISSION_DENIED, status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        hitman_id = request.session.get("hitman_id")
        if request.user.is_superuser:
            hits = Hit.objects.all()
        elif request.user.is_staff:
            manager_detail_api_view = ManagerDetailAPIView()
            lackeys_response = manager_detail_api_view.get_object(hitman_id=hitman_id)
            lackey_ids = []

            if lackeys_response.status_code == status.HTTP_200_OK:
                lackeys_list = lackeys_response.data
                lackey_ids = [lackey[1] for lackey in lackeys_list]
            lackey_ids.append(hitman_id)
            hits = Hit.objects.filter(assignee__in=lackey_ids)
        else:
            hits = Hit.objects.filter(assignee=hitman_id)
        hit_serializer = HitSerializer(hits, many=True)
        return Response(hit_serializer.data)


class HitDetailView(APIView):

    def get(self, request, hit_id):
        hit = get_object_or_404(Hit, id=hit_id)
        hit_serializer = HitSerializer(hit)
        return Response(hit_serializer.data)

    def put(self, request, hit_id):
        hitmans = False
        if request.user.is_staff:
            hitman = get_object_or_404(Hitman, user=request.user)
            manager = get_object_or_404(Manager, user=hitman)
            hitmans = manager.lackeys.filter(id=request.data.get("assignee")).exists()

        if hitmans or request.user.is_superuser:
            hit = get_object_or_404(Hit, id=hit_id)
            hit_serializer = HitSerializer(hit, data=request.data)
            if hit_serializer.is_valid():
                hit_serializer.save()
                return Response(hit_serializer.data)
            return Response(hit_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                ERROR_PERMISSION_DENIED,
                status=status.HTTP_404_NOT_FOUND,
            )


class ManagerListAPIView(APIView):

    def get(self, request):
        managers = Manager.objects.all()
        serializer = ManagerSerializer(managers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ManagerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update_is_staff(request.data["user"])
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManagerDetailAPIView(APIView):

    def get_object(self, hitman_id):
        try:
            return Response(
                status=status.HTTP_200_OK,
                data=Manager.objects.get(user_id=hitman_id).lackeys.values_list(
                    "user__email", "id"
                ),
            )
        except Manager.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, hitman_id):
        manager = self.get_object(hitman_id)
        serializer = ManagerSerializer(manager)
        return Response(serializer.data)

    def put(self, request, hitman_id):
        manager = Manager.objects.get(user_id=hitman_id)
        serializer = ManagerSerializer(manager, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, hitman_id):
        manager = self.get_object(hitman_id)
        manager.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
