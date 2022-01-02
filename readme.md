# Documentation
## To run this project
                        
            >> git clone https://github.com/OsamaHaikal/backend_api.git
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

     >> WishList model
           user: ForeignKey

     >> WishList item model
            wishlist: ForeignKey
            product: ForeignKey

     >> WishList item model
            wishlist: ForeignKey
            product: ForeignKey

     >> CheckoutDetails model
            user: ForeignKey
            cart: ForeignKey
            name_of_receiver: CharField
            main_address: CharField
            secondary_address: CharField
            delivery_address: CharField
            phone_number: 
            postal_code:
     >> Shipping details model
            user: ForeignKey
            cart: ForeignKey
            name_of_receiver: CharField
            main_address: CharField
            city: CharField
            secondary_address: CharField
            delivery_address: CharField
            phone_number: 
            postal_code:

    
# API Documentation

    To change the permissions of any endpoint just add permission_classes in the api.views 

        permssion_classes=  [AllowAny, . . . ]

    
    <note: if you didn't write allowany it will require token authentication because its the default persmission in settings>
    
## localhost:8000/:

    This endpoint returns the available endpoints with link and allowed HTTP methods

    [
    {
        "Method": "POST",
        "ENDPOINT": "http://127.0.0.1:8000/api/send_email/"
    },
    {
        "Method": "POST",
        "ENDPOINT": "http://127.0.0.1:8000/api/shipping/1"
    },
    {
        "Method": "POST",
        "ENDPOINT": "http://127.0.0.1:8000/api/register/"
    },
    {
        "Method": "POST",
        "ENDPOINT": "http://127.0.0.1:8000/api/login/"
    },
    {
        "Method": "POST",
        "ENDPOINT": "http://127.0.0.1:8000/api/refresh_token/"
    },
    {
        "Method": [
            "GET",
            "POST"
        ],
        "ENDPOINT": "http://127.0.0.1:8000/api/categories/"
    },
    {
        "Method": [
            "GET",
            "PUT",
            "DELETE"
        ],
        "ENDPOINT": "http://127.0.0.1:8000/api/categories/1"
    },
    {
        "Method": [
            "GET",
            "POST"
        ],
        "ENDPOINT": "http://127.0.0.1:8000/api/products/"
    },
    {
        "Method": [
            "GET",
            "PUT",
            "DELETE"
        ],
        "ENDPOINT": "http://127.0.0.1:8000/api/products/1"
    },
    {
        "Method": [
            "GET",
            "PUT",
            "DELETE"
        ],
        "ENDPOINT": "http://127.0.0.1:8000/api/products/1/reviews"
    },
    {
        "Method": [
            "POST"
        ],
        "ENDPOINT": "http://127.0.0.1:8000/api/checkout/"
    },
    {
        "Method": [
            "GET"
        ],
        "ENDPOINT": "http://127.0.0.1:8000/api/cart/"
    },
    {
        "Method": [
            "GET",
            "PUT",
            "DELETE"
        ],
        "ENDPOINT": "http://127.0.0.1:8000/api/cart/1/"
    }
]
## localhost:8000/api/send_email/

            methods: POST
            Content-Type: application/json

            {
                 "email":
                    "This field is required."
            }

            to change body and subjet go to /api/views

            to change the email host settings go to /core/settings


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

## localhost:8000/api/cart/

    methods GET, POST

    Authenticate: Bearer realm="api"

    user must be authenticated and signed-in

    returns:
        
        {
            "detail": "Authentication credentials were not provided."
        }

        or 
        {
            "error":"login required"
        }

## localhost:8000/api/cart/<str:id>

    methods: GET, PUT, PATCH, DELETE

    returns the items in each cart and if user is not authenticated it will return:

    HTTP 403 Forbidden

            
        {
            "detail": "Sorry this cart not belong to you"
        }
## http://127.0.0.1:8000/api/shipping/1/

    methods: GET, PUT, PATCH, DELETE

        {
            "name_of_receiver": "",
            "main_address": "",
            "delivery_address": "",
            "city": "",
            "postal_code": "",
            "phone_number": ""
        }

## http://127.0.0.1:8000/api/checkout/ 

    Allow: GET, POST, HEAD, OPTIONS


            {
            "cart": null,
            "name_of_receiver": "",
            "main_address": "",
            "secondary_address": "",
            "city": "",
            "postal_code": "",
            "phone_number": ""
        }

# References
1. https://github.com/django-oscar
2. https://www.django-rest-framework.org/
3. https://django-rest-framework-simplejwt.readthedocs.io/en/latest/

4. https://docs.djangoproject.com/en/4.0/topics/class-based-views/generic-display/

5. https://www.django-rest-framework.org/tutorial/3-class-based-views/

6. https://www.django-rest-framework.org/topics/documenting-your-api/