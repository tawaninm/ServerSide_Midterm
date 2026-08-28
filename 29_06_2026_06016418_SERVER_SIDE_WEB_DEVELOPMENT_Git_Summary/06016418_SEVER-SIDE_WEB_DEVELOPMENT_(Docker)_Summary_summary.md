---
course: "Server-Side Web Development"
topic: "Docker & Containerization"
date: 2026-06-29
type: "lecture_note"
status: "completed"
tags: [Docker, Containerization, Virtualization, Dockerfile, DockerCompose, ServerSide]
---

# 🐳 Server-Side Web Development: Docker & Containerization
## บทเรียนเจาะลึก 360 องศา: Docker, Containers & Microservices Infrastructure

สรุปเนื้อหาบทเรียนยกระดับเข้มข้นจากวิชา Server-Side Web Development (KMITL IT)

---

## 1. ปัญหาของพัฒนาซอฟต์แวร์ยุคเก่า vs คอนเทนเนอร์ (The "Works on My Machine" Problem)

### ❌ ปัญหาแบบดั้งเดิม (Traditional Development Pain Points):
* **Environment Discrepancy:** สภาพแวดล้อมบนเครื่อง Developer (เช่น macOS/Windows, Node v20, MySQL 8) ไม่ตรงกับเครื่อง Staging/Production (Ubuntu Server, Node v18, MySQL 5.7) ส่งผลให้เกิดข้อผิดพลาดคลาสสิก: *"It works on my machine!"*
* **Dependency Hell:** ปัญหาไลบรารีและแพ็กเกจตีกันเมื่อรันหลายแอปพลิเคชันบน Physical/Virtual Host เดียวกัน
* **Heavy Virtualization (VM Overheads):** การใช้ Virtual Machines (เช่น VMware, VirtualBox) จำเป็นต้องมี **Guest OS** เต็มรูปแบบในทุกๆ VM ส่งผลให้สิ้นเปลืองทรัพยากร CPU, RAM และพื้นที่ดิสก์อย่างมาก ใช้เวลา Boot นานหลายนาที

---

## 2. VM Architecture vs Docker Container Architecture

```
         VIRTUAL MACHINES (VMs)                       DOCKER CONTAINERS
+-------------------------------------+     +-------------------------------------+
| App A     | App B     | App C       |     | App A     | App B     | App C       |
| Bins/Libs | Bins/Libs | Bins/Libs   |     | Bins/Libs | Bins/Libs | Bins/Libs   |
+-----------+-----------+-------------+     +-----------+-----------+-------------+
| Guest OS  | Guest OS  | Guest OS    |     |    Docker Engine (Daemon)           |
+-----------+-----------+-------------+     +-------------------------------------+
| Hypervisor (Type 1 or 2)            |     | Host Operating System (Linux Kernel)|
+-------------------------------------+     +-------------------------------------+
| Infrastructure (Physical Hardware)  |     | Infrastructure (Physical Hardware)  |
+-------------------------------------+     +-------------------------------------+
```

| คุณลักษณะ (Property) | Virtual Machine (VM) | Docker Container |
| :--- | :--- | :--- |
| **ระดับการแยกส่วน (Isolation)** | Hypervisor Level (Hardware Virtualization) | OS Level (Kernel Sharing via Namespaces/cgroups) |
| **Guest OS** | **มี Guest OS เต็มรูปแบบทุก VM** (หลาย GB) | **ไม่มี Guest OS** (แชร์ Linux Kernel ของ Host) |
| **ขนาดไฟล์ (Size)** | ใหญ่มาก (หลาย GB ถึงสิบ GB) | เล็กมาก (MB เดียวถึงไม่กี่ร้อย MB) |
| **เวลาในการ Boot** | นาน (หลายสิบวินาที ถึง นาที) | เร็วมาก (ระดับ Millisecond หรือวินาที) |
| **การใช้ทรัพยากร (Resource Overhead)** | สูงมาก (กิน CPU/RAM ประจำเพื่อเลี้ยง Guest OS) | ต่ำมาก (กินทรัพยากรตามที่ App ใช้งานจริง) |

---

## 3. กลไกการทำงานภายในของ Docker (Namespaces & cgroups)

Docker ไม่ใช่เวทมนตร์ แต่เป็นการประยุกต์ใช้ฟีเจอร์ระดับลึกของ **Linux Kernel** 2 ตัวหลัก:

1. **Linux Namespaces (การแยกมุมมองของระบบ):**
   * **PID Namespace:** ทำให้ Container เห็นเฉพาะ Process ของตัวเอง (PID 1) ไม่เห็น Process ของ Host หรือ Container อื่น
   * **NET Namespace:** แยก Network Stack, IP Address และ Port ของแต่ละ Container ออกจากกัน
   * **MNT Namespace:** แยก File System Mount Point ออกจากกัน
   * **IPC Namespace:** แยก Inter-Process Communication
   * **UTS Namespace:** แยก Hostname และ Domain Name
