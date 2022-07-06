import razorpay
from shop.models import APIRazor

# client = razorpay.Client(auth=("rzp_live_LQb1lTTOEq2GqI", "X2BTvQCiFrl7N2TIwMcRj9Cp"))
api = APIRazor.objects.first()
client = razorpay.Client(auth=(api.api_key, api.api_secret))