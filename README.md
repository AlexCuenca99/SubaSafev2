# ❗ **IMPORTANT: This an API for Online Auction System SubaSafe**

# Getting Started with Suba Safe Online Auction Site

## 👩‍🏫 How it woks?

Don't worry. It is easy to use. You must follow these steps:

1. **Required Packages:** Before starting, you need to install Python and pip. Then you have to install Django. **Don't forget to use a virtual enviroment!**

2. **Download the source project:** Download or clone the project to your computer.

3. **Open the project (Optional):** Once you have downloaded the project, extract it! You should open the project in your code editor so that you can see or understand the structure of the project.

4. **Before execute the project:**

    1. **makemigrations:** Open new terminal and inside the root directory type: `python manage.py makemigrations` to create the migrations (generate the SQL commands).
    2. **migrate:** Then run `python manage.py migrate` to run the migrations (execute the SQL commands).
    3. **Dump data:** Make sure your DB is completely empty and then run `python manage.py loaddata subasafe_data.json`

    **Not necessary**

    4. **Create a superuser:** To get logged into the application you have to create a superuser. Use `python manage.py createsuperuser`then complete the requested data.

5. **Execute the project:** Now you have completed the previous steps, run `python manage.py runserver` on the root directory. If everything went well, you should be able to observe a line with the following: `Starting development server at http://127.0.0.1:8000/`. All you have to do is copy that address and paste it into your search bar. Also, you can type the address `localhost:8000`.

# Python Version

**3.7.9**

# 📢 USEFUL INFORMATION

## FIREBASE UNIQUE IDENTIFIER

`subasafe-e683d`

# ☑️ USEFUL COMMANDS

-   In order to activate the Virtual Enviroment on Windows OS use `.\envs\subaSafe\Scripts\activate`

-   **SuperUser:**

    -   Username: `admin`,
    -   Email: `admin@subasafe.com`,
    -   Password: `admin`

-   **All users:**

    -   username: `<my_username>`
    -   email: `<my_username>@subasafe.com`
    -   password: `<my_username>`

-   **How to know my installed packages**

    -   `pip freeze --local`

-   **Registrar un usuario vía Firebase (Google):**

    1. Ingresar a la URL `http://localhost:8000/login/` aplastar sobre registrar y registrar la cuenta de google
    2. Desde la consola del navegador, copiar el token otorgado por Firebase y copiarlo en la dirección `http://localhost:8000/api/google-login/`
    3. Ahora se ha guardado un token dentro de la base de datos.

-   **Registrar un usuario dentro de la app interna:**

    1.  Ingresar a la URL `http://127.0.0.1:8000/api/auth/register/` y proveer los datos.
    2.  Ingresar al correo. Se observará algo así: `Hi AlexSubaSafe Use the link below to verify your email http://127.0.0.1:8000/verificar-email/? token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9. eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUyNjQ5NTMwLCJpYXQiOjE2NDIyODE1MzAsImp0a SI6IjNkZGJhMThkMzBhMDQ4N2ZiYzM0NGQzYTYxMTg4OTI4IiwidXNlcl9pZCI6NH0. XktbXFfCutND9AlmJKasaLoXmn4vxEEwo53ls1Uk-hY`.

        **Debería copiar:** `eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9. eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjUyNjQ5NTMwLCJpYXQiOjE2NDIyODE1MzAsImp0a SI6IjNkZGJhMThkMzBhMDQ4N2ZiYzM0NGQzYTYxMTg4OTI4IiwidXNlcl9pZCI6NH0. XktbXFfCutND9AlmJKasaLoXmn4vxEEwo53ls1Uk-hY`.

    3.  Copie el token en la dirección `​http://127.0.0.1:8000/verificar-email​/`. Si tiene un mensaje de `{"STATUS": "El usuario ha sido activado"}` entonces puede continuar.

-   **Autenticación de Sesión con Firebase Google:**

    1. Para poder hacer las operaciones CRUD, se debe enviar los datos por cabecera.

        **Key:** Authorization **Value:** Token 'token en la BD'

-   **Autenticación de Sesión con un usuario interno:**

    1. Ingrese en la dirección `http://127.0.0.1:8000/api/auth/login/` y loguee el correo y contraseña.
    2. Para poder hacer las operaciones CRUD, se debe enviar los datos por cabecera.

        **Key:** Authorization **Value:** Bearer 'token de acceso del paso anterior'

# ⁉️ TROUBLESHOOTING

-   **ERROR:** django is not recognized as a command:

    **SOLUTION:** python and python3: Use python only when you are going to use manage.py file.

-   **ERROR:** AssertionError at /api/users/
    'UserApiViewSet' should either include a `queryset` attribute, or override the `get_queryset()` method.

    **SOLUTION:** <https://stackoverflow.com/questions/40721512/assertionerror-at-posts-postlist-should-either-include-a-queryset-attribut>

-   **ERROR:** partial_update method is not working

    **SOLUTION:** Make sure that the last field doesn't end in a comma.

-   **ERROR:** 'Manager' object has no attribute 'get_by_natural_key'

    **SOLUTION:** Define an object which contains the manager for that model. <https://www.google.com/search?q=which&oq=wich&aqs=edge.1.69i57j0i10i512j0i512l2j0i10j0i10i512j0i10j0i10i512j0i10.1448j0j1&sourceid=chrome&ie=UTF-8>

-   **ERROR:** TemplateDoesNotExist: users/login.html

    **SOLUTION:** Install Unipath package, then change the BASE_DIR to `BASE_DIR = Path(__file__).resolve().ancestor(3)`. Once made that, change \_DIRS\* in TEMPLATES to `'DIRS': [BASE_DIR.child('templates')],`. In **settings/local.py** change DATABASE/default/NAME to `'NAME': BASE_DIR.child('db.sqlite3')`

-   **ERROR:** The serializer field might be named incorrectly and not match any attribute or key on the `QuerySet` instance. Original exception text was: 'QuerySet' object has no attribute 'username'.

    **SOLUTION:** Add many=True to the **serialized_users** <https://stackoverflow.com/questions/61162245/original-exception-text-was-queryset-object-has-no-attribute-name-using-dja>

-   **ERROR:** Add null field to a serializer

    **SOLUTION:** Add allow_null=True in serializer field. <https://stackoverflow.com/questions/42158692/django-nested-serializer-allow-null-true>

-   **ERROR:** Turn single fields in an object field

    **SOLUTION:** Make a new SerializerMethodField Where the desired fields are included. Then create a serializer to those fields.

_By: Alex Cuenca_
