from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from products.models import MyProducts, BundledPlan, Order, Coupon, CouponUsage
from django.utils import timezone
from decimal import Decimal
import razorpay

@login_required
def checkout(request, type, slug):
    # Get the item
    if type == 'bundle':
        item = get_object_or_404(BundledPlan, slug=slug, is_active=True)
        price = item.selling_price
        original_price = item.original_price
    else:
        item = get_object_or_404(MyProducts, slug=slug, is_active=True)
        price = item.base_price
        original_price = item.base_price

    # Coupon Logic
    coupon = None
    discount_amount = Decimal('0')
    coupon_code = request.session.get('coupon_code')
    
    if coupon_code:
        try:
            coupon = Coupon.objects.get(code=coupon_code, is_active=True)
            if coupon.is_valid():
                # Check user usage limit again
                user_usage_count = CouponUsage.objects.filter(coupon=coupon, user=request.user).count()
                if coupon.max_uses_per_user > 0 and user_usage_count >= coupon.max_uses_per_user:
                    del request.session['coupon_code']
                    messages.error(request, "Coupon usage limit reached")
                    coupon = None
                else:
                    # Check applicability again
                    is_applicable = True
                    if type == 'bundle':
                        if coupon.applicable_plans.exists() and item not in coupon.applicable_plans.all():
                            is_applicable = False
                    else:
                        if coupon.applicable_products.exists() and item not in coupon.applicable_products.all():
                            is_applicable = False
                    
                    if is_applicable:
                        discount_amount = coupon.calculate_discount(price)
                    else:
                        del request.session['coupon_code']
                        messages.error(request, "Coupon not applicable to this item")
                        coupon = None
            else:
                del request.session['coupon_code']
                messages.error(request, "Coupon expired or invalid")
                coupon = None
        except Coupon.DoesNotExist:
            del request.session['coupon_code']
            coupon = None

    final_price = price - discount_amount

    if request.method == "POST":
        # Create Order
        order = Order.objects.create(
            user=request.user,
            bundled_plan=item if type == 'bundle' else None,
            product=item if type != 'bundle' else None,
            original_price=original_price,
            final_price=final_price,
            discount_amount=discount_amount,
            coupon_code=coupon.code if coupon else '',
            coupon_discount=discount_amount,
            status='pending'
        )
        
        # Initialize Razorpay Client
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET_KEY))
        
        # Create Razorpay Order
        payment_data = {
            'amount': int(final_price * 100), # Amount in paise
            'currency': 'INR',
            'receipt': order.order_id,
            'payment_capture': '1'
        }
        
        try:
            razorpay_order = client.order.create(data=payment_data)
            
            # Save Razorpay Order ID to Order
            order.razorpay_order_id = razorpay_order['id']
            order.save()
            
            context = {
                'order': order,
                'razorpay_order_id': razorpay_order['id'],
                'razorpay_merchant_key': settings.RAZORPAY_API_KEY,
                'razorpay_amount': payment_data['amount'],
                'currency': payment_data['currency'],
                'callback_url': request.build_absolute_uri('/checkout/payment/success/'),
                'item': item,
                'type': type
            }
            
            return render(request, 'checkout/payment.html', context)
        except Exception as e:
            messages.error(request, f"Error creating payment order: {str(e)}")
            return redirect('checkout:checkout_view', type=type, slug=slug)

    context = {
        'item': item,
        'type': type,
        'price': price,
        'original_price': original_price,
        'coupon': coupon,
        'discount_amount': discount_amount,
        'final_price': final_price,
    }
    return render(request, 'checkout/checkout.html', context)

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            
            order = Order.objects.get(razorpay_order_id=razorpay_order_id)
            
            client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET_KEY))
            
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            
            # Verify signature
            try:
                client.utility.verify_payment_signature(params_dict)
            except Exception:
                messages.error(request, "Payment signature verification failed")
                order.status = 'failed'
                order.save()
                return redirect('checkout:payment_failed')
            
            # Update Order
            order.razorpay_payment_id = payment_id
            order.razorpay_signature = signature
            order.mark_completed() # This handles status and subscription
            
            # Record Coupon Usage
            if order.coupon_code:
                try:
                    coupon = Coupon.objects.get(code=order.coupon_code)
                    CouponUsage.objects.create(
                        coupon=coupon,
                        user=order.user,
                        order=order,
                        discount_amount=order.coupon_discount
                    )
                    coupon.current_uses += 1
                    coupon.save()
                except Coupon.DoesNotExist:
                    pass # Should not happen if logic is correct, but safe to ignore
            
            # Clear coupon from session
            if 'coupon_code' in request.session:
                del request.session['coupon_code']
            
            messages.success(request, "Payment successful! Your subscription is active.")
            return render(request, 'checkout/success.html', {'order': order})
            
        except Order.DoesNotExist:
            messages.error(request, "Order not found")
            return redirect('checkout:payment_failed')
        except Exception as e:
            messages.error(request, f"Payment verification failed: {str(e)}")
            return redirect('checkout:payment_failed')
            
    return redirect('dashboard:products:products')

def payment_failed(request):
    return render(request, 'checkout/failed.html')

@login_required
def apply_coupon(request):
    if request.method == "POST":
        code = request.POST.get('promo_code')
        type = request.POST.get('type')
        slug = request.POST.get('slug')
        
        if not code:
            messages.error(request, "Please enter a promo code")
            return redirect('checkout:checkout_view', type=type, slug=slug)
            
        try:
            coupon = Coupon.objects.get(code=code, is_active=True)
            
            # Check validity
            if not coupon.is_valid():
                messages.error(request, "This coupon is invalid or expired")
                return redirect('checkout:checkout_view', type=type, slug=slug)
                
            # Check user usage limit
            user_usage_count = CouponUsage.objects.filter(coupon=coupon, user=request.user).count()
            if coupon.max_uses_per_user > 0 and user_usage_count >= coupon.max_uses_per_user:
                messages.error(request, "You have already used this coupon the maximum number of times")
                return redirect('checkout:checkout_view', type=type, slug=slug)
            
            # Check applicability
            if type == 'bundle':
                item = get_object_or_404(BundledPlan, slug=slug)
                if coupon.applicable_plans.exists() and item not in coupon.applicable_plans.all():
                    messages.error(request, "This coupon is not applicable to this plan")
                    return redirect('checkout:checkout_view', type=type, slug=slug)
            else:
                item = get_object_or_404(MyProducts, slug=slug)
                if coupon.applicable_products.exists() and item not in coupon.applicable_products.all():
                    messages.error(request, "This coupon is not applicable to this product")
                    return redirect('checkout:checkout_view', type=type, slug=slug)
            
            # If all checks pass
            request.session['coupon_code'] = code
            messages.success(request, "Coupon applied successfully!")
            
        except Coupon.DoesNotExist:
            messages.error(request, "Invalid coupon code")
            
        return redirect('checkout:checkout_view', type=type, slug=slug)
    
    return redirect('dashboard:home')

@login_required
def remove_coupon(request, type, slug):
    if 'coupon_code' in request.session:
        del request.session['coupon_code']
        messages.success(request, "Coupon removed successfully")
    return redirect('checkout:checkout_view', type=type, slug=slug)