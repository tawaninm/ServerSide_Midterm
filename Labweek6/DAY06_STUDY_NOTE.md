---
title: "สรุปเนื้อหาเชิงลึก Day 06: Express.js Middleware, Dotenv, MySQL Docker, Soft Delete Pattern และ MongoDB Mongoose ODM"
course_id: "06016418"
course_name: "Server-Side Web Development"
institution: "คณะเทคโนโลยีสารสนเทศ สถาบันเทคโนโลยีพระจอมเกล้าเจ้าคุณทหารลาดกระบัง (KMITL IT)"
semester: "2026-Semester"
date: 2026-08-07
tags:
  - express
  - middleware
  - dotenv
  - mysql
  - docker
  - soft-delete
  - mongodb
  - mongoose
  - nodejs
  - nosql
  - rdbms
---

# 📚 สรุปเนื้อหาเชิงลึก Day 06: Express Middleware, Database Integrations (MySQL & MongoDB) & Soft Delete Architecture

> **รายวิชา:** 06016418 Server-Side Web Development (School of Information Technology, KMITL)  
> **ผู้สอน:** sarayut@it.kmitl.ac.th  
> **หัวข้อหลัก:** สถาปัตยกรรม Express Middleware, การจัดการตัวแปรสภาพแวดล้อมด้วย `dotenv`, การติดตั้งและเชื่อมต่อ MySQL 8.0 ผ่าน Docker Container, กลไก Prepared Statements ป้องกัน SQL Injection, สถาปัตยกรรม Soft Delete Pattern, พื้นฐานฐานข้อมูล NoSQL และ Document Database (MongoDB Atlas & Local) ร่วมกับ Mongoose ODM ใน Node.js

---

## 🎯 วัตถุประสงค์การเรียนรู้และภาพรวมเชิงบริหาร (Executive Summary & Learning Objectives)

1. **Express.js Middleware Pipeline:** เข้าใจสถาปัตยกรรม Request-Response Lifecycle ของ Express อย่างถ่องแท้ การทำงานของฟังก์ชัน Middleware ตัวกลาง การสกัดข้อมูล Request Header/Body กลไกส่งต่อการประมวลผลด้วย `next()` และผลกระทบของการลืมเรียก `next()`
2. **Environment Variable & Security Hygiene:** เข้าใจหลักการ 12-Factor App ในการแยกการตั้งค่าและรหัสลับ (Secrets, Passwords, API Keys, Database URLs) ออกจาก Source Code โดยใช้ `.env` ร่วมกับแพ็กเกจ `dotenv`
3. **Containerized Database Operations (MySQL with Docker):** รัน MySQL Database Server ด้วย Docker Compose เชื่อมต่อผ่าน Node.js Driver (`mysql2`) และการใช้ **Prepared Statements** (`?` Placeholders) เพื่อป้องกันช่องโหว่ SQL Injection 100%
4. **Soft Delete Architecture vs. Hard Delete:** วิเคราะห์ความแตกต่างเชิงสถาปัตยกรรมระหว่างการลบข้อมูลจริงออกจากดิสก์ (Hard Delete) กับการคงข้อมูลไว้เพื่อการตรวจสอบและกู้คืน (Soft Delete ผ่านฟิลด์ `deleted_at`) พร้อมการแปลง Query ทุก Endpoint ให้รองรับเงื่อนไข `deleted_at IS NULL`
5. **NoSQL & Document Database (MongoDB):** เข้าใจความแตกต่างเชิงสถาปัตยกรรมระหว่าง Relational SQL vs NoSQL Document Store (Schema-less, Horizontal Scalability) ลำดับชั้นข้อมูล (Database ➔ Collection ➔ Document ➔ Field) และเครื่องมือใน Ecosystem เช่น MongoDB Atlas, Compass และ Drivers
6. **Object-Document Mapping (Mongoose ODM):** กำหนดโครงสร้าง Schema และ Data Validation ผ่าน Mongoose Model (`models/User.js`) และการพัฒนา RESTful CRUD APIs แบบ Asynchronous (Async/Await) ครบทั้ง 5 เส้นทาง

---

## 1. ⚙️ Module 1: สถาปัตยกรรม Express.js Middleware (Middleware Architecture)

### 1.1 Middleware คืออะไร?
**Middleware** คือฟังก์ชันการทำงานที่อยู่ตรงกลางระหว่าง **Request ขาเข้า (Incoming HTTP Request)** จาก Client และ **Response ขาออก (Outgoing HTTP Response)** ที่ส่งกลับไป โดยฟังก์ชัน Middleware ทุกตัวใน Express จะสามารถเข้าถึงพารามิเตอร์ 3 ตัวหลัก ได้แก่:
1. `req` (Request Object): ข้อมูลคำขอที่ส่งมาจาก Client เช่น Headers, Params, Query, Body
2. `res` (Response Object): อ็อบเจกต์ที่ใช้สำหรับส่งผลลัพธ์กลับไปยัง Client เช่น `.send()`, `.json()`, `.status()`
3. `next` (Next Middleware Function): ฟังก์ชัน Callback สำหรับส่งต่อการทำงานไปยัง Middleware หรือ Route Handler ลำดับถัดไปใน Pipeline

