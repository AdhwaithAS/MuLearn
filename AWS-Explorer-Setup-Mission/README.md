# 🚀 AWS Explorer - Setup Mission

### Secure Access Using `.env` + Python Script to List AWS Regions

---

## 📌 Overview

This project demonstrates how to:

* Install and configure **AWS SDK (boto3)**
* Securely load credentials using a **`.env` file**
* Write a Python script to **list all AWS regions**
* Keep credentials safe and outside your source code

Perfect for beginners and developers looking for a clean and secure AWS setup.

---

## 🖼️ Project Preview / Architecture

### 🔹 Image: Output Example (CLI Screenshot)

<img width="668" height="817" alt="image" src="https://github.com/user-attachments/assets/119dc151-8c07-4105-baa1-8e74542253bd" />


---

## 📦 Installation

### 1️⃣ Install Required Packages

```bash
pip install boto3 python-dotenv
```

### 2️⃣ Create a `.env` File

Create a file named `.env` in your project root:

```
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_DEFAULT_REGION=us-east-1
```



## ▶️ Running the Script

```bash
python main.py
```

**Expected Output:**

```
Available AWS Regions:
- us-east-1 (ec2.us-east-1.amazonaws.com)
- ap-south-1 (ec2.ap-south-1.amazonaws.com)
...
```
