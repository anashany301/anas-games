import os
import re

# زرار نظيف وثابت فوق في أعلى الصفحة يودي لصفحة الأكواد
top_button_code = """
<div id="topRoomBtnContainer" style="position: fixed; top: 10px; left: 50%; transform: translateX(-50%); z-index: 999999; font-family: Tahoma, sans-serif;">
    <a href="room.html" style="background: linear-gradient(135deg, #3b82f6, #1d4ed8); color: white; padding: 8px 20px; border-radius: 20px; text-decoration: none; font-weight: bold; box-shadow: 0 4px 15px rgba(0,0,0,0.5); border: 1px solid #60a5fa; font-size: 14px; display: inline-block;">🔑 لدخول الغرفة بالأكواد</a>
</div>
"""

for filename in os.listdir('.'):
    if filename.endswith('.html') and filename not in ['index.html', 'room.html']:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        content_lower = content.lower()
        
        # شرط دقيق للألعاب الجماعية الحقيقية فقط (التي تستخدم نظم الغرف أو PeerJS)
        is_multi = (
            'إنشاء غرفة' in content or 
            'انشاء غرفة' in content or 
            'peerjs' in content_lower or 
            'socket.io' in content_lower or 
            'multiplayer' in content_lower
        )

        if is_multi:
            # تنظيف أي زرار أو أكواد قديمة ومزعجة
            content = re.sub(r'<div id="(perfectRoomOverlay|realRoomSystem|superRoomSystem|smartRoomOverlay|cleanRoomOverlay|fixedRoomLauncher|topRoomBtnContainer).*?</div>\s*</div>', '', content, flags=re.DOTALL)
            content = re.sub(r'<div id="topRoomBtnContainer".*?</div>', '', content, flags=re.DOTALL)
            
            # حقن الزرار العلوي الجديد ببراعة
            if "<body>" in content:
                content = content.replace("<body>", "<body>\n" + top_button_code)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✨ تم إضافة زرار الأكواد العلوي بنجاح في اللعبة الجماعية: {filename}")
