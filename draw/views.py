import json
import random
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import LuckyDraw, Ticket
from .serializers import LuckyDrawSerializer
from users.models import UserProfile


# =============================
# DASHBOARD
# =============================
def dashboard(request):
    return render(request, 'home.html')


# =============================
# JOIN DRAW (BUY TICKETS)
# =============================
@require_POST
@login_required
def join_draw(request, draw_id):
    draw = get_object_or_404(LuckyDraw, id=draw_id)

    if draw.status != 'OPEN':
        return JsonResponse({'error': 'Draw is closed'}, status=400)

    profile = UserProfile.objects.get(user=request.user)

    # ---- READ JSON BODY (FETCH FIX) ----
    try:
        data = json.loads(request.body)
        tickets_to_buy = int(data.get('tickets', 1))
    except Exception:
        return JsonResponse({'error': 'Invalid request'}, status=400)

    if tickets_to_buy < 1:
        return JsonResponse({'error': 'Invalid ticket count'}, status=400)

    TICKET_PRICE = 10
    TOTAL_TICKETS = 50

    cost = tickets_to_buy * TICKET_PRICE
    tickets_sold = draw.tickets.count()
    remaining = TOTAL_TICKETS - tickets_sold

    if tickets_to_buy > remaining:
        return JsonResponse(
            {'error': f'Only {remaining} tickets left'},
            status=400
        )

    if profile.wallet_balance < cost:
        return JsonResponse({'error': 'Insufficient balance'}, status=400)

    # ---- ATOMIC TRANSACTION ----
    with transaction.atomic():
        profile.wallet_balance -= cost
        profile.save()

        tickets = [
            Ticket(draw=draw, user_profile=profile)
            for _ in range(tickets_to_buy)
        ]
        Ticket.objects.bulk_create(tickets)

    # ---- CHECK & PICK WINNER ----
    result = check_and_pick_winner(draw)

    return JsonResponse({
        'message': f'{tickets_to_buy} ticket(s) purchased successfully',
        'tickets_left': TOTAL_TICKETS - draw.tickets.count(),
        'winner': result
    })


# =============================
# PICK WINNER LOGIC
# =============================
def check_and_pick_winner(draw):
    tickets = list(draw.tickets.all())

    if len(tickets) < 50:
        return None

    winning_ticket = random.choice(tickets)
    winner_profile = winning_ticket.user_profile

    # ---- SHARES ----
    WINNER_AMOUNT = 450
    PLATFORM_SHARE = 25
    CLIENT_SHARE = 25

    winner_profile.wallet_balance += WINNER_AMOUNT
    winner_profile.save()

    draw.winner = winner_profile.user
    draw.platform_share = PLATFORM_SHARE
    draw.client_share = CLIENT_SHARE
    draw.status = 'CLOSED'
    draw.save()

    return {
        'winner_public_id': winner_profile.public_id,
        'ticket_code': winning_ticket.ticket_code
    }


# =============================
# CURRENT DRAW
# =============================
@api_view(['GET'])
def current_draw(request):
    draw = get_or_create_active_draw()
    serializer = LuckyDrawSerializer(draw)
    return Response(serializer.data)


# =============================
# RECENT WINNERS
# =============================
@api_view(['GET'])
def recent_winners(request):
    draws = LuckyDraw.objects.filter(status='CLOSED').order_by('-id')[:10]

    data = []
    for draw in draws:
        winning_ticket = draw.tickets.first()
        if winning_ticket:
            data.append({
                'winner_public_id': winning_ticket.user_profile.public_id,
                'winning_ticket': winning_ticket.ticket_code
            })

    return Response(data)


# =============================
# DRAW CREATION / ROLLOVER
# =============================
def get_or_create_active_draw():
    draw = LuckyDraw.objects.filter(status='OPEN').last()

    if draw and draw.end_time > timezone.now():
        return draw

    if draw:
        draw.status = 'CLOSED'
        draw.save()

    start_time = timezone.now()
    end_time = start_time + timedelta(hours=1)

    return LuckyDraw.objects.create(
        start_time=start_time,
        end_time=end_time,
        status='OPEN'
    )

def draw_page(request):
    return render(request, 'draw.html')

def draw_queue(request):
    """
    Returns 5–6 draws spaced by 5 minutes
    Demo-safe, backend-ready
    """
    now = timezone.now()

    draws = []
    for i in range(6):
        start = now + timedelta(minutes=i * 5)
        end = start + timedelta(minutes=5)

        draws.append({
            'id': i + 1,
            'prize': 450,
            'ticket_price': 10,
            'total_tickets': 50,
            'tickets_sold': i * 7 % 50,
            'end_time': end.isoformat(),
            'status': 'OPEN' if i == 0 else 'UPCOMING'
        })

    return JsonResponse(draws, safe=False)