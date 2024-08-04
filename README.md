# Skeleton Django + PostgreSQL - Custom User With `DRF Token` and `Django Groups & Permissions` and `NO Repository Pattern`

- Deps:

```sh
pip install django djangorestframework django-cors-headers python-dotenv psycopg2-binary
pip install django-filter
pip install drf-yasg
pip install django-redis
```


Description:
  - djangorestframework:            REST Framework
  - djangorestframework-simplejwt:  W con JWT
  - pillow:                         W con Images
  - django-cors-headers:            CORS
  - python-dotenv:                  EnvV
  - drf-yasg:                       Swagger with serializers
  - django-filter                   Easy way to work with filters in Django
  - django-redis                    Redis with Django



## Set up
### Virtual Env
- --- Crear el Virtual Environment
  - Creamos VE para aislar cada Project con sus propias Deps, e incluso versiones de Python

  - -- Instalamos de manera Global la Dep para poder crear estos Virtual Envs   (solo si no lo tenemos)
    - run:    `pip install virtualenv`
      
  - -- Creamos el entorno virtual en directorio del project
    - run:    `python -m virtualenv venv`
      - Esto lo crea, pero NO lo activa

  - -- Activamos el Virtual Env (linux)  -  Esto solo aplica a la Terminal q lo corre
    - run:    `. venv/bin/activate`

    - -- Activar el   Virtual Env   en todo   `VSCode`
      - `Ctrl+Shift+P` >> Python: Select Interprete >> Seleccionamos el de la Star







### Install and run Django and DRF

```sh
pip install django djangorestframework django-cors-headers python-dotenv psycopg2-binary
pip install django-filter
pip install drf-yasg
```

- -- Comprobamos q se haya instalado correctamente
  - run:    `django-admin --version`
  - run:    `python -m django --version`


- --- Creamos el    `requirements.txt`     para tener registro de los packages instalados
  - -- Como tener un package.json
    - run:    `pip freeze > requirements.txt`

  - -- En prod o en otra PC simplemente los instalamos leyendo ese archivo:
    - run:    `pip install -r requirements.txt`





#### Init Django App
- --- Creamos el     `Project`      con Django como en cualquier project d django
  - -- NO usar palabras claves para nombrar el proyecto como django, test, ect.
    - run:    `django-admin startproject backend .`
      - Lo crea en el path q estoy


  - -- Registramos REST Framework en el    `settings.py >> INSTALLED_APPS`
    - `'rest_framework',`


  - -- Levantar el dev server con 1 PORT especifico
    - run:    `python manage.py runserver 3300`



#### Migrations
- --- Debemos crear las tablas mediante la creacion y correr MIGRACIONES
  - -- Al INICIO corremos de todas las migraciones para q se cree las tablas q django trae x default
    - run:    `python manage.py makemigrations`
    - run:    `python manage.py migrate`

    - Una vez se Corra la migration vemos q ya tenemos la tabla de user y demas tablas q nos da x default django



- --- Crear y Correr MIGRACIONES propias basadas en nuestros MODELS
  - -- Podemos especificar el    `App`   para solo crear y correr sus migraciones
    - run:    `python manage.py makemigrations users`
    - run:    `python manage.py migrate users`










