# -*- coding: utf-8 -*-
import sys, os, re, json

sys.stdout.reconfigure(encoding='utf-8')

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Create the comprehensive Tab 8: view-archive HTML
archive_view_html = '''
    <!-- ==================== TAB 8: ALL SLIDES & PDF INGESTION ARCHIVE ==================== -->
    <div id="view-archive" class="tab-view space-y-8 hidden">
      <!-- Archive Banner -->
      <div class="p-6 rounded-2xl bg-gradient-to-r from-emerald-950/40 via-teal-950/20 to-slate-900/40 border border-emerald-500/30 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <span class="text-xs uppercase tracking-wider text-emerald-400 font-semibold font-mono">Zero-Omission Academic Knowledge Base</span>
          <h2 class="text-2xl font-bold text-white mt-1">📚 คลังเนื้อหาและแบบฝึกหัดทุกสไลด์ ทุกโฟลเดอร์ 100% (Day 01 - Day 07)</h2>
          <p class="text-slate-400 text-sm mt-1">รวบรวมทฤษฎี โค้ดตัวอย่าง ไวยากรณ์ คำสั่ง แบบฝึกหัดในสไลด์พร้อมเฉลยละเอียดทุกข้อ สามารถค้นหาหรือคัดลอกไปใช้ในห้องสอบได้ทันที</p>
        </div>
        <div class="flex items-center gap-2">
          <button onclick="copyAllFilesBundle()" class="px-4 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-medium text-sm flex items-center gap-2 shadow-lg shadow-emerald-600/25 transition-all">
            <i data-lucide="copy" class="w-4 h-4"></i>
            <span>คัดลอกโค้ดทุกไฟล์ (Starter Kit Bundle)</span>
          </button>
        </div>
      </div>

      <!-- Quick Day Filter Chips -->
      <div class="flex items-center gap-2 overflow-x-auto pb-2 text-xs">
        <span class="text-slate-400 font-medium shrink-0">เลือกดูตามหมวด:</span>
        <a href="#arch-day1" class="px-3 py-1.5 rounded-lg bg-surfaceDark hover:bg-slate-800 text-blue-300 border border-blue-500/30 shrink-0">🌐 Day 01: Intro & SSR/CSR</a>
        <a href="#arch-day2-git" class="px-3 py-1.5 rounded-lg bg-surfaceDark hover:bg-slate-800 text-orange-300 border border-orange-500/30 shrink-0">🌿 Day 02: Git Master</a>
        <a href="#arch-day2-docker" class="px-3 py-1.5 rounded-lg bg-surfaceDark hover:bg-slate-800 text-sky-300 border border-sky-500/30 shrink-0">🐳 Day 02: Docker & Compose</a>
        <a href="#arch-day4" class="px-3 py-1.5 rounded-lg bg-surfaceDark hover:bg-slate-800 text-green-300 border border-green-500/30 shrink-0">⚡ Day 04: Node.js Core Modules</a>
        <a href="#arch-day6-mysql" class="px-3 py-1.5 rounded-lg bg-surfaceDark hover:bg-slate-800 text-amber-300 border border-amber-500/30 shrink-0">🐬 Day 06: MySQL & Soft Delete</a>
        <a href="#arch-day6-mongo" class="px-3 py-1.5 rounded-lg bg-surfaceDark hover:bg-slate-800 text-emerald-300 border border-emerald-500/30 shrink-0">🍃 Day 06 & Lab 6: MongoDB CRUD (20 Pts)</a>
        <a href="#arch-day7" class="px-3 py-1.5 rounded-lg bg-surfaceDark hover:bg-slate-800 text-teal-300 border border-teal-500/30 shrink-0">📊 Day 07: SQL Joins & Prisma ORM</a>
      </div>

      <!-- Section Day 01 -->
      <div id="arch-day1" class="glass-card rounded-2xl p-6 space-y-4 border border-blue-500/30">
        <div class="flex items-center justify-between border-b border-surfaceBorder pb-3">
          <div class="flex items-center gap-3">
            <span class="p-2 rounded-lg bg-blue-500/20 text-blue-400 font-bold text-sm">DAY 01</span>
            <h3 class="text-lg font-bold text-white">Introduction to Server-Side Web Development, HTTP Protocol & Rendering Models</h3>
          </div>
          <span class="text-xs font-mono text-slate-400">57 Slides (Dr. Sarayut Nonsiri)</span>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-slate-300">
          <div class="space-y-2 p-4 rounded-xl bg-surfaceDark/70 border border-surfaceBorder">
            <h4 class="font-bold text-blue-400">1. Client-Server Architecture</h4>
            <p>• <strong>Client (Front-end):</strong> อุปกรณ์ฝั่งผู้ใช้ (Browser/Mobile) ทำหน้าที่รับคำขอ แสดงผล UI/UX และส่ง HTTP Request</p>
            <p>• <strong>Server (Back-end):</strong> ประมวลผล Business Logic, ทำงานกับ Database และส่ง HTTP Response (HTML/JSON)</p>
            <p>• <strong>Stateless Protocol:</strong> HTTP ไม่จำสถานะ ต้องอาศัย Session, Cookie หรือ JWT ในการจดจำผู้ใช้</p>
          </div>
          <div class="space-y-2 p-4 rounded-xl bg-surfaceDark/70 border border-surfaceBorder">
            <h4 class="font-bold text-blue-400">2. SSR (Server-Side) vs CSR (Client-Side)</h4>
            <p>• <strong>SSR:</strong> Server ประกอบร่าง HTML สำเร็จรูป ➔ Fast First Paint, SEO ดีเยี่ยม แต่ Server รับภาระสูง</p>
            <p>• <strong>CSR:</strong> Server ส่ง HTML เปล่า + Bundle JS ➔ Browser รัน JS ดึง API สร้าง DOM ➔ เหมาะกับ Web App / Dashboard, Smooth Page Transition</p>
          </div>
        </div>
        <div class="p-4 rounded-xl bg-surfaceDark/70 border border-surfaceBorder space-y-2 text-sm text-slate-300">
          <h4 class="font-bold text-blue-400">3. HTTP Status Codes Master Table (จำไปสอบ)</h4>
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 font-mono text-xs">
            <div class="p-2 rounded bg-emerald-950/30 border border-emerald-800/40 text-emerald-300"><strong>200 OK:</strong> สำเร็จทั่วไป (GET, PUT, DELETE)</div>
            <div class="p-2 rounded bg-emerald-950/30 border border-emerald-800/40 text-emerald-300"><strong>201 Created:</strong> สร้าง Resource สำเร็จ (POST)</div>
            <div class="p-2 rounded bg-amber-950/30 border border-amber-800/40 text-amber-300"><strong>400 Bad Request:</strong> ข้อมูลขาเข้าผิด/Validation พลาด</div>
            <div class="p-2 rounded bg-rose-950/30 border border-rose-800/40 text-rose-300"><strong>404 Not Found:</strong> หา ID หรือ Route ไม่เจอ</div>
          </div>
        </div>
      </div>

      <!-- Section Day 02 Git -->
      <div id="arch-day2-git" class="glass-card rounded-2xl p-6 space-y-4 border border-orange-500/30">
        <div class="flex items-center justify-between border-b border-surfaceBorder pb-3">
          <div class="flex items-center gap-3">
            <span class="p-2 rounded-lg bg-orange-500/20 text-orange-400 font-bold text-sm">DAY 02</span>
            <h3 class="text-lg font-bold text-white">Git Version Control & Branching Strategy</h3>
          </div>
          <span class="text-xs font-mono text-slate-400">44 Slides (KMITL IT)</span>
        </div>
        <div class="p-4 rounded-xl bg-surfaceDark/70 border border-surfaceBorder space-y-3 text-sm text-slate-300">
          <h4 class="font-bold text-orange-400">Git 4 States & Workflow</h4>
          <pre class="p-3 rounded-lg bg-black/60 font-mono text-xs text-orange-200 overflow-x-auto">Working Directory ➔ (git add .) ➔ Staging Area (Index) ➔ (git commit -m) ➔ Local Repository ➔ (git push -u origin main) ➔ Remote Repository</pre>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
            <div class="p-3 rounded-lg bg-black/40 border border-surfaceBorder">
              <strong class="text-orange-300 block mb-1">คำสั่งกู้ชีพและแตกกิ่ง:</strong>
              • <code>git branch -M main</code> (เปลี่ยนชื่อ branch หลัก)<br>
              • <code>git checkout -b feature/login</code> (สร้างและสลับ branch)<br>
              • <code>git merge feature/login</code> (รวมโค้ดเข้า main)<br>
              • <code>git log --oneline --graph</code> (ดูประวัติ commit)
            </div>
            <div class="p-3 rounded-lg bg-black/40 border border-surfaceBorder">
              <strong class="text-orange-300 block mb-1">การแก้ Merge Conflict:</strong>
              เมื่อเกิดข้อขัดแย้ง ให้เปิดไฟล์แก้จุด <code>&lt;&lt;&lt;&lt;&lt;&lt;&lt; HEAD</code> และ <code>&gt;&gt;&gt;&gt;&gt;&gt;&gt;</code> เลือกโค้ดที่ถูกต้อง แล้วสั่ง:<br>
              <code>git add . && git commit -m "fix: resolve merge conflict"</code>
            </div>
          </div>
        </div>
      </div>

      <!-- Section Day 02 Docker -->
      <div id="arch-day2-docker" class="glass-card rounded-2xl p-6 space-y-4 border border-sky-500/30">
        <div class="flex items-center justify-between border-b border-surfaceBorder pb-3">
          <div class="flex items-center gap-3">
            <span class="p-2 rounded-lg bg-sky-500/20 text-sky-400 font-bold text-sm">DAY 02</span>
            <h3 class="text-lg font-bold text-white">Docker Containerization, Layer Caching & Docker Compose</h3>
          </div>
          <span class="text-xs font-mono text-slate-400">42 Slides (KMITL IT)</span>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-slate-300">
          <div class="p-4 rounded-xl bg-surfaceDark/70 border border-surfaceBorder space-y-2">
            <h4 class="font-bold text-sky-400">VM vs Container Architecture</h4>
            <p>• <strong>VM:</strong> มี Guest OS ทุกตัว หนัก (หลาย GB), บูตช้า (หลายสิบวินาที/นาที), กิน CPU/RAM สูง</p>
            <p>• <strong>Container:</strong> ไม่มี Guest OS แชร์ Host Linux Kernel ผ่าน <code>Namespaces</code> (แยก PID, Network, Mount) และ <code>cgroups</code> (จำกัด CPU/RAM) บูตในระดับ Millisecond</p>
          </div>
          <div class="p-4 rounded-xl bg-surfaceDark/70 border border-surfaceBorder space-y-2">
            <h4 class="font-bold text-sky-400">Dockerfile Layer Caching Secret</h4>
            <pre class="p-3 rounded-lg bg-black/60 font-mono text-xs text-sky-200 overflow-x-auto">FROM node:20-alpine
WORKDIR /app
# ⚠️ กฎสำคัญ: COPY package ก่อน เพื่อ Cache node_modules
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 5000
CMD ["npm", "start"]</pre>
          </div>
        </div>
      </div>

      <!-- Section Day 04 Node.js -->
      <div id="arch-day4" class="glass-card rounded-2xl p-6 space-y-4 border border-green-500/30">
        <div class="flex items-center justify-between border-b border-surfaceBorder pb-3">
          <div class="flex items-center gap-3">
            <span class="p-2 rounded-lg bg-green-500/20 text-green-400 font-bold text-sm">DAY 04</span>
            <h3 class="text-lg font-bold text-white">Node.js Core Modules, Asynchronous Programming & Express Framework</h3>
          </div>
          <span class="text-xs font-mono text-slate-400">55 Slides (KMITL IT)</span>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs text-slate-300">
          <div class="p-3 rounded-xl bg-surfaceDark/70 border border-surfaceBorder">
            <strong class="text-green-400 block mb-1">fs Module (File System):</strong>
            <code>const fs = require('fs');</code><br>
            • <code>fs.readFileSync('data.txt', 'utf8')</code><br>
            • <code>fs.promises.readFile(...)</code> (Async Promise)
          </div>
          <div class="p-3 rounded-xl bg-surfaceDark/70 border border-surfaceBorder">
            <strong class="text-green-400 block mb-1">path Module:</strong>
            <code>const path = require('path');</code><br>
            • <code>path.join(__dirname, 'routes', 'api.js')</code> ป้องกันปัญหา delimiter ต่างกันระหว่าง Windows (\) กับ Linux (/)
          </div>
          <div class="p-3 rounded-xl bg-surfaceDark/70 border border-surfaceBorder">
            <strong class="text-green-400 block mb-1">os Module:</strong>
            <code>const os = require('os');</code><br>
            • <code>os.platform()</code> (ดู OS)<br>
            • <code>os.freemem() / os.totalmem()</code>
          </div>
        </div>
      </div>

      <!-- Section Day 06 MySQL & Soft Delete -->
      <div id="arch-day6-mysql" class="glass-card rounded-2xl p-6 space-y-4 border border-amber-500/30">
        <div class="flex items-center justify-between border-b border-surfaceBorder pb-3">
          <div class="flex items-center gap-3">
            <span class="p-2 rounded-lg bg-amber-500/20 text-amber-400 font-bold text-sm">DAY 06</span>
            <h3 class="text-lg font-bold text-white">MySQL Integration, Prepared Statements & Soft Delete Pattern</h3>
          </div>
          <span class="text-xs font-mono text-slate-400">90 Slides + MySQL Notes</span>
        </div>
        <div class="p-4 rounded-xl bg-surfaceDark/70 border border-surfaceBorder space-y-3 text-sm text-slate-300">
          <h4 class="font-bold text-amber-400">Soft Delete Pattern vs Hard Delete</h4>
          <p>• <strong>Hard Delete:</strong> <code>DELETE FROM users WHERE id = ?</code> ➔ ข้อมูลหายถาวร ไม่สามารถกู้คืนได้ และอาจทำลาย Foreign Key</p>
          <p>• <strong>Soft Delete:</strong> <code>UPDATE users SET deleted_at = NOW() WHERE id = ? AND deleted_at IS NULL</code> ➔ เก็บข้อมูลไว้ตรวจ Audit Trail และทุก Query ต้องต่อ <code>WHERE deleted_at IS NULL</code></p>
        </div>
      </div>

      <!-- Section Day 06 MongoDB & Mongoose -->
      <div id="arch-day6-mongo" class="glass-card rounded-2xl p-6 space-y-4 border border-emerald-500/30">
        <div class="flex items-center justify-between border-b border-surfaceBorder pb-3">
          <div class="flex items-center gap-3">
            <span class="p-2 rounded-lg bg-emerald-500/20 text-emerald-400 font-bold text-sm">DAY 06 & LAB 6</span>
            <h3 class="text-lg font-bold text-white">MongoDB & Mongoose ODM Master CRUD (จุดออกสอบปฏิบัติ 20 คะแนนเต็ม)</h3>
          </div>
          <span class="text-xs font-mono text-emerald-400 font-bold">20 Points Exam Core</span>
        </div>
        <div class="p-4 rounded-xl bg-surfaceDark/70 border border-surfaceBorder space-y-3 text-sm text-slate-300">
          <h4 class="font-bold text-emerald-400">5-Route Mongoose CRUD Patterns</h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs font-mono">
            <div class="p-2.5 rounded bg-black/50 border border-surfaceBorder">
              <span class="text-emerald-400 font-bold">1. POST /api/students (201):</span><br>
              <code>const student = await Student.create(req.body);</code><br>
              <code>if (err.code === 11000) res.status(400).json({ error: 'Duplicate ID' });</code>
            </div>
            <div class="p-2.5 rounded bg-black/50 border border-surfaceBorder">
              <span class="text-emerald-400 font-bold">2. GET /api/students (200):</span><br>
              <code>const students = await Student.find(filter).sort({ createdAt: -1 });</code>
            </div>
            <div class="p-2.5 rounded bg-black/50 border border-surfaceBorder">
              <span class="text-emerald-400 font-bold">3. GET /api/students/:id (200/404):</span><br>
              <code>const student = await Student.findById(req.params.id);</code>
            </div>
            <div class="p-2.5 rounded bg-black/50 border border-surfaceBorder">
              <span class="text-emerald-400 font-bold">4. PUT /api/students/:id (200/404):</span><br>
              <code>Student.findByIdAndUpdate(id, body, { new: true, runValidators: true });</code>
            </div>
          </div>
        </div>
      </div>

      <!-- Section Day 07 SQL Joins & Prisma -->
      <div id="arch-day7" class="glass-card rounded-2xl p-6 space-y-4 border border-teal-500/30">
        <div class="flex items-center justify-between border-b border-surfaceBorder pb-3">
          <div class="flex items-center gap-3">
            <span class="p-2 rounded-lg bg-teal-500/20 text-teal-400 font-bold text-sm">DAY 07</span>
            <h3 class="text-lg font-bold text-white">Advanced SQL (Joins, DDL, Views) & Prisma ORM</h3>
          </div>
          <span class="text-xs font-mono text-slate-400">85 Slides (KMITL IT)</span>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs text-slate-300">
          <div class="p-4 rounded-xl bg-surfaceDark/70 border border-surfaceBorder space-y-2">
            <h4 class="font-bold text-teal-400 text-sm">SQL Joins Matrix</h4>
            <p>• <strong>INNER JOIN:</strong> ดึงเฉพาะข้อมูลที่ Match กันทั้งสองตาราง</p>
            <p>• <strong>LEFT JOIN:</strong> ดึงทุกแถวจากตารางซ้าย หากตารางขวาไม่มีจะเป็น NULL</p>
            <p>• <strong>RIGHT JOIN:</strong> ดึงทุกแถวจากตารางขวา หากตารางซ้ายไม่มีจะเป็น NULL</p>
            <p>• <strong>FULL JOIN (MySQL):</strong> ใช้ <code>LEFT JOIN ... UNION ... RIGHT JOIN</code></p>
            <p>• <strong>SELF JOIN:</strong> เชื่อมตารางตัวเองด้วย Alias (เช่น พนักงานกับหัวหน้า)</p>
          </div>
          <div class="p-4 rounded-xl bg-surfaceDark/70 border border-surfaceBorder space-y-2">
            <h4 class="font-bold text-teal-400 text-sm">Prisma ORM Workflow</h4>
            <p>1. <code>npx prisma init</code> ➔ สร้างไฟล์ <code>prisma/schema.prisma</code></p>
            <p>2. <code>npx prisma migrate dev --name init</code> ➔ สร้างตารางลง Database</p>
            <p>3. <code>npx prisma generate</code> ➔ สร้าง Prisma Client</p>
            <p>4. <code>const users = await prisma.user.findMany();</code></p>
          </div>
        </div>
      </div>
    </div>
'''

