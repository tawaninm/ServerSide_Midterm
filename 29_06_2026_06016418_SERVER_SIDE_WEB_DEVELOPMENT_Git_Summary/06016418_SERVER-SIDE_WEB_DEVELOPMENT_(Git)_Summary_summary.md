---
course_code: "06016418"
course_name: "Server-Side Web Development"
topic: "Git & Version Control Systems"
date: 2026-06-29
type: "study-note"
status: "completed"
tags: [ServerSide, Git, VersionControl, GitHub, Branching, DevOps, KMITL]
source_file: "06016418 SERVER-SIDE WEB DEVELOPMENT (Git).pdf"
---

# 📌 สรุปเนื้อหา Server-Side Web Development: Git & Version Control Systems

> **วิชา:** Server-Side Web Development (06016418)  
> **หัวข้อ:** Git, Distributed Version Control, Branching Strategy & Remote Collaboration  
> **สถาบัน:** คณะเทคโนโลยีสารสนเทศ พระจอมเกล้าลาดกระบัง (KMITL IT)

---

## 1. 🚀 รู้จักกับ Version Control System (VCS)

### Version Control System คืออะไร?
**Version Control System (VCS)** คือระบบจัดเก็บและติดตามการเปลี่ยนแปลงของซอฟต์แวร์/ซอร์สโค้ดตามช่วงเวลา ช่วยให้นักพัฒนาสามารถ:
*   ย้อนกลับไปดูซอร์สโค้ดในอดีต (Revert) หรือเปรียบเทียบความแตกต่าง (Diff)
*   ทำงานร่วมกันในทีมโดยไม่ทับซ้อนซอร์สโค้ดของกันและกัน
*   ติดตามประวัติว่าใครแก้ไขไฟล์ใด เมื่อไหร่ และทำไม (Traceability)

### ประเภทของ VCS:
1.  **Centralized VCS (CVCS):** มี Server กลางเครื่องเดียวเก็บประวัติทั้งหมด (เช่น Subversion / SVN) หาก Server ล่ม จะไม่สามารถ commit งานได้
2.  **Distributed VCS (DVCS):** เช่น **Git** นักพัฒนาทุกคนจะมีสำเนาของ Repository สมบูรณ์แบบอยู่ในเครื่องตนเอง (Local Repo) สามารถ commit/check-out ได้แม้ไม่มีอินเทอร์เน็ต

---

## 2. 🏗️ สถาปัตยกรรมและสถานะของ Git (Git Architecture & States)

การทำงานของ Git แบ่งออกเป็น 4 ขอบเขตหลัก:

```
┌─────────────────┐       git add       ┌─────────────────┐
│ Working Directory│────────────────────►│  Staging Area   │
└─────────────────┘                     └─────────────────┘
         ▲                                       │
         │ git checkout                          │ git commit
         │                                       ▼
┌─────────────────┐      git push       ┌─────────────────┐
│ Remote Repository│◄────────────────────│ Local Repository│
└─────────────────┘      git pull       └─────────────────┘
```

1.  **Working Directory (Workspace):** ไดเรกทอรีทำงานจริงในเครื่องที่เรากำลังแก้ไขไฟล์
2.  **Staging Area (Index):** พื้นที่พักข้อมูลสำหรับเตรียมเข้าสู่การ Commit ต่อไป (จัดกลุ่มไฟล์ที่ต้องการบันทึก)
3.  **Local Repository (.git):** ฐานข้อมูล Git ในเครื่องของเราที่จัดเก็บประวัติการ Commit ทั้งหมด
4.  **Remote Repository:** เซิร์ฟเวอร์กลางบน Cloud (เช่น GitHub, GitLab, Bitbucket) สำหรับแบ่งปันซอร์สโค้ดร่วมกับทีม

---

## 3. 🛠️ คำสั่งพื้นฐานของ Git (Git Core Commands)

### 3.1 การเริ่มต้นโปรเจกต์และการตั้งค่า
```bash
# กำหนดชื่อและอีเมลผู้ใช้งาน (Global Config)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# เริ่มต้นสร้าง Git Repository ในโฟลเดอร์ปัจจุบัน
git init
```

