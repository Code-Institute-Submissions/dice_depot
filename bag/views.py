from django.shortcuts import render, redirect

# Create your views here.

def view_bag(request):
    """ Renders customers bag contents page """
    return render(request, 'bag/bag.html')

def add_item(request, product_id):
    """
    Add game to bag in chosen quantity
    """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if product_id in list(bag.keys()):
        bag[product_id] += quantity
    else:
        bag[product_id] = quantity

    request.session['bag'] = bag
    return redirect(redirect_url)

