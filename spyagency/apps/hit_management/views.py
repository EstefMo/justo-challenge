from apps.hit_management.api_view import (
    HitView,
    HitDetailView,
    HitmanView,
    HitmanDetailView,
    ManagerDetailAPIView,
)
from django.shortcuts import render
from rest_framework import status


def login_view(request):
    return render(request, "login.html")


def register_view(request):
    return render(request, "register.html")


def hits_view(request):
    hits_api_view = HitView()
    hits = hits_api_view.get(request=request)
    return render(request, "hits.html", {"hits": hits.data})


def hit_detail_view(request, hit_id):
    hits_detail_api_view = HitDetailView()
    hit = hits_detail_api_view.get(request=request, hit_id=hit_id)
    api_hitman = HitmanView()
    hitmans = api_hitman.get(request=request)
    return render(
        request, "hit_detail.html", {"hit": hit.data, "hitmans": hitmans.data}
    )


def create_hit_view(request):
    api_hitman = HitmanView()
    hitmans = api_hitman.get(request=request)
    return render(request, "create_hit.html", {"hitmans": hitmans.data})


def hitmen_view(request):
    api_hitman = HitmanView()
    hitmans = api_hitman.get(request=request)
    data = []
    if hitmans.status_code == status.HTTP_200_OK:
        data = hitmans.data
    else:
        data = {}
    return render(request, "hitmen.html", {"hitmen": data})


def Hitman_detail_view(request, hitman_id):
    hitman_detail_view = HitmanDetailView()
    hitman_response = hitman_detail_view.get(request=request, hitman_id=hitman_id)

    manager_detail_api_view = ManagerDetailAPIView()
    lackeys_response = manager_detail_api_view.get_object(hitman_id=hitman_id)
    lackeys_list = []
    lackey_ids = []

    if lackeys_response.status_code == status.HTTP_200_OK:
        lackeys_list = lackeys_response.data
        lackey_ids = [lackey[1] for lackey in lackeys_list]

    hitman_view = HitmanView()
    hitmans_response = hitman_view.get(request=request)
    hitmans = []

    if hitmans_response.status_code == status.HTTP_200_OK:
        hitmans = hitmans_response.data

    return render(
        request,
        "hitman_detail.html",
        {
            "hitman": hitman_response.data,
            "lackeys": lackeys_list,
            "hitmans": hitmans,
            "lackey_ids": lackey_ids,
        },
    )
