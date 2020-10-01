import stripe,os
from dotenv import load_dotenv
load_dotenv() 

stripe.api_key =  os.getenv("STRIPE_API")