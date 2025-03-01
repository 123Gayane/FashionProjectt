from django.contrib.auth.models import User
import datetime
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Fashion, Contact, Trend, Outfit, Fashion2
from .serializers import FashionSerializer, ContactSerializer, Fashion2Serializer
from django.core.mail import send_mail
from django.conf import settings
from django.core.validators import validate_email
from django.views.decorators.csrf import csrf_exempt
import json


@api_view(['POST'])
def signin(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'message': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)

    if not user:
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    token, created = Token.objects.get_or_create(user=user)

    return Response({'token': token.key}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def fashion_list(request):
    if request.method == 'GET':
        fashions = Fashion.objects.all()
        serializer = FashionSerializer(fashions, many=True)
        print(serializer.data)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = FashionSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.is_valid())
            fashion = serializer.save()

            if fashion.email:
                subject = 'New Fashion Item Added'
                message = f'A new fashion item "{fashion.name}" has been added. Details: {fashion.description}'
                from_email = settings.EMAIL_HOST_USER
                recipient_list = [fashion.email]

                try:
                    send_mail(subject, message, from_email, recipient_list)
                except Exception as e:
                    return Response({"message": f"Fashion added, but email sending failed: {str(e)}"},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# {
#     "name": "Stylish Jacket",
#     "description": "A trendy jacket for winter",
#     "size": "M",
#     "color": "Red",
#     "quantity": 10,
#     "email":"poxos@gmail.com",
#     "number":5678
# }

@api_view(['GET', 'PUT', 'DELETE'])
def fashion_detail(request, pk):
    try:
        fashion = Fashion.objects.get(pk=pk)
    except Fashion.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FashionSerializer(fashion)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = FashionSerializer(fashion, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        fashion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def contact_list(request):
    if request.method == 'GET':
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ContactSerializer(data=request.data)

        email = request.data.get('email')

        # if Contact.objects.filter(email=email).exists():
        #     return Response({'error': 'This email has already been used to contact us.'},
        #                     status=status.HTTP_400_BAD_REQUEST)
        # this code is not right

        try:
            validate_email(email)
        except ValidationError:
            return Response({'error': 'Invalid email address'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            contact = serializer.save()
            send_mail(
                'Contact Form Submission',
                'Thank you for reaching out! We have received your message and will get back to you shortly.',
                'your_email@example.com',
                [email],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def contact_detail(request, pk):
    try:
        contact = Contact.objects.get(pk=pk)
    except Contact.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ContactSerializer(contact)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ContactSerializer(contact, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        contact.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def fashion2_list(request):
    if request.method == 'GET':
        fashion2_items = Fashion2.objects.all()
        serializer = Fashion2Serializer(fashion2_items, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = Fashion2Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def fashion2_detail(request, pk):
    try:
        fashion2 = Fashion2.objects.get(pk=pk)
    except Fashion2.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = Fashion2Serializer(fashion2)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = Fashion2Serializer(fashion2, data=request.data, partial=True)
        if serializer.is_valid():
            # print(serializer.is_valid(),"hvcxhjsa")
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        fashion2.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#
# @csrf_exempt
# def process_payment(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             card_number = data.get("card_number", "")
#             expiry_date = data.get("expiry_date", "")
#             cvv = data.get("cvv", "")
#             amount = data.get("amount", 0)
#
#             if not (card_number.isdigit() and len(card_number) in [13, 16, 19] and luhn_check(card_number)):
#                 return JsonResponse({"error": "Invalid card number"}, status=400)
#
#             if not validate_expiry_date(expiry_date):
#                 return JsonResponse({"error": "Invalid or expired card"}, status=400)
#
#             if not (cvv.isdigit() and len(cvv) in [3, 4]):
#                 return JsonResponse({"error": "Invalid CVV"}, status=400)
#
#             return JsonResponse({"message": "Payment successful!"}, status=200)
#
#         except json.JSONDecodeError:
#             return JsonResponse({"error": "Invalid JSON data"}, status=400)
#
#     return JsonResponse({"error": "Invalid request method"}, status=405)
#
#
# def luhn_check(card_number):
#
#     digits = [int(d) for d in card_number[::-1]]
#     checksum = sum(digits[0::2]) + sum(sum(divmod(d * 2, 10)) for d in digits[1::2])
#     return checksum % 10 == 0
#
#
# def validate_expiry_date(expiry_date):
#
#     try:
#         parts = expiry_date.split("/")
#         if len(parts) != 2:
#             return False
#
#         month, year = int(parts[0]), int(parts[1])
#         if len(str(year)) == 2:
#             year += 2000
#
#         today = datetime.date.today()
#         card_expiry = datetime.date(year, month, 1)
#
#         return 1 <= month <= 12 and card_expiry > today
#     except ValueError:
#         return False


from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
import json
import datetime

@csrf_protect  # Use CSRF protection instead of csrf_exempt
def process_payment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            card_number = data.get("card_number", "")
            expiry_date = data.get("expiry_date", "")
            cvv = data.get("cvv", "")
            amount = data.get("amount", 0)

            # Validate card details
            if not (card_number.isdigit() and len(card_number) in [13, 16, 19] and luhn_check(card_number)):
                return JsonResponse({"error": "Invalid card number"}, status=400)

            if not validate_expiry_date(expiry_date):
                return JsonResponse({"error": "Invalid or expired card"}, status=400)

            if not (cvv.isdigit() and len(cvv) in [3, 4]):
                return JsonResponse({"error": "Invalid CVV"}, status=400)

            # Process the payment via a secure payment gateway (e.g., Stripe, PayPal)
            # Here you would integrate with a real payment processor

            return JsonResponse({"message": "Payment successful!"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def luhn_check(card_number):
    digits = [int(d) for d in card_number[::-1]]
    checksum = sum(digits[0::2]) + sum(sum(divmod(d * 2, 10)) for d in digits[1::2])
    return checksum % 10 == 0


def validate_expiry_date(expiry_date):
    try:
        parts = expiry_date.split("/")
        if len(parts) != 2:
            return False

        month, year = int(parts[0]), int(parts[1])
        if len(str(year)) == 2:
            year += 2000

        today = datetime.date.today()
        card_expiry = datetime.date(year, month, 1)

        return 1 <= month <= 12 and card_expiry > today
    except ValueError:
        return False
