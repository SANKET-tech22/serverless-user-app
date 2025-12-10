# 🌐 Serverless User Management Application  
A fully serverless CRUD-style mini application built using **AWS Lambda**, **API Gateway**, **DynamoDB**, and **S3 Static Website Hosting**.  
The application allows users to be added from the frontend and stores their data inside DynamoDB using a serverless backend.

---

## 🚀 Project Overview
This project demonstrates how to build and deploy a **dynamic serverless web application** using AWS managed services.  
The backend is powered by Lambda functions, the API is exposed using API Gateway,  
the data is stored in DynamoDB, and the frontend is hosted on S3.

---

## 🛠 Technologies Used
- **AWS Lambda** – Backend compute without servers  
- **Amazon API Gateway** – REST API endpoints  
- **Amazon DynamoDB** – NoSQL database to store user details  
- **Amazon S3** – Hosting the frontend (HTML, CSS, JS)  
- **IAM** – Permissions & roles  
- **Python** – Lambda backend logic  
- **JavaScript** – Frontend API calls  

---

## 📦 Architecture Overview

Frontend (HTML/CSS/JS) → S3 Static Website Hosting
↓
API Gateway (REST API)
↓
Lambda Functions (save_user, get_users)
↓
DynamoDB Users Table



---

## 🧩 AWS Setup Steps (My Process)

### 🔐 1. IAM Role Setup
- Created an IAM role for Lambda functions.  
- Attached DynamoDB full access permissions so Lambda could perform read/write operations.

### 🧠 2. Lambda Functions
Created two Lambda functions:

#### `save_user`
- Saves a new user in DynamoDB  
- Validates input  
- Returns proper CORS headers  

#### `get_users`
- Fetches all user records  
- Returns data with CORS headers  

Both functions were deployed.

### 🌐 3. API Gateway (REST API)
- Created a REST API named **users**  
- Added a `/users` resource  
- Added **POST**, **GET**, and **OPTIONS** methods  
- Integrated POST → `save_user` Lambda  
- Integrated GET → `get_users` Lambda  
- Enabled **CORS** for all three methods  
- Deployed API to the **dev** stage  

### 🔁 4. CORS Configuration
- Selected GET, POST, OPTIONS  
- Added S3 website origin to `Access-Control-Allow-Origin`  
- Redeployed changes  

### 🗄 5. DynamoDB
- Created a DynamoDB **Users** table  
- Verified user entries after API calls  

### 🪣 6. S3 Frontend Hosting
- Created an S3 bucket  
- Uploaded frontend files (HTML, CSS, JS)  
- Added a public bucket policy  
- Enabled **Static Website Hosting**  
- Used the S3 website endpoint to access the live app  

---

## ✔ Final Testing
- Accessed the S3 website URL  
- Added sample user entries  
- Confirmed data being saved and fetched from DynamoDB  

---

## ⭐ Advantages of Serverless Architecture
- No server management required  
- Automatic scaling  
- Pay only for usage  
- Highly available  
- Faster development  
- Ideal for CRUD apps, dashboards, registration forms, prototypes  

---

## 🌍 Real-World Use Cases
- User registration systems  
- Contact/feedback forms  
- Admin dashboards  
- Mobile/IoT backend APIs  
- Event registration systems  

---

## 📁 GitHub Repository
This repository contains both frontend and backend code.  
Feel free to explore or contribute!

---

## 📸 Screenshots
_Add screenshots inside an `/images` folder and reference them here:_

