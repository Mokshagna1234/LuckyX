from django.urls import path
from .views import join_draw, current_draw, recent_winners,draw_queue,draw_page

urlpatterns = [
    path('',draw_page),
    path('queue/', draw_queue), 
    path('join/<int:draw_id>/', join_draw),
    path('current/', current_draw),
    path('winners/', recent_winners),
]

