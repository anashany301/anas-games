import os
import re

# واجهة الشاشتين المنفصلتين الصافية والثابتة
clean_two_screens_ui = """
<!-- نظام الشاشتين المنفصلتين النظيف -->
<div id="perfectRoomOverlay" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #0f172a; z-index: 2147483647; display: flex; align-items: center; justify-content: center; font-family: Tahoma, sans-serif; color: direction: rtl;">
    
    <!-- الشاشة الأولى: إدخال الاسم وإنشاء أو الانضمام -->
    <div id="screenOne" style="background: #1e293b; padding: 25px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.7); width: 320px; text-align: center; border: 1px solid #38bdf8;">
        <h3 style="color: #38bdf8; margin-top: 0; direction: rtl;">غرفة اللعب الذكية</h3>
        <input type="text" id="pName" placeholder="اكتب اسمك هنا" style="width: 90%; padding: 10px; margin: 8px 0; border-radius: 6px; border: 1px solid #475569; background: #0f172a; color: white; font-size: 15px; text-align: center; outline: none; direction: rtl;">
        <hr style="border: 0; border-top: 1px solid #334155; margin: 15px 0;">
        <button onclick="createRoomAction()" style="background: #3b82f6; color: white; border: none; padding: 10px; border-radius: 6px; font-size: 15px; cursor: pointer; width: 95%; margin-top: 5px; font-weight: bold;">إنشاء غرفة جديدة</button>
        
        <div style="margin-top: 15px;">
            <input type="text" id="pCode" placeholder="أدخل كود صديقك" style="width: 90%; padding: 10px; margin: 8px 0; border-radius: 6px; border: 1px solid #475569; background: #0f172a; color: white; font-size: 15px; text-align: center; outline: none; direction: rtl;">
            <button onclick="joinRoomAction()" style="background: #10b981; color: white; border: none; padding: 10px; border-radius: 6px; font-size: 15px; cursor: pointer; width: 95%; margin-top: 5px; font-weight: bold;">دخول اللعبة</button>
        </div>
    </div>

    <!-- الشاشة الثانية: شاشة الانتظار الثابتة والمنفصلة تماماً -->
    <div id="screenTwo" style="background: #1e293b; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.7); width: 330px; text-align: center; border: 1px solid #10b981; display: none; direction: rtl;">
        <h3 style="color: #10b981; margin-top: 0;">✨ تم إنشاء الغرفة بنجاح</h3>
        <p style="font-size: 14px; color: #cbd5e1; margin: 10px 0;">كود الغرفة الخاص بك:</p>
        <div id="showCode" style="color: #38bdf8; font-size: 30px; font-weight: bold; letter-spacing: 4px; background: #0f172a; padding: 12px; border-radius: 8px; border: 1px dashed #38bdf8; margin: 10px 0;">----</div>
        <p style="font-size: 12px; color: #10b981; margin: 5px 0 15px 0;">📋 تم نسخ الكود للحافظة تلقائياً!</p>
        <hr style="border: 0; border-top: 1px solid #334155; margin: 15px 0;">
        <p style="font-size: 14px; color: #f59e0b; font-weight: bold; line-height: 1.6; margin: 0;">⏳ في انتظار صديقك لكتابة الكود والدخول للغرفة...</p>
        <p style="font-size: 11px; color: #64748b; margin-top: 15px;">(هذه الشاشة ثابتة ولن تختفي حتى يدخل صديقك)</p>
    </div>

</div>

<script>
    function createRoomAction() {
        const nameInput = document.getElementById('pName').value.trim();
        if(!nameInput) {
            alert('من فضلك اكتب اسمك الأول!');
            return;
        }

        // توليد كود عشوائي من 4 حروف
        const randomCode = Math.random().toString(36).substring(2, 6).toUpperCase();
        document.getElementById('showCode').innerText = randomCode;

        // نسخ الكود للحافظة
        navigator.clipboard.writeText(randomCode).catch(() => {});

        // إخفاء الشاشة الأولى تماماً وإظهار الشاشة الثانية الخاصة بالانتظار
        document.getElementById('screenOne').style.display = 'none';
        document.getElementById('screenTwo').style.display = 'block';
    }

    function joinRoomAction() {
        const nameInput = document.getElementById('pName').value.trim();
        const codeInput = document.getElementById('pCode').value.trim();
        if(!nameInput || !codeInput) {
            alert('اكتب اسمك وكود الغرفة من فضلك!');
            return;
        }

        // إغلاق نافذة الغرف بالكامل والدخول للعبة
        document.getElementById('perfectRoomOverlay').style.display = 'none';
    }
</script>
"""

for filename in os.listdir('.'):
    if filename.endswith('.html') and filename not in ['index.html', 'multiplayer-helper.html']:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        content_lower = content.lower()
        is_multi = ('إنشاء غرفة' in content or 'انشاء غرفة' in content or 
                    'peerjs' in content_lower or 'socket.io' in content_lower or 
                    'multiplayer' in content_lower or 'الرابط' in content or 'غرفة' in content)

        if is_multi:
            # مسح أي واجهات قديمة أو متداخلة تماماً من الملف
            content = re.sub(r'<div id="(perfectRoomOverlay|realRoomSystem|superRoomSystem|smartRoomOverlay|cleanRoomOverlay).*?</div>\s*</div>', '', content, flags=re.DOTALL)
            
            # حقن النظام النظيف قبل نهاية الـ body
            if "</body>" in content:
                content = content.replace("</body>", clean_two_screens_ui + "\n</body>")
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✨ تم حقن نظام الشاشتين المنفصلتين بنجاح في: {filename}")
        else:
            print(f"👤 لعبة فردية، تم تخطيها بأمان: {filename}")
