from django.views.generic import ListView, DetailView
from products.models import Article, Order
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from users.models import Profile
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from .serializers import *
from rest_framework import permissions
from rest_framework.response import Response


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests

        # Instance must have an attribute named `owner`.
        return obj.ownwer == request.user


class ArticleView(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class AddToCartView(APIView):

     def post(self, request, *args, **kwargs):
        user_profile = get_object_or_404(Profile, user=request.user)
        p = get_object_or_404(Article, pk=kwargs['pk'])
        if user_profile is None:
            return Response(status=HTTP_401_UNAUTHORIZED)

        if p is None:
            return Response(status=HTTP_404_NOT_FOUND)

        order, status = Order.objects.get_or_create(ownwer=user_profile)
        order.items.add(p)
        order.save()
        return Response(HTTP_200_OK)


class OrderView(generics.RetrieveAPIView):
    print('aa')
    serializer_class = OrderSerializer
    print('bb')
    permission_classes = (IsOwner,)

    def get_object(self):
        try:
            print(self.request.user)
            profile = get_object_or_404(Profile, user=self.request.user)
            order = Order.objects.filter(ownwer=profile).first()
            return order
        except ObjectDoesNotExist:
            raise HTTP_404_NOT_FOUND("You do not have an active order")

"""""
class OrderView(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        user_profile = get_object_or_404(Profile, user=self.request.user)
        return get_object_or_404(Order, ownwer=user_profile)

"""""

def home(request):

    cards = Article.objects.all()
    card_type = []
    if(cards.type not in card_type):
        card_type.append(cards.type)

    return render(request, 'products/home.html', context={'cards': cards, 'card_type': card_type})


class ArticleListView(ListView):

    model = Article
    template_name = 'products/home.html'
    context_object_name = 'cards'
    ordering = ['-price']
    paginate_by = 8


class ArticleDetailView(DetailView):

    model = Article
    template_name = 'products/detail_view.html'
    context_object_name = 'card'


def search(request):
    if request.method =='GET':

        cards = Article.objects.all().filter(name__istartswith=request.GET.get('search'))

    return render(request, 'products/home.html', {'cards': cards})


@login_required
def view_cart(request):

    user_profile = get_object_or_404(Profile, user=request.user)
    print(user_profile)
    order = Order.objects.filter(ownwer=user_profile).first()
    print(order)
    cart_items = order.cart_items()
    total = order.cart_total()


    context = {'cart_items': cart_items, 'total': total}

    return render(request, "products/cart.html", context)


@login_required
def add_to_cart(request, **kwargs):


    user_profile = get_object_or_404(Profile, user = request.user)
    p = get_object_or_404(Article, pk=kwargs['pk'])
    order, status = Order.objects.get_or_create(ownwer=user_profile)
    order.items.add(p)
    order.save()

    messages.success(request, f'{p} Have Been Added To Cart ')

    return redirect('products-home')


@login_required
def delete_item(request, **kwargs):

    user_profile = get_object_or_404(Profile, user=request.user)
    item = get_object_or_404(Article, pk=kwargs['pk'])
    order, status = Order.objects.get_or_create(ownwer=user_profile)
    order.items.remove(item)

    return redirect('cart')



