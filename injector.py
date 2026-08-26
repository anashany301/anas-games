import os
import re

# نظام الغرف الحقيقي المتصل بشبكة ربط الأجهزة (PeerJS) لتشتغل الغرفة بجد بين جهازين
real_room_ui = """
<!-- مكتبة الربط الحقيقي بين الأجهزة -->
<script src="https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js"></script>

<script>
(function() {
    if (document.getElementById('realRoomSystem')) return;

    const container = document.createElement('div');
    container.id = 'realRoomSystem';
    container.style.cssText = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #0f172a; z-index: 2147483647; display: flex; align-items: center; justify-content: center; font-family: Tahoma, sans-serif; color: white; direction: rtl;';
    
    container.innerHTML = `
        <div id="rBoxStep1" style="background: #1e293b; padding: 25px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.7); width: 320px; text-align: center; border: 1px solid #38bdf8;">
            <h3 style="color: #38bdf8; margin-top: 0;">الغرفة الحقيقية أونلاين</h3>
            <input type="text" id="rNameInput" placeholder="اكتب اسمك هنا" style="width: 90%; padding: 10px; margin: 8px 0; border-radius: 6px; border: 1px solid #475569; background: #0f172a; color: white; font-size: 15px; text-align: center; outline: none;">
            <hr style="border: 0; border-top: 1px solid #334155; margin: 15px 0;">
            <button id="rCreateBtn" style="background: #3b82f6; color: white; border: none; padding: 10px; border-radius: 6px; font-size: 15px; cursor: pointer; width: 95%; margin-top: 5px; font-weight: bold;">إنشاء غرفة جديدة</button>
            <div style="margin-top: 15px;">
                <input type="text" id="rCodeInput" placeholder="أدخل كود صديقك (مثال: AB12)" style="width: 90%; padding: 10px; margin: 8px 0; border-radius: 6px; border: 1px solid #475569; background: #0f172a; color: white; font-size: 15px; text-align: center; outline: none; text-transform: uppercase;">
                <button id="rJoinBtn" style="background: #10b981; color: white; border: none; padding: 10px; border-radius: 6px; font-size: 15px; cursor: pointer; width: 95%; margin-top: 5px; font-weight: bold;">دخول الغرفة</button>
            </div>
            <p id="rStatusMsg" style="font-size: 12px; color: #94a3b8; margin-top: 12px;"></p>
        </div>

        <div id="rBoxStep2" style="background: #1e293b; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.7); width: 330px; text-align: center; border: 1px solid #10b981; display: none;">
            <h3 style="color: #10b981; margin-top: 0;">✨ تم إنشاء الغرفة بنجاح</h3>
            <p style="font-size: 14px; color: #cbd5e1; margin: 10px 0;">كود الغرفة الخاص بك:</p>
            <div id="rDisplayCode" style="color: #38bdf8; font-size: 28px; font-weight: bold; letter-spacing: 3px; background: #0f172a; padding: 10px; border-radius: 8px; border: 1px dashed #38bdf8; margin: 10px 0;">----</div>
            <p style="font-size: 12px; color: #10b981; margin: 5px 0 15px 0;">📋 تم نسخ الكود للحافظة تلقائياً!</p>
            <hr style="border: 0; border-top: 1px solid #334155; margin: 15px 0;">
            <p style="font-size: 14px; color: #f59e0b; font-weight: bold; line-height: 1.6; margin: 0;">⏳ في انتظار صديقك لكتابة الكود والدخول...</p>
            <button id="rCancelBtn" style="background: #ef4444; color: white; border: none; padding: 8px; border-radius: 6px; font-size: 13px; cursor: pointer; width: 80%; margin-top: 15px;">إلغاء والرجوع</button>
        </div>
    `;

    document.body.appendChild(container);

    setTimeout(() => {
        let peer = null;
        let conn = null;
        const statusMsg = document.getElementById('rStatusMsg');

        // توليد كود قصير ومنسق (مثلا من 4 حروف)
        function generateShortCode() {
            return Math.random().toString(36).substring(2, 6).toUpperCase();
        }

        // إنشاء غرفة (Host)
        document.getElementById('rCreateBtn').onclick = function() {
            const name = document.getElementById('rNameInput').value.trim();
            if(!name) { alert('من فضلك اكتب اسمك الأول!'); return; }

            statusMsg.innerText = 'جاري إنشاء الغرفة على السيرفر...';
            const shortCode = 'GM-' + generateShortCode(); // كود مميز للغرفة

            // إنشاء الاتصال بالسيرفر المجاني
            peer = new Peer(shortCode);

            peer.on('open', (id) => {
                document.getElementById('rDisplayCode').innerText = shortCode;
                navigator.clipboard.writeText(shortCode).catch(() => {});
                
                document.getElementById('rBoxStep1').style.display = 'none';
                document.getElementById('rBoxStep2').style.display = 'block';
            });

            peer.on('error', (err) => {
                statusMsg.innerText = 'خطأ في الاتصال، جرب مرة تانية.';
                console.error(err);
            });

            // عندما يتصل الصديق بالغرقة
            peer.on('connection', (connection) => {
                conn = connection;
                statusMsg.innerText = 'انضم صديقك بنجاح! جاري فتح اللعبة...';
                setTimeout(() => {
                    document.getElementById('realRoomSystem').style.display = 'none';
                }, 1000);
            });
        };

        // الدخول لغرفة صديقك (Client)
        document.getElementById('rJoinBtn').onclick = function() {
            const name = document.getElementById('rNameInput').value.trim();
            const code = document.getElementById('rCodeInput').value.trim().toUpperCase();
            
            if(!name || !code) { alert('اكتب اسمك وكود غرفة صديقك بدقة!'); return; }

            statusMsg.innerText = 'جاري البحث عن غرفة صديقك والدخول إليها...';

            // إنشاء عميل مؤقت للاتصال
            const tempPeer = new Peer();

            tempPeer.on('open', () => {
                const connection = tempPeer.connect(code);

                connection.on('open', () => {
                    statusMsg.innerText = 'تم الاتصال بنجاح! جارٍ الدخول...';
                    setTimeout(() => {
                        document.getElementById('realRoomSystem').style.display = 'none';
                    }, 800);
                });

                connection.on('error', (err) => {
                    alert('عذراً، لم يتم العثور على الغرفة أو أن الكود غير صحيح!');
                    statusMsg.innerText = 'فشل الدخول، تأكد من الكود.';
                });
            });
        };

        document.getElementById('rCancelBtn').onclick = function() {
            if(peer) peer.destroy();
            document.getElementById('rBoxStep2').style.display = 'none';
            document.getElementById('rBoxStep1').style.display = 'block';
            statusMsg.innerText = '';
        };

    }, 500);
})();
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
            # تنظيف أي أكواد قديمة وحقن نظام الغرف الحقيقي المتصل بالشبكة
            content = re.sub(r'<div id="(realRoomSystem|superRoomSystem|smartRoomOverlay|cleanRoomOverlay).*?</div>\s*</div>', '', content, flags=re.DOTALL)
            
            if "</body>" in content:
                content = content.replace("</body>", real_room_ui + "\n</body>")
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"🌐 تم حقن نظام الغرف الحقيقي أونلاين في: {filename}")
        else:
            print(f"👤 لعبة فردية، تم تخطيها بأمان: {filename}")
