**🏥 Healthcare Backend System**

A backend system for managing patients and doctors using Django, Django REST Framework (DRF), PostgreSQL, and JWT Authentication.
This project provides secure APIs for user registration, login, and managing healthcare data.


**🚀 Features**

User registration and login with JWT authentication

Secure CRUD operations for Patients and Doctors

PostgreSQL database integration

Token-based authentication (Access & Refresh tokens)

RESTful API endpoints


**🛠️ Tech Stack**

Backend: Django, Django REST Framework

Authentication: JWT (djangorestframework-simplejwt)

Database: PostgreSQL

Testing: Thunder Client / Postman


**📌 API Endpoints**
**🔐 Auth**

POST /api/token/ → Get JWT tokens (access + refresh)

POST /api/token/refresh/ → Refresh access token

**🧑‍⚕️ Doctors**

GET /api/doctors/ → List doctors

POST /api/doctors/ → Create doctor

PUT /api/doctors/{id}/ → Update doctor

DELETE /api/doctors/{id}/ → Delete doctor

**🧑 Patients**

GET /api/patients/ → List patients

POST /api/patients/ → Create patient

PUT /api/patients/{id}/ → Update patient

DELETE /api/patients/{id}/ → Delete patient


**5️⃣ Run Migrations**
python manage.py migrate

**6️⃣ Create Superuser**
python manage.py createsuperuser

**7️⃣ Start Server**
python manage.py runserver
