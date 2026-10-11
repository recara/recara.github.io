from pathlib import Path
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT
from pypdf import PdfReader
r=Path(__file__).resolve().parents[1]
for name,file in [('Arial','Arial.ttf'),('ArialBold','Arial Bold.ttf'),('Georgia','Georgia.ttf')]:pdfmetrics.registerFont(TTFont(name,'/System/Library/Fonts/Supplemental/'+file))
pdfmetrics.registerFontFamily('Arial',normal='Arial',bold='ArialBold',italic='Arial',boldItalic='ArialBold')
ink=colors.HexColor('#172334'); muted=colors.HexColor('#506071'); accent=colors.HexColor('#2344af')
styles={
 'name':ParagraphStyle('name',fontName='Georgia',fontSize=25,leading=30,textColor=ink,spaceAfter=7),
 'role':ParagraphStyle('role',fontName='ArialBold',fontSize=12,leading=16,textColor=ink,spaceAfter=8),
 'meta':ParagraphStyle('meta',fontName='Arial',fontSize=9,leading=13,textColor=muted,spaceAfter=10),
 'h':ParagraphStyle('h',fontName='ArialBold',fontSize=13,leading=17,textColor=accent,spaceBefore=14,spaceAfter=7,keepWithNext=True),
 'sub':ParagraphStyle('sub',fontName='ArialBold',fontSize=10.5,leading=14,textColor=ink,spaceBefore=8,spaceAfter=5,keepWithNext=True),
 'p':ParagraphStyle('p',fontName='Arial',fontSize=10,leading=14.5,textColor=ink,spaceAfter=5),
 'bullet':ParagraphStyle('bullet',fontName='Arial',fontSize=10,leading=14,textColor=ink,leftIndent=10,firstLineIndent=-10,spaceAfter=4),
}
sections=[];md=[]
def add(text,style='p'):
 sections.append(Paragraph(text,styles[style]));md.append(replace_tags(text))
def replace_tags(t):
 import re
 return re.sub('<[^>]+>','',t).replace('&amp;','&')
def bullet(t):add('- '+t,'bullet')
# Preserve readable line breaks in editable content.
def replace_tags(t):
 import re
 t=re.sub(r'<br\s*/?>','\n',t)
 return re.sub('<[^>]+>','',t).replace('&amp;','&')
add('Гнеушев Данил Анатольевич','name')
add('Data Scientist Intern / Python-разработчик','role')
add('Владивосток · <link href="https://github.com/recara" color="#2344af">GitHub: github.com/recara</link> · <link href="https://t.me/byUnleash" color="#2344af">Telegram: @byUnleash</link><br/>Портфолио: <link href="https://recara.github.io/" color="#2344af">https://recara.github.io/</link>','meta')
add('Профиль','h')
add('Ищу стажировку в Data Science / Risk&amp;Research. Студент 2-го курса ДВФУ; могу работать 30 часов в неделю. Практика: табличный ML, feature engineering и проверка моделей, NLP/эмбеддинги и RAG. Разрабатываю коммерческий прогноз закупок для ресторанов «Токио» и сервисы видеоаналитики. Есть антифрод-кейс на банковских транзакциях и научная публикация об AI-интервьюере.')
add('Образование','h')
add('ДВФУ · Программная инженерия, бакалавриат. 2-й курс, очная форма обучения.<br/>Доступность для стажировки: 30 часов в неделю.')
add('Технологии и методы','h')
add('<b>Python и данные:</b> pandas, NumPy, SQL, DuckDB, PostgreSQL, SQLite, CSV/Parquet, Jupyter.<br/><b>Табличный ML:</b> scikit-learn, CatBoost, HistGradientBoosting; feature engineering, временные признаки, бэктесты, GroupKFold, WAPE/bias. LightGBM, XGBoost, Optuna, SHAP.<br/><b>Computer vision / DL:</b> PyTorch (эксперименты), предобученные YOLO/Ultralytics, ByteTrack, OpenCV; обработка видео, трекинг, пересечения линий.<br/><b>Текст / NLP и AI:</b> sentence-transformers, эмбеддинги, HDBSCAN, Ollama, RAG, pgvector, интеграции LLM.<br/><b>Сервисы:</b> FastAPI, aiogram, REST API, Git, pytest, Docker, Linux; React/TypeScript для интерфейсов.')
add('Опыт работы','h')
add('Коммерческие проекты · прикладной ML и CV','sub')
bullet('<b>Рестораны «Токио» / Forecast:</b> расчёт спроса и закупок по точкам и товарам, временные признаки и HGB/CatBoost, ограничения поставки, ручные корректировки и Excel-заявки.')
bullet('<b>Видеоаналитика / TrafficVision и CameraFlow:</b> детекция и трекинг, правила подсчёта проездов, событийное хранение, фоновая обработка и интерфейс проверки результата.')
add('DA | Studio · Backend / Support Engineer','sub')
add('Сентябрь 2025 - настоящее время','meta')
bullet('Сопровождение коммерческих систем: диагностика обмена с 1С, цен и остатков, разбор инцидентов по логам, проверка импорта и товарных фидов. Bitrix, WordPress, PHP, Linux.')
add('Другой коммерческий опыт','sub')
add('PAOLA - WordPress/WooCommerce; ВИК - поддержка сайта; avt.25 - разработка на OpenCart; «Антарктида» - доработки по 152-ФЗ; palletorgdv - обновление дизайна сайта.','meta')
add('Конкурсы и достижения','h')
add('Победитель регионального и заключительного этапов «Национального Достояния России», информатика. 4 место - «Сириус. ИИ», BioCAD. Финалист MTS True Tech («Алгоритмы»), полуфиналист Deadline / Т1 Гении.','p')
sections.append(PageBreak());md.append('\n---\n')
add('Проекты и исследование','name')
add('Технические кейсы: <link href="https://recara.github.io/#work" color="#2344af">recara.github.io/#work</link>. Приватные исходники могут быть предоставлены по согласованию.','meta')
def case(title,body,stack):
 sections.append(KeepTogether([Paragraph(title,styles['sub']),Paragraph(body,styles['p']),Paragraph(stack,styles['meta'])]));md.extend([title,body,stack])
