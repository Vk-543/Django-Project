from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import razorpay
from .models import Theater, Seat, Booking
from django.contrib.auth.decorators import login_required

# Initialize Razorpay client
client = razorpay.Client(auth=("YOUR_RAZORPAY_KEY_ID", "YOUR_RAZORPAY_SECRET"))

def payment_view(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        currency = "INR"
        order = client.order.create({'amount': amount, 'currency': currency, 'payment_capture': '1'})
        razorpay_order_id = order['id']
        return render(request, 'movies/payment.html', {'razorpay_order_id': razorpay_order_id, 'amount': amount})

@csrf_exempt
def payment_confirm(request):
    if request.method == "POST":
        razorpay_order_id = request.POST.get("razorpay_order_id")
        payment_id = request.POST.get("payment_id")
        return JsonResponse({"status": "success", "razorpay_order_id": razorpay_order_id, "payment_id": payment_id})

def book_seats(request, theater_id):
    if request.method == "POST":
        selected_seat_ids = request.POST.getlist("seat_id")  # Retrieve a list of selected seat IDs
        theater = Theater.objects.get(id=theater_id)

        # Create bookings for each selected seat
        for seat_id in selected_seat_ids:
            seat = Seat.objects.get(id=seat_id)
            booking = Booking.objects.create(
                user=request.user,
                seat=seat,
                movie=theater.movie,
                theater=theater,
                show_time=theater.time,  # Set the show time from the theater
                payment_status='pending'  # Default status
            )

        return render(request, 'movies/booking_confirmation.html', {'theater_id': theater_id})
    else:
        available_seats = get_available_seats(theater_id)  # Placeholder for actual seat retrieval logic
        return render(request, 'movies/seat_selection.html', {'theater_id': theater_id, 'available_seats': available_seats})

@login_required
def user_profile(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'users/profile.html', {'bookings': bookings})

def search_movies(request):
    search_term = request.GET.get('search', '')
    movies = Movie.objects.filter(name__icontains=search_term)
    return render(request, 'movies/movie_list.html', {'movies': movies})

def movie_list(request):
    return render(request, 'movies/movie_list.html')

def theater_list(request, movie_id):
    return render(request, 'movies/theater_list.html', {'movie_id': movie_id})
