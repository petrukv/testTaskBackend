from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from django.utils import timezone  # Використовуємо timezone для обробки часу
from .models import Event, Registration, User
from .serializers import EventSerializer, RegistrationSerializer, UserSerializer
from rest_framework.views import APIView
import jwt, datetime

class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

from rest_framework.permissions import IsAuthenticated

class RegistrationCreateView(generics.CreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        # Користувач вводить свій email та реєструється без аутентифікації
        client_email = request.data.get('client_email')
        
        if not client_email:
            return Response({"detail": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Додаємо email до даних запиту
        request.data['client_email'] = client_email

        # Викликаємо батьківський метод create
        return super().create(request, *args, **kwargs)




class UserRegistrationsView(generics.ListAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        # Використовуємо метод POST для отримання реєстрацій
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        # Отримуємо email з тіла запиту
        client_email = self.request.data.get('client_email')

        if client_email:
            # Фільтруємо реєстрації за email
            return Registration.objects.filter(client_email=client_email)

        return Registration.objects.none()



class RegistrationCancelView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, manage_code):
        try:
            registration = Registration.objects.get(manage_code=manage_code)
            event = registration.event
            if (event.start_date - timezone.now().date()).days <= 2 or (event.end_date - event.start_date).days > 2:
                raise ValidationError("Cannot cancel registration for events lasting longer than 2 days or less than 2 days before the event.")
            registration.delete()
            return Response({"detail": "Registration cancelled."}, status=status.HTTP_204_NO_CONTENT)
        except Registration.DoesNotExist:
            return Response({"detail": "Invalid code."}, status=status.HTTP_404_NOT_FOUND)


class EventDetailView(generics.RetrieveDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def delete(self, request, *args, **kwargs):
        event = self.get_object()
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        now = datetime.datetime.utcnow()
        payload = {
            'id': user.id,
            'exp': now + datetime.timedelta(minutes=60),
            'iat': now
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        # Відправляємо токен в відповіді
        return Response({'jwt': token})


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])  # Correct handling of algorithms
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
    
class MyRegistrationsView(generics.ListAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Registration.objects.filter(user=self.request.user)