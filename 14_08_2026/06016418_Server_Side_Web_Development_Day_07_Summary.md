---
title: "Day 07 Deep-Dive Note: Comprehensive SQL Architecture, Constraints, Joins, Aggregations, Views & Prisma ORM"
course_id: "06016418"
course_name: "Server-Side Web Development"
institution: "KMITL IT"
semester: "2026-Semester"
date: 2026-08-14
tags:
  - sql
  - mysql
  - ddl
  - dml
  - joins
  - constraints
  - aggregations
  - views
  - orm
  - prisma
  - nodejs
  - express
---

# 📚 Day 07 Deep-Dive Academic Guide: SQL Architecture, Joins, Constraints & Modern ORM (Prisma)

> **Course:** 06016418 Server-Side Web Development (School of Information Technology, KMITL)  
> **Instructor:** sarayut@it.kmitl.ac.th  
> **Topic:** Comprehensive Relational Database Engineering (SQL Sublanguages, Schema Alteration, Advanced Queries & Filtering, Data Integrity Constraints, Table Joins, Aggregate Analytics, Subqueries, Virtual Views, Date Management) & Next-Gen ORM Architecture with Prisma in Node.js/Express.

---

## 🎯 Executive Summary & Learning Objectives

1. **SQL Language Taxonomy:** แยกแยะและเข้าใจบทบาทของ SQL Sublanguages ทั้ง 4 หมวดหมู่อย่างถ่องแท้ ได้แก่ DDL (โครงสร้าง), DML (ข้อมูล), DCL (ความปลอดภัย/สิทธิ์), และ TCL (Transaction & ACID).
2. **Schema Definition & Modification (DDL):** เข้าใจคำสั่ง `CREATE`, `ALTER` (Add/Drop/Rename/Modify Column, Add Constraint, Rename Table), `DROP` และเปรียบเทียบข้อแตกต่างเชิงลึกระหว่าง `DROP TABLE` vs `TRUNCATE TABLE`.
3. **Data Lifecycle & Safeguards (DML):** ปฏิบัติการ `INSERT`, `UPDATE`, `DELETE` อย่างปลอดภัย พร้อมตระหนักถึงหายนะของ Unbounded Updates/Deletes และกลยุทธ์ป้องกันข้อมูลเสียหาย (Data Corruption).
4. **Advanced Querying & Wildcard Matching:** ควบคุมการค้นหาข้อมูลด้วย `SELECT DISTINCT`, Multi-Condition `WHERE` (`AND`, `OR`, `NOT`), การจัดการ `NULL` ด้วย `IS NULL` / `IS NOT NULL`, การแบ่งหน้าด้วย `LIMIT`, และการจับคู่รูปแบบข้อความด้วย `LIKE` ร่วมกับ Wildcard Characters (`%`, `_`, `[ ]`, `^`, `-`, `{ }`).
5. **Data Aggregation & Group Analytics:** คำนวณค่าสถิติด้วย Aggregate Functions (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`), จัดกลุ่มข้อมูลด้วย `GROUP BY`, และเข้าใจข้อแตกต่างเชิงโครงสร้างระหว่างการกรองก่อนจัดกลุ่ม (`WHERE`) กับการกรองหลังคำนวณกลุ่ม (`HAVING`).
6. **Relational Joins & Subqueries:** เชื่อมโยงข้อมูลข้ามตารางด้วย `INNER JOIN`, `LEFT JOIN`, `RIGHT JOIN`, `FULL JOIN` (รวมถึงการทำ Full Outer Join บน MySQL ด้วย `UNION`), `SELF JOIN` สำหรับโครงสร้างแบบลำดับขั้น (Hierarchy), และการใช้ `EXISTS` ใน Correlated Subqueries.
7. **Data Integrity Constraints & Virtual Views:** บังคับใช้กฎความถูกต้องของข้อมูลผ่าน 6 Core Constraints (`PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `NOT NULL`, `CHECK`, `DEFAULT`), การสร้างตารางเสมือน (`VIEW`), การจัดการชนิดข้อมูลวัน-เวลา (Date & Time Types), และการใช้ `CASE` Expression.
8. **Modern ORM Architecture (Prisma ORM):** เข้าใจแนวคิด Object-Relational Mapping (ORM) เพื่อเชื่อมโยง Application Domain Objects กับ Database Schema, การติดตั้งและตั้งค่า Prisma CLI & Client, การทำ Database Migration (`prisma migrate dev`), และการเขียน CRUD Operations พร้อม Fallback ไปยัง Raw SQL (`$queryRaw`, `$executeRaw`).

---

## 1. 🏗️ Module 1: สถาปัตยกรรมภาษา SQL และการจัดหมวดหมู่คำสั่ง (SQL Sublanguages)

Structured Query Language (SQL) เป็นภาษามาตรฐานระดับสากลที่ใช้ในการจัดการและเข้าถึง Relational Database Management Systems (RDBMS) เช่น MySQL, PostgreSQL, MariaDB, SQL Server และ Oracle โครงสร้างของคำสั่ง SQL ถูกแบ่งออกเป็น 4 หมวดหมู่หลักตามหน้าที่และขอบเขตการทำงาน:

```
                          ┌─────────────────────────────────────────┐
                          │         SQL Sublanguage Taxonomy        │
                          └────────────────────┬────────────────────┘
                                               │
         ┌───────────────────┬─────────────────┴─────────────────┬───────────────────┐
         ▼                   ▼                                   ▼                   ▼
 ┌───────────────┐   ┌───────────────┐                   ┌───────────────┐   ┌───────────────┐
 │      DDL      │   │      DML      │                   │      DCL      │   │      TCL      │
 │Data Definition│   │  Data Manip.  │                   │ Data Control  │   │Trans. Control │
 ├───────────────┤   ├───────────────┤                   ├───────────────┤   ├───────────────┤
 │• CREATE       │   │• INSERT       │                   │• GRANT        │   │• COMMIT       │
 │• ALTER        │   │• UPDATE       │                   │• REVOKE       │   │• ROLLBACK     │
 │• DROP         │   │• DELETE       │                   └───────────────┘   │• SAVEPOINT    │
 │• TRUNCATE     │   │• SELECT (DQL) │                                       └───────────────┘
 └───────────────┘   └───────────────┘
```

