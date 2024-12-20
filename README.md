# Multi-Tenant Django Application

## **Overview**

This document provides a comprehensive overview of the architecture, design decisions, and setup instructions for the multi-tenant Django application. It focuses on scalability, performance, and maintainability to ensure smooth operation and adaptability to future requirements.

---

## **Architecture**

### **1. Application Structure**

The project is designed with modularity and scalability in mind. Below is the directory structure:

```
project_root/
├── auth_jwt/
│   ├── models.py
│   ├── admin.py
│   ├── apps.py
│   ├── views.py
│   ├── middleware.py
├── notifications/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── management/
│   │   ├── commands/
│   │   │   ├── rebuild_indices.py
│   ├── tests.py
│   ├── admin.py
│   ├── apps.py
│   ├── routing.py
│   ├── signals.py
│   ├── consumers.py
│   ├── elasticsearch_utils.py
├── tenants/
│   ├── models.py
│   ├── admin.py
│   ├── tests.py
│   ├── apps.py
├── search/
│   ├── models.py
│   ├── serializers.py
│   ├── admin.py
│   ├── apps.py
│   ├── views.py
│   ├── urls.py
├── project/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
└── manage.py
```

### **2. Key Components**

#### **a. Tenancy Management**

- **`tenants`**\*\* app:\*\* Handles the creation and management of tenants (organizations) and their schemas.
- **`django-tenants`**\*\* library:\*\* Utilized to implement schema-based multi-tenancy.
- Each tenant has its own schema in the database, ensuring data isolation and easy scalability.

#### **b. Authentication (JWT)**

- **`auth_jwt`**\*\* app:\*\* Custom implementation of `TokenObtainPairView` from `django-rest-framework-simplejwt` to add tenant-specific claims.
- Tokens include tenant-specific information to ensure proper tenant identification.

#### **c. Notifications**

- **`notifications`**\*\* app:\*\* Manages user-specific notifications with support for marking notifications as read.
- Uses `schema_context` from `django-tenants` to ensure tenant-aware operations.

#### **d. Search**

- **`search`**\*\* app:\*\* Facilitates data indexing and search operations using ElasticSearch.
- Provides efficient querying capabilities across tenant-specific data.

#### **e. Scalability Enhancements**

- **Database:** PostgreSQL is used for its robust support of multi-tenancy and schema management.
- **Caching:** Redis can be integrated for caching frequent queries and notifications.
- **Asynchronous Processing:** Celery with RabbitMQ is recommended for background tasks like sending notifications or processing large datasets.

---

## **Design Decisions**

### **1. Multi-Tenancy**

- **Reasoning:** Schema-based multi-tenancy ensures complete isolation of tenant data while sharing the same database instance.
- **Benefits:**
  - Easier maintenance and backups.
  - Better security and data isolation.
  - Scales well as the number of tenants increases.

### **2. Token-Based Authentication**

- **Reasoning:** JWT (JSON Web Token) provides a stateless, scalable, and secure way to authenticate API requests.
- **Enhancement:** Tenant-specific claims in tokens allow the backend to identify and handle requests efficiently.

### **3. REST API Design**

- **Framework:** Django REST Framework (DRF).
- **Reasoning:** DRF simplifies API creation with features like serializers, viewsets, and authentication integration.

### **4. Logging**

- **Logging:** Configured to log errors, warnings, and important events using Python’s `logging` module.



---

### Setup Instructions

#### 1. Prerequisites
Ensure the following dependencies are installed on your system:
- **Python**: Version 3.9 or higher
- **PostgreSQL**: Version 12 or higher
- **Redis**
- **Elasticsearch**

#### 2. Installation

##### Clone the Repository
```bash
git clone <repository-url>
cd project_root
```

##### Set Up a Virtual Environment
```bash
python -m venv env
source env/bin/activate   # On Windows: env\Scripts\activate
pip install -r requirements.txt
```

##### Configure the `.env` File
Create a `.env` file in the project root directory and add the following:
```plaintext
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

##### Apply Migrations
Generate and apply the necessary database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

##### Create a Tenant
Create a tenant with the required schema, name, and domain:
```bash
python manage.py create_tenant --schema_name=tenant1 --name="Tenant 1" --domain=tenant1.localhost
```

##### Run the Server
Start the Django development server:
```bash
python manage.py runserver
```

You can now access the application at:  
[http://tenant1.localhost:8000/](http://tenant1.localhost:8000/)

---

#### 3. Frontend Setup

##### Navigate to the Frontend Directory
```bash
cd frontend
```

##### Install Dependencies
```bash
npm install
```

##### Start the Frontend Server
```bash
npm start
```

Access the frontend application at:  
[http://localhost:3000/](http://localhost:3000/)


---

## **Testing**

### **1. Running Tests**

Run all tests:

```bash
python manage.py test
```

## **Scalability and Performance Considerations**

### **1. Database Optimization**

- Use PostgreSQL connection pooling to optimize database connections.
- Index frequently queried fields like `created_at` in the `notifications` model.

### **2. Caching**

- Use Redis to cache frequently accessed data like user notifications.
- Implement Django’s built-in caching framework with `django-redis`.

## **Adherence to Requirements**

### **1. Multi-Tenant Architecture**

- **Implementation:**
  - Multi-tenancy is achieved using `django-tenants`, where each tenant has its own isolated database schema.
  - Routing capabilities ensure that tenant-specific requests are directed to the correct schema.
- **Benefits:**
  - Enhanced security and data isolation.
  - Simplified scalability as tenants increase.

### **2. Django Admin Panel**

- **Customizations:**
  - Admin panel is enhanced to support multi-tenancy.
  - Superusers can manage tenants and their users through a centralized interface.

### **3. Public & Private Schema**

- **Design:**
  - Public schema stores shared data accessible to all tenants (e.g., tenant metadata).
  - Private schema stores tenant-specific data to maintain isolation and security.

### **4. ElasticSearch Implementation**

- **Integration:**
  - ElasticSearch is used to index and search data across tenants.
  - Data isolation is maintained by scoping search queries to specific tenant schemas.

### **5. WebSockets for Notifications**

- **Implementation:**
  - WebSockets are implemented using Django Channels for real-time notifications.
  - A simple React app connects to the WebSocket server to display notifications to users.

---

## **Conclusion**

This application is designed with scalability, performance, and maintainability at its core. By following the setup instructions and best practices outlined above, the system can handle multiple tenants, provide robust authentication, and deliver a seamless user experience.

