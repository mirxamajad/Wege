from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import CustomerSerializer
from .models import Customer
import jwt, datetime

# Create your views here.
class CustomerRegisterView(APIView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CustomerLoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        customer = Customer.objects.filter(email=email).first()

        if customer is None:
            raise AuthenticationFailed('Customer not found!')

        if not customer.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        payload = {
            'id': customer.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        # token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response


class CustomerUserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        customer = Customer.objects.filter(id=payload['id']).first()
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)


class CustomerLogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response