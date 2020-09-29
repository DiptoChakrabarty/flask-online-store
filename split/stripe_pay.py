import stripe,os
from dotenv import load_dotenv
load_dotenv()  


stripe.api_key =  os.getenv("STRIPE_API")
print(stripe.api_key)


product = stripe.Product.create(
  name='T-shirt',
)

print(product)




price = stripe.Price.create(
  product= product["id"],
  unit_amount=2000,
  currency='usd',
)

# Set your secret key. Remember to switch to your live secret key in production!
# See your keys here: https://dashboard.stripe.com/account/apikeys
#stripe.api_key = 'sk_test_51HVJvaHDRl8tTEurQNRYDhVKuwt085thjj0Xw4u7G9CQgHQlRbPn1ywCUot82MVjtBNl9neDwMB4IcCeZwAI8iTj00rSoswdxn'

session = stripe.checkout.Session.create(
  payment_method_types=['card'],
  line_items=[{
    'price': product["id"],
    'quantity': 1,
  }],
  mode='payment',
  success_url='https://example.com/success?session_id={CHECKOUT_SESSION_ID}',
  cancel_url='https://example.com/cancel',
)
