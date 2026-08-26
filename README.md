# 🚀 Server-Side Web Development Practical Exam Drill & Grill Hub (06016418)

> **KMITL IT — Faculty of Information Technology, Multimedia & Game Development**  
> **Midterm Practical Examination Master Blueprint & Drill Platform (20 Points)**

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new)
[![License: MIT](https://img.shields.io/badge/License-MIT-indigo.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/Node.js-20.x-green.svg)](https://nodejs.org/)
[![Express.js](https://img.shields.io/badge/Express-4.x-black.svg)](https://expressjs.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-6.0-green.svg)](https://www.mongodb.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://www.docker.com/)

---

## 📖 ภาพรวมของระบบ (Overview)

เว็บแอปพลิเคชันสำหรับการฝึกซ้อมแบบเข้มข้น (Drill & Grill) และเปิดเป็น **Reference Hub** ระหว่างการสอบปฏิบัติวิชา **06016418 Server-Side Web Development** โดยเน้นหัวข้อหลักที่ออกสอบปฏิบัติ:
- 🐙 **Git & Workflow:** การสร้าง Repository, Branching, `.gitignore` และการ Push งาน
- 🐳 **Docker & Docker Compose:** Dockerfile Layer Caching, Named Volumes, Port Mapping (`HOST:CONTAINER`)
- 🟢 **Node.js & Express.js:** RESTful API Architecture, Middleware Lifecycle, Global Error Handler
- 🍃 **MongoDB & Mongoose:** Connection Module, Schema Validation Rules, 5-Route Async CRUD, Duplicate Key Error Handling

---

## 🛠️ 6 ฟีเจอร์หลักในระบบ (Core Modules)

1. **📚 1. Study Hub (สรุปทฤษฎี & สถาปัตยกรรม):** สรุปเปรียบเทียบ VM vs Container, Mongoose Lifecycle Hooks, Parameterized Queries และ 12-Factor App Configurations
2. **⚡ 2. Step-by-Step Blueprint (ขั้นตอนคำสั่งสด 0-9):** พิมพ์ตามได้ทันทีตั้งแต่ `mkdir` จนถึง `git push` พร้อมคำอธิบายและปุ่ม Copy โค้ด
3. **🧪 3. Hands-on Coding Labs (10 ข้อปฏิบัติ):** ระบบ Interactive Code Editor ตรวจสอบ Regex Auto-Validation สดทันที
4. **🔥 4. Grill Exam Simulator (ข้อสอบจับเวลา):** ข้อสอบจำลอง 15 ข้อ พร้อมเฉลยละเอียดและวิเคราะห์จุดหลอก
5. **⚡ 5. Quick Cheat Sheet (กู้ชีพหน้าห้องสอบ):** สรุปโค้ดจำเป็นสำหรับคัดลอกด่วน (Connection, Model, Router, Compose, cURL)
6. **✅ 6. Exam Readiness Checklist:** เช็กลิสต์ความพร้อมก่อนกดส่งข้อสอบ 100%

---

## 🧭 Master 10-Step Blueprint (ขั้นตอน 0 - 9 สำหรับสอบจริง)

```
[0. Git & Repo] ➔ [1. NPM Init] ➔ [2. .env Config] ➔ [3. Docker & Compose] 
       ➔ [4. DB Connection] ➔ [5. Mongoose Schema] ➔ [6. Express Server] 
       ➔ [7. 5-Route CRUD] ➔ [8. cURL Test] ➔ [9. Git Push]
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

### 2. Deploy ขึ้น Vercel (1 คำสั่งจบ)
```bash
npx vercel --prod
```

---

## 👨‍💻 ผู้จัดทำ (Author)
- **Thanatphat Promthong (Tawan)** — [GitHub Profile](https://github.com/tawaninm)
- **Course:** 06016418 Server-Side Web Development
- **Institute:** Faculty of Information Technology, King Mongkut's Institute of Technology Ladkrabang (KMITL)
