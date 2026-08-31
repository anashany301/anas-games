import os
import subprocess
import arcade

# 1. تحديد مسار مجلد sprites اللي في جذر المشروع (بالرجوع خطوة للوراء باستخدام ..)
current_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.abspath(os.path.join(current_dir, "../assets/sprites"))

os.makedirs(output_dir, exist_ok=True)
print(f"[*] سيتم حفظ الصور في المسار: {output_dir}")

arcade_path = os.path.dirname(arcade.__file__)
count = 0

# 2. سحب الصور من مكتبة أركيد
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

# 3. رفع التغييرات لجيت هب تلقائياً
try:
    # بنطلع مجلدين للوراء عشان نعمل git add للمجلد الرئيسي للمشروع
    os.chdir(os.path.abspath(os.path.join(current_dir, "..")))
    
    subprocess.run(["git", "add", "assets/sprites/"], check=True)
    subprocess.run(["git", "commit", "-m", "Auto-upload extracted arcade sprites for offline web"], check=True)
    subprocess.run(["git", "push"], check=True)
    print("[+] تم رفع الصور وتحديث المستودع على جيت هب بنجاح!")
except Exception as e:
    print(f"[-] خطأ أثناء الرفع لجيت هب: {e}")