### 1.1 Data Definition Language (DDL) - ภาษาจัดการโครงสร้าง
- **หน้าที่:** กำหนด, ปรับปรุง, และทำลายโครงสร้างของ Database Objects (Database, Table, Index, View)
- **คำสั่งหลัก:**
  - `CREATE DATABASE` / `CREATE TABLE`: สร้างฐานข้อมูลหรือตารางใหม่
  - `ALTER TABLE`: ปรับปรุงโครงสร้างตารางเดิม (เพิ่ม/ลบ/แก้คอลัมน์, เพิ่มข้อจำกัด)
  - `DROP TABLE` / `DROP DATABASE`: ลบตารางหรือฐานข้อมูลทิ้งถาวร
  - `TRUNCATE TABLE`: ล้างข้อมูลทั้งหมดในตารางทิ้งอย่างรวดเร็ว แต่ยังคงโครงสร้างไว้

### 1.2 Data Manipulation Language (DML) - ภาษาจัดการข้อมูล
- **หน้าที่:** เพิ่ม, แก้ไข, ลบ, และค้นคืนข้อมูลภายในตาราง (Data Records / Rows)
- **คำสั่งหลัก:**
  - `INSERT INTO`: เพิ่มแถวข้อมูลใหม่
  - `UPDATE`: แก้ไขข้อมูลในแถวที่มีอยู่เดิม
  - `DELETE`: ลบแถวข้อมูลออกจากตาราง
  - `SELECT`: ค้นหาและดึงข้อมูล (บางตำราจะแยกย่อยเป็น DQL: Data Query Language)

### 1.3 Data Control Language (DCL) - ภาษาควบคุมสิทธิ์และความปลอดภัย
- **หน้าที่:** ควบคุมและกำหนดสิทธิ์การเข้าถึงข้อมูลของผู้ใช้งาน (User Roles & Permissions)
- **คำสั่งหลัก:**
  - `GRANT`: มอบสิทธิ์การเข้าถึงหรือสิทธิ์การรันคำสั่งให้แก่ User
  - `REVOKE`: เพิกถอนหรือยกเลิกสิทธิ์ที่เคยให้ไว้

### 1.4 Transaction Control Language (TCL) - ภาษาควบคุม Transaction
- **หน้าที่:** ควบคุมความสมบูรณ์ของการทำงานเป็นชุดคำสั่ง (Transaction Management) ตามหลัก ACID Properties (Atomicity, Consistency, Isolation, Durability)
- **คำสั่งหลัก:**
  - `COMMIT`: บันทึกการเปลี่ยนแปลงทั้งหมดใน Transaction ลง Database อย่างถาวร
  - `ROLLBACK`: ยกเลิกและย้อนกลับสถานะของข้อมูลทั้งหมดใน Transaction เมื่อเกิดข้อผิดพลาด (Revert to state before transaction)
  - `SAVEPOINT`: กำหนดจุดย้อนกลับชั่วคราวภายใน Transaction

---

## 2. 📐 Module 2: DDL ในทางปฏิบัติ — การสร้างและปรับปรุงโครงสร้างตาราง (ALTER, DROP & TRUNCATE)

### 2.1 การสร้างฐานข้อมูลและตารางพื้นฐาน (`CREATE`)
```sql
-- สร้าง Database ใหม่
CREATE DATABASE company_db;
USE company_db;

-- สร้างตารางพื้นฐาน
CREATE TABLE employees (
    emp_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    hire_date DATE NOT NULL,
    salary DECIMAL(10, 2) DEFAULT 15000.00
);
```

### 2.2 ปฏิบัติการ `ALTER TABLE` อย่างละเอียด
คำสั่ง `ALTER TABLE` ใช้เมื่อต้องการปรับโครงสร้างตารางหลังจากที่สร้างขึ้นไปแล้ว:

```sql
-- 1. ADD Column: เพิ่มคอลัมน์ใหม่
ALTER TABLE employees 
ADD phone_number VARCHAR(20);

-- 2. DROP Column: ลบคอลัมน์ที่ไม่ใช้งานออก
ALTER TABLE employees 
DROP COLUMN phone_number;

-- 3. RENAME Column: เปลี่ยนชื่อคอลัมน์เดิม
ALTER TABLE employees 
RENAME COLUMN email TO corporate_email;

-- 4. MODIFY Datatype: เปลี่ยนประเภทข้อมูลหรือขยายขนาดคอลัมน์
-- (สำหรับ MySQL / MariaDB / Oracle)
ALTER TABLE employees 
MODIFY COLUMN salary DECIMAL(12, 2) NOT NULL;

-- 5. ADD CONSTRAINT: เพิ่มข้อจำกัดความถูกต้องให้ตาราง
ALTER TABLE employees 
ADD CONSTRAINT chk_salary_min CHECK (salary >= 10000.00);

-- 6. RENAME TABLE: เปลี่ยนชื่อตาราง
ALTER TABLE employees 
RENAME TO staff_members;
```

