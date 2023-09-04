from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import CustomerSerializer
from rest_framework import status
from .models import Customer
import jwt, datetime

# Create your views here.
class CustomerRegisterView(APIView):
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data": serializer.data,"message": "Success", "status": status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)


class CustomerLoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        customer = Customer.objects.filter(email=email).first()

        if customer is None:
            return Response({'message':'Customer not found!', "status": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

        if not customer.check_password(password):
            return Response({'error': 'Unauthorized', "status": status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)

        payload = {
            'id': customer.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        # token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        
        response = Response(status=status.HTTP_200_OK)

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'token': token,
            "status": status.HTTP_200_OK
        }
        return response


class CustomerUserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            return Response({'error': 'Unauthorized', "status": status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
             return Response({'error': 'Unauthorized', "status": status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_401_UNAUTHORIZED)

        customer = Customer.objects.filter(id=payload['id']).first()
        serializer = CustomerSerializer(customer)
        return Response({"data":serializer.data , "status": status.HTTP_200_OK},status=status.HTTP_200_OK)


class CustomerLogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success',
            "status": status.HTTP_200_OK
        }
        return response