<!-- ================================================================ -->
<!-- //////////////////////////////////////////////////////////////// -->
# Settings & Envs
- --- Configuramos los Envs para q puedan ser cargamos desde el    `.env`    gracias al    python-dotenv     q instalamos
  - -- Configuramos eso para la    SECRED_KEY
  - -- Configuramos los   CORS   como middleware
    
    ```py
      from datetime import timedelta

      # EnvV
      import os
      from dotenv import load_dotenv

      load_dotenv()


      # ## Load Envs from  .env
      SECRET_KEY = os.environ.get('SECRET_KEY') 


      MIDDLEWARE = [
        # CORS headers: before CommonMiddleware
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
      ]


      # ### Static files: Vamos a meter Reat dentro d Django (esta app es asi, pudo haber sido solo api y react aparte)
      STATIC_URL = 'static/'
      STATIC_ROOT = os.path.join(BASE_DIR, 'static')
      STATICFILES_DIRS = [
          os.path.join(BASE_DIR, 'dist/static')
      ]
      MEDIA_URL = 'media/'
      MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



      # ### CORS Origin
      CORS_ALLOWED_ORIGINS = [
          # React app - dev
          'http://localhost:5173'
      ]
      CORS_ALLOW_CREDENTIALS = True



      # ### JWT
      SIMPLE_JWT = {
          'ACCESS_TOKEN_LIFETIME': timedelta(hours=3),
          'REFRESH_TOKEN_LIFETIME': timedelta(hours=3),
          'ROTATE_REFRESH_TOKENS': True,
          'BLACKLIST_AFTER_ROTATION': True, # llevar al blacklist los usados
          'UPDATE_LAST_LOGIN': False,

          'ALGORITHM': 'HS256',

          'VERIFYING_KEY': SECRET_KEY,
          'AUDIENCE': None,
          'ISSUER': None,
          'JWK_URL': None,
          'LEEWAY': 0,

          'AUTH_HEADER_TYPES': ('Bearer',),
          'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
          'USER_ID_FIELD': 'id',
          'USER_ID_CLAIM': 'user_id',
          'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

          'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
          'TOKEN_TYPE_CLAIM': 'token_type',
          'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

          'JTI_CLAIM': 'jti',
      }

      REST_FRAMEWORK = {
          'DEFAULT_AUTHENTICATION_CLASSES': (
              'rest_framework_simplejwt.authentication.JWTAuthentication',
          )
      }

    ```





<!-- ================== Views ==================== -->
# Flux:
1. Model
   1. Set in Installed apps
2. Filters
3. Serializers
4. Views
5. Urls





















<!-- ================================================================ -->
<!-- //////////////////////////////////////////////////////////////// -->
## Creamos el    Users    Application
- --- Simplemente es la creacion del application de python
  - -- run:   `python manage.py startapp users`



- --- Creamos el   User Model    q es propio, no el q trae x default en    `models.py`
  - -- Como Django ya nos da 1 model d    User    para usar 1 custom Debemos Configurar y Registrarlo en Django
    - Lo registramos en el    `settings.py`
      ```py
        # ### Custom User Model: app.Model
        AUTH_USER_MODEL = 'users.User'
      ```


- --- Al crear las    Migrations     veremos q tb se crea para el    token_blacklist
  - -- Aqui se iran registrando los tokens ya usados



## Auth with Custom User Model
- --- Como tenemos 1 custom UserModel y vamos a aplicar  `JWT`   debemos gestionar manualmente los Serializers y Views para los methods de   Auth



- --- Creamos el     `serializers.py`     para definir los Serializers para el Auth
  - -- Creamos el    `RegisterUserSerializer`     q sera el serializer (like DTO)
    - Los   fields    q definamos ahi sera lo q se envie serializado a JSON en al Response

  - -- Como estamos W con    JWT    debemso gestionar su creacion. Q nomas vamos a incluir en el Payload del token.
    - Para esto creamos el    `MyTokenObtainPairSerializer`    q hara el build del JWT
      - Este sera retornado en el     `LoginView`     cuando sea llamado x la   urls.py   al atender a la req q deba



- --- Creamos las views en el      `views.py`     para q sean invocadas x las urls.py
  - -- Creamos el method     `register()`     q se encargara de la creacion y persistencia en DB del user
    - Este W con el      RegisterUserSerializer      para retornar como Respnose esa serializacino
      - Al ser invocado x urls.py en el:
            path('register/', views.register),

  - -- Creamos el     `LoginView`     q es la    Class    q al HEREDAR d    TokenObtainPairView     seteara   el    MyTokenObtainPairSerializer    para q sea tomado en cuenta y cree el JWT con ese payload en especifico
    - Este sera usado en las     views.py     como 1 view methdo y no como class
        path('login/', views.LoginView.as_view()),