### 3.2 การติดตามและบันทึกความเปลี่ยนแปลง
```bash
# ตรวจสอบสถานะของไฟล์ใน Working Directory และ Staging Area
git status

# ย้ายไฟล์เข้าสู่ Staging Area (พร้อมสำหรับการ commit)
git add filename.js
git add .               # เพิ่มทุกไฟล์ที่มีการเปลี่ยนแปลง

# บันทึกความเปลี่ยนแปลงลงใน Local Repository พร้อมข้อความอธิบาย
git commit -m "feat: add user authentication API"
```

### 3.3 การตรวจสอบประวัติและการเปรียบเทียบ
```bash
# ดูประวัติการ Commit ย้อนหลัง
git log
git log --oneline --graph --all   # แสดงแบบย่อและเป็นต้นไม้

# เปรียบเทียบความแตกต่างระหว่างไฟล์ใน Working Directory กับ Staging Area
git diff
```

---

## 4. 🌿 การบริหารจัดการ Branch และการ Merge (Branching & Merging)

### 4.1 Branch คืออะไร?
Branch คือเส้นทางการพัฒนาซอร์สโค้ดแบบขนาน ช่วยให้นักพัฒนาสามารถแยกไปทำฟีเจอร์ใหม่ (Feature Branch) โดยไม่กระทบซอร์สโค้ดหลักในสายการผลิต (`main` หรือ `master`)

```bash
# ดูรายการ Branch ทั้งหมด
git branch

# สร้าง Branchใหม่
git branch feature/login

# สลับไปยัง Branch ที่ต้องการ
git checkout feature/login
git switch feature/login          # คำสั่งสมัยใหม่

# สร้างและสลับไปยัง Branch ใหม่ทันที
git checkout -b feature/login
```

### 4.2 การรวม Branch (Merging)
เมื่อพัฒนาฟีเจอร์เสร็จแล้ว ต้องการนำกลับมารวมเข้ากับ Branch หลัก (`main`):

```bash
git checkout main
git merge feature/login
```

> [!WARNING]
> **Merge Conflicts (ข้อขัดแย้งในการรวมไฟล์):** เกิดขึ้นเมื่อมีการแก้ไขไฟล์เดียวกัน ในบรรทัดเดียวกัน จาก 2 Branch นักพัฒนาต้องเปิดไฟล์เพื่อแก้ไขความขัดแย้งเลือกซอร์สโค้ดที่ถูกต้อง แล้วจึงสั่ง `git add .` และ `git commit` อีกครั้ง

---

## 5. 🌐 การทำงานกับ Remote Repository (GitHub / Remote Collaboration)

```bash
# เชื่อมต่อ Local Repo เข้ากับ Remote Repo บน GitHub
git remote add origin https://github.com/username/repository.git

# ส่งการเปลี่ยนแปลงจาก Local Repo ขึ้นไปยัง Remote Repo
git push -u origin main

# ดึงซอร์สโค้ดจาก Remote Repo มาอัปเดตและรวมกับ Local Branch ทันที
git pull origin main

# คัดลอกโปรเจกต์จาก Remote Repo มายังเครื่องใหม่
git clone https://github.com/username/repository.git
```

---

## 6. 🏆 ข้อปฏิบัติที่ดีในการใช้งาน Git (Best Practices)

1.  **Commit Often, Commit Small:** ทำการ Commit บ่อยๆ เมื่อทำงานเสร็จแต่ละส่วนย่อย เพื่อให้ง่ายต่อการติดตามและย้อนกลับ
2.  **Meaningful Commit Messages:** เขียนคำอธิบาย Commit ให้ชัดเจน (เช่น ใช้ Convention `feat:`, `fix:`, `docs:`, `refactor:`)
3.  **Use `.gitignore`:** สร้างไฟล์ `.gitignore` เพื่อป้องกันไม่ให้ยิงไฟล์ที่ไม่จำเป็นขึ้น Git เช่น `node_modules/`, `.env`, `dist/`, `.DS_Store`