```
                       ┌──────────────────────────────────────────────────┐
                       │           Express.js Request Pipeline            │
                       └────────────────────────┬─────────────────────────┘
                                                │
                                    Incoming HTTP Request
                                                │
                                                ▼
                                    ┌───────────────────────┐
                                    │   Logger Middleware   │ ──▶ Log วัน-เวลา, HTTP Method, URL
                                    └───────────┬───────────┘
                                                │ next()
                                                ▼
                                    ┌───────────────────────┐
                                    │  express.json() Body  │ ──▶ แปลง JSON Payload เป็น req.body
                                    └───────────┬───────────┘
                                                │ next()
                                                ▼
                                    ┌───────────────────────┐
                                    │     Route Handler     │ ──▶ ทำ Business Logic / Query Database
                                    └───────────┬───────────┘
                                                │ res.status(200).json(...)
                                                ▼
                                    Outgoing HTTP Response
```

---

### 1.2 กฎเหล็กของ `next()`
- เมื่อ Middleware ตัวปัจจุบันทำงานเสร็จสิ้น และ**ยังไม่ได้ส่ง Response กลับหา Client** (เช่น ยังไม่ได้เรียก `res.json()`) ฟังก์ชันนั้น **"จำเป็นต้องเรียก `next()` เสมอ"** เพื่อส่งต่อการทำงานไปยัง Middleware ลำดับถัดไป
- ⚠️ **ข้อควรระวัง (Critical Hazard):** หากลืมเรียก `next()` และไม่มีการส่ง Response คำขอของ Client จะค้างอยู่ตรง Middleware นั้นทันที (Hanging Request) จนกระทั่งเกิด Request Timeout ในที่สุด

---

### 1.3 ประเภทของ Middleware ใน Express
1. **Application-level Middleware:** ผูกติดกับอ็อบเจกต์ `app` ผ่าน `app.use()` หรือ `app.METHOD()` ให้ทำงานกับทุก Request หรือเฉพาะ Path ที่กำหนด
2. **Router-level Middleware:** ผูกติดกับ `express.Router()` ทำงานเฉพาะกลุ่มของ Route ย่อย
3. **Built-in Middleware:** ตัวช่วยที่ Express มีมาให้ในตัว เช่น `express.json()` (แปลง JSON Request Body), `express.urlencoded()` (แปลง Form URL-Encoded), `express.static()` (เสิร์ฟไฟล์ Static Assets)
4. **Third-party Middleware:** ไลบรารีภายนอกที่ติดตั้งผ่าน npm เช่น `cors`, `morgan`, `helmet`
5. **Error-handling Middleware:** Middleware พิเศษสำหรับดักจับข้อผิดพลาดทั่วทั้งระบบ โดยต้องรับพารามิเตอร์ครบ 4 ตัวเสมอ: `(err, req, res, next)`

---

### 1.4 โค้ดตัวอย่าง Custom Request Logger Middleware
```javascript
const express = require('express');
const app = express();

// 1. Built-in Middleware แปลง JSON Body
app.use(express.json());

// 2. Custom Application-Level Middleware สำหรับบันทึก Log
const requestLogger = (req, res, next) => {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] ${req.method} ${req.originalUrl || req.url}`);
    next(); // ส่งต่อการทำงานไปยังฟังก์ชันถัดไปใน Pipeline
};

// ลงทะเบียนใช้งาน Global Middleware
app.use(requestLogger);
```

---

## 2. 🔐 Module 2: การจัดการตัวแปรสภาพแวดล้อมอย่างปลอดภัยด้วย `dotenv`

### 2.1 หลักการ 12-Factor App (The Twelve-Factor App Methodology)
ในการพัฒนาซอฟต์แวร์ระดับมืออาชีพและระบบ Production ห้ามใส่รหัสผ่านฐานข้อมูล, Private Keys, หรือ API Tokens ลงใน Source Code โดยตรง (Hardcoded Secrets) เพราะเสี่ยงต่อการรั่วไหลเมื่อ Push ขึ้น Git Repository  
หลักการ **The Twelve-Factor App (ข้อที่ 3: Config)** แนะนำให้เก็บการตั้งค่าทั้งหมดไว้ใน **Environment Variables** เพื่อให้แอปพลิเคชันสามารถ Deploy ไปยังสภาพแวดล้อม Development, Staging, และ Production ได้อย่างปลอดภัยโดยไม่ต้องแก้โค้ด

---

### 2.2 โครงสร้างไฟล์ `.env` และ `.env.example`
สร้างไฟล์ `.env` ไว้ที่ Root ของโปรเจกต์ (และเพิ่มชื่อไฟล์ `.env` ลงใน `.gitignore` เสมอ):

#### `.env` (ไฟล์จริง - มีข้อมูล Credentials ห้าม Commit ขึ้น Git)
```env
# Application Server Port
PORT=3000

