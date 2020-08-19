
from django.views.generic import ListView, DetailView
from products.models import Article, Order
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from users.models import Profile




def home(request):

    cards = Article.objects.all()
    card_type=[]
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
    order = Order.objects.filter(ownwer=user_profile).first()
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




