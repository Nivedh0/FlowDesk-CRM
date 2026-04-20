from django.urls import NoReverseMatch, reverse
from django.utils.cache import add_never_cache_headers


class NoCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        content_type = response.get("Content-Type", "")
        if "text/html" not in content_type.lower():
            return response

        should_disable_cache = False

        if getattr(request, "user", None) and request.user.is_authenticated:
            should_disable_cache = True
        else:
            try:
                auth_paths = {
                    reverse("login"),
                    reverse("logout"),
                    reverse("password_reset"),
                    reverse("password_reset_done"),
                }
            except NoReverseMatch:
                auth_paths = set()

            if request.path in auth_paths or request.path.startswith("/reset/"):
                should_disable_cache = True

        if should_disable_cache:
            add_never_cache_headers(response)

        return response
