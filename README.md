# Authenove Ecommerce Website With Django, Django Template Rendering(HTML,Bootstrap and Vanilla JS)

Live Demo can be viewed at https://authenove.herokuapp.com/

![DEMO](../master/static/images/Authenove.PNG)

# Features

- Full featured shopping cart
- Latest 12 products on home page
- User profile with orders
- Admin product management
- Admin user management
- Admin Order details page
- Mark orders as delivered option
- Checkout process (shipping, payment method, etc)

# Download & Setup Instructions

- 1 - Clone project: git clone https://github.com/MosarrofSakib/Authenove_test
- 2 - cd Authenove_test
- 3 - Create virtual environment: virtualenv myenv
- 4 - myenv\scripts\activate
- 5 - pip install -r requirements.txt
- 6 - Create a .env file inside "ecommerce" folder and variables for database(postgresql) as mentioned below:
  - DB_NAME=your_database_name
  - DB_USER=your_database_username
  - DB_PASSWORD=your_database_password
  - DB_HOST=your_database_hostname
  - DB_PORT=your_database_port_no
- 6(alternative) - If you want to use default sqlite database, then comment out the postgresql db section and uncomment the sqlite db section inside settings.py
- 7 - python manage.py runserver

# Additional setup for admin panel

- 1 - Craete a superuser with "python manage.py superuser"
- 2 - Restart the server and go to http://127.0.0.1:8000/admin, Then login with superuser credentials
- 3 - Select Groups and create 2 groups named with "admin" and "customer"

# Add new products

- 1 - Start the server with "python manage.py runserver"
- 2 - Open http://127.0.0.1:8000/admin and login with superuser credentials
- 3 - Select products from the left menu and add products
