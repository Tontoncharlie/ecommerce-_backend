from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Product, Order, OrderItem
from .serializers import ProductSerializer, UserRegisterSerializer, OrderItemSerializer, OrderSerializer
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('created_at')
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = []
        return [p() for p in permission_classes]
    
class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'user_id': user.id,
                'username': user.username,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = get_object_or_404(User, username=username)
        if not user.check_password(password):
            return Response({'detail': 'Invalid credential'}, status=status.HTTP_400_BAD_REQUEST)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    
class CartAPIView(APIView):
    def get(self, request):
        cart = request.session.get('cart', {})
        items = []
        total = 0

        for pid, qty in cart.items():
            try:
                product = Product.objects.get(pk=pid)
            except product.DoesNotExist:
                continue

            items.append({
                'product_id': product.id,
                'name': product.name,
                'price': str(product.price),
                'quantity': qty,
                'subtotal': str(product.price * qty)
            })

            total += product.price * qty

        return Response({'items': items, 'total': str(total)})
        
class OrderAPIView(APIView):
    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()

            for item in request.data.get('items', []):
                product = get_object_or_404(Product, pk=item['product_id'])
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item['quantity'],
                    price=product.price
                )
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)