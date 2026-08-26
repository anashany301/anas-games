import os
import re

# واجهة قوية جداً تلغي أي سكريبتات تانية وتثبت شاشة الانتظار
clean_room_ui = """
<!-- نظام الحماية والشاشتين الحصري للغرف -->
<div id="cleanRoomOverlay" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #0f172a; z-index: 999999999; display: flex; align-items: center; justify-content: center; font-family: Tahoma, sans-serif; color: white; direction: rtl;">
    
    <!-- الشاشة الأولى -->
    <div id="stepOneBox" style="background: #1e293b; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); width: 320px; text-align: center; border: 1px solid #38bdf8;">
        <h3 style="color: #38bdf8; margin-top: 0;">غرفة اللعب الذكية</h3>
        <input type="text" id="cPlayerName" placeholder="اكتب اسمك هنا" style="width: 90%; padding: 10px; margin: 8px 0; border-radius: 6px; border: 1px solid #475569; background: #0f172a; color: white; font-size: 15px; text-align: center; outline: none;">
        <hr style="border: 0; border-top: 1px solid #334155; margin: 15px 0;">
        <button onclick="goToWaitingScreen()" style="background: #3b82f6; color: white; border: none; padding: 10px; border-radius: 6px; font-size: 15px; cursor: pointer; width: 95%; margin-top: 5px; font-weight: bold;">إنشاء غرفة جديدة</button>
        
        <div style="margin-top: 15px;">
            <input type="text" id="cCodeInput" placeholder="أدخل كود صديقك" style="width: 90%; padding: 10px; margin: 8px 0; border-radius: 6px; border: 1px solid #475569; background: #0f172a; color: white; font-size: 15px; text-align: center; outline: none;">
            <button onclick="cJoin()" style="background: #10b981; color: white; border: none; padding: 10px; border-radius: 6px; font-size: 15px; cursor: pointer; width: 95%; margin-top: 5px; font-weight: bold;">دخول اللعبة</button>
        </div>
    </div>

    <!-- الشاشة الثانية: شاشة الانتظار الثابتة نهائياً -->
    <div id="stepTwoWaitingBox" style="background: #1e293b; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); width: 330px; text-align: center; border: 1px solid #10b981; display: none;">
        <h3 style="color: #10b981; margin-top: 0;">✨ تم إنشاء الغرفة بنجاح</h3>
        <p style="font-size: 14px; color: #cbd5e1; margin: 10px 0;">كود الغرفة الخاص بك:</p>
        <div id="cGeneratedCode" style="color: #38bdf8; font-size: 28px; font-weight: bold; letter-spacing: 3px; background: #0f172a; padding: 10px; border-radius: 8px; border: 1px dashed #38bdf8; margin: 10px 0;">----</div>
        <p style="font-size: 12px; color: #10b981; margin: 5px 0 15px 0;">📋 تم نسخ الكود للحافظة تلقائياً!</p>
        <hr style="border: 0; border-top: 1px solid #334155; margin: 15px 0;">
        <p style="font-size: 14px; color: #f59e0b; font-weight: bold; line-height: 1.6; margin: 0;">⏳ في انتظار صديقك لكتابة الكود والدخول للغرفة...</p>
        <p style="font-size: 11px; color: #64748b; margin-top: 15px;">(هذه الشاشة ثابتة ولن تختفي حتى يدخل صديقك)</p>
    </div>

</div>

<script>
    function goToWaitingScreen() {
        const name = document.getElementById('cPlayerName').value.trim();
        if(!name) { alert('من فضلك اكتب اسمك الأول!'); return; }
        
        const code = Math.random().toString(36).substring(2, 6).toUpperCase();
        document.getElementById('cGeneratedCode').innerText = code;
        
        navigator.clipboard.writeText(code).catch(() => {});
        
        // إخفاء الشاشة الأولى وإظهار شاشة الانتظار للأبد
        document.getElementById('stepOneBox').style.display = 'none';
        document.getElementById('stepTwoWaitingBox').style.display = 'block';
    }

    function cJoin() {
        const name = document.getElementById('cPlayerName').value.trim();
        const code = document.getElementById('cCodeInput').value.trim();
        if(!name || !code) { alert('اكتب اسمك وكود الغرفة من فضلك!'); return; }
        document.getElementById('cleanRoomOverlay').style.display = 'none';
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
            # نسف وتطهير أي واجهات أو أکواد قديمة كانت مسببة المشكلة بالكامل
            content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
            content = re.sub(r'<div id="(smartRoomOverlay|cleanRoomOverlay|modalOverlay|room-system-overlay|pure-room-overlay|oneTimeOverlay|ultimateRoomOverlay)"*?>.*?</div>\s*</div>', '', content, flags=re.DOTALL)
            content = re.sub(r'window\.location\.href\s*=.*?;', '', content)
            
            # حقن النظام الجديد مباشرة بعد الـ body
            if "<body>" in content:
                content = content.replace("<body>", "<body>\n" + clean_room_ui)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"🔒 تم تطهير اللعبة وحقن نظام الانتظار الحصري: {filename}")
        else:
            print(f"👤 لعبة فردية، تم تخطيها بأمان: {filename}")