> [!CAUTION]
> **ข้อควรระวังร้ายแรงเกี่ยวกับ ALTER TABLE ในระบบ Production:**
> การรัน `ALTER TABLE` บนตารางที่มีข้อมูลอยู่เป็นจำนวนมาก (เช่น ตารางขนาดหลายล้านแถว) อาจทำให้เกิด Table Lock นาน ส่งผลให้ระบบหยุดชะงัก (Downtime) หรือหากแปลง Data Type ที่แคบลง (เช่น VARCHAR(100) -> VARCHAR(20)) อาจทำให้ข้อมูลส่วนเกินถูกตัดขาด (Data Truncation) หรือสูญหายได้อย่างถาวร!

### 2.3 การเปรียบเทียบเชิงลึก: `DROP TABLE` vs `TRUNCATE TABLE` vs `DELETE FROM`

| มิติการเปรียบเทียบ | `DROP TABLE` | `TRUNCATE TABLE` | `DELETE FROM` |
|---|---|---|---|
| **หมวดหมู่คำสั่ง** | DDL | DDL | DML |
| **สิ่งที่ถูกลบ** | ทั้งข้อมูล (Data) และโครงสร้างตาราง (Schema) | ลบข้อมูลทุกแถวทิ้งทั้งหมด | ลบเฉพาะแถวข้อมูลตามเงื่อนไข `WHERE` |
| **โครงสร้างตารางคงอยู่ไหม?** | ❌ ไม่คงอยู่ (ตารางหายไปจากระบบ) | ✅ คงอยู่ (พร้อมรองรับการ Insert ใหม่) | ✅ คงอยู่ |
| **ความเร็วในการทำงาน** | รวดเร็วมาก | รวดเร็วมาก (Deallocate Data Pages) | ช้ากว่า (ต้องสแกนและบันทึก Row-by-Row Log) |
| **Transaction Log** | บันทึกเฉพาะ Schema Drop | บันทึกน้อยมาก (Minimal Logging) | บันทึก Log ทุกแถวที่ถูกลบ |
| **การ Rollback** | Rollback ยากมาก (บาง RDBMS ไม่อนุญาต) | ไม่อนุญาตให้ Rollback ในบางระบบ | ✅ สามารถ `ROLLBACK` ได้สมบูรณ์ |
| **Auto Increment Counter** | ถูกทำลายทิ้ง | 🔄 รีเซ็ตค่ากลับไปเป็น 1 เสมอ | ❌ ไม่รีเซ็ต (นับเลขต่อจากค่าสูงสุดเดิม) |
| **Trigger Activation** | ไม่เรียก Trigger | ไม่เรียก `ON DELETE` Triggers | ✅ เรียก `ON DELETE` Trigger ในแต่ละแถว |

---

## 3. 📝 Module 3: DML ในทางปฏิบัติ — การจัดการข้อมูลอย่างปลอดภัย (INSERT, UPDATE & DELETE)

### 3.1 การเพิ่มข้อมูล (`INSERT INTO`)
การเพิ่มข้อมูลลงในตารางสามารถทำได้หลายรูปแบบ:

```sql
-- รูปแบบที่ 1: ระบุชื่อคอลัมน์ชัดเจน (แนะนำที่สุด - Best Practice ป้องกันข้อผิดพลาดเมื่อ Schema เปลี่ยน)
INSERT INTO staff_members (first_name, last_name, corporate_email, hire_date, salary)
VALUES ('Somchai', 'Jaidee', 'somchai@company.com', '2026-01-15', 35000.00);

-- รูปแบบที่ 2: เพิ่มเฉพาะบางคอลัมน์ (คอลัมน์ที่เหลือต้องยอมรับ NULL หรือมี DEFAULT)
INSERT INTO staff_members (first_name, last_name, corporate_email, hire_date)
VALUES ('Suda', 'Maneerat', 'suda@company.com', '2026-02-01');

-- รูปแบบที่ 3: Bulk Insert (เพิ่มหลายแถวพร้อมกันในคำสั่งเดียว เพื่อประสิทธิภาพสูงสุด)
INSERT INTO staff_members (first_name, last_name, corporate_email, hire_date, salary)
VALUES 
    ('Anan', 'Suksan', 'anan@company.com', '2026-03-01', 28000.00),
    ('Kanya', 'Rattana', 'kanya@company.com', '2026-03-15', 42000.00);
```

### 3.2 การแก้ไขข้อมูล (`UPDATE`) และข้อควรระวัง
คำสั่ง `UPDATE` ใช้แก้ไขค่าในคอลัมน์ของแถวที่ตรงกับเงื่อนไข:

```sql
-- ตัวอย่างการ UPDATE อย่างถูกต้องและปลอดภัย
UPDATE staff_members 
SET salary = salary * 1.10, corporate_email = 'somchai.j@company.com'
WHERE emp_id = 1;
```

> [!WARNING]
> **🚨 กฎเหล็กแห่งความปลอดภัยของ UPDATE & DELETE:**
> หากรันคำสั่ง `UPDATE staff_members SET salary = 50000;` หรือ `DELETE FROM staff_members;` โดย **ไม่มีเงื่อนไข `WHERE`** ระบบจะดำเนินการกับ **ทุกแถวในตารางโดยไม่มีการเตือน!**  
> **แนวทางป้องกัน:**
> 1. เขียน `SELECT ... WHERE ...` เพื่อตรวจสอบชุดแถวเป้าหมายก่อนแปลงเป็น `UPDATE` หรือ `DELETE`
> 2. เปิดใช้งาน MySQL Safe Updates Mode (`SET SQL_SAFE_UPDATES = 1;`) ซึ่งจะปฏิเสธการ Update/Delete ที่ไม่มี Key ใน Where Clause

### 3.3 การลบข้อมูล (`DELETE`)
```sql
-- ลบเฉพาะแถวที่ตรงเงื่อนไข
DELETE FROM staff_members 
WHERE emp_id = 2;
```

---

