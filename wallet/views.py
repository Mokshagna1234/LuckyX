from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from users.models import UserProfile

@login_required
def wallet_page(request):
    return render(request, 'wallet.html')

@login_required
def wallet_balance(request):
    profile = UserProfile.objects.get(user=request.user)
    return JsonResponse({
        'wallet_balance': float(profile.wallet_balance)
    })