# MySQL Database Configuration
DB_HOST=localhost
DB_PORT=3307
DB_USER=myuser
DB_PASSWORD=mypassword
DB_NAME=mydatabase

# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/mydatabase
# หรือสำหรับ MongoDB Atlas:
# MONGODB_URI=mongodb+srv://admin:<PASSWORD>@cluster0.abcde.mongodb.net/mydatabase?retryWrites=true&w=majority
```

#### `.env.example` (ไฟล์แม่แบบ - Commit ขึ้น Git ได้ เพื่อให้เพื่อนในทีมทราบโครงสร้าง Key)
```env
PORT=3000
DB_HOST=localhost
DB_PORT=3307
DB_USER=
DB_PASSWORD=
DB_NAME=
MONGODB_URI=
```

---

### 2.3 การโหลดใช้งานใน Node.js
ติดตั้งแพ็กเกจ: `npm install dotenv`  
โหลดการตั้งค่าไว้ที่จุดเริ่มต้นบนสุดของไฟล์หลัก (`server.js` หรือ `index.js`):
```javascript
require('dotenv').config();

const PORT = process.env.PORT || 3000;
const dbHost = process.env.DB_HOST;
const dbUser = process.env.DB_USER;
```

---

## 3. 🐬 Module 3: การเชื่อมต่อฐานข้อมูลเชิงสัมพันธ์ MySQL ผ่าน Docker Container

### 3.1 ฐานข้อมูลและระบบจัดการฐานข้อมูล (Database & DBMS Fundamentals)
- **Database (ฐานข้อมูล):** แหล่งที่ใช้สำหรับจัดเก็บรวบรวมข้อมูลที่มีความสัมพันธ์กันให้อยู่ในที่เดียวกันอย่างเป็นระเบียบ
- **Database Management System (DBMS):** ซอฟต์แวร์ที่ทำหน้าที่เป็นตัวกลางระหว่างผู้ใช้ แอปพลิเคชัน และฐานข้อมูล เพื่อใช้ในการสร้าง ค้นหา ปรับปรุง และจัดการข้อมูล
- **ประวัติของ MySQL & ตระกูลฐานข้อมูล:**
  - **MySQL:** เป็น Open-source RDBMS ยอดนิยม ก่อตั้งโดย Michael "Monty" Widenius โดยชื่อ "My" มาจากชื่อลูกสาวคนแรกของเขา
  - **MariaDB:** เป็น Community Fork ของ MySQL ที่พัฒนาขึ้นเมื่อ MySQL ถูกซื้อกิจการ เพื่อให้คงความเป็น Open-source 100% โดยชื่อ "Maria" มาจากชื่อลูกสาวคนที่สองของ Monty
  - **MaxDB:** RDBMS ที่รองรับมาตรฐาน ANSI SQL-92 พัฒนาโดย SAP AG ร่วมกับ MySQL AB โดย "Max" มาจากชื่อลูกชายของ Monty

---

### 3.2 การรัน MySQL 8.0 ด้วย Docker Compose
การใช้งาน Docker ช่วยให้ทุกคนในทีมมี Database Server เวอร์ชั่นเดียวกัน ทำงานเหมือนกันทุกประการ โดยไม่ต้องติดตั้ง MySQL ลงในเครื่อง Local โดยตรง

#### `docker-compose.yaml`
```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    container_name: lab6_mysql
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: mydatabase
      MYSQL_USER: myuser
      MYSQL_PASSWORD: mypassword
    ports:
      # แมปพอร์ต Host (3307) -> Container (3306) เพื่อหลีกเลี่ยงพอร์ตชนกับ MySQL ในเครื่อง
      - "3307:3306"
    volumes:
      # บันทึกข้อมูลลง Volume เพื่อไม่ให้ข้อมูลหายเมื่อ Restart Container
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

**คำสั่งจัดการ Container:**
```bash
# เริ่มต้นรัน MySQL Container ใน Background
docker-compose up -d

# ตรวจสอบสถานะการทำงาน
docker ps

# หยุดการทำงาน
docker-compose down
```

---

