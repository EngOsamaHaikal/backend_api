# Documentation
## To run this project
                        
            >> git clone <github link>
            >> python3 -m venv env
            >> source env/bin/activate
            >> pip install -r requirements.txt

### This project consists of two user defined apps
        
            1. accounts
            2. store

### The core folder which contains the settings and urls files

# 
## Account app

    models
        >> UserManager model
        >> CustomUser model

    where both models inherit from the abstract django models and the goal is to create custom user model that contains phonenumber field and requires the email field instead of username field in registration

    Phonenumber field documentation:
    
    https://pypi.org/project/django-phonenumber-field/

    To use this custom user model in settings:

    USER_AUTH_MODEL = accounts.CustomUser

## Store app

    models
      >> custom Base abstract model with two attributes

      >> category model
            name: CharField
            slug: SlugField

      >> variant model
            name: CharField
            slug: SlugField

      >> Product model
            categories: ManyToManyField
            variant: ManyToManyField
            titlle: CharField
            slug: SlugField
            description: TextField
            price: PositiveIntegerField
            discount: IntegerField
            stock: IntegerField
            available: BooleanField
            image: ImageField
            status: CharField|choices
        
      >> Reviews Model
            product: ForeignKey
            user: ForeignKey
            content: CharField

      >> Cart model
            user: ForeignKey
            total: DecimalField

    ## each time user is created a cart model also created belongs to this userb 

     >> Cart item model
        cart: ForeignKey
        product: ForeignKey
        quantity: IntegerField

# API Documentation

## localhost:8000/:

    this endpoint returns the available endpoints with link and allowed HTTP methods

## localhost:8000/api/resgister/

        methods: POST
            Content-Type: application/json

        {
                "username": 
                    "This field is required."
                ,
                "password": 
                    "This field is required."
                ,
                "password2":
                    "This field is required."
                ,
                "email":
                    "This field is required."
                ,
                "phone_number":
                    "This field is required."
                
        }

        username, phonenumber and email must be unique

        phone number in this format +962xxxxxxx

        to change the format follow the documanation link
        https://pypi.org/project/django-phonenumber-field/


## localhost:8000/api/token/

        methods: POST
        Content-Type: application/json
        {
            "email": "",
            "password": ""
        }

        returns {
            "refresh":"<your_token>",
            "access":"your_token"
        }

## localhost:8000/api/refrest_token/
        methods: POST
        Content-Type: application/json
        
        {
            "refresh": ""
        }

        returns {
            access: ""
        }

 ## localhost:8000/api/categories/

        you can paginate using url/?limit=<int> & offset=<int>

        methods: POST, GET
        Content-Type: application/json
        to add new category:

            POST:
                {
                    "name": "",
                    "slug": ""
                }

        returns
            {
                "count": number of elements,
                "next": "link" or null,
                "previous": "link" or null,
                "results": [
                    {
                        "id": 1,
                        "name": "category",
                        "slug": "category"
                    },
                    ...
            }

 ## localhost:8000/api/categories/<str:id>

        methods: Allow: GET, PUT, PATCH, DELETE

        returns:  {
                id: "cat_id",
                "name": "cat_name",
                "slug": "cat_slug"
            }

## localhost:8000/api/products/
        you can paginate using url/?limit=<int> & offset=<int>

        methods: POST, GET
        Content-Type: application/json
        to add new product:
            POST:
            {
                "title": "",
                "slug": "",
                "description": "",
                "price": null,
                "discount": null,
                "stock": null,
                "available": false,
                "sizes": null,
                "status": null,
                "image": null,
                "category": [],
                "variant": []
            }

        returns
            {
                "count": number of elements,
                "next": "link" or null,
                "previous": "link" or null,
                "results": [
                    {
                        "id": 1,
                         ...
                    },
                    ...
            }

        and this endpoint is cached

## localhost:8000/api/products/<str:id>

        methods: Allow: GET, PUT, PATCH, DELETE

        returns:  {
            "id": ,
            "updated_on": "",
            "created_on": "",
            "title": "",
            "slug": "",
            "description": "",
            "price": ,
            "discount": ,
            "stock": ,
            "available": ,
            "sizes": "",
            "status": "",
            "image": "",
            "category": [
               
            ],
            "variant": [
                
            ]
        }

## localhost:8000/api/products/<str:id>/reviews/
        methods: GET, PUT, PATCH, DELETE
        Content-Type: application/json

        returns: 

                {
                    "id": ,
                    "product": ,
                    "user":,
                    "content": ""
                }




