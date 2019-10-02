#-*-coding:utf-8-*-
import datetime
from django.conf import settings
from django.core.cache import cache
from rest_framework import status, exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.utils.translation import ugettext_lazy as _

EXPIRE_MINUTES = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_MINUTES', 1)


class ObtainExpiringAuthToken(ObtainAuthToken):
    """Create user token"""

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.validated_data['user'])

            time_now = datetime.datetime.now()

            if created or token.created < time_now - datetime.timedelta(minutes=EXPIRE_MINUTES):
                # Update the created time of the token to keep it valid
                token.delete()
                token = Token.objects.create(user=serializer.validated_data['user'])
                token.created = time_now
                token.save()

            return Response({'token': token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


obtain_expiring_auth_token = ObtainExpiringAuthToken.as_view()
