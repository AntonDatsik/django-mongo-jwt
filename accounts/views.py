from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Account
from accounts.serializers import AccountSerializer, create_token

from rest_framework.permissions import AllowAny


class AccountCreateView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountInfoView(APIView):
    def get(self, request):
        return Response({'username': request.user.username})


class AccountLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        account = Account.objects.get(username=username)

        if account is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if account.check_password(password):
            account.email = None
            token = create_token(account)
            return Response({'token': token}, status=status.HTTP_200_OK)
        else:
            return Response('Wrong password', status=status.HTTP_400_BAD_REQUEST)
