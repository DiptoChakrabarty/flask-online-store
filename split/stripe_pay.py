import stripe,os
from dotenv import load_dotenv
load_dotenv()  
from flask import Flask,url_for,render_template

app=Flask(__name__)

stripe.api_key =  os.getenv("STRIPE_API")
public_key = os.getenv("STRIPE_API_PUBLIC")


def create_product(name,price):
  product = stripe.Product.create(
    name=name,
  )
  price = stripe.Price.create(
  product= product["id"],
  unit_amount=price,
  currency='usd',
)
  return product["id"]




token=stripe.Token.create(
  card={
    "number": "4242424242424242",
    "exp_month": 9,
    "exp_year": 2021,
    "cvc": "314",
  },
)

print(token)


'''
@app.route("/")
def index():
  session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
      'price': 10,
      'quantity': 1,
    }],
    mode='payment',
    success_url=url_for("thanks",_external=True) + '?session_id={CHECKOUT_SESSION_ID}',
    cancel_url=url_for("index",_external=True),
  )
  return render_template("index.html",check_session_id=session["id"],
      checkout_public_key=stripe.api_key)
'''