## 4. 🔍 Module 4: การค้นหา กรองข้อมูล และการจับคู่รูปแบบ (SELECT, WHERE, NULL & Wildcards)

### 4.1 การดึงข้อมูลและตัดค่าซ้ำ (`SELECT` & `SELECT DISTINCT`)
```sql
-- ดึงทุกคอลัมน์
SELECT * FROM staff_members;

-- ดึงเฉพาะคอลัมน์ที่ต้องการ (ประหยัด Network I/O และ Memory)
SELECT first_name, salary FROM staff_members;

-- ตัดข้อมูลที่ซ้ำกันออก ให้เหลือเฉพาะค่าที่ไม่ซ้ำ (Unique Values)
SELECT DISTINCT department_id FROM staff_members;
```

### 4.2 การกรองด้วย `WHERE` และ Logical Operators
```sql
SELECT * FROM staff_members
WHERE salary >= 30000.00 
  AND hire_date >= '2026-01-01' 
  AND NOT (department_id = 5);
```

### 4.3 กฎเหล็กของการจัดการค่าว่าง (`NULL` vs `IS NULL`)
ในภาษา SQL ค่า `NULL` ไม่ใช่เลข 0 และไม่ใช่ String ว่าง `""` แต่หมายถึง **"Unknown" (ไม่ทราบค่า)** หรือ **"Missing Value"**
- **ห้ามเปรียบเทียบด้วย `=` หรือ `<>`:** `WHERE salary = NULL` จะได้ผลลัพธ์เป็น `UNKNOWN` (False) เสมอ
- **ต้องใช้ `IS NULL` หรือ `IS NOT NULL` เท่านั้น:**

```sql
-- ค้นหาพนักงานที่ยังไม่มีเบอร์โทรศัพท์บันทึกไว้
SELECT * FROM staff_members 
WHERE phone_number IS NULL;

-- ค้นหาพนักงานที่มีการระบุเบอร์โทรศัพท์เรียบร้อยแล้ว
SELECT * FROM staff_members 
WHERE phone_number IS NOT NULL;
```

### 4.4 การจำกัดจำนวนผลลัพธ์และการแบ่งหน้า (`LIMIT` & `OFFSET`)
```sql
-- ดึง 5 แถวแรก
SELECT * FROM staff_members 
ORDER BY salary DESC 
LIMIT 5;

-- การทำ Pagination (หน้าที่ 2 โดยดึงหน้าละ 10 แถว -> ข้าม 10 แถวแรก)
SELECT * FROM staff_members 
ORDER BY emp_id ASC 
LIMIT 10 OFFSET 10;
```

### 4.5 Pattern Matching ด้วย `LIKE` และ Wildcard Characters

| Wildcard Symbol | ความหมายและพฤติกรรมการค้นหา | ตัวอย่างการใช้งาน | ผลลัพธ์ที่ตรงเงื่อนไข |
|---|---|---|---|
| `%` | แทนอักขระกี่ตัวก็ได้ (0 ตัวขึ้นไป) | `LIKE 'J%'` (Starts with) | 'John', 'Jane', 'J' |
| `%` | อยู่หน้าและหลัง (Contains / Substring) | `LIKE '%dev%'` | 'Web developer', 'device' |
| `%` | อยู่ข้างหน้า (Ends with) | `LIKE '%ing'` | 'King', 'running' |
| `_` | แทนอักขระ **1 ตัวพอดี** (Single Character) | `LIKE '_o%'` (ตัวที่ 2 เป็น 'o') | 'Tom', 'John', 'Code' |
| `_` | หลายตัวติดกัน | `LIKE 'T__'` (ขึ้นต้น T ตามด้วย 2 ตัว) | 'Tom', 'Top', 'Tim' |
| `[ ]` | ตัวอักษรใดตัวหนึ่งในเซ็ต (Set Match) | `LIKE '[bsp]%'` | 'bank', 'sun', 'pen' |
| `^` / `!` | ยกเว้นตัวอักษรในเซ็ต (Negative Set) | `LIKE '[^a-c]%'` | 'dog', 'zoo' (ไม่ขึ้นต้นด้วย a, b, c) |
| `-` | ระบุช่วงของอักขระ (Character Range) | `LIKE '[a-f]%'` | 'apple', 'cat', 'fox' |
| `{ }` | ODBC Escape Sequence | ใช้ Escape คำสั่งเฉพาะทาง | ไวยากรณ์เฉพาะ Engine |

```sql
-- ตัวอย่างการค้นหาแบบผสมผสาน (Combine Wildcards)
-- ค้นหาชื่อที่ขึ้นต้นด้วย 'J' ตัวที่ 2 เป็นอะไรก็ได้ และตัวที่ 3 เป็น 'n'
SELECT * FROM customers 
WHERE customer_name LIKE 'J_n%';
```

---

## 5. 📊 Module 5: การวิเคราะห์ข้อมูลขั้นสูง (Aggregate Functions, GROUP BY & HAVING)

### 5.1 ฟังก์ชันคำนวณค่าสถิติรวม (Aggregate Functions)
- `COUNT(*)`: นับจำนวนแถวทั้งหมด (รวมแถวที่มี NULL)
- `COUNT(column)`: นับเฉพาะแถวที่คอลัมน์นั้น **ไม่เป็น NULL**
- `SUM(column)`: หาผลรวมของตัวเลขในคอลัมน์
- `AVG(column)`: หาค่าเฉลี่ยของตัวเลขในคอลัมน์
- `MIN(column)` / `MAX(column)`: หาค่าน้อยที่สุด / มากที่สุด

```sql
SELECT 
    COUNT(*) AS total_employees,
    AVG(salary) AS average_salary,
    MIN(salary) AS lowest_salary,
    MAX(salary) AS highest_salary,
    SUM(salary) AS total_payroll
FROM staff_members;
```

