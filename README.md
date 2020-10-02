# Flask Online Store

### About the Project :open_book:

- API built using flask 
- The api comes with a bunch of functionalities
- The api is being upgraded you can checkout [issues here](https://github.com/DiptoChakrabarty/online-store/issues)
- DataBase is integrated with the api



### How to run the project  :horse_racing:
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

## Repository Structure :deciduous_tree:

 <img src="images/struct.png">

Based on the directories present

* Model directory contains all the database model class and methods associated
 
* Resource directory contains api resource classes 

* Schemas is for the marshmallow schemas 

* Split contains sample code which can help you understand the code base

* Static is the directory where user images are uploaded

* Templates conatins html templates


## DataBase Architecture :desktop_computer:
```sh

There are mainly four schemas 

* Users - which contains details about the users
* Store - which contains details about the store
* Items - which conatins deatisl about the items
* Order - which is for ordering stuff

### DataBase Architecture

- store and item : one to many 
- item and order: many to many 


```

## Functionalities present

1) flask_jwt_extended
  - [Read about it here](https://flask-jwt-extended.readthedocs.io/en/stable/)

  - flask jwt extended allows us to generate access and refresh tokens
  ```sh
        access_token = create_access_token(identity=user.id,fresh=True)
        refresh_token = create_refresh_token(user.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        },200
   ```
    
  - For all post and put methods jwt token is required

  - Deletion requires a fresh jwt token so might prompt you to sign in again

2) flask marshmallow
  - [Read about it here](https://flask-marshmallow.readthedocs.io/en/latest/)

  - flask marshmallow allows us to easily seralize and desarlize data 

  - Check marsh_app.py file under split directory which contains simple example of using flask marshmallow
  
   ```sh
        class RewardSchema(ma.SQLAlchemyAutoSchema):
            class Meta:
                model = Reward
                load_instance = True

        class MarshSchema(ma.SQLAlchemyAutoSchema):
            rewards = ma.Nested(RewardSchema,many=True)
            class Meta:
                model = Marsh
                load_instance = True

   ```
   
  - The example used above has been similarly implemented in the project

  - flask marshmallow latest version has syantax  different from previous versions 

  - marshamllow integrates well with SQLAlchemy 

3) flask mail 
  - [Read about it here](https://pythonhosted.org/Flask-Mail/)

  - flask mail allows us to integrate mailing service with flask easily

  - Check mail.py file under split directory which contains simple example to use flask mail
  
  ```sh
        msg= Message("Confirm Email",recipients=[email])
        link = url_for("token_verify",token=tok,_external=True)
        msg.body = "Verify email address by clicking here {}".format(link)
        mail.send(msg)
  ```
  
  - This is used for user confirmation during signup 

## Contribution Guidelines  🙂

When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.


## Pull Request Process

* Ensure any install or build dependencies are removed before the end of the layer when doing a build.
* Update the README.md with details of changes to the interface, this includes new environment variables, exposed ports, useful file locations and container parameters.
* Only send your pull requests to the development branch where once we reach a stable point it will be merged with the master branch .
* Associate each Pull Request with the required issue number.
* Please provide relevant steps to use your codebase adding few extra lines of comments or commands to run would be helpful for others to follow along .

## Branch Policy
- development: If you are making a contribution make sure to send your Pull Request to this branch . All developments goes in this branch.

- master: After significant features/bug-fixes are accumulated in development branch we merge it with the master branch.

## Contribution Practices

- Please be respectful of others , do not indulge in unacceptable behaviour 
- If a person is working or has been assigned an issue and you want to work on it please ask him/her if he is working on it
- We are happy to allow you to work on your issues , but in case of long period of inactivity  the issue will be approved to another volunteer
- If you report a bug please provide steps to reproduce the bug.
- In case of changing the backend routes please submit an updated routes documentation for the same.
- If there is an UI related change it would be great if you could attach a screenshot with the resultant changes so it is easier to review for the maintainers