2. **Control Groups (cgroups - การจำกัดทรัพยากร):**
   * กำหนดเพดานจำกัดการใช้ทรัพยากรทางกายภาพ (เช่น จำกัด Container A ให้ใช้ CPU ไม่เกิน 2 Cores และ RAM ไม่เกิน 512MB)

---

## 4. องค์ประกอบหลักของ Docker (Docker Ecosystem Components)

```
[ Dockerfile ] ----(docker build)----> [ Docker Image ] ----(docker run)----> [ Docker Container ]
                                              ^
                                              | (push/pull)
                                       [ Docker Hub / Registry ]
```

1. **Dockerfile:** ไฟล์สคริปต์ข้อความที่ระบุคำสั่งขั้นตอนการสร้าง Docker Image
2. **Docker Image:** ภาพจำลองดิสก์ที่มีสถานะอ่านอย่างเดียว (Read-Only Template) ที่รวบรวมโค้ด, Runtime, Libraries, และการตั้งค่าทั้งหมด
3. **Docker Container:** Instance ที่กำลังทำงานอยู่ของ Docker Image (มี Read-Write Layer ซ้อนอยู่บนสุด)
4. **Docker Daemon (`dockerd`):** เบื้องหลังกระบวนการที่คอยรับคำสั่งและบริหารจัดการ Images, Containers, Networks, Volumes
5. **Docker Registry / Docker Hub:** คลังเก็บและแบ่งปัน Docker Images สาธารณะหรือส่วนตัว

---

## 5. คำสั่งพื้นฐานและการเขียน Dockerfile แบบมืออาชีพ

### 📜 5.1 ตัวอย่าง Dockerfile ที่ได้มาตรฐานสำหรับ Node.js Web App:

```dockerfile
# 1. Base Image
FROM node:20-alpine AS builder

# 2. Set Working Directory
WORKDIR /app

# 3. Copy Dependency Definitions & Install (Optimized for Docker Caching)
COPY package*.json ./
RUN npm ci --only=production

# 4. Copy Application Source Code
COPY . .

# 5. Environment Variables & Expose Port
ENV NODE_ENV=production
EXPOSE 3000

# 6. Non-root User for Security
USER node

# 7. Start Command
CMD ["node", "server.js"]
```

### ⚡ 5.2 คำสั่ง Docker CLI ที่ต้องใช้บ่อย:

```bash
# การสร้าง Image จาก Dockerfile
docker build -t my-web-app:v1 .

# การรัน Container ในแบบ Detached Mode (-d) พร้อมตั้ง Port Forwarding (-p host:container)
docker run -d -p 8080:3000 --name my-running-app my-web-app:v1

# ตรวจสอบสถานะ Container ที่กำลังรันอยู่
docker ps

# ดู Logs ของ Container
docker logs -f my-running-app

# เข้าไปรัน Bash Shell ภายใน Container
docker exec -it my-running-app sh

# หยุดและลบ Container
docker stop my-running-app && docker rm my-running-app
```

---

## 6. Docker Compose & Multi-Container Architecture

Docker Compose ช่วยให้บริหารจัดการแอปพลิเคชันที่มีหลาย Container (Multi-Container Architecture) ได้ผ่านไฟล์ `docker-compose.yml` เพียงไฟล์เดียว:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DB_HOST=database
      - DB_PASS=secret123
    depends_on:
      - database

  database:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=appdb
      - POSTGRES_PASSWORD=secret123
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### 🚀 คำสั่ง Docker Compose:
* `docker-compose up -d`: สั่ง Build และรันทุก Service ในเบื้องหลัง
* `docker-compose down`: สั่งหยุดและลบทุก Container, Networks ที่สร้างขึ้น

---

## 🎯 สรุปสาระสำคัญสำหรับเตรียมสอบ (Exam Key Takeaways)

1. **VM vs Container:** VM มี Guest OS ในทุกตัว (หนัก/ช้า) vs Container แชร์ Host Kernel (เบา/เร็ว)
2. **Kernel Features:** Namespaces (แยกมุมมอง Process/Net/MNT) + cgroups (จำกัด CPU/RAM)
3. **Dockerfile Best Practices:** วาง `COPY package*.json` ก่อน `COPY .` เพื่อใช้ประโยชน์จาก Build Cache + สลับไปใช้ Non-root User
4. **Docker Compose:** ใช้บริหารจัดการ Multi-container Web App + DB ในสคริปต์เดียว