### 5.2 การจัดกลุ่มข้อมูล (`GROUP BY`) ร่วมกับ Aggregate Functions
```sql
SELECT 
    department_id, 
    COUNT(*) AS num_staff, 
    AVG(salary) AS dept_avg_salary
FROM staff_members
GROUP BY department_id;
```

### 5.3 ข้อแตกต่างเชิงสถาปัตยกรรม: `WHERE` vs `HAVING`

```
 ┌───────────────────────────────────────────────────────────┐
 │                   Query Execution Lifecycle               │
 └─────────────────────────────┬─────────────────────────────┘
                               │
                               ▼
 ┌───────────────────────────────────────────────────────────┐
 │ 1. FROM & JOIN: รวบรวมตารางต้นทาง                         │
 └─────────────────────────────┬─────────────────────────────┘
                               │
                               ▼
 ┌───────────────────────────────────────────────────────────┐
 │ 2. WHERE Clause: กรองแถวข้อมูลระดับ Row ก่อนการจัดกลุ่ม   │
 └─────────────────────────────┬─────────────────────────────┘
                               │
                               ▼
 ┌───────────────────────────────────────────────────────────┐
 │ 3. GROUP BY: จัดกลุ่มแถวที่เหลือตามคีย์ที่ระบุ             │
 └─────────────────────────────┬─────────────────────────────┘
                               │
                               ▼
 ┌───────────────────────────────────────────────────────────┐
 │ 4. AGGREGATION: คำนวณ COUNT(), SUM(), AVG() ในแต่ละกลุ่ม  │
 └─────────────────────────────┬─────────────────────────────┘
                               │
                               ▼
 ┌───────────────────────────────────────────────────────────┐
 │ 5. HAVING Clause: กรองผลลัพธ์ของกลุ่มหลังคำนวณ Aggregate │
 └─────────────────────────────┬─────────────────────────────┘
                               │
                               ▼
 ┌───────────────────────────────────────────────────────────┐
 │ 6. SELECT, ORDER BY, LIMIT: จัดรูปแบบและส่งผลลัพธ์        │
 └───────────────────────────────────────────────────────────┘
```

```sql
-- ตัวอย่างการใช้ WHERE และ HAVING ร่วมกันอย่างถูกต้อง
SELECT 
    department_id, 
    COUNT(*) AS staff_count,
    AVG(salary) AS avg_sal
FROM staff_members
WHERE salary >= 20000.00              -- กรองรายบุคคลก่อนนำไปคำนวณกลุ่ม
GROUP BY department_id
HAVING COUNT(*) >= 5 AND AVG(salary) >= 35000.00; -- กรองเฉพาะแผนกที่มีคนตั้งแต่ 5 คนขึ้นไปและเงินเดือนเฉลี่ย >= 35000
```

### 5.4 ตัวดำเนินการ `IN`, `BETWEEN` และ `AS` (Aliases)
```sql
-- IN Operator: เทียบเท่าการเชื่อมด้วย OR หลายๆ ครั้ง
SELECT * FROM staff_members 
WHERE department_id IN (1, 3, 5, 7);

-- BETWEEN Operator: รวมค่าหัวและท้าย (Inclusive: [20000, 40000])
SELECT * FROM staff_members 
WHERE salary BETWEEN 20000.00 AND 40000.00;

-- Table & Column Aliases เพื่อความกระชับ
SELECT e.first_name AS given_name, e.salary AS monthly_income
FROM staff_members AS e;
```

---

## 6. 🔗 Module 6: การเชื่อมโยงความสัมพันธ์ของตาราง (Table Joins & Subqueries)

การทำงานใน Relational Database จำเป็นต้องแยกข้อมูลออกเป็นหลายตารางตามหลัก Normalization แล้วนำมาเชื่อมความสัมพันธ์ (Relationship) เข้าด้วยกันผ่าน Join Operations:

```
      Table A (Left)               Table B (Right)
   ┌──────────────────┐         ┌──────────────────┐
   │ ┌──────────────┐ │         │ ┌──────────────┐ │
   │ │ Only Left    │ │ ┌─────┐ │ │ Only Right   │ │
   │ │              │ │ │MATCH│ │ │              │ │
   │ └──────────────┘ │ └─────┘ │ └──────────────┘ │
   └──────────────────┘         └──────────────────┘
```

### 6.1 ประเภทของ Joins ในเชิงลึก

```
1. INNER JOIN             2. LEFT JOIN               3. RIGHT JOIN              4. FULL JOIN (UNION)
   ┌───────┬───────┐         ┌───────┬───────┐          ┌───────┬───────┐          ┌───────┬───────┐
   │       │███████│         │███████│███████│          │       │███████│          │███████│███████│
   │   A   │██B████│         │███A███│██B████│          │   A   │███B███│          │███A███│███B███│
   │       │███████│         │███████│       │          │       │███████│          │███████│███████│
   └───────┴───────┘         └───────┴───────┘          └───────┴───────┘          └───────┴───────┘
   Matching only             All Left + Match Right     Match Left + All Right     All Left + All Right
```

#### 1) `INNER JOIN`
ดึงเฉพาะแถวที่มี Foreign Key และ Primary Key ตรงกันทั้งสองตารางเท่านั้น (Intersection):
```sql
SELECT e.first_name, e.last_name, d.department_name
FROM staff_members e
INNER JOIN departments d ON e.department_id = d.department_id;
```

