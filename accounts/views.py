from django.contrib.auth import authenticate, login, get_user_model
from django.db import transaction
from django.shortcuts import render
from accounts.models import Accounts
from cart.models import Cart
from orders.models import Order
from accounts.serializers import AccountsSerializer, UserDataSerializer, AvatarSerializer, SecurityQuestionSerializer
from accounts.serializers import UsernameChangeSerializer, PasswordChangeSerializer, SecuritySerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404


class AccountsViewSet(viewsets.ModelViewSet):
    queryset = Accounts.objects.all()
    serializer_class = AccountsSerializer


' Oftener Token, access, refresh Login '


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super(CustomTokenObtainPairView, self).post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            access_token = response.data.get('access', None)
            refresh_token = response.data.get('refresh', None)

            if access_token and refresh_token:
                return Response({'access_token': access_token, 'refresh_token': refresh_token},
                                status=status.HTTP_200_OK)
        return response


' registry '


User = get_user_model()


class RegisterClientView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        existing_user = User.objects.filter(username=username).first()

        if existing_user:
            return Response({'success': False, 'error': 'Username already exists.'}, status=status.HTTP_409_CONFLICT)
        else:
            try:
                with transaction.atomic():
                    user = User.objects.create_user(username=username, password=password)
                    accounts = Accounts.objects.create(user=user)
                    cart = Cart.objects.create(user_account=accounts.user)
                    order = Order.objects.create(user_account=accounts, total_price=0, is_completed=False)
            except Exception as e:
                return Response({'success': False, 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({'success': True, 'user_id': user.id}, status=status.HTTP_201_CREATED)




@authentication_classes([JWTAuthentication])
@permission_classes({IsAuthenticated})
class UserGetView(APIView):

    def get(self, request):
        user = request.user
        serializer = UserDataSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@authentication_classes([JWTAuthentication])
@permission_classes({IsAuthenticated})
class UserPUTView(APIView):
    def put(self, request):
        user = request.user
        serializer = UserDataSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTAuthentication])
@permission_classes({IsAuthenticated})
class UserDeleteView(APIView):
    def delete(self, request):
        user = request.user
        user.delete()

        return Response({"message": "Usuario eliminado correctamente."}, status=status.HTTP_204_NO_CONTENT)


@authentication_classes([JWTAuthentication])
@permission_classes({IsAuthenticated})
class UserListView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        users = User.objects.all()
        serializer = UserDataSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@authentication_classes([JWTAuthentication])
@permission_classes({IsAuthenticated})
class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserDataSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


' get de accounts '


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class AccountsGetView(APIView):

    def get(self, request):
        user = request.user

        try:
            accounts_instance = user.accounts
        except Accounts.DoesNotExist:
            return Response({"error": "No se encontraron datos de cuentas para este usuario"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = AccountsSerializer(accounts_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class AccountsPutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user

        try:
            accounts_instance = user.accounts
        except Accounts.DoesNotExist:
            return Response({"error": "No se encontraron datos de cuentas para este usuario"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = AccountsSerializer(accounts_instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Data
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
class AccountsListView(APIView):
    def get(self, request):
        accounts = Accounts.objects.all()
        serializer = AccountsSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsAdminUser])
class AccountsDetailsView(APIView):
    def get(self, request, pk):
        try:
            account = Accounts.objects.get(pk=pk)
        except Accounts.DoesNotExist:
            return Response({"error": "Datos de cuenta no encontrados"}, status=status.HTTP_404_NOT_FOUND)

        serializer = AccountsSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)


#

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class AvatarUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        user = request.user
        accounts, created = Accounts.objects.get_or_create(user=user)

        if accounts.avatar:
            return Response({"error": "El usuario ya tiene una imagen asociada"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = AvatarSerializer(accounts, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "La imagen se subió correctamente"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        user = request.user
        accounts = get_object_or_404(Accounts, user=user)
        serializer = AvatarSerializer(accounts, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "La imagen se actualizó correctamente"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        user = request.user
        accounts = get_object_or_404(Accounts, user=user)

        if not accounts.avatar:
            return Response({"error": "El usuario no tiene una imagen asociada"}, status=status.HTTP_404_NOT_FOUND)

        accounts.avatar.delete()
        accounts.avatar = None
        accounts.save()

        return Response({"message": "La imagen se eliminó correctamente"}, status=status.HTTP_204_NO_CONTENT)


# segurity

class SecurityQuestionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            security_question = Accounts.objects.get(user=user)
            serializer = SecurityQuestionSerializer(security_question)
            return Response(serializer.data)
        except Accounts.DoesNotExist:
            return Response({"detail": "Security question not set"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        user = request.user
        try:
            security_question = Accounts.objects.get(user=user)
            serializer = SecurityQuestionSerializer(security_question, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Security question updated successfully"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Accounts.DoesNotExist:
            return Response({"detail": "Security question not set"}, status=status.HTTP_404_NOT_FOUND)


@authentication_classes([JWTAuthentication])
@permission_classes({IsAuthenticated})
class AnswerVerificationView(APIView):

    def post(self, request):
        serializer = SecuritySerializer(data=request.data)
        if serializer.is_valid():
            answer = serializer.validated_data.get('answer')

            accounts = self.get_accounts(request.user)

            if accounts is not None:
                is_correct_answer = accounts.verify_security_answer(answer)

                return Response({"is_correct_answer": is_correct_answer}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "accounts no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_accounts(self, user):
        try:
            accounts = Accounts.objects.get(user=user)
            return accounts
        except Accounts.DoesNotExist:
            return None


#
@authentication_classes([JWTAuthentication])
@permission_classes({IsAuthenticated})
class PasswordChangeView(APIView):
    def put(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data.get('new_password')

            user = request.user

            if user is not None:
                user.set_password(new_password)
                user.save()

                authenticated_user = authenticate(request, username=user.username, password=new_password)
                if authenticated_user is not None:
                    login(request, authenticated_user)

                return Response({"message": "Contraseña cambiada con éxito"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@authentication_classes([JWTAuthentication])
@permission_classes({IsAuthenticated})
class UsernameChangeView(APIView):
    def put(self, request):
        serializer = UsernameChangeSerializer(data=request.data)
        if serializer.is_valid():
            new_username = serializer.validated_data.get('new_username')

            user = request.user

            if user is not None:
                user.username = new_username
                user.save()

                return Response({"message": "Nombre de usuario cambiado con éxito"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