case('Data Fusion 2026 · антифрод на банковских транзакциях','Задача «Страж»: признаки для классификации операций, GroupKFold, LightGBM и CatBoost. Эксперименты с нейросетью и ансамблем; оценка PR-AUC. Репозиторий: <link href="https://github.com/recara/data-fusion-contest-2026" color="#2344af">github.com/recara/data-fusion-contest-2026</link>.','Python · pandas · LightGBM · CatBoost · PyTorch.')
case('Forecast · прогноз закупок для сети ресторанов «Токио»','Подготовка истории продаж по точкам и SKU, временные признаки, расчёты HGB/CatBoost и рекомендации на D+2, D+3, D+4. Бэктесты и метрики WAPE/bias; ограничения поставки и ручная корректировка заявки. Результат - сервис планирования с экспортом Excel.','Python · pandas · CatBoost · HGB · FastAPI. Публичное демо на синтетических данных.')
case('TrafficVision / CameraFlow · коммерческая видеоаналитика','Проект для кофейной точки: отдельный учёт проездов через обслуживание и дорожного объезда. Сервис анализа видео: загрузка записи, настройка линии и два направления подсчёта. Детекция/трекинг, независимая фоновая обработка, SQLite, события, размеченное видео и CSV.','Python · YOLO · ByteTrack · OpenCV · FastAPI · SQLite · React/TypeScript.')
case('Inventory · подготовка данных и разбор инвентаризаций','ETL/OData-контекст в DuckDB, сверка учётных остатков и пересчёта, выделение строк для проверки. API решений сотрудников, журнал, аналитика по точкам и Excel/CSV-выгрузки.','Python · FastAPI · DuckDB · SQL · OData.')
case('NLP / RAG · AI-бот и SEO-кластеризация','Ассистент с локальной LLM и retrieval-augmented generation (RAG): поиск контекста для ответа. Группировка поисковых запросов по смыслу: мультиязычные эмбеддинги и HDBSCAN.','Python · Ollama · PostgreSQL/pgvector · sentence-transformers · HDBSCAN.')
case('E-CUP 2025 / YOLOv8 segmentation','Рекомендательный baseline на данных Ozon: популярность, свежесть и сезонность, исключение просмотренных товаров, top-100. CV-эксперименты: обучение, валидация и инференс YOLOv8; подготовка COCO-аннотаций.','Python · NumPy · pandas · PyArrow · Parquet · YOLOv8.')
add('Научная публикация','h')
add('<link href="https://kmu.itmo.ru/digests/article/16567" color="#2344af">ИИ-интервьюер для технических собеседований с системой прокторинга · kmu.itmo.ru/digests/article/16567</link>.')
def footer(c,doc):
 c.setStrokeColor(colors.HexColor('#dce2e8'));c.line(42,37,553,37);c.setFont('Arial',8);c.setFillColor(muted);c.drawString(42,23,'Данил Гнеушев · Data Science / Python · октябрь 2026');c.drawRightString(553,23,f'{doc.page} / 2')
SimpleDocTemplate(str(r/'resume.pdf'),pagesize=(595.276,841.89),rightMargin=42,leftMargin=42,topMargin=35,bottomMargin=47,title='Данил Гнеушев - Data Scientist / Python',author='Данил Гнеушев').build(sections,onFirstPage=footer,onLaterPages=footer)
(r/'resume.md').write_text('\n\n'.join(md)+'\n')
reader=PdfReader(r/'resume.pdf');print('Pages:',len(reader.pages));assert len(reader.pages)==2
text='\n'.join(p.extract_text() for p in reader.pages)
for n in ['Токио','palletorgdv','GroupKFold','Forecast','эмбеддинги','30 часов','SQL','RAG']:assert n in text
