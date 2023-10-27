from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response

from accounts.serializers import UserSerializer
from accounts.permissions import IsOwner


User = get_user_model()


class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        user = User.objects.create_user(
            email=data.get('email', ''),
            password=str(data.get('password', ''))
        )
        serializer = self.get_serializer(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        return User.objects.all().filter(pk=self.request.user.pk)


class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwner]
