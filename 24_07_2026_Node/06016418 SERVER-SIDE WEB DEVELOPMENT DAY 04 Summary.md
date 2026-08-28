---
course_code: "06016418"
course_name: "Server-Side Web Development"
topic: "Day 04 - Node.js, Core Modules & Express.js"
date: 2026-07-24
type: study-note
tags:
  - study
  - kmitl
  - nodejs
  - express
  - javascript
  - backend
source_file: "06016418 SERVER-SIDE WEB DEVELOPMENT DAY 04.pdf"
---

# 📌 สรุปเนื้อหา Server-Side Web Development (Day 04)

> **วิชา:** Server-Side Web Development (06016418)  
> **หัวข้อ:** Node.js, Asynchronous Programming, Core Modules, npm & Express.js  
> **สถาบัน:** คณะเทคโนโลยีสารสนเทศ พระจอมเกล้าลาดกระบัง (KMITL IT)

---

## 1. 🚀 รู้จักกับ Node.js (Introduction to Node.js)

### Node.js คืออะไร?
* **Runtime Environment** ที่ช่วยให้สามารถเขียนภาษา **JavaScript ฝั่ง Backend (Server-side)** ได้ จากเดิมที่ JavaScript มักจะรันได้แค่บน Web Browser (Frontend) เท่านั้น
* ทำงานอยู่บน **V8 JavaScript Engine** (ตัวเดียวกับที่ใช้อยู่ใน Google Chrome)

### ทำไม Node.js ถึงได้รับความนิยม?
1. **Single Language (ภาษาเดียวทั้งระบบ):** นักพัฒนาใช้ JavaScript เขียนได้ทั้ง Frontend และ Backend
2. **High Performance:** สถาปัตยกรรมแบบ **Event-driven** และ **Non-blocking I/O** รองรับคำขอ (Request) จำนวนมากได้พร้อมกัน
3. **Large Ecosystem:** มี Community ขนาดใหญ่ มี Package/Library ให้เลือกใช้มากมายใน `npm`
4. **Real-time Friendly:** เหมาะกับการสร้างแอปพลิเคชันที่ต้องการการอัปเดตข้อมูลแบบทันที เช่น Chat Application หรือ Live Dashboard

---

## 2. ⚡ การเขียนโปรแกรมแบบ Asynchronous (Asynchronous Programming)

เปรียบเทียบการทำงานแบบ **Synchronous** (ทำงานทีละขั้นตอน ต้องรอให้งานก่อนหน้าเสร็จ) กับ **Asynchronous** (ประมวลผลพร้อมกันหลายงานได้โดยไม่ต้องรอ)

```
Synchronous:  Task 1 (20s) ──> Task 2 (7s) ──> Task 3 (10s) ──> Task 4 (8s)  => รวม 45s
Asynchronous: Task 1 (20s) ─┐
              Task 2 (7s)  ─┼─> ประมวลผลขนานกัน                        => รวม 20s
              Task 3 (10s) ─┤
              Task 4 (8s)  ─┘
```

### 2.1 Callback Functions
* ฟังก์ชันที่ถูกส่งเข้าไปเป็น Argument ให้กับอีกฟังก์ชันหนึ่ง เพื่อให้เรียกใช้งานเมื่อการทำงานที่ใช้เวลานาน (เช่น อ่านไฟล์, ดึงข้อมูลจาก Server) เสร็จสิ้น
* **ข้อเสีย (Callback Hell / Pyramid of Doom):** เมื่อมีการซ้อน Callback หลายชั้น Code จะอ่านยาก ดูแลรักษาและแก้ Bug ได้ยากมาก

### 2.2 Promise
* Object ที่ถูกสร้างขึ้นเพื่อเป็นตัวแทนของผลลัพธ์ที่จะเกิดขึ้นในอนาคต ช่วยแก้ปัญหา Callback Hell
* **วิธีใช้งาน:**
  * `.then()` : จัดการผลลัพธ์เมื่อ Promise ทำงานสำเร็จ (Resolve)
  * `.catch()` : จัดการ Error เมื่อ Promise ล้มเหลว (Reject)

