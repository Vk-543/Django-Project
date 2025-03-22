from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Theater, Seat, Booking
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
import razorpay
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=("YOUR_KEY_ID", "YOUR_KEY_SECRET"))

def movie_list(request):
    search_query = request.GET.get('search')
    if search_query:
        movies = Movie.objects.filter(name__icontains=search_query)
    else:
        movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})

def theater_list(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    theater = Theater.objects.filter(movie=movie)
    return render(request, 'movies/theater_list.html', {'movie': movie, 'theaters': theater})

@login_required(login_url='/login/')
def book_seats(request, theater_id):
    theaters = get_object_or_404(Theater, id=theater_id)
    seats = Seat.objects.filter(theater=theaters)
    if request.method == 'POST':
        selected_Seats = request.POST.getlist('seats')
        error_seats = []
        if not selected_Seats:
            return render(request, "movies/seat_selection.html", {'theater': theaters, "seats": seats, 'error': "No seat selected"})
        
        for seat_id in selected_Seats:
            seat = get_object_or_404(Seat, id=seat_id, theater=theaters)
            if seat.is_booked:
                error_seats.append(seat.seat_number)
                continue
            try:
                # Create a booking but do not save it yet
                booking = Booking(
                    user=request.user,
                    seat=seat,
                    movie=theaters.movie,
                    theater=theaters
                )
                seat.is_booked = True
                seat.save()
            except IntegrityError:
                error_seats.append(seat.seat_number)
        
        if error_seats:
            error_message = f"The following seats are already booked: {', '.join(error_seats)}"
            return render(request, 'movies/seat_selection.html', {'theater': theaters, "seats": seats, 'error': error_message})
        
        # Create a Razorpay order
        razorpay_order = razorpay_client.order.create({
            'amount': 50000,  # Amount in paise
            'currency': 'INR',
            'payment_capture': '1'
        })
        
        # Redirect to payment page with order details
        return render(request, 'movies/payment.html', {
            'razorpay_order_id': razorpay_order['id'],
            'amount': 50000,
            'booking': booking
        })
    
    return render(request, 'movies/seat_selection.html', {'theater': theaters, "seats": seats})

@receiver(post_save, sender=Booking)
def update_seat_availability(sender, instance, created, **kwargs):
    if created:
        instance.seat.is_booked = True
        instance.seat.save()

def reserve_seats(seats):
    for seat in seats:
        seat.is_booked = True
        seat.reservation_time = timezone.now()
        seat.save()

def release_reserved_seats():
    now = timezone.now()
    timeout_duration = timedelta(minutes=5)
    expired_seats = Seat.objects.filter(is_booked=True, reservation_time__lt=now - timeout_duration)
    for seat in expired_seats:
        seat.is_booked = False
        seat.save()
