import shutil, os
src = r"D:\Tawanagent\ServerSide_Midterm\index.html"
dst = r"D:\Tawanagent\TAWAN-OS\02_STUDY\2026-Semester\Server_Side_Web_Development\exam_practice_web\index.html"
shutil.copy2(src, dst)
print("Synced to TAWAN-OS vault successfully!")
