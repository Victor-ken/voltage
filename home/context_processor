from multiprocessing import context
from.models import Shopcart



def readcart(request):
    cart =Shopcart.objects.filter(user__username = request.user.username, paid=False)

    cartcount = 0
    for count in cart:
        cartcount += count.quantity

    context = {
        'cartcount':cartcount
    }
    return context