#### 2) `LEFT JOIN` (LEFT OUTER JOIN)
ดึงข้อมูล **ทุกแถวจากตารางซ้าย** (Table A) เสมอ แม้ว่าจะไม่มีข้อมูลที่ตรงกันในตารางขวา (Table B) โดยคอลัมน์ของตารางขวาจะแสดงผลเป็น `NULL`:
```sql
-- ดึงพนักงานทุกคน แม้จะยังไม่สังกัดแผนกใดเลยก็ตาม
SELECT e.first_name, e.last_name, d.department_name
FROM staff_members e
LEFT JOIN departments d ON e.department_id = d.department_id;
```

#### 3) `RIGHT JOIN` (RIGHT OUTER JOIN)
ดึงข้อมูล **ทุกแถวจากตารางขวา** (Table B) เสมอ แม้ว่าจะไม่มีพนักงานคนใดสังกัดแผนกนั้น:
```sql
SELECT e.first_name, e.last_name, d.department_name
FROM staff_members e
RIGHT JOIN departments d ON e.department_id = d.department_id;
```

#### 4) `FULL JOIN` (FULL OUTER JOIN)
ดึงข้อมูลทุกแถวจากทั้งสองตาราง หากฝั่งใดไม่มีคู่แมตช์จะเติมค่าด้วย `NULL`  
*(หมายเหตุ: ใน MySQL ไม่มีคีย์เวิร์ด `FULL OUTER JOIN` โดยตรง ให้จำลองด้วยการทำ `LEFT JOIN` รวมกับ `RIGHT JOIN` ผ่านตัวดำเนินการ `UNION`)*:
```sql
-- Emulating FULL OUTER JOIN in MySQL
SELECT e.first_name, d.department_name
FROM staff_members e
LEFT JOIN departments d ON e.department_id = d.department_id
UNION
SELECT e.first_name, d.department_name
FROM staff_members e
RIGHT JOIN departments d ON e.department_id = d.department_id;
```

#### 5) `SELF JOIN`
การเชื่อมโยงตารางเข้ากับตัวเอง มักใช้กับโครงสร้างข้อมูลแบบลำดับขั้น (Hierarchical Structure / Tree) เช่น การเก็บข้อมูลพนักงานและหัวหน้างาน (Manager) ไว้ในตารางเดียวกัน:
```sql
SELECT 
    e.first_name AS employee_name,
    m.first_name AS manager_name
FROM staff_members e
LEFT JOIN staff_members m ON e.manager_id = m.emp_id;
```

### 6.2 `EXISTS` Operator และ Correlated Subquery
`EXISTS` เป็น Logical Operator ที่ใช้ตรวจสอบว่า Subquery ภายในวงเล็บส่งคืนแถวข้อมูลกลับมาอย่างน้อย 1 แถวหรือไม่
- **ข้อได้เปรียบด้านประสิทธิภาพ:** เมื่อ Database Engine พบ Record แรกที่ตรงเงื่อนไข จะหยุดการสแกนทันที (Short-circuit Evaluation) ทำให้ทำงานเร็วกว่า `IN (subquery)` ในตารางขนาดใหญ่:

```sql
-- ค้นหาผู้ใช้ทั้งหมดที่มีประวัติการสั่งซื้อสินค้าอย่างน้อย 1 ออเดอร์
SELECT u.user_id, u.username
FROM users u
WHERE EXISTS (
    SELECT 1 
    FROM orders o 
    WHERE o.user_id = u.user_id
);
```

---

## 7. 🛡️ Module 7: Data Integrity, Constraints, Dates, CASE & Views

### 7.1 กฎความถูกต้องของข้อมูล (6 Core Constraints)

```
 ┌────────────────────────────────────────────────────────────────────────────┐
 │                            6 Core SQL Constraints                          │
 ├────────────────┬───────────────────────────────────────────────────────────┤
 │ 1. NOT NULL    │ บังคับว่าห้ามมีค่าว่าง (NULL) ต้องส่งค่ามาเสมอ           │
 ├────────────────┼───────────────────────────────────────────────────────────┤
 │ 2. UNIQUE      │ ค่าในคอลัมน์ห้ามซ้ำกัน (แต่สามารถมีค่า NULL ได้)          │
 ├────────────────┼───────────────────────────────────────────────────────────┤
 │ 3. PRIMARY KEY │ คีย์หลักระบุเอกลักษณ์แต่ละแถว (NOT NULL + UNIQUE รวมกัน)   │
 ├────────────────┼───────────────────────────────────────────────────────────┤
 │ 4. FOREIGN KEY │ คีย์นอกเชื่อมโยงไปยัง PK ของตารางอื่น เพื่อรักษาความสัมพันธ์│
 ├────────────────┼───────────────────────────────────────────────────────────┤
 │ 5. CHECK       │ บังคับให้ค่าต้องผ่านเงื่อนไขที่กำหนด เช่น age >= 18       │
 ├────────────────┼───────────────────────────────────────────────────────────┤
 │ 6. DEFAULT     │ กำหนดค่าเริ่มต้นอัตโนมัติหากผู้ใช้ไม่ได้ส่งข้อมูลคอลัมน์นี้มา │
 └────────────────┴───────────────────────────────────────────────────────────┘
```

#### ตัวอย่างการสร้างตารางที่ใช้ Constraints ครบทั้ง 6 รูปแบบ:
```sql
CREATE TABLE departments (
    dept_id INT AUTO_INCREMENT PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE employees_v2 (
    emp_id INT AUTO_INCREMENT PRIMARY KEY,                  -- 1. PRIMARY KEY
    email VARCHAR(100) NOT NULL UNIQUE,                     -- 2. NOT NULL + UNIQUE
    age INT CHECK (age >= 18),                              -- 3. CHECK
    salary DECIMAL(10, 2) DEFAULT 15000.00,                 -- 4. DEFAULT
    dept_id INT,
    CONSTRAINT fk_employee_dept                             -- 5. FOREIGN KEY
        FOREIGN KEY (dept_id) 
        REFERENCES departments(dept_id)
        ON DELETE SET NULL 
        ON UPDATE CASCADE
);
```

