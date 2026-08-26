import os
import re

# واجهة الأكواد النظيفة والصافية تماماً
clean_room_ui = """
<!-- واجهة الأكواد الصافية والنهائية -->
<div id="cleanRoomOverlay" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #0f172a; z-index: 9999999; display: flex; align-items: center; justify-content: center; font-family: Tahoma, sans-serif; color: white; direction: rtl;">
    <div style="background: #1e293b; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); width: 320px; text-align: center; border: 1px solid #38bdf8;">
        <h3 style="color: #38bdf8; margin-top: 0;">غرفة اللعب الذكية</h3>
        <input type="text" id="cPlayerName" placeholder="اكتب اسمك هنا" style="width: 90%; padding: 10px; margin: 8px 0; border-radius: 6px; border: 1px solid #475569; background: #0f172a; color: white; font-size: 15px; text-align: center; outline: none;">
        <hr style="border: 0; border-top: 1px solid #334155; margin: 15px 0;">
        <button onclick="cCreate()" style="background: #3b82f6; color: white; border: none; padding: 10px; border-radius: 6px; font-size: 15px; cursor: pointer; width: 95%; margin-top: 5px; font-weight: bold;">إنشاء غرفة جديدة</button>
        <div id="cCodeBox" style="color: #38bdf8; font-weight: bold; margin: 12px 0; font-size: 20px; letter-spacing: 2px; display:none;">
            الكود: <span id="cGeneratedCode" style="color: #10b981;"></span>
            <p style="font-size: 11px; color: #cbd5e1; margin: 5px 0 0 0;">📋 تم نسخ الكود للحافظة! أرسله لصديقك.</p>
        </div>
        <div id="cJoinSection" style="margin-top: 10px;">
            <input type="text" id="cCodeInput" placeholder="أدخل كود صديقك" style="width: 90%; padding: 10px; margin: 8px 0; border-radius: 6px; border: 1px solid #475569; background: #0f172a; color: white; font-size: 15px; text-align: center; outline: none;">
            <button onclick="cJoin()" style="background: #10b981; color: white; border: none; padding: 10px; border-radius: 6px; font-size: 15px; cursor: pointer; width: 95%; margin-top: 5px; font-weight: bold;">دخول اللعبة</button>
        </div>
    </div>
</div>

<script>
    function cCreate() {
        const name = document.getElementById('cPlayerName').value.trim();
        if(!name) { alert('من فضلك اكتب اسمك الأول!'); return; }
        const code = Math.random().toString(36).substring(2, 6).toUpperCase();
        
        document.getElementById('cGeneratedCode').innerText = code;
        document.getElementById('cCodeBox').style.display = 'block';
        document.getElementById('cJoinSection').style.display = 'none';
        
        navigator.clipboard.writeText(code).catch(() => {});

        setTimeout(() => {
            document.getElementById('cleanRoomOverlay').style.display = 'none';
        }, 3500);
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
        
        # هل هذه اللعبة جماعية (تحتوي على غرف أو لينكات أو مكتبات تفاعل سابقة)؟
        is_multi = ('إنشاء غرفة' in content or 'انشاء غرفة' in content or 
                    'peerjs' in content_lower or 'socket.io' in content_lower or 
                    'multiplayer' in content_lower or 'الرابط' in content or 'غرفة' in content)

        if is_multi:
            # 1. نسف وتطهير أي كود قديم أو لينكات أو واجهات سابقة من جذورها
            content = re.sub(r'<!--.*?-->', '', content, flags=dotall := re.DOTALL) # حذف التعليقات القديمة
            content = re.sub(r'<div id="(smartRoomOverlay|cleanRoomOverlay|modalOverlay|room-system-overlay|pure-room-overlay|oneTimeOverlay|ultimateRoomOverlay)"*?>.*?</div>\s*</div>', '', content, flags=re.DOTALL)
            content = re.sub(r'window\.location\.href\s*=.*?;', '', content) # مسح أي إعادة توجيه قديمة
            
            # 2. حقن الواجهة الصافية الجديدة مباشرة تحت الـ body
            if "<body>" in content:
                content = content.replace("<body>", "<body>\n" + clean_room_ui)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✨ تم تطهير اللعبة وحذف أي لينكات قديمة وحقن نظام الأكواد الصافي: {filename}")
        else:
            print(f"👤 لعبة فردية، تم تخطيها: {filename}")