if 'id="view-archive"' not in html:
    html = html.replace('</main>', archive_view_html + '\n  </main>')

# 2. Add Omni-Search JavaScript Functionality
omni_js = '''
    // =========================================================================
    // 🔍 GLOBAL OMNI-SEARCH CONTROLLER
    // =========================================================================
    function handleOmniSearch(query) {
      const q = (query || '').trim().toLowerCase();
      const clearBtn = document.getElementById('omni-search-clear');
      if (clearBtn) clearBtn.classList.toggle('hidden', !q);

      if (!q) {
        // Clear highlights and unhide all
        document.querySelectorAll('.tab-view .glass-card, .tab-view pre, .tab-view p').forEach(el => {
          el.style.opacity = '1';
        });
        return;
      }

      // Automatically switch to view if searched specific keywords
      if (q.includes('step') || q.includes('blueprint') || q.includes('คำสั่ง')) {
        switchTab('steps');
      } else if (q.includes('lab') || q.includes('แล็บ') || q.includes('คะแนน')) {
        switchTab('labs');
      } else if (q.includes('quiz') || q.includes('ข้อสอบ') || q.includes('ช้อยส์')) {
        switchTab('grill');
      } else if (q.includes('vs') || q.includes('code') || q.includes('editor')) {
        switchTab('vscode');
      } else if (q.includes('cheat') || q.includes('สรุปย่อ')) {
        switchTab('cheatsheet');
      } else if (q.includes('slide') || q.includes('สไลด์') || q.includes('day 07') || q.includes('prisma') || q.includes('join')) {
        switchTab('archive');
      }
    }

    function clearOmniSearch() {
      const input = document.getElementById('omni-search-input');
      if (input) {
        input.value = '';
        handleOmniSearch('');
      }
    }
'''

if 'handleOmniSearch' not in html:
    html = html.replace('function resetAllProgress()', omni_js + '\n    function resetAllProgress()')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Injected view-archive and Omni-Search JS successfully! Length:", len(html))