### 7.2 การเขียนเงื่อนไขด้วย `CASE` Expression
ทำหน้าที่เหมือน `if-else` หรือ `switch-case` ในภาษาโปรแกรมเพื่อแปลงค่าที่แสดงผลแบบไดนามิก:
```sql
SELECT 
    product_name, 
    price,
    CASE 
        WHEN price < 20.00 THEN 'Low Cost Tier'
        WHEN price BETWEEN 20.00 AND 50.00 THEN 'Medium Cost Tier'
        ELSE 'High Cost / Premium Tier'
    END AS price_category
FROM products;
```

### 7.3 การจัดการชนิดข้อมูล วัน-เวลา (Date & Time Types)
- `DATE`: จัดเก็บเฉพาะวันที่ รูปแบบ `YYYY-MM-DD` (เช่น `2026-08-14`)
- `DATETIME`: จัดเก็บทั้งวันที่และเวลา รูปแบบ `YYYY-MM-DD HH:MM:SS`
- `TIMESTAMP`: จัดเก็บวันที่และเวลาเป็น UTC Epoch Timestamp (เหมาะสำหรับบันทึก `created_at`, `updated_at` อัตโนมัติ)
- `TIME`: จัดเก็บเฉพาะเวลา `HH:MM:SS`
- `YEAR`: จัดเก็บเฉพาะปี `YYYY`

### 7.4 ตารางเสมือน (SQL Views)
View คือ **Virtual Table** ที่เกิดจากการบันทึกชุดคำสั่ง `SELECT` เอาไว้ โดย View จะไม่เก็บข้อมูลซ้ำซ้อนในตัวเอง (ยกเว้น Materialized View) แต่จะดึงข้อมูลสดจาก Base Table ทุกครั้งที่มีการเรียกใช้

```sql
-- สร้าง View รวมข้อมูลลูกค้าในประเทศบราซิล
CREATE VIEW brazil_customers_view AS
SELECT customer_id, customer_name, contact_name, city
FROM customers
WHERE country = 'Brazil';

-- เรียกใช้งาน View เหมือนตารางปกติ
SELECT * FROM brazil_customers_view WHERE city = 'Rio de Janeiro';

-- ลบ View
DROP VIEW brazil_customers_view;
```

**ประโยชน์ของ SQL Views:**
1. **Security & Abstraction:** ซ่อนคอลัมน์ที่เป็นความลับ (เช่น Password Hash, บัญชีธนาคาร) ไม่ให้ผู้ใช้ภายนอกเห็น
2. **Simplicity:** ห่อหุ้มความซับซ้อนของคำสั่ง Multi-Table Join หรือ Subquery ให้เหลือเพียง `SELECT * FROM view_name`
3. **Consistency:** สร้างมาตรฐานเดียวกันในการดึงรายงานทางธุรกิจ (Business Logic Standardization)

---

## 8. ⚡ Module 8: Next-Gen ORM Architecture — การทำงานกับ Prisma ORM ใน Node.js / Express

### 8.1 Object-Relational Mapping (ORM) คืออะไร?
ORM คือเครื่องมือหรือไลบรารีที่ทำหน้าที่เป็นตัวกลางในการเชื่อมโยง (Map) ระหว่าง **Object ในโค้ดโปรแกรมมิ่ง (เช่น JavaScript/TypeScript Class หรือ Object)** กับ **Table และ Record ใน Relational Database**

```
 ┌───────────────────────────────────────────────────────────┐
 │               Node.js / Express Application               │
 │    const users = await prisma.user.findMany();            │
 └─────────────────────────────┬─────────────────────────────┘
                               │ (JavaScript Object / Promise)
                               ▼
 ┌───────────────────────────────────────────────────────────┐
 │                        Prisma ORM                         │
 │     • Translates JS/TS Calls -> Optimized SQL Queries     │
 │     • Enforces TypeScript Strict Typing & Auto-completion │
 └─────────────────────────────┬─────────────────────────────┘
                               │ (Raw SQL Queries over TCP)
                               ▼
 ┌───────────────────────────────────────────────────────────┐
 │               Database (PostgreSQL / MySQL)               │
 │     SELECT id, name, email, created_at FROM "users";      │
 └───────────────────────────────────────────────────────────┘
```

#### เปรียบเทียบข้อดี - ข้อจำกัดของ ORM:
- **ข้อดี (Advantages):**
  - **Developer Productivity:** เขียนโค้ดเป็นฟังก์ชันภาษาหลัก ไม่ต้องสลับบริบทไปเขียน Raw SQL
  - **Type Safety & Auto-complete:** ตรวจสอบความถูกต้องของชื่อฟิลด์ตั้งแต่ขั้นตอนเขียนโค้ด (Compile-time Check)
  - **Automated Migrations:** บริหารจัดการประวัติการแก้ Database Schema อย่างเป็นระบบ
  - **Database Agnostic:** เปลี่ยน Database Engine ได้ง่ายโดยแก้แค่ Configuration
- **ข้อจำกัด (Trade-offs):**
  - มี Performance Overhead เล็กน้อยเมื่อเทียบกับ Hand-crafted SQL ที่จูนละเอียด
  - Query ที่ซับซ้อนมากๆ (เช่น Analytical Window Functions ลึกๆ) อาจเขียนผ่าน ORM Method ได้ยาก

### 8.2 การติดตั้งและตั้งค่า Prisma Project
```bash
# 1. สร้าง Node.js Project และลง Dependencies
npm init -y
npm i -D prisma typescript @types/node ts-node
npm i @prisma/client

# 2. เริ่มต้น Prisma Scaffolding
npx prisma init

# หรือระบุ Database Provider ชัดเจน (เช่น PostgreSQL หรือ MySQL)
npx prisma init --datasource-provider mysql
```

