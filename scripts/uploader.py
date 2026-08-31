import os
import subprocess
import arcade

# 1. استخراج الصور من مكتبة أركيد محلياً
output_dir = "assets/sprites"
os.makedirs(output_dir, exist_ok=True)

arcade_path = os.path.dirname(arcade.__file__)
count = 0

for root, dirs, files in os.walk(arcade_path):
    for file in files:
        if file.endswith(('.png', '.gif', '.jpg')):
            src = os.path.join(root, file)
            dst = os.path.join(output_dir, file)
            if not os.path.exists(dst):
                with open(src, 'rb') as f_src, open(dst, 'wb') as f_dst:
                    f_dst.write(f_src.read())
                count += 1

print(f"[+] تم استخراج {count} صورة بنجاح.")

# 2. أتمتة الرفع لجيت هب تلقائياً
try:
    subprocess.run(["git", "add", output_dir], check=True)
    subprocess.run(["git", "commit", "-m", "Auto-upload extracted arcade sprite assets for offline use"], check=True)
    subprocess.run(["git", "push"], check=True)
    print("[+] تم رفع الصور وتحديث المستودع على جيت هب بنجاح أوفلاين وأونلاين!")
except Exception as e:
    print(f"[-] خطأ أثناء الرفع لجيت هب: {e}")
