import os
import re

# زرار نظيف وثابت يوجه لغرفة الانتظار الحقيقية من غير ما يلخبط اللعبة
clean_button_injection = """
<div id="fixedRoomLauncher" style="position: fixed; top: 15px; right: 15px; z-index: 999999; font-family: Tahoma, sans-serif;">
    <a href="room.html" style="background: #3b82f6; color: white; padding: 10px 18px; border-radius: 8px; text-decoration: none; font-weight: bold; box-shadow: 0 4px 12px rgba(0,0,0,0.4); border: 1px solid #60a5fa; display: inline-block;">🎮 إدارة الغرفة وأكواد اللعب</a>
</div>
"""

for filename in os.listdir('.'):
    if filename.endswith('.html') and filename not in ['index.html', 'room.html', 'multiplayer-helper.html']:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        content_lower = content.lower()
        is_multi = ('إنشاء غرفة' in content or 'انشاء غرفة' in content or 
                    'peerjs' in content_lower or 'socket.io' in content_lower or 
                    'multiplayer' in content_lower or 'الرابط' in content or 'غرفة' in content)

        if is_multi:
            # تنظيف تام لأي دوشة قديمة
            content = re.sub(r'<div id="(perfectRoomOverlay|realRoomSystem|superRoomSystem|smartRoomOverlay|cleanRoomOverlay).*?</div>\s*</div>', '', content, flags=re.DOTALL)
            content = re.sub(r'<div id="fixedRoomLauncher".*?</div>\s*</div>', '', content, flags=re.DOTALL)
            
            # زرار ثابت وآمن فوق في الشاشة يودي لغرفة الانتظار الصافية
            if "<body>" in content:
                content = content.replace("<body>", "<body>\n" + clean_button_injection)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"🔗 تم ربط اللعبة بزرار الغرفة الثابت في: {filename}")
        else:
            print(f"👤 لعبة فردية، تم تخطيها بأمان: {filename}")