### 3.3 การออกแบบตาราง SQL Schema (`schema.sql`)
```sql
CREATE DATABASE IF NOT EXISTS mydatabase;
USE mydatabase;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    fullname VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    deleted_at DATETIME DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

---

### 3.4 Prepared Statements และการป้องกันช่องโหว่ SQL Injection
- ❌ **อันตราย (String Concatenation - SQL Injection Vulnerability):**
  ```javascript
  // ห้ามทำเด็ดขาด! หาก User ส่ง email = "test@gmail.com' OR '1'='1" ข้อมูลทั้งหมดจะรั่วไหล
  const query = "SELECT * FROM users WHERE email = '" + req.params.email + "'";
  db.query(query, callback);
  ```
- ✅ **ปลอดภัยสูงสุด (Prepared Statements with Parameterized Query):**
  ```javascript
  // ใช้สัญลักษณ์ ? แทนค่าของตัวแปร โดย Database Driver จะ Escape ข้อมูลให้โดยอัตโนมัติ
  const query = "SELECT * FROM users WHERE email = ? AND deleted_at IS NULL";
  db.query(query, [req.params.email], callback);
  ```

---

## 4. 🗑️ Module 4: สถาปัตยกรรม Soft Delete Pattern vs Hard Delete

### 4.1 ตารางเปรียบเทียบเชิงลึก: Hard Delete vs. Soft Delete

| มิติการเปรียบเทียบ | Hard Delete (`DELETE FROM`) | Soft Delete (`UPDATE ... SET deleted_at`) |
| :--- | :--- | :--- |
| **สภาพข้อมูลบน Physical Disk** | ข้อมูลถูกลบออกจาก Hard Disk / Storage ถาวร | ข้อมูลยังคงอยู่ในตารางเดิม เพียงแค่ถูกอัปเดตฟิลด์สถานะ |
| **ความสามารถในการกู้คืน (Recovery)** | ไม่สามารถกู้คืนได้ ยกเว้นต้อง Restore จาก Backup ก้อนใหญ่ | กู้คืนได้ทันที เพียงอัปเดต `SET deleted_at = NULL` |
| **มาตรฐานการตรวจสอบ (Audit & Compliance)** | ผิดมาตรฐานทางการเงิน/กฎหมาย (Audit Trail ขาดหาย) | สมบูรณ์แบบ รองรับการตรวจสอบย้อนหลังทางกฎหมาย |
| **ผลกระทบต่อ Foreign Key** | อาจเกิด Error หรือลบตารางลูกเป็นทอดๆ (Cascade Delete) | ไม่กระทบ Relational Constraints ของตารางอื่น |
| **ความซับซ้อนในการ Query** | ใช้คำสั่ง SQL มาตรฐานตามปกติ | ต้องเพิ่มเงื่อนไข `WHERE deleted_at IS NULL` ในทุกคำสั่งค้นหา |

---

### 4.2 กฎการแปลง SQL Query เพื่อรองรับ Soft Delete ทั้งระบบ

```
   ┌────────────────────────────────────────────────────────────────────────────┐
   │                  Soft Delete Query Transformation Rules                    │
   └────────────────────────────────────────────────────────────────────────────┘

   1. ดึงข้อมูลทั้งหมด (Active Users Only):
      SELECT * FROM users WHERE deleted_at IS NULL;

   2. ดึงข้อมูลรายบุคคล (Single Active User):
      SELECT * FROM users WHERE email = ? AND deleted_at IS NULL;

   3. แก้ไขข้อมูล (Update Active User):
      UPDATE users SET password = ? WHERE email = ? AND deleted_at IS NULL;

   4. สั่งลบข้อมูลแบบ Soft Delete:
      UPDATE users SET deleted_at = NOW() WHERE email = ? AND deleted_at IS NULL;

   5. กู้คืนข้อมูลที่ถูกลบไปแล้ว (Restore):
      UPDATE users SET deleted_at = NULL WHERE email = ? AND deleted_at IS NOT NULL;
```

---

## 5. 🍃 Module 5: โลกของ NoSQL และ Document Database (MongoDB)

### 5.1 แนวคิด NoSQL (Not Only SQL)
NoSQL เกิดขึ้นเพื่อตอบสนองการประมวลผลข้อมูลยุคใหม่ที่มีปริมาณมหาศาล (Big Data), ข้อมูลไม่มีโครงสร้างแน่นอน (Unstructured/Semi-Structured Data), และต้องการความเร็วสูงในการขยายระบบในแนวนอน (Horizontal Scalability / Sharding)
- **คุณสมบัติ Schema-less:** แต่ละ Document ใน Collection เดียวกันไม่จำเป็นต้องมีฟิลด์เหมือนกันทุกประการ สามารถเพิ่มฟิลด์ใหม่ได้ทันทีโดยไม่ต้องรันคำสั่ง `ALTER TABLE`

---

### 5.2 ตารางเปรียบเทียบคำศัพท์: SQL (Relational) vs MongoDB (Document)

| แนวคิดใน SQL (Relational DB) | แนวคิดใน MongoDB (Document DB) | คำอธิบายเชิงโครงสร้าง |
| :--- | :--- | :--- |
| **Database** | **Database** | แหล่งรวมชุดข้อมูลระดับสูงสุด |
| **Table** | **Collection** | กลุ่มของข้อมูลประเภทเดียวกัน (เช่น `users`, `orders`) |
| **Row / Record** | **Document** | ข้อมูล 1 แถว/รายการ เก็บในรูปแบบ JSON/BSON |
| **Column** | **Field** | แอตทริบิวต์หรือคู่ Key-Value ภายใน Document |
| **Primary Key (`id`)** | **`_id` (ObjectId)** | คีย์หลักที่ MongoDB สร้างให้แบบ 12-byte Hex String อัตโนมัติ |
| **JOIN** | **Embedding / `$lookup`** | การฝังเอกสารย่อย (Embedded Documents) หรือเชื่อมโยงข้ามคอลเลกชัน |

---

### 5.3 ระบบนิเวศของ MongoDB (MongoDB Ecosystem)
1. **MongoDB Community Server:** ตัว Database Engine แบบ Open-source สำหรับดาวน์โหลดมาติดตั้งบนเครื่อง Local หรือ On-Premise Server
2. **MongoDB Atlas:** บริการ Cloud Database แบบ Managed Service (Database-as-a-Service / DBaaS) รันบน AWS, GCP หรือ Azure โดยไม่ต้องจัดการ Server เอง
3. **MongoDB Compass:** โปรแกรม GUI สวยงามสำหรับเปิดดู ค้นหา วิเคราะห์ Schema และจัดการข้อมูลใน MongoDB ได้โดยไม่ต้องพิมพ์คำสั่งใน Terminal
4. **MongoDB Drivers:** ไลบรารีเชื่อมต่อฐานข้อมูลสำหรับแต่ละภาษาโปรแกรม (เช่น Mongoose / `mongodb` สำหรับ Node.js, `PyMongo` สำหรับ Python)

---

### 5.4 ลำดับชั้นโครงสร้างข้อมูลใน MongoDB (Data Hierarchy)
```
  Cluster (Server Group บน MongoDB Atlas หรือ Local Engine)
     │
     └── Database (เช่น mydatabase)
            │
            └── Collection (เช่น users)
                   │
                   ├── Document 1: { _id: ObjectId("..."), email: "tawan@kmitl.ac.th", fullname: "Tawan" }
                   ├── Document 2: { _id: ObjectId("..."), email: "doro@kmitl.ac.th", fullname: "Doro" }
                   └── Document 3: { ... }
```

---

### 5.5 ขั้นตอนการสร้างและเชื่อมต่อ MongoDB Atlas (Cloud Database)
1. สมัครสมาชิกและเข้าสู่คอนโซลที่ [https://cloud.mongodb.com](https://cloud.mongodb.com)
2. สร้าง **Organization** และ **Project** สำหรับรายวิชา
3. เลือกสร้าง **Database Cluster** โดยเลือกแพ็กเกจ **M0 Free Tier** (แชร์คลัสเตอร์ฟรี 512MB)
4. ตั้งค่า **Database Access (User & Password):** สร้าง Username และกำหนดรหัสผ่าน (เก็บรหัสผ่านไว้ใช้ใน Connection String)
5. ตั้งค่า **Network Access (IP Whitelist):** เพิ่ม IP Address `0.0.0.0/0` (Allow Access from Anywhere) สำหรับการพัฒนาในห้องแล็บ
6. รับ **Connection String (SRV URI):**
   ```
   mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/mydatabase?retryWrites=true&w=majority
   ```
7. นำ Connection String ไปใส่ในตัวแปร `MONGODB_URI` ในไฟล์ `.env`

---

## 6. 📦 Module 6: สถาปัตยกรรม Mongoose ODM และการสร้าง Data Models

### 6.1 Mongoose คืออะไร?
**Mongoose** เป็นไลบรารีประเภท **Object-Document Mapper (ODM)** สำหรับ Node.js ทำหน้าที่สร้างโครงสร้าง Schema และกฎระเบียบ (Validation, Default values, Middleware Hooks) ให้กับข้อมูลใน MongoDB เพื่อช่วยให้โค้ดฝั่งแอปพลิเคชันมีความเป็นระเบียบและปลอดภัย

---

### 6.2 การสร้าง User Model (`models/User.js`)
```javascript
const mongoose = require('mongoose');

// กำหนด Schema สำหรับ Collection 'users'
const userSchema = new mongoose.Schema(
    {
        email: {
            type: String,
            required: [true, 'Email is required'],
            unique: true,
            trim: true,
            lowercase: true
        },
        fullname: {
            type: String,
            required: [true, 'Fullname is required'],
            trim: true
        },
        password: {
            type: String,
            required: [true, 'Password is required']
        },
        deleted_at: {
            type: Date,
            default: null // ค่าเริ่มต้นเป็น null สำหรับรองรับ Soft Delete
        }
    },
    {
        timestamps: true // สร้างฟิลด์ createdAt และ updatedAt ให้อัตโนมัติ
    }
);

// สร้างและ Export Model เพื่อนำไปใช้ Query
module.exports = mongoose.model('User', userSchema);
```

---

### 6.3 เมธอด Asynchronous CRUD พื้นฐานของ Mongoose

| ปฏิบัติการ (CRUD) | เมธอด Mongoose | ตัวอย่างคำสั่งที่รองรับ Soft Delete |
| :--- | :--- | :--- |
| **Create (สร้าง)** | `Model.create()` | `await User.create({ email, fullname, password })` |
| **Read All (ดึงทั้งหมด)** | `Model.find()` | `await User.find({ deleted_at: null })` |
| **Read Single (ดึงรายเดียว)** | `Model.findOne()` | `await User.findOne({ email, deleted_at: null })` |
| **Update (แก้ไข)** | `Model.findOneAndUpdate()` | `await User.findOneAndUpdate({ email, deleted_at: null }, { password: newPassword }, { new: true })` |
| **Soft Delete (สั่งลบ)** | `Model.findOneAndUpdate()` | `await User.findOneAndUpdate({ email, deleted_at: null }, { deleted_at: new Date() }, { new: true })` |

> 💡 **ข้อควรจำสำคัญ:** ในเมธอด `findOneAndUpdate()` อ็อปชัน `{ new: true }` มีหน้าที่สั่งให้ Mongoose ส่งคืนข้อมูล Document **เวอร์ชันที่อัปเดตใหม่แล้ว** กลับมา หากไม่ระบุ Mongoose จะส่งข้อมูลเวอร์ชันเดิมก่อนอัปเดตกลับมาแทน

---

## 7. 🛠️ โค้ดตัวอย่างระบบสมบูรณ์ระดับ Production (Complete Source Code)

### 7.1 `server_mysql.js` (Express + MySQL2 + Prepared Statements + Soft Delete)
```javascript
const express = require('express');
const mysql = require('mysql2');
require('dotenv').config();

const app = express();
app.use(express.json());

// 1. Custom Logger Middleware
const loggerMiddleware = (req, res, next) => {
    console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
    next();
};
app.use(loggerMiddleware);

// 2. MySQL Database Connection Pool / Connection
const db = mysql.createConnection({
    host: process.env.DB_HOST || 'localhost',
    user: process.env.DB_USER || 'myuser',
    password: process.env.DB_PASSWORD || 'mypassword',
    database: process.env.DB_NAME || 'mydatabase',
    port: process.env.DB_PORT || 3307
});

db.connect((err) => {
    if (err) {
        console.error('❌ ไม่สามารถเชื่อมต่อ MySQL ได้:', err);
    } else {
        console.log('✅ เชื่อมต่อ MySQL Database สำเร็จเรียบร้อย!');
    }
});

// 3. CREATE Route - เพิ่มผู้ใช้ใหม่
app.post('/create', (req, res) => {
    const { email, name, password } = req.body;
    if (!email || !name || !password) {
        return res.status(400).json({ error: 'กรุณากรอก email, name และ password ให้ครบถ้วน' });
    }

    const sql = "INSERT INTO users(email, fullname, password) VALUES(?, ?, ?)";
    db.query(sql, [email, name, password], (err, results) => {
        if (err) {
            console.error('SQL Error:', err);
            return res.status(400).json({ error: err.message });
        }
        res.status(201).json({
            message: "สร้างผู้ใช้ใหม่สำเร็จเรียบร้อย!",
            userId: results.insertId
        });
    });
});

// 4. READ ALL Route - ดึงผู้ใช้ที่ยังไม่ถูกลบทั้งหมด
app.get('/read', (req, res) => {
    const sql = "SELECT id, email, fullname, created_at, updated_at FROM users WHERE deleted_at IS NULL";
    db.query(sql, (err, results) => {
        if (err) {
            console.error('SQL Error:', err);
            return res.status(500).json({ error: 'เกิดข้อผิดพลาดในการดึงข้อมูล' });
        }
        res.status(200).json(results);
    });
});

// 5. READ SINGLE Route - ดึงข้อมูลผู้ใช้ตาม Email
app.get('/read/single/:email', (req, res) => {
    const email = req.params.email;
    const sql = "SELECT id, email, fullname, created_at, updated_at FROM users WHERE email = ? AND deleted_at IS NULL";
    
    db.query(sql, [email], (err, results) => {
        if (err) {
            console.error('SQL Error:', err);
            return res.status(500).json({ error: 'เกิดข้อผิดพลาดในการดึงข้อมูล' });
        }
        if (results.length === 0) {
            return res.status(404).json({ message: "ไม่พบผู้ใช้นี้ หรือผู้ใช้ถูกลบออกจากระบบแล้ว" });
        }
        res.status(200).json(results[0]);
    });
});

// 6. UPDATE Route - แก้ไขรหัสผ่านของผู้ใช้
app.patch('/update/:email', (req, res) => {
    const email = req.params.email;
    const { newPassword } = req.body;

    if (!newPassword) {
        return res.status(400).json({ error: 'กรุณาระบุ newPassword ที่ต้องการเปลี่ยน' });
    }

    const sql = "UPDATE users SET password = ? WHERE email = ? AND deleted_at IS NULL";
    db.query(sql, [newPassword, email], (err, results) => {
        if (err) {
            console.error('SQL Error:', err);
            return res.status(500).json({ error: 'เกิดข้อผิดพลาดในการอัปเดตข้อมูล' });
        }
        if (results.affectedRows === 0) {
            return res.status(404).json({ message: "ไม่พบผู้ใช้นี้ หรือผู้ใช้ถูกลบออกจากระบบแล้ว" });
        }
        res.status(200).json({ message: "อัปเดตรหัสผ่านสำเร็จเรียบร้อย!" });
    });
});

// 7. SOFT DELETE Route - ลบผู้ใช้แบบ Soft Delete
app.delete('/delete/:email', (req, res) => {
    const email = req.params.email;
    const sql = "UPDATE users SET deleted_at = NOW() WHERE email = ? AND deleted_at IS NULL";

    db.query(sql, [email], (err, results) => {
        if (err) {
            console.error('SQL Error:', err);
            return res.status(500).json({ error: 'เกิดข้อผิดพลาดในการลบข้อมูล' });
        }
        if (results.affectedRows === 0) {
            return res.status(404).json({ message: "ไม่พบผู้ใช้นี้ หรือผู้ใช้ถูกลบไปก่อนหน้าแล้ว" });
        }
        res.status(200).json({ message: "ทำการ Soft Delete ผู้ใช้สำเร็จเรียบร้อย!" });
    });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`🚀 MySQL Server ทำงานที่ http://localhost:${PORT}`));
```

---

### 7.2 `server_mongodb.js` (Express + Mongoose + MongoDB Atlas/Local + Soft Delete)
```javascript
const express = require('express');
const mongoose = require('mongoose');
require('dotenv').config();

const User = require('./models/User');

const app = express();
app.use(express.json());

// 1. Custom Logger Middleware
const loggerMiddleware = (req, res, next) => {
    console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
    next();
};
app.use(loggerMiddleware);

// 2. การเชื่อมต่อ MongoDB ผ่าน Mongoose
const mongoURI = process.env.MONGODB_URI || 'mongodb://localhost:27017/mydatabase';
mongoose.connect(mongoURI)
    .then(() => console.log('✅ เชื่อมต่อ MongoDB สำเร็จเรียบร้อย!'))
    .catch((err) => console.error('❌ ข้อผิดพลาดในการเชื่อมต่อ MongoDB:', err));

// 3. CREATE Route - เพิ่มผู้ใช้ใหม่ลง MongoDB
app.post('/create', async (req, res) => {
    const { email, name, password } = req.body;
    try {
        const newUser = await User.create({
            email,
            fullname: name,
            password
        });
        return res.status(201).json({
            message: 'สร้างผู้ใช้ใน MongoDB สำเร็จเรียบร้อย!',
            user: newUser
        });
    } catch (err) {
        console.error('Mongoose Create Error:', err);
        return res.status(400).json({ error: err.message });
    }
});

// 4. READ ALL Route - ค้นหาผู้ใช้ที่ยังไม่ถูกลบทั้งหมด
app.get('/read', async (req, res) => {
    try {
        const users = await User.find({ deleted_at: null }).select('-password');
        return res.status(200).json(users);
    } catch (err) {
        console.error('Mongoose Read Error:', err);
        return res.status(500).json({ error: 'เกิดข้อผิดพลาดภายในเซิร์ฟเวอร์' });
    }
});

// 5. READ SINGLE Route - ค้นหาผู้ใช้รายเดียวตาม Email
app.get('/read/single/:email', async (req, res) => {
    const { email } = req.params;
    try {
        const user = await User.findOne({ email, deleted_at: null }).select('-password');
        if (!user) {
            return res.status(404).json({ message: 'ไม่พบผู้ใช้นี้ หรือผู้ใช้ถูกลบออกจากระบบแล้ว' });
        }
        return res.status(200).json(user);
    } catch (err) {
        console.error('Mongoose Read Single Error:', err);
        return res.status(500).json({ error: 'เกิดข้อผิดพลาดภายในเซิร์ฟเวอร์' });
    }
});

// 6. UPDATE Route - แก้ไขรหัสผ่านของผู้ใช้
app.patch('/update/:email', async (req, res) => {
    const { email } = req.params;
    const { newPassword } = req.body;

    if (!newPassword) {
        return res.status(400).json({ error: 'กรุณาระบุ newPassword ที่ต้องการเปลี่ยน' });
    }

    try {
        const updatedUser = await User.findOneAndUpdate(
            { email, deleted_at: null },
            { password: newPassword },
            { new: true } // สั่งให้ส่งคืน Document ใหม่หลังอัปเดต
        ).select('-password');

        if (!updatedUser) {
            return res.status(404).json({ message: 'ไม่พบผู้ใช้นี้ หรือผู้ใช้ถูกลบออกจากระบบแล้ว' });
        }

        return res.status(200).json({
            message: 'อัปเดตรหัสผ่านสำเร็จเรียบร้อย!',
            user: updatedUser
        });
    } catch (err) {
        console.error('Mongoose Update Error:', err);
        return res.status(500).json({ error: 'เกิดข้อผิดพลาดภายในเซิร์ฟเวอร์' });
    }
});

