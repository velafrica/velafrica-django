from rest_framework.decorators import api_view
from rest_framework.response import Response

from velafrica.api.user.serializer import UserSerializer


@api_view(['GET'])
def current_user(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)
