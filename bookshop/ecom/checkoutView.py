from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
import uuid


@login_required
def add_address(req):
    if req.method == 'POST':
        form = AddressInsertForm(req.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = req.user
            address.save()
            return redirect('checkout')
    else:
        form = AddressInsertForm()

    data = {
        'title': 'Add Address',
        'form': form,
        'generes': Genere.objects.all(),
    }
    return render(req, 'add_address.html', data)


@login_required
def checkout(req):
    order = Order.objects.filter(user=req.user, status='pending').first()
    if order is None:
        return redirect('cart')

    items = OrderItem.objects.filter(order=order).select_related('book')
    if not items.exists():
        return redirect('cart')

    addresses = Address.objects.filter(user=req.user).order_by('-id')

    if req.method == 'POST':
        selected_address_id = req.POST.get('selected_address', '').strip()
        selected_payment = req.POST.get('payment_method', '').strip()

        selected_address = addresses.filter(id=selected_address_id).first()

        if selected_address and selected_payment:
            payment = Payment.objects.create(
                user=req.user,
                amount=order.get_final_total(),
                payment_method=selected_payment,
                transaction_id=f"TXN-{uuid.uuid4().hex[:12].upper()}",
            )

            order.address = selected_address
            order.payment = payment
            order.total_price = order.get_final_total()
            order.status = 'confirmed'
            order.save()

            return redirect('home')

    subtotal = order.get_subtotal()
    delivery_charge = order.get_delivery_charge()
    coupon_discount = order.get_coupon_discount()
    tax_amount = order.get_tax_amount()
    grand_total = order.get_final_total()

    data = {
        'title': 'Checkout',
        'order': order,
        'items': items,
        'addresses': addresses,
        'subtotal': subtotal,
        'delivery_charge': delivery_charge,
        'coupon_discount': coupon_discount,
        'tax_amount': tax_amount,
        'grand_total': grand_total,
        'generes': Genere.objects.all(),
    }
    return render(req, 'checkout.html', data)


def _update_order_total(order):
    order.total_price = order.get_subtotal()
    order.save()




@login_required
def addToCart(req, slug):
    book = Book.objects.get(slug=slug)
    order = Order.objects.filter(user=req.user, status='pending').first()

    if order is None:
        order = Order.objects.create(
            user=req.user,
            total_price=0,
            status='pending'
        )

    order_item = OrderItem.objects.filter(order=order, book=book).first()

    if order_item:
        order_item.quantity += 1
        order_item.save()
    else:
        OrderItem.objects.create(order=order, book=book, quantity=1)

    _update_order_total(order)

    return redirect('cart')


@login_required
def cart(req):
    order = Order.objects.filter(user=req.user, status='pending').first()

    if order is None:
        data = {
            'title': 'Cart',
            'order': None,
            'items': [],
            'generes': Genere.objects.all(),
        }
        return render(req, 'cart.html', data)

    if req.method == 'POST':
        action = req.POST.get('action')
        if action == 'remove_coupon':
            order.coupon = None
            order.save(update_fields=['coupon'])
            return redirect('cart')

        coupon_code = req.POST.get('coupon_code', '').strip()
        if coupon_code:
            coupon = Coupopn.objects.filter(
                code__iexact=coupon_code,
                active=True,
            ).first()
            order.coupon = coupon
            order.save(update_fields=['coupon'])
        else:
            order.coupon = None
            order.save(update_fields=['coupon'])
        return redirect('cart')

    items = OrderItem.objects.filter(order=order).select_related('book')
    _update_order_total(order)

    for item in items:
        if item.book.discount_price is not None:
            item_price = item.book.discount_price
        else:
            item_price = item.book.price
        item.item_total = item_price * item.quantity

    subtotal = order.get_subtotal()
    delivery_charge = order.get_delivery_charge()
    coupon_discount = order.get_coupon_discount()
    tax_amount = order.get_tax_amount()
    grand_total = order.get_final_total()

    data = {
        'title': 'Cart',
        'order': order,
        'items': items,
        'subtotal': subtotal,
        'delivery_charge': delivery_charge,
        'coupon_discount': coupon_discount,
        'tax_amount': tax_amount,
        'grand_total': grand_total,
        'generes': Genere.objects.all(),
    }
    return render(req, 'cart.html', data)


@login_required
def remove_from_cart(req, item_id):
    order_item = OrderItem.objects.filter(id=item_id, order__user=req.user, order__status='pending').first()
    if order_item:
        if order_item.quantity > 1:
            order_item.quantity -= 1
            order_item.save()
        else:
            order_item.delete()

        order = Order.objects.filter(user=req.user, status='pending').first()
        if order:
            _update_order_total(order)

    return redirect('cart')