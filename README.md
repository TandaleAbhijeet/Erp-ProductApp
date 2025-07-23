# 🛍️ Product Management API (Django + DRF)


This is a Django REST Framework-based backend API for managing product data. The API supports importing product data from an external source (FakeStore API), and provides endpoints for listing, creating, updating, deleting (single and bulk), and retrieving product information.

---

## 📌 Features

- ✅ Import products from [FakeStore API](https://fakestoreapi.com/products)
- ✅ List products with pagination and title-based search
- ✅ Retrieve single product details
- ✅ Create, update, and delete individual products
- ✅ Bulk delete products
- ✅ Virtual field for INR price (conversion from USD)
- ✅ Swagger (drf_yasg) documentation

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/TandaleAbhijeet/Erp-ProductApp.git
cd Erp-ProductApp
```

### 2. Create a Virtual Environment
```bash
python -m venv env
source env/bin/activate   # On Windows: env\Scripts\activate
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

### 4. Apply Migrations 
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Run the Server
```bash
python manage.py runserver
```

Now visit:  
🔗 `http://localhost:8000/swagger/` for Swagger API docs  
🔗 `http://localhost:8000/products/` for product list endpoint

---

## 📦 Requirements

```
Django>=4.0
djangorestframework
drf-yasg
```
Generate this with:
```bash
pip freeze > requirements.txt
```

---


## 📝 License

This project is for educational and demonstration purposes. Free to use or modify.

---

## 🙋 Need Help?

If you need help deploying or extending this project, feel free to reach out.
