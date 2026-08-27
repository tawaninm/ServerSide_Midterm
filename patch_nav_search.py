# -*- coding: utf-8 -*-
import sys, os, re, json, shutil

sys.stdout.reconfigure(encoding='utf-8')

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

print("Original index.html length:", len(html))

# 1. Update Navigation Bar to include Tab 8 (All Slides & PDF Ingestion Archive)
tab_checklist_btn = '<button onclick="switchTab(\'checklist\')" id="tab-checklist"'
tab_archive_btn = '''<button onclick="switchTab('archive')" id="tab-archive" class="tab-btn px-4 py-2 rounded-lg border border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-2 transition-all">
        <i data-lucide="library" class="w-4 h-4 text-emerald-400"></i>
        <span>8. All Slides & PDF Ingestion Archive (คลังสรุปครบ 100% ทุกสไลด์)</span>
      </button>'''

if 'id="tab-archive"' not in html:
    html = html.replace(tab_checklist_btn, tab_archive_btn + '\n      ' + tab_checklist_btn)

# 2. Add Omni-Search Bar in Top Header if not present
header_search_target = '<div class="flex items-center gap-2.5">'
omni_search_html = '''<!-- Omni-Search Bar (Global Instant Finder) -->
      <div class="relative w-full max-w-xs md:max-w-md hidden sm:block">
        <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
          <i data-lucide="search" class="w-4 h-4"></i>
        </div>
        <input type="text" id="omni-search-input" oninput="handleOmniSearch(this.value)" placeholder="ค้นหาคำสั่ง, ทฤษฎี, โค้ด, จุดหลอก (เช่น docker, 11000, findByIdAndUpdate)..." class="w-full pl-9 pr-8 py-2 bg-surfaceDark/90 border border-surfaceBorder rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:border-brandIndigo focus:ring-1 focus:ring-brandIndigo transition-all font-sans">
        <button id="omni-search-clear" onclick="clearOmniSearch()" class="hidden absolute inset-y-0 right-0 pr-3 flex items-center text-slate-400 hover:text-white">
          <i data-lucide="x" class="w-3.5 h-3.5"></i>
        </button>
      </div>'''

if 'id="omni-search-input"' not in html:
    # Add search bar before the right side buttons
    html = html.replace('<div class="flex items-center gap-3">', '<div class="flex items-center gap-3">\n      ' + omni_search_html)

print("Nav & Search bar injected.")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Updated index.html successfully.")