### 2.3 Async / Await
* Syntax สมัยใหม่ที่สร้างอยู่บนพื้นฐานของ Promise ช่วยให้เขียนโค้ด Asynchronous ให้มีโครงสร้างอ่านง่ายเหมือน Synchronous
* `async` : เติมหน้าฟังก์ชัน เพื่อบอกว่าฟังก์ชันนี้ทำงานแบบ Asynchronous และคืนค่าเป็น Promise เสมอ
* `await` : ใช้ภายในฟังก์ชัน `async` เพื่อ **รอ** ให้ Promise ทำงานสำเร็จก่อน จึงไปรันบรรทัดถัดไป
* **Error Handling:** ใช้ `try...catch` block ในการดักจับข้อผิดพลาด

---

## 3. 📦 ระบบโมดูลของ Node.js (Node Module System)

| คุณสมบัติ | CommonJS (CJS) | ES Modules (ESM) |
| :--- | :--- | :--- |
| **ความเป็นมา** | ระบบดั้งเดิมของ Node.js | มาตรฐานอย่างเป็นทางการของ JS (ES2015+) |
| **Syntax ส่งออก (Export)** | `module.exports = { add };` | `export function add() {}` |
| **Syntax นำเข้า (Import)** | `const calc = require('./calculator');` | `import { add } from './calculator.js';` |
| **การทำงาน** | Synchronous (โหลดเสร็จก่อนค่อยรัน) | Asynchronous |
| **การใช้งาน** | ฝั่ง Server / Node.js ดั้งเดิม | ทั้ง Node.js รุ่นใหม่ และ Browser (ต้องระบุ `.js` ใน path) |

---

## 4. 🛠️ Node.js Core Modules ที่สำคัญ

Node.js มี Built-in Modules ที่สามารถดึงมาใช้งานได้ทันทีโดยไม่ต้องติดตั้งเพิ่ม:

### 4.1 `fs` (File System)
จัดการไฟล์และโฟลเดอร์ในเครื่อง เช่น อ่านไฟล์ (`readFile` / `readFileSync`) และ เขียนไฟล์ (`writeFile` / `writeFileSync`)

```javascript
// ตัวอย่าง CommonJS (CJS)
const fs = require('fs');
try {
  const data = fs.readFileSync('hello.txt', 'utf8');
  console.log(data);
} catch (err) {
  console.error(err);
}
```

### 4.2 `path`
จัดการกับเส้นทางไฟล์ (File Paths) และไดเรกทอรี เพื่อป้องกันปัญหาโครงสร้าง Path ที่แตกต่างกันระหว่าง OS (เช่น `/` บน Linux/macOS vs `\` บน Windows)
* ใช้ `path.join('users', 'john', 'documents', 'report.pdf')` ในการเชื่อม Path อย่างปลอดภัย

### 4.3 `os` (Operating System)
ดึงข้อมูลเกี่ยวกับระบบปฏิบัติการและทรัพยากรของเครื่อง Server
* `os.platform()` : ดูระบบปฏิบัติการ
* `os.totalmem()` / `os.freemem()` : ดูขนาดหน่วยความจำ (RAM) ทั้งหมด / ที่เหลืออยู่
* `os.uptime()` : ดูระยะเวลาที่เปิดเครื่องมาแล้ว (วินาที)

---

## 5. 📦 การจัดการ Package ด้วย npm และ `package.json`

### 5.1 คำสั่ง npm ที่สำคัญ
* `npm init` / `npm init -y` : เริ่มต้นโปรเจกต์ใหม่และสร้างไฟล์ `package.json` (ตัว `-y` คือสร้างแบบข้ามคำถามทั้งหมด)
* `npm install <package>` หรือ `npm i` : ติดตั้ง Library เข้าโปรเจกต์ (บันทึกลง `dependencies`)
* `npm install -D <package>` : ติดตั้ง Library ที่ใช้เฉพาะตอนพัฒนา (บันทึกลง `devDependencies` เช่น `nodemon`)
* `npm uninstall <package>` : ลบ Package ออกจากโปรเจกต์

### 5.2 โครงสร้างไฟล์ `package.json`
เปรียบเสมือน "บัตรประชาชน" ของโปรเจกต์ ประกอบด้วย:
* `name`, `version`, `description` : ข้อมูลพื้นฐานโปรเจกต์
* `main` : ไฟล์จุดเริ่มต้น (Entry Point) เช่น `app.js` หรือ `index.js`
* `scripts` : คำสั่งลัดในการรันโปรเจกต์ (เช่น `"start": "node app.js"`, `"dev": "nodemon app.js"`) -> รันด้วย `npm run dev`
* `dependencies` : Library ที่ต้องใช้รันบน Production
* `devDependencies` : Library ที่ใช้เฉพาะช่วง Development

---

## 6. 🌐 การสร้าง HTTP Server เบื้องต้นด้วย Node.js

### 6.1 ตัวอย่างการ Setup HTTP Server
```javascript
const http = require('http');
const port = 3000;

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end('Hello World');
});

