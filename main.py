from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import socket
import threading
from urllib.parse import quote

try:
	from importlib import import_module

	try:
		webview = import_module("webview")
	except ImportError:
		webview = None
except ImportError:
	webview = None


PAGE = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Saudi National Day Quiz | اختبار اليوم الوطني السعودي</title>
<style>
body{margin:0;background:#063b2b;color:#fff;font:18px system-ui;text-align:center}main{max-width:700px;margin:35px auto;padding:28px;background:#087443;border-radius:20px;box-shadow:0 8px 25px #021d15}h1{color:#f4c542}.flag{font-size:70px;margin:5px}.question{font-size:25px;margin:25px 0 18px}.answers{display:grid;gap:12px}.answers button,#next{padding:14px;border:0;border-radius:10px;font-size:17px;cursor:pointer}.answers button{background:#fff;color:#063b2b}.answers button:hover{background:#f4c542}.correct{background:#75d69a!important}.wrong{background:#f38b8b!important}#next{margin-top:22px;background:#f4c542;color:#063b2b;display:none}.score{color:#f4c542}.qr{margin-top:25px;padding:16px;background:#fff;color:#063b2b;border-radius:12px}.qr img{width:180px;height:180px;display:block;margin:10px auto}.qr small{word-break:break-all}
</style></head><body><main><div class="flag">🇸🇦</div><h1>Saudi National Day Quiz</h1><p>Test your knowledge of the Kingdom!</p><div class="score" id="score">Score: 0</div><div class="question" id="question"></div><div class="answers" id="answers"></div><button id="next">Next question</button></main>





<div class="qr"><strong>Scan to open this quiz</strong><img src="https://quickchart.io/qr?size=180&margin=1&text=__QUIZ_URL_ENCODED__" alt="QR code for this quiz"><small>__QUIZ_URL__</small></div></main>

<script>
const questions=[
 {q:'When is Saudi National Day celebrated?',a:['23 September','1 January','22 February','30 November'],c:0},
 {q:'What is the capital city of Saudi Arabia?',a:['Jeddah','Riyadh','Makkah','Dammam'],c:1},
 {q:'What color is the Saudi flag?',a:['Blue and white','Red and gold','Green and white','Black and yellow'],c:2},
 {q:'What does “Saudi” refer to?',a:['The sea','The House of Saud','A mountain','A flower'],c:1},
 {q:'Saudi National Day commemorates the unification of which kingdom?',a:['The Kingdom of Saudi Arabia','The Kingdom of Bahrain','The United Arab Emirates','The Hashemite Kingdom'],c:0},
 {q:'In which year was the Kingdom of Saudi Arabia unified?',a:['1902','1932','1945','1953'],c:1},
 {q:'Which symbol appears on the Saudi flag?',a:['A palm tree','A falcon','A sword','A star'],c:2},
 {q:'What is the official language of Saudi Arabia?',a:['Arabic','English','Urdu','French'],c:0},
 {q:'What is Saudi Arabia’s currency?',a:['Dinar','Riyal','Dirham','Pound'],c:1},
 {q:'Which famous city is home to the Kaaba?',a:['Taif','Madinah','Makkah','Abha'],c:2},
 {q:'Who founded the modern Kingdom of Saudi Arabia?',a:['King Abdulaziz Ibn Saud','King Faisal','King Khalid','King Abdullah'],c:0},
 {q:'What is another name for Saudi National Day?',a:['Founding Day','Al-Yaom Al-Watani','Heritage Day','Unity Festival'],c:1},
 {q:'What does the Arabic inscription on the Saudi flag say?',a:['God is Great','There is no god but Allah, and Muhammad is the Messenger of Allah','Peace and Prosperity','Long Live the Kingdom'],c:1},
 {q:'What is the national animal of Saudi Arabia?',a:['Arabian oryx','Camel','Falcon','Horse'],c:0},
 {q:'Which sea lies west of Saudi Arabia?',a:['Arabian Sea','Red Sea','Mediterranean Sea','Black Sea'],c:1},
 {q:'Which gulf lies east of Saudi Arabia?',a:['Gulf of Oman','Persian Gulf','Gulf of Aden','Suez Gulf'],c:1},
 {q:'What is Saudi Arabia’s largest city by population?',a:['Riyadh','Jeddah','Makkah','Medina'],c:0},
 {q:'Which region is Saudi Arabia part of?',a:['Southeast Asia','The Middle East','North Africa','Central Europe'],c:1},
 {q:'What is the name of Saudi Arabia’s national airline?',a:['Emirates','Qatar Airways','Saudia','Gulf Air'],c:2},
 {q:'Which desert covers much of southern Saudi Arabia?',a:['Sahara Desert','Rub al-Khali','Gobi Desert','Atacama Desert'],c:1},
 {q:'What is Rub al-Khali also known as?',a:['The Empty Quarter','The Golden Desert','The Great Dune','The Silent Sands'],c:0},
 {q:'Which city is known as the Bride of the Red Sea?',a:['Riyadh','Jeddah','Dammam','Tabuk'],c:1},
 {q:'What is the national tree of Saudi Arabia?',a:['Date palm','Olive tree','Acacia tree','Palm tree'],c:0},
 {q:'Which important pilgrimage takes place in Makkah?',a:['Hajj','Diwali','Easter','Nowruz'],c:0},
 {q:'What is the traditional Saudi coffee called?',a:['Qahwa','Chai','Espresso','Mocha'],c:0},
 {q:'Which mountain is near Makkah?',a:['Mount Uhud','Jabal al-Nour','Mount Sinai','Jabal al-Akhdar'],c:1},
 {q:'What is Saudi Arabia’s largest administrative region by area?',a:['Riyadh Region','Makkah Region','Eastern Province','Northern Borders Region'],c:2},
 {q:'Which modern project is being developed in northwestern Saudi Arabia?',a:['NEOM','Masdar City','The Line of Cairo','Silk City'],c:0},
 {q:'What is the traditional Saudi dance often performed at celebrations?',a:['Ardah','Dabke','Samba','Haka'],c:0}
];
const arabicQuestions=[
 'متى يتم الاحتفال باليوم الوطني السعودي؟','ما عاصمة المملكة العربية السعودية؟','ما لون العلم السعودي؟','إلى ماذا تشير كلمة سعودي؟','اليوم الوطني السعودي يحيي ذكرى توحيد أي مملكة؟','في أي عام توحدت المملكة العربية السعودية؟','ما الرمز الموجود على العلم السعودي؟','ما اللغة الرسمية في المملكة العربية السعودية؟','ما عملة المملكة العربية السعودية؟','أي مدينة تشتهر بوجود الكعبة؟','من أسس المملكة العربية السعودية الحديثة؟','ما الاسم الآخر لليوم الوطني السعودي؟','ماذا تقول العبارة العربية على العلم السعودي؟','ما الحيوان الوطني في المملكة العربية السعودية؟','أي بحر يقع غرب المملكة العربية السعودية؟','أي خليج يقع شرق المملكة العربية السعودية؟','ما أكبر مدينة في المملكة العربية السعودية من حيث عدد السكان؟','في أي منطقة تقع المملكة العربية السعودية؟','ما اسم شركة الطيران الوطنية السعودية؟','أي صحراء تغطي جزءاً كبيراً من جنوب المملكة العربية السعودية؟','بماذا تُعرف صحراء الربع الخالي أيضاً؟','أي مدينة تُعرف بعروس البحر الأحمر؟','ما الشجرة الوطنية في المملكة العربية السعودية؟','ما فريضة الحج المهمة التي تُؤدى في مكة؟','ماذا تُسمى القهوة السعودية التقليدية؟','أي جبل يقع بالقرب من مكة؟','ما أكبر منطقة إدارية في المملكة العربية السعودية من حيث المساحة؟','ما المشروع الحديث الذي يُطوَّر في شمال غرب المملكة العربية السعودية؟','ما الرقصة السعودية التقليدية التي تؤدى غالباً في الاحتفالات؟'
];
const arabicAnswers=[
 ['23 سبتمبر','1 يناير','22 فبراير','30 نوفمبر'],['جدة','الرياض','مكة المكرمة','الدمام'],['أزرق وأبيض','أحمر وذهبي','أخضر وأبيض','أسود وأصفر'],['البحر','آل سعود','جبل','زهرة'],['المملكة العربية السعودية','مملكة البحرين','الإمارات العربية المتحدة','المملكة الهاشمية'],['1902','1932','1945','1953'],['نخلة','صقر','سيف','نجمة'],['العربية','الإنجليزية','الأردية','الفرنسية'],['دينار','ريال','درهم','جنيه'],['الطائف','المدينة المنورة','مكة المكرمة','أبها'],['الملك عبدالعزيز بن سعود','الملك فيصل','الملك خالد','الملك عبدالله'],['يوم التأسيس','اليوم الوطني السعودي','يوم التراث','مهرجان الوحدة'],['الله أكبر','لا إله إلا الله محمد رسول الله','السلام والازدهار','عاشت المملكة'],['المها العربي','الجمل','الصقر','الحصان'],['بحر العرب','البحر الأحمر','البحر المتوسط','البحر الأسود'],['خليج عُمان','الخليج العربي','خليج عدن','خليج السويس'],['الرياض','جدة','مكة المكرمة','المدينة المنورة'],['جنوب شرق آسيا','الشرق الأوسط','شمال أفريقيا','وسط أوروبا'],['طيران الإمارات','الخطوط الجوية القطرية','الخطوط السعودية','طيران الخليج'],['الصحراء الكبرى','الربع الخالي','صحراء جوبي','صحراء أتاكاما'],['الربع الفارغ','الصحراء الذهبية','الكثبان الكبرى','الرمال الصامتة'],['الرياض','جدة','الدمام','تبوك'],['نخلة التمر','شجرة الزيتون','شجرة الأكاسيا','النخيل'],['الحج','ديوالي','عيد الفصح','النوروز'],['القهوة','الشاي','الإسبريسو','الموكا'],['جبل أحد','جبل النور','جبل سيناء','جبل الأخضر'],['منطقة الرياض','منطقة مكة المكرمة','المنطقة الشرقية','منطقة الحدود الشمالية'],['نيوم','مدينة مصدر','خط القاهرة','مدينة الحرير'],['العرضة','الدبكة','السامبا','الهاكا']
];
let index=0,score=0,answersGiven=[],arabic=false;const q=document.getElementById('question'), answers=document.getElementById('answers'), next=document.getElementById('next');
function show(){q.textContent=arabic?`${arabicQuestions[index]}\n${questions[index].q}`:`${questions[index].q}\n${arabicQuestions[index]}`;q.style.whiteSpace='pre-line';answers.innerHTML='';next.style.display='none';questions[index].a.forEach((text,i)=>{let b=document.createElement('button');b.textContent=arabic?`${arabicAnswers[index][i]} — ${text}`:`${text} — ${arabicAnswers[index][i]}`;b.onclick=()=>answer(b,i);answers.appendChild(b)});}
function answer(button,i){let x=questions[index];[...answers.children].forEach(b=>b.disabled=true);answersGiven[index]=i;if(i===x.c){button.classList.add('correct');score++;}else{button.classList.add('wrong');answers.children[x.c].classList.add('correct')}document.getElementById('score').textContent=`Score: ${score}`;setTimeout(()=>{index++;if(index<questions.length)show();else finish()},700);}
function finish(){q.textContent=arabic?`اكتمل الاختبار! نتيجتك ${score}/${questions.length}.\nQuiz complete! You scored ${score}/${questions.length}.`:`Quiz complete! You scored ${score}/${questions.length}.\nاكتمل الاختبار! نتيجتك ${score}/${questions.length}.`;answers.innerHTML='<h2>Check your answers | راجع إجاباتك</h2>';questions.forEach((x,i)=>{let item=document.createElement('div');item.style.cssText='text-align:left;background:#fff;color:#063b2b;padding:12px;border-radius:8px;margin:8px 0';let chosen=answersGiven[i];item.innerHTML=`<strong>${i+1}. ${x.q}<br>${arabicQuestions[i]}</strong><br>Your answer | إجابتك: ${chosen===undefined?'No answer | لا توجد إجابة':`${chosen+1}. ${x.a[chosen]} — ${arabicAnswers[i][chosen]}`}<br>Correct answer | الإجابة الصحيحة: ${x.c+1}. ${x.a[x.c]} — ${arabicAnswers[i][x.c]}`;item.style.borderLeft=`6px solid ${chosen===x.c?'#35a866':'#d9534f'}`;answers.appendChild(item)});next.textContent='Play again | العب مرة أخرى';next.style.display='inline-block';next.onclick=()=>{index=0;score=0;answersGiven=[];document.getElementById('score').textContent='Score: 0 | النتيجة: 0';next.textContent='Next question | السؤال التالي';show()};}
show();
</script></body></html>'''


# Set QUIZ_PUBLIC_URL to your public quiz URL when hosting it online.
PUBLIC_URL = os.environ.get(
	"QUIZ_PUBLIC_URL",
	"",
)


def quiz_url():
	if PUBLIC_URL:
		return PUBLIC_URL
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as probe:
			probe.connect(("8.8.8.8", 80))
			host = probe.getsockname()[0]
	except OSError:
		host = "127.0.0.1"
	return f"http://{host}:8000/"


class QuizHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		url = quiz_url()
		page = PAGE.replace("__QUIZ_URL__", url).replace("__QUIZ_URL_ENCODED__", quote(url, safe=""))
		self.send_response(200)
		self.send_header("Content-Type", "text/html; charset=utf-8")
		self.send_header("Content-Disposition", "inline")
		self.end_headers()
		self.wfile.write(page.encode("utf-8"))

	def log_message(self, *_):
		pass


if __name__ == "__main__":
	# Run as a desktop app when pywebview is installed; otherwise use the browser.
	PORT = int(os.environ.get("PORT", "8000"))
	server = HTTPServer(("0.0.0.0", PORT), QuizHandler)
	url = quiz_url()
	print(f"Saudi National Day Quiz is running at {url}")
	server_thread = threading.Thread(target=server.serve_forever, daemon=True)
	server_thread.start()
	try:
		if webview is not None:
			webview.create_window("Saudi National Day Quiz", url, width=900, height=800)
			webview.start()
		else:
			import webbrowser
			webbrowser.open_new(url)
			server_thread.join()
	except KeyboardInterrupt:
		print("\nApp closed.")
	finally:
		server.shutdown()
		server.server_close()