- --- Creamos el    `urls.py`     q tendra todos los endpoints y las views q se haran cargo
  - -- NOOO se hace como en Fazt con el       routers.DefaultRouter()      d REST Framework
    - Sino q se hace normal, como en Django normal
      - Con el     path     `<---`     NOOOOO crea los Verbos HTTP para las CRUD operations
        - NO se crea ni siquiera el      ViewSet      q habilita todas las operaciones CRUD


  - -- Registramos estos    endpoints    en el     `urls.py`    principal del   `PROJECT`
    - Tal q asi
      ```py
        path('users/', include('users.urls'))
      ```



  - -- Con esto     Baicamente     hemos culminado el Auth en Django
    - Con el   UserModel   Custom   y con la implementacion del    `JWT`


















<!-- ================================================================ -->
<!-- //////////////////////////////////////////////////////////////// -->
# Products App
- --- Creamos el App de products
  - -- Usamos el    manage.py   startapp
    - run:    `python3 manage.py startapp products`


  - -- Creamos el Model para Product y para Review
    - Vamos a tener       Relaciones/Asociaciones       entre tablas
      - Entonces definimos los models en     `models.py`
        - Product & Review


  - -- Creamos y Corremos las migraciones:
    - run:    `python3 manage.py makemigrations products`
    - run:    `python3 manage.py migrate products`




- --- Creamos el     `serializer.py`       para definir los Serializers de products
  - -- Creamos el    `ProductSerializer`      q tendra    RELACION/ASOCIACION     con   reviews
    - Aqui incluso serializamos las relaciones
    - Tener en cuenta la   fn()   q obtiene la data d la recion



- --- Creamos las     Views     en el `views.py`
  - -- Definimos manualmente las views q responderan a cada operacion CRUD
    - NOOOO usamos    REST Framework    para q los cree en auto, sino q son custom x nosotros
        @api_view(['GET'])
        @api_view(['POST'])
        @api_view(['PUT'])
        @api_view(['DELETE'])



- --- Definimos los      Endpoints     en el     `urls.py`
  - -- Igualmente, manual para c/view method del CRUD
    - Lo malo es q quedan medias raras con el:    /post    /get/1/







## Pagination
- --- Creamos el     `pagination.py`     q tendra la logica de la paginacion. Lo creamos en el     PROJECT
  - -- El    `CustomPagination`     es general para todo tipo de response
    - Simplemente el     paginate_queryset()      recibe:
      - El QuerySet a paginar
      - Request actual





## Categories
- --- Lo maneja en el Products mismo xq no es una tabla aparte la de Categories
  - -- s




## Users
- --- Get all users
  - -- Creamos el     `UserSerializer`     para serializar lo q viene d DB x el ORM a JSON
    - Aqui especificamos los    fileds   q queremos incluir
  
  - -- Creamos el     `get_users`       view para q solo el Admin pueda acceder
    - Evaluamos si es admin basado en el      `is_staff`





















<!-- ================================================================ -->
<!-- //////////////////////////////////////////////////////////////// -->
# Orders App  -  `PayPal`
- --- Para todo el tema de las Compras vamos a manejar x Ordenes de Compra x PayPal
  - -- Comenzamos x crear la    App   d Django
    - run:    `python manage.py startapp orders`

  - -- Agregamos esta app al   INSTALLED_APPS    del     settings.py

  - -- Creamos la URL para esta app en el    urls.py    del PROJECT


  - -- Corremos las Migraciones
    - run:    `python manage.py makemigrations orders`
    - run:    `python manage.py migrate orders`








# OJO
- --- Tuve problemas con el    `image`    de product xq espera 1 File, este lo almancena en FileSystem en    'media/'
  - -- Con el valor x default ya no envie en el JSON y ya funco
      ```py
        image = models.ImageField(default='placeholder.png')
      ```



