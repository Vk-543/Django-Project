from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import razorpay

# Initialize Razorpay client
client = razorpay.Client(auth=("YOUR_RAZORPAY_KEY_ID", "YOUR_RAZORPAY_SECRET"))

# Create your views here.
def payment_view(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        currency = "INR"
        # Create a Razorpay order
        order = client.order.create({'amount': amount, 'currency': currency, 'payment_capture': '1'})
        razorpay_order_id = order['id']
        return render(request, 'movies/payment.html', {'razorpay_order_id': razorpay_order_id, 'amount': amount})

@csrf_exempt
def payment_confirm(request):
    if request.method == "POST":
        # Handle payment confirmation logic here
        razorpay_order_id = request.POST.get("razorpay_order_id")
        payment_id = request.POST.get("payment_id")
        # Verify the payment with Razorpay
        # Add your verification logic here
        return JsonResponse({"status": "success", "razorpay_order_id": razorpay_order_id, "payment_id": payment_id})

def book_seats(request, theater_id):
    if request.method == "POST":
        # Logic to handle seat booking
        # You may want to retrieve the selected seats and save the booking to the database
        return render(request, 'movies/booking_confirmation.html', {'theater_id': theater_id})
    else:
        # Render the seat selection page
        return render(request, 'movies/seat_selection.html', {'theater_id': theater_id})

def movie_list(request):
    return render(request, 'movies/movie_list.html')  # Make sure this template exists

def theater_list(request, movie_id):
    # Dummy logic for now
    return render(request, 'movies/theater_list.html', {'movie_id': movie_id})