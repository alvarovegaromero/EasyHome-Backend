from django.http import HttpResponse
from rest_framework.views import APIView

from ...utils.verify_email import verify_email_with_token


class EmailVerificationAPIView(APIView):
    def get(self, request):
        token = request.GET.get("token")
        if not token:
            return HttpResponse("<h1>Token is required</h1>", status=400)

        is_verified, message = verify_email_with_token(token)
        if is_verified:
            return HttpResponse(
                f"<h1>{message}</h1> <p> You can go now log into the app <p> ", status=200
            )
        else:
            return HttpResponse(f"<h1>{message}</h1>", status=400)