ไฟล์ `.env` จะถูกสร้างขึ้นพร้อม `DATABASE_URL`:
```env
DATABASE_URL="mysql://root:password123@localhost:3306/my_database"
```

### 8.3 การออกแบบ Database Schema ใน `prisma/schema.prisma`
```prisma
datasource db {
  provider = "mysql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  name      String?
  role      String   @default("USER")
  posts     Post[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@map("users")
}

model Post {
  id        Int      @id @default(autoincrement())
  title     String
  content   String?  @db.Text
  published Boolean  @default(false)
  authorId  Int
  author    User     @relation(fields: [authorId], references: [id], onDelete: Cascade)

  @@map("posts")
}
```

### 8.4 คำสั่งสำคัญของ Prisma CLI
- `npx prisma migrate dev --name init`: รัน Migration เพื่อสร้างตารางใน Database จริง พร้อม generate TypeScript types
- `npx prisma db pull`: ดึงโครงสร้างตารางที่มีอยู่เดิมใน Database มาสร้างเป็น `schema.prisma` (Introspection)
- `npx prisma studio`: เปิด Visual GUI บนเบราว์เซอร์ (`http://localhost:5555`) สำหรับดูและแก้ไขข้อมูลสดในฐานข้อมูล

### 8.5 การทำ CRUD Operations ด้วย Prisma Client ใน Express/Node.js

```javascript
const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

// 1. CREATE: สร้างข้อมูลใหม่
async function createUser(name, email) {
    const newUser = await prisma.user.create({
        data: {
            name: name,
            email: email
        }
    });
    console.log('Created User:', newUser);
    return newUser;
}

// 2. READ: ดึงข้อมูลทั้งหมด หรือค้นหาแบบมีเงื่อนไข
async function getAllUsers() {
    const users = await prisma.user.findMany({
        include: { posts: true } // Eager loading ความสัมพันธ์
    });
    return users;
}

async function getUserByEmail(email) {
    const user = await prisma.user.findUnique({
        where: { email: email }
    });
    return user;
}

// 3. UPDATE: แก้ไขข้อมูล
async function updateUserName(id, newName) {
    const updatedUser = await prisma.user.update({
        where: { id: parseInt(id) },
        data: { name: newName }
    });
    return updatedUser;
}

// 4. DELETE: ลบข้อมูล
async function deleteUser(id) {
    const deletedUser = await prisma.user.delete({
        where: { id: parseInt(id) }
    });
    return deletedUser;
}
```

### 8.6 การรัน Raw SQL Query ใน Prisma (`$queryRaw` & `$executeRaw`)
ในกรณีที่ต้องการรัน Query ซับซ้อน หรือ Performance-critical query สามารถใช้ Safe Template Strings ได้:

```javascript
// ดึงข้อมูลด้วย Raw SQL SELECT (Safe from SQL Injection)
async function getRawUsers(emailDomain) {
    const users = await prisma.$queryRaw`
        SELECT id, name, email 
        FROM users 
        WHERE email LIKE ${'%' + emailDomain}
    `;
    return users;
}

// แก้ไขข้อมูลด้วย Raw SQL UPDATE / INSERT
async function executeRawUpdate(oldRole, newRole) {
    const affectedRows = await prisma.$executeRaw`
        UPDATE users 
        SET role = ${newRole} 
        WHERE role = ${oldRole}
    `;
    console.log(`Rows affected: ${affectedRows}`);
    return affectedRows;
}
```

---

## 9. 🧠 Key Takeaways & Exam Preparation Blueprint (สรุปจุดเน้นสำหรับสอบ)

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                  🎯 MIDTERM EXAM QUICK RECAP                                    │
├─────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. DDL vs DML: DDL แก้ไขโครงสร้าง (CREATE, ALTER, DROP, TRUNCATE) vs DML จัดการแถวข้อมูล        │
│    (INSERT, UPDATE, DELETE, SELECT)                                                             │
│ 2. TRUNCATE vs DELETE: TRUNCATE เร็วกว่า, รีเซ็ต Auto-increment, ไม่เรียก Delete Trigger       │
│ 3. NULL Rule: ต้องใช้ 'IS NULL' หรือ 'IS NOT NULL' เท่านั้น (ห้ามใช้ '= NULL')                  │
│ 4. WHERE vs HAVING: WHERE กรองก่อน Group (ระดับแถว), HAVING กรองหลัง Aggregate (ระดับกลุ่ม)      │
│ 5. JOIN Mechanics:                                                                              │
│    - INNER JOIN: เฉพาะคีย์ที่ตรงกันทั้ง 2 ฝั่ง                                                  │
│    - LEFT JOIN: เอาฝั่งซ้ายทั้งหมด + ฝั่งขวาที่ตรงกัน (ไม่ตรงเป็น NULL)                         │
│    - FULL JOIN in MySQL: ใช้ LEFT JOIN UNION RIGHT JOIN                                         │
│ 6. 6 Constraints: NOT NULL, UNIQUE, PRIMARY KEY, FOREIGN KEY, CHECK, DEFAULT                    │
│ 7. EXISTS vs IN: EXISTS ประสิทธิภาพสูงกว่าในกรณี Subquery ขนาดใหญ่เพราะมี Short-circuit        │
│ 8. Prisma ORM: จัดการ Schema ผ่าน schema.prisma, เชื่อมด้วย PrismaClient, สลับ DB ได้ง่าย      │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---
*Generated & Grounded strictly according to Day 07 Curriculum (06016418 Server-Side Web Development, KMITL IT).*
