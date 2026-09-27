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
  {q:'What does the Arabic inscription on the Saudi flag say?',a:['God is Great','There is no god but Allah, and Muhammad is the Messenger of Allah','Peace and Prosperity','Long Live the Kingdom'],c:1},
 {q:'What is the national animal of Saudi Arabia?',a:['Camel','Arabian oryx','Falcon','Horse'],c:0},
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
 {q:'What is the traditional Saudi dance often performed at celebrations?',a:['Ardah','Dabke','Samba','Haka'],c:0},
 {q:'Which country will host the FIFA World Cup 2034?',a:['Saudi Arabia','Qatar','Morocco','United Arab Emirates'],c:0},
 {q:'Which countries will host the main FIFA World Cup 2030?',a:['Saudi Arabia, Qatar and UAE','Spain, Portugal and Morocco','France, Italy and Germany','Brazil, Argentina and Chile'],c:1},
 {q:'Which three South American countries will host centenary celebration matches at the 2030 World Cup?',a:['Brazil, Chile and Peru','Colombia, Ecuador and Bolivia','Uruguay, Argentina and Paraguay','Mexico, USA and Canada'],c:2},
 {q:'Why is the 2030 FIFA World Cup special for the tournament’s history?',a:['It celebrates 50 years of the World Cup','It celebrates 100 years since the first World Cup','It is the first World Cup in Asia','It is the first World Cup with 16 teams'],c:1},
 {q:'Will the FIFA World Cup 2034 be hosted in one city or multiple cities?',a:['One city only','Multiple cities across Saudi Arabia','Only Riyadh and Jeddah','Only coastal cities'],c:1},
 {q:'What does hosting the FIFA World Cup 2034 mean for Saudi Arabia?',a:['Saudi Arabia will host the FIFA World Cup','Saudi Arabia will host the Olympics','Saudi Arabia will host the Asian Games for the first time','Saudi Arabia will host the 2030 World Cup'],c:0},
 {q:'What is the Esports World Cup commonly abbreviated as?',a:['EWC','EFC','ESC','EWCup'],c:0},
 {q:'Which Saudi city hosts the Esports World Cup?',a:['Riyadh','Jeddah','Dammam','Medina'],c:0},
 {q:'What type of competition is the Esports World Cup?',a:['A football tournament only','A multi-game esports competition','A motorsport championship','A tennis tournament'],c:1},
 {q:'Which Saudi national development plan is associated with major projects and the growth of sports and entertainment?',a:['Vision 2030','Vision 2020','Saudi Plan 2040','Kingdom 2050'],c:0},
 {q:'What is NEOM?',a:['A Saudi Arabian development project','A football club','A national airline','An esports team'],c:0},
 {q:'Which Saudi city is the capital and a major host city for international sports and esports events?',a:['Riyadh','Taif','Tabuk','Jazan'],c:0}
];
const arabicQuestions=[
 'متى يتم الاحتفال باليوم الوطني السعودي؟','ما عاصمة المملكة العربية السعودية؟','ما لون العلم السعودي؟','إلى ماذا تشير كلمة سعودي؟','اليوم الوطني السعودي يحيي ذكرى توحيد أي مملكة؟','في أي عام توحدت المملكة العربية السعودية؟','ما الرمز الموجود على العلم السعودي؟','ما اللغة الرسمية في المملكة العربية السعودية؟','ما عملة المملكة العربية السعودية؟','أي مدينة تشتهر بوجود الكعبة؟','من أسس المملكة العربية السعودية الحديثة؟','ماذا تقول العبارة العربية على العلم السعودي؟','ما الحيوان الوطني في المملكة العربية السعودية؟','أي بحر يقع غرب المملكة العربية السعودية؟','أي خليج يقع شرق المملكة العربية السعودية؟','ما أكبر مدينة في المملكة العربية السعودية من حيث عدد السكان؟','في أي منطقة تقع المملكة العربية السعودية؟','ما اسم شركة الطيران الوطنية السعودية؟','أي صحراء تغطي جزءاً كبيراً من جنوب المملكة العربية السعودية؟','بماذا تُعرف صحراء الربع الخالي أيضاً؟','أي مدينة تُعرف بعروس البحر الأحمر؟','ما الشجرة الوطنية في المملكة العربية السعودية؟','ما فريضة الحج المهمة التي تُؤدى في مكة؟','ماذا تُسمى القهوة السعودية التقليدية؟','أي جبل يقع بالقرب من مكة؟','ما أكبر منطقة إدارية في المملكة العربية السعودية من حيث المساحة؟','ما المشروع الحديث الذي يُطوَّر في شمال غرب المملكة العربية السعودية؟','ما الرقصة السعودية التقليدية التي تؤدى غالباً في الاحتفالات؟',
'أي دولة ستستضيف كأس العالم لكرة القدم 2034؟',
'ما الدول التي ستستضيف كأس العالم لكرة القدم 2030 بشكل رئيسي؟',
'ما الدول الثلاث في أمريكا الجنوبية التي ستستضيف مباريات احتفالية بمناسبة مئوية كأس العالم 2030؟',
'لماذا تُعد بطولة كأس العالم 2030 مميزة في تاريخ البطولة؟',
'هل ستقام كأس العالم 2034 في مدينة واحدة أم عدة مدن؟',
'ماذا تعني استضافة كأس العالم لكرة القدم 2034 للمملكة العربية السعودية؟',
'ما الاختصار الشائع لكأس العالم للرياضات الإلكترونية؟',
'أي مدينة سعودية تستضيف كأس العالم للرياضات الإلكترونية؟',
'ما نوع المنافسة التي يمثلها كأس العالم للرياضات الإلكترونية؟',
'ما خطة التنمية السعودية المرتبطة بالمشاريع الكبرى ونمو الرياضة والترفيه؟',
'ما هي نيوم؟',
'أي مدينة سعودية هي العاصمة وتستضيف العديد من الفعاليات الرياضية والرياضات الإلكترونية الدولية؟'
];
const arabicAnswers=[
 ['23 سبتمبر','1 يناير','22 فبراير','30 نوفمبر'],['جدة','الرياض','مكة المكرمة','الدمام'],['أزرق وأبيض','أحمر وذهبي','أخضر وأبيض','أسود وأصفر'],['البحر','آل سعود','جبل','زهرة'],['المملكة العربية السعودية','مملكة البحرين','الإمارات العربية المتحدة','المملكة الهاشمية'],['1902','1932','1945','1953'],['نخلة','صقر','سيف','نجمة'],['العربية','الإنجليزية','الأردية','الفرنسية'],['دينار','ريال','درهم','جنيه'],['الطائف','المدينة المنورة','مكة المكرمة','أبها'],['الملك عبدالعزيز بن سعود','الملك فيصل','الملك خالد','الملك عبدالله'],['الله أكبر','لا إله إلا الله محمد رسول الله','السلام والازدهار','عاشت المملكة'],['الجمل','المها العربي','الصقر','الحصان'],['بحر العرب','البحر الأحمر','البحر المتوسط','البحر الأسود'],['خليج عُمان','الخليج العربي','خليج عدن','خليج السويس'],['الرياض','جدة','مكة المكرمة','المدينة المنورة'],['جنوب شرق آسيا','الشرق الأوسط','شمال أفريقيا','وسط أوروبا'],['طيران الإمارات','الخطوط الجوية القطرية','الخطوط السعودية','طيران الخليج'],['الصحراء الكبرى','الربع الخالي','صحراء جوبي','صحراء أتاكاما'],['الربع الفارغ','الصحراء الذهبية','الكثبان الكبرى','الرمال الصامتة'],['الرياض','جدة','الدمام','تبوك'],['نخلة التمر','شجرة الزيتون','شجرة الأكاسيا','النخيل'],['الحج','ديوالي','عيد الفصح','النوروز'],['القهوة','الشاي','الإسبريسو','الموكا'],['جبل أحد','جبل النور','جبل سيناء','جبل الأخضر'],['منطقة الرياض','منطقة مكة المكرمة','المنطقة الشرقية','منطقة الحدود الشمالية'],['نيوم','مدينة مصدر','خط القاهرة','مدينة الحرير'],['العرضة','الدبكة','السامبا','الهاكا'],
['المملكة العربية السعودية','قطر','المغرب','الإمارات العربية المتحدة'],
['السعودية وقطر والإمارات','إسبانيا والبرتغال والمغرب','فرنسا وإيطاليا وألمانيا','البرازيل والأرجنتين وتشيلي'],
['البرازيل وتشيلي وبيرو','كولومبيا والإكوادور وبوليفيا','أوروغواي والأرجنتين وباراغواي','المكسيك والولايات المتحدة وكندا'],
['الاحتفال بمرور 50 عاماً على كأس العالم','الاحتفال بمرور 100 عام على أول كأس عالم','أول كأس عالم في آسيا','أول كأس عالم بمشاركة 16 منتخباً'],
['مدينة واحدة فقط','عدة مدن في المملكة العربية السعودية','الرياض وجدة فقط','المدن الساحلية فقط'],
['استضافة المملكة العربية السعودية لكأس العالم لكرة القدم','استضافة المملكة للألعاب الأولمبية','استضافة المملكة لدورة الألعاب الآسيوية لأول مرة','استضافة المملكة لكأس العالم 2030'],
['EWC','EFC','ESC','EWCup'],
['الرياض','جدة','الدمام','المدينة المنورة'],
['بطولة كرة قدم فقط','منافسة للرياضات الإلكترونية متعددة الألعاب','بطولة لرياضة السيارات','بطولة للتنس'],
['رؤية السعودية 2030','رؤية 2020','خطة السعودية 2040','المملكة 2050'],
['مشروع تطوير في المملكة العربية السعودية','نادٍ لكرة القدم','شركة طيران وطنية','فريق للرياضات الإلكترونية'],
['الرياض','الطائف','تبوك','جازان']
];
let index=0,score=0,answersGiven=[],arabic=false;
let quizIndices=[];
function makeQuiz(){
  quizIndices=[...Array(questions.length).keys()].sort(()=>Math.random()-0.5).slice(0,10);
}
const q=document.getElementById('question'), answers=document.getElementById('answers'), next=document.getElementById('next');
function show(){let qi=quizIndices[index];q.textContent=arabic?`${arabicQuestions[qi]}\n${questions[qi].q}`:`${questions[qi].q}\n${arabicQuestions[qi]}`;q.style.whiteSpace='pre-line';answers.innerHTML='';next.style.display='none';questions[qi].a.forEach((text,i)=>{let b=document.createElement('button');b.textContent=arabic?`${arabicAnswers[qi][i]} — ${text}`:`${text} — ${arabicAnswers[qi][i]}`;b.onclick=()=>answer(b,i);answers.appendChild(b)});}
function answer(button,i){let qi=quizIndices[index],x=questions[qi];[...answers.children].forEach(b=>b.disabled=true);answersGiven[index]=i;if(i===x.c){button.classList.add('correct');score++;}else{button.classList.add('wrong');answers.children[x.c].classList.add('correct')}document.getElementById('score').textContent=`Score: ${score}`;setTimeout(()=>{index++;if(index<quizIndices.length)show();else finish()},700);}
function finish(){q.textContent=arabic?`اكتمل الاختبار! نتيجتك ${score}/${quizIndices.length}.\nQuiz complete! You scored ${score}/${quizIndices.length}.`:`Quiz complete! You scored ${score}/${quizIndices.length}.\nاكتمل الاختبار! نتيجتك ${score}/${quizIndices.length}.`;answers.innerHTML='<h2>Check your answers | راجع إجاباتك</h2>';quizIndices.forEach((qi,i)=>{let x=questions[qi],item=document.createElement('div');item.style.cssText='text-align:left;background:#fff;color:#063b2b;padding:12px;border-radius:8px;margin:8px 0';let chosen=answersGiven[i];item.innerHTML=`<strong>${i+1}. ${x.q}<br>${arabicQuestions[qi]}</strong><br>Your answer | إجابتك: ${chosen===undefined?'No answer | لا توجد إجابة':`${chosen+1}. ${x.a[chosen]} — ${arabicAnswers[qi][chosen]}`}<br>Correct answer | الإجابة الصحيحة: ${x.c+1}. ${x.a[x.c]} — ${arabicAnswers[qi][x.c]}`;item.style.borderLeft=`6px solid ${chosen===x.c?'#35a866':'#d9534f'}`;answers.appendChild(item)});next.textContent='Play again | العب مرة أخرى';next.style.display='inline-block';next.onclick=()=>{index=0;score=0;answersGiven=[];makeQuiz();document.getElementById('score').textContent='Score: 0 | النتيجة: 0';next.textContent='Next question | السؤال التالي';show()};}
makeQuiz();
show();
</script></body></html>'''


# Set QUIZ_PUBLIC_URL to your public quiz URL when hosting it online.
PUBLIC_URL = "https://saudi-national-day-quiz.onrender.com/"


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