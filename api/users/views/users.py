from rest_framework import  status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.users.models import User
from api.users.serializers.users import UserModelSerializer

from api.authentication import  InfojobsAuthentication


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    authentication_classes = [InfojobsAuthentication]
    permission_classes = [IsAuthenticated]


    @action(detail=False, methods=['get'])
    def whoami(self, request):
        data = {
            'user': UserModelSerializer(instance=request.user, context={
                'request': request}).data,
            'candidate': self.request.auth
        }
        return Response(data, status=status.HTTP_200_OK)

  

    

    
    
