from django.http import HttpRequest, HttpResponse
from django.utils.timezone import now

class UpdateLastActivityMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        if request.user.is_authenticated:
            user = request.user
            user.last_activity = now()
            user.is_online = True
            user.save()
        return self.get_response(request)