server.listen(port, () => {
  console.log('Server running...');
});
```

### 6.2 รหัสสถานะ HTTP (HTTP Status Codes)
* **1XX (Informational):** ข้อมูลข่าวสาร / สถานะคำขอ
* **2XX (Success):** ทำงานสำเร็จ (เช่น `200 OK`, `201 Created`, `204 No Content`)
* **3XX (Redirection):** การแจ้งเปลี่ยนเส้นทาง (เช่น `301 Moved Permanently`, `302 Found`, `304 Not Modified`)
* **4XX (Client Error):** ข้อผิดพลาดจากฝั่ง Client (เช่น `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`)
* **5XX (Server Error):** ข้อผิดพลาดจากฝั่ง Server (เช่น `500 Internal Server Error`, `502 Bad Gateway`, `503 Service Unavailable`)

### 6.3 โครงสร้าง HTTP Messages
ประกอบด้วย **Start-line** (ระบุ HTTP Method/URL หรือ Status Code), **Headers** (ข้อมูลกำกับ Name-Value) และ **Body** (เนื้อหาข้อมูลที่ส่งไปมา)

---

## 7. 🔀 การทำ Routing, Response & Parsing ใน HTTP Core

1. **Routing เบื้องต้น:** ตรวจสอบ `req.url` เพื่อส่งผลลัพธ์ตาม path ต่างๆ (เช่น `/`, `/about`, `/contact`)
2. **การส่ง Response เป็น JSON:**
   ```javascript
   res.setHeader('Content-Type', 'application/json');
   res.end(JSON.stringify({ message: 'Hello World', status: 'success' }));
   ```
3. **การดึง Query Parameters:** ใช้โมดูล `url` ทำการ `url.parse(req.url, true)` เพื่ออ่าน Query String เช่น `?q=nodejs`
4. **การอ่าน Headers:** อ่านค่าจาก `req.headers['user-agent']` เพื่อดูข้อมูลของ Client Browser

---

## 8. ⚡ Express.js Framework & Express Router

### 8.1 Express.js คืออะไร?
* **Web Framework** ยอดนิยมสำหรับ Node.js ช่วยให้การเขียนเว็บหรือ REST API มีประสิทธิภาพและรวดเร็วยิ่งขึ้น
* **จุดเด่น:** มีระบบ Routing ที่ง่าย มี Middleware ยืดหยุ่น และช่วยลด Code ซ้ำซ้อน

```javascript
const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.send('Hello, Express');
});

app.listen(port, () => console.log('Server is running...'));
```

### 8.2 Express Router
* เครื่องมือสำหรับแยก Route ออกเป็นไฟล์เฉพาะกิจ (Modular Routing) ช่วยจัดระเบียบ Code ไม่ให้รวมกันอยู่ที่ไฟล์หลัก `app.js`

```javascript
// routes/user.js
const express = require('express');
const router = express.Router();

router.get('/', (req, res) => res.send('User home page'));
router.get('/:id', (req, res) => res.send(`User ID: ${req.params.id}`));

module.exports = router;

// app.js
const userRouter = require('./routes/user');
app.use('/user', userRouter);
```
