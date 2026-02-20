from django.http import HttpRequest, JsonResponse
from django.views.generic import View


class UserInfoView(View):
    """
    Retrieve info related to the current authenticated user.

    Note that this endpoint is only available to authenticated users. Unauthenticated
    requests will receive a 401 error response.
    """

    def get(self, request: HttpRequest):
        if not request.user.is_authenticated:
            return JsonResponse(
                {"error": "This endpoint requires authentication."}, status=401
            )

        return JsonResponse({"authStatus": {"mfaVerified": request.user.is_verified()}})
