from django.utils.deprecation import MiddlewareMixin
from web.models import UserInfo


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):
        user_id = request.session.get('user_id', -1)
        user = UserInfo.objects.filter(id=user_id).first()
        request.mp = user
