from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied


def role_required(allowed_roles=None):
    """
    allowed_roles: list of roles allowed to access the view
    Example: @role_required(['admin', 'cre'])
    """

    def decorator(view_func):
        def wrapper(request, *args, **kwargs):

            # Not logged in
            if not request.user.is_authenticated:
                return redirect("login")

            # Superuser always allowed
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            # If user has no profile
            if not hasattr(request.user, "userprofile"):
                raise PermissionDenied

            user_role = request.user.userprofile.role

            if allowed_roles and user_role not in allowed_roles:
                raise PermissionDenied

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorator
