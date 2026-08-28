# 🚀 Server-Side Web Development Practical Exam Drill & Grill Hub (06016418)

> **KMITL IT — Faculty of Information Technology, Multimedia & Game Development**  
> **Midterm Practical Examination Master Blueprint & Drill Platform (20 Points)**  
> 🌐 **Live Web Simulator:** [https://serverside-midterm.vercel.app](https://serverside-midterm.vercel.app)

[![Live Web](https://img.shields.io/badge/Live_App-serverside--midterm.vercel.app-blueviolet.svg?style=flat-square&logo=vercel)](https://serverside-midterm.vercel.app)
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new)
[![License: MIT](https://img.shields.io/badge/License-MIT-indigo.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/Node.js-20.x-green.svg)](https://nodejs.org/)
[![Express.js](https://img.shields.io/badge/Express-4.x-black.svg)](https://expressjs.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-6.0-green.svg)](https://www.mongodb.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://www.docker.com/)

---

## 📖 ภาพรวมของ Repository (Repository Overview)

คลังความรู้ สรุปเนื้อหา เลกเชอร์ สไลด์ โค้ดแล็บปฏิบัติการ และเว็บแอปพลิเคชันสำหรับฝึกซ้อมสอบปฏิบัติวิชา **06016418 Server-Side Web Development** (สอบกลางภาค 20 คะแนน)

---

## 📂 โครงสร้างไฟล์และเนื้อหาใน Repository (Directory Structure)

```
📦 ServerSide_Midterm
├── 🌐 index.html                 # Web Exam Simulator & Reference Hub (8 Tabs Interactive UI)
├── 📦 package.json               # Node Package Config
├── ⚡ vercel.json                # Vercel Deployment Configuration
├── 📝 README.md                  # เอกสารแนะนำและสารบัญเนื้อหา
│
├── 📂 03_07_2026_1_Introduction_to_Server_side_Web_Development_Summary/
│   ├── 📄 1. Introduction to Server-side Web Development.pdf
│   └── 📝 1._Introduction_to_Server-side_Web_Development_Summary_summary.md
│
├── 📂 29_06_2026_06016418_SERVER_SIDE_WEB_DEVELOPMENT_Git_Summary/
│   ├── 📄 06016418 SERVER-SIDE WEB DEVELOPMENT (Git).pdf
│   ├── 📄 06016418 SEVER-SIDE WEB DEVELOPMENT (Docker).pdf
│   ├── 📝 06016418_SERVER-SIDE_WEB_DEVELOPMENT_(Git)_Summary_summary.md
│   └── 📝 06016418_SEVER-SIDE_WEB_DEVELOPMENT_(Docker)_Summary_summary.md
│
├── 📂 24_07_2026_Node/
│   ├── 📄 06016418 SERVER-SIDE WEB DEVELOPMENT DAY 04.pdf
│   └── 📝 06016418 SERVER-SIDE WEB DEVELOPMENT DAY 04 Summary.md
│
├── 📂 07_08_2026_06_Server_Side_Web_Development_Day_06_Notes/
│   ├── 📄 6. 06016418 Server-Side Web Development Day 06.pdf
│   ├── 📄 MySQL.pdf
│   └── 📝 06_Server_Side_Web_Development_Day_06_Notes_summary.md
│
├── 📂 14_08_2026/
│   └── 📄 7. 06016418 Server-Side Web Development Day 07.pdf
│
├── 📂 Labweek6/                  # ตัวอย่างโค้ด Express + MySQL + MongoDB Backend
│   ├── 🐳 docker-compose.yaml    # Container Setup (MySQL / MongoDB)
│   ├── 📄 server_mysql.js        # Express + mysql2 (Prepared Statements, CRUD)
│   ├── 📄 server_mongodb.js      # Express + Mongoose (Schema, CRUD, Validation)
│   ├── 📄 schema.sql             # MySQL Table Schema
│   ├── 📄 models/User.js         # Mongoose User Model
│   ├── 📝 DAY06_STUDY_NOTE.md    # สรุปขั้นตอนทำแล็บ Week 6 ละเอียด
│   └── 📄 .env.example           # Environment Variables Template
│
├── 🔗 LinkSlide.txt              # ลิงก์รวมสไลด์และเอกสารประกอบการสอน
└── 📝 Ref Study Server-Side.md    # บันทึก Reference และลิงก์ศึกษาเพิ่มเติม
```

---

## 🛠️ 8 ฟีเจอร์หลักในระบบ Web Exam Hub (`index.html`)

1. **📚 1. Study Hub (สรุปทฤษฎี & สถาปัตยกรรม):** สรุปเปรียบเทียบ VM vs Container, Mongoose Lifecycle Hooks, Parameterized Queries และ 12-Factor App Configurations
2. **⚡ 2. Step-by-Step Blueprint (ขั้นตอนคำสั่งสด 0-9):** พิมพ์ตามได้ทันทีตั้งแต่ `mkdir` จนถึง `git push` พร้อมคำอธิบายและปุ่ม Copy โค้ด
3. **💻 3. VS Code Live Simulator:** จำลอง IDE พร้อม Live Terminal และ Syntax Auto-Validation
4. **🧪 4. Hands-on Coding Labs (10 ข้อปฏิบัติ):** ระบบ Interactive Code Editor ตรวจสอบ Regex Auto-Validation สดทันที
5. **🔥 5. Grill Exam Simulator (ข้อสอบจับเวลา 65 ข้อ):** คลังข้อสอบจำลองพร้อมเฉลยละเอียดและวิเคราะห์จุดหลอก
6. **⚡ 6. Quick Cheat Sheet (กู้ชีพหน้าห้องสอบ):** สรุปโค้ดจำเป็นสำหรับคัดลอกด่วน (Connection, Model, Router, Compose, cURL)
7. **✅ 7. Exam Readiness Checklist:** เช็กลิสต์ความพร้อมก่อนกดส่งข้อสอบ 100%
8. **📦 8. Resource Archive:** รวมลิงก์สไลด์ เอกสาร และ Repo อ้างอิง

---

## 🧭 Master 10-Step Blueprint (ขั้นตอน 0 - 9 สำหรับสอบจริง)

```
[0. Git & Repo] ➔ [1. NPM Init] ➔ [2. .env Config] ➔ [3. Docker & Compose] 
       ➔ [4. DB Connection] ➔ [5. Mongoose Schema] ➔ [6. Express Server] 
       ➔ [7. 5-Route CRUD] ➔ [8. Postman & cURL Test] ➔ [9. Git Push]
```

### สรุปคำสั่งด่วน (Quick Run Commands)

```bash
# Step 0: Git Setup
mkdir server-exam-2026 && cd server-exam-2026
git init
git branch -M main

# Step 1: Install Dependencies
npm init -y
npm install express mongoose dotenv cors
npm install -D nodemon

# Step 3: Start Database with Docker
docker compose up -d

# Step 8: Start Express Server
npm run dev
```

---

## 🌐 การเปิดใช้งานและการ Deploy (Usage & Deployment)

### 1. เปิดใช้งานแบบ Local
เปิดไฟล์ `index.html` ในเบราว์เซอร์โดยตรง หรือรันผ่าน Live Server / npx:
```bash
npx serve .
```

### 2. Deploy ขึ้น Vercel
```bash
npx vercel --prod
```

---

## 👨‍💻 ผู้จัดทำ (Author)
- **Thanatphat Promthong (Tawan)** — [GitHub Profile](https://github.com/tawaninm)
- **Course:** 06016418 Server-Side Web Development
- **Institute:** Faculty of Information Technology, King Mongkut's Institute of Technology Ladkrabang (KMITL)