// 7. SOFT DELETE Route - ทำการ Soft Delete ผู้ใช้
app.delete('/delete/:email', async (req, res) => {
    const { email } = req.params;
    try {
        const deletedUser = await User.findOneAndUpdate(
            { email, deleted_at: null },
            { deleted_at: new Date() },
            { new: true }
        );

        if (!deletedUser) {
            return res.status(404).json({ message: 'ไม่พบผู้ใช้นี้ หรือผู้ใช้ถูกลบไปก่อนหน้าแล้ว' });
        }

        return res.status(200).json({
            message: 'ทำการ Soft Delete ผู้ใช้ใน MongoDB สำเร็จเรียบร้อย!'
        });
    } catch (err) {
        console.error('Mongoose Delete Error:', err);
        return res.status(500).json({ error: 'เกิดข้อผิดพลาดภายในเซิร์ฟเวอร์' });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`🚀 MongoDB Server ทำงานที่ http://localhost:${PORT}`));
```

---

## 8. 🧪 คู่มือการทดสอบ API ผ่าน Postman & cURL (API Testing & Verification)

### 1. ทดสอบสร้างผู้ใช้ใหม่ (POST `/create`)
```bash
curl -X POST http://localhost:3000/create   -H "Content-Type: application/json"   -d '{
    "email": "tawan@kmitl.ac.th",
    "name": "Thanatphat Promthong",
    "password": "SecurePassword123!"
  }'
```
*HTTP Response Expected: `201 Created`*

---

### 2. ทดสอบดึงข้อมูลผู้ใช้ทั้งหมดที่ยังไม่ถูกลบ (GET `/read`)
```bash
curl -X GET http://localhost:3000/read
```
*HTTP Response Expected: `200 OK` (Array ของ User Object)*

---

### 3. ทดสอบดึงข้อมูลผู้ใช้รายบุคคล (GET `/read/single/:email`)
```bash
curl -X GET http://localhost:3000/read/single/tawan@kmitl.ac.th
```
*HTTP Response Expected: `200 OK` (Single User Object)*

---

### 4. ทดสอบแก้ไขรหัสผ่าน (PATCH `/update/:email`)
```bash
curl -X PATCH http://localhost:3000/update/tawan@kmitl.ac.th   -H "Content-Type: application/json"   -d '{
    "newPassword": "SuperNewSecretPassword2026"
  }'
```
*HTTP Response Expected: `200 OK`*

---

### 5. ทดสอบลบผู้ใช้แบบ Soft Delete (DELETE `/delete/:email`)
```bash
curl -X DELETE http://localhost:3000/delete/tawan@kmitl.ac.th
```
*HTTP Response Expected: `200 OK`*

---

### 6. ตรวจสอบยืนยันผลหลังการ Soft Delete (GET `/read/single/:email`)
```bash
curl -X GET http://localhost:3000/read/single/tawan@kmitl.ac.th
```
*HTTP Response Expected:* **`404 Not Found`** `{"message": "ไม่พบผู้ใช้นี้ หรือผู้ใช้ถูกลบออกจากระบบแล้ว"}`

---

## 💡 จุดเน้นสำหรับข้อสอบ Midterm & Exam Takeaways (สรุปจุดดัก & ประเด็นสำคัญ)

1. **ลำดับการทำงานของ Middleware:** Express จะรัน Middleware ตามลำดับบรรทัดที่ลงทะเบียนไว้ (`app.use()`) ก่อน-หลังอย่างเคร่งครัด หาก Middleware ตัวก่อนหน้าไม่เรียก `next()` และไม่ส่ง Response คำขอจะค้าง (Hangs) ทันที
2. **ความสำคัญของ `express.json()`:** หากไม่ใส่ `app.use(express.json())` ตัวแปร `req.body` จะมีค่าเป็น `undefined` ทันทีเมื่อ Client ส่ง JSON Payload มา
3. **การป้องกัน SQL Injection:** การใช้ Prepared Statements ด้วย Placeholder เครื่องหมาย `?` ใน MySQL2 จะช่วยแยกโค้ดคำสั่ง SQL ออกจากข้อมูลที่ผู้ใช้ป้อนเข้ามา ป้องกันการแทรกคำสั่งแปลกปลอมได้ 100%
4. **หลักการ Soft Delete:** ไม่ใช้คำสั่ง `DELETE FROM users` แต่ใช้คำสั่ง `UPDATE users SET deleted_at = NOW()` และในคำสั่ง `SELECT`, `UPDATE`, `DELETE` ต่อจากนั้นทั้งหมด ต้องไม่ลืมต่อท้ายเงื่อนไข `WHERE deleted_at IS NULL`
5. **อ็อปชัน `{ new: true }` ใน Mongoose:** เมธอด `findOneAndUpdate()` ของ Mongoose โดยค่าเริ่มต้นจะส่งคืนเอกสารเวอร์ชันเก่าก่อนอัปเดต หากต้องการได้เอกสารตัวใหม่ที่อัปเดตแล้วทันที ต้องส่งอ็อปชัน `{ new: true }` ไปด้วยเสมอ
6. **SQL vs MongoDB Identity:** ใน SQL คีย์หลักถูกกำหนดด้วย `PRIMARY KEY` (มักเป็นตัวเลข Auto Increment เช่น `id = 1`) ส่วนใน MongoDB คีย์หลักคือฟิลด์ `_id` ซึ่งเก็บเป็นชนิดข้อมูล `ObjectId` 12-byte Hex String อัตโนมัติ
