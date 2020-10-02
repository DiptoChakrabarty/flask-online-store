# Flask Online Store

### About the Project

- API built using flask 
- The api comes with a bunch of functionalities
- The api is being upgraded you can checkout issues here
- DataBase is integrated with the api



### How to run the project 
```sh
* Clone the repository 
 git clone https://github.com/DiptoChakrabarty/online-store.git

* Enter directory 
 cd flask-online-store

* Activate virtual environment
  source venv/bin/activate

* Install packages
  pip3 install -r requirements.txt

* Set environment variables
 cp .env.example .env

* Fill the parameters

  CLIENT_ID= {Github Client Id}
  CILENT_SECRET= {Github Client Secret}
  STRIPE_API= {Stripe token}
  MAIL_USERNAME = {Email Id }
  MAIL_PASSWORD = {Email Password}

* Remove site.db to start from fresh database
  rm site.db

* Start app
  python3 app.py

* Head over to http://localhost:5000
  (it is preferable if you use something as postman as most are post requests)


```