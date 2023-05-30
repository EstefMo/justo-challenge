from rest_framework.permissions import BasePermission


class RoleBossPermission(BasePermission):
    """
    This class validates if the user is a boss.
    """

    def has_permission(self, request, view):
        print(request.session["user_type"])
        if request.user.is_authenticated and request.session["user_type"] == "boss":
            return True
        return False


class RoleManagerPermission(BasePermission):
    """
    This class validates if the user is a manager.
    """

    def has_permission(self, request, view):
        print(request.session["user_type"])
        if request.user.is_authenticated and request.session["user_type"] == "manager":
            return True
        return False


class RoleHitmanPermission(BasePermission):
    """
    This class validates if the user is a hitman.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.session["user_type"] == "hitman":
            return True
        return False
