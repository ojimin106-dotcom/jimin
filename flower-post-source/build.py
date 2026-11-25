# -*- coding: utf-8 -*-
"""꽃말 우체국 정적 사이트 생성기 — python3 build.py 로 dist/ 를 다시 만듭니다."""
import json, os, html

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, '..', 'dist')
SITE_URL = 'https://ojimin106-dotcom.github.io/jimin/'

# ---------------------------------------------------------------- 데이터
PRODUCTS = [
    {
        'id': 'letter', 'name': '편지 + 꽃 1~2송이', 'short': '한 송이 편지', 'price': 19000,
        'img': 'assets/img/letter-flowers.svg', 'alt': '실링 왁스로 봉인한 편지 위에 빨간 장미와 리시안셔스를 올린 그림',
        'summary': '직접 쓴 편지에 꽃말 꽃 한두 송이를 곁들이는 가장 가벼운 구성이에요.',
        'includes': ['보내주신 편지 1통', '꽃말 꽃 1~2송이 (마음에 맞춰 선택)', '와인색 실링 왁스 봉인 봉투', '꽃 이름과 꽃말을 적은 꽃말 카드'],
        'good': ['기념일이 아닌 평범한 날의 고마움', '짧게라도 꼭 전하고 싶은 한마디', '처음 꽃을 선물해 보는 분'],
    },
    {
        'id': 'mini', 'name': '편지 + 미니 꽃다발', 'short': '미니 꽃다발', 'price': 35000,
        'img': 'assets/img/bouquet-friend.png', 'alt': '수국과 데이지, 물망초로 엮은 미니 꽃다발 그림',
        'summary': '꽃말 꽃 세 종류를 작게 엮어, 편지와 함께 손에 쥐기 좋은 크기로 보내드려요.',
        'includes': ['보내주신 편지 1통', '꽃말 꽃 3종 미니 꽃다발', '실링 왁스 봉인 봉투', '꽃말 카드'],
        'good': ['친구와의 화해, 응원의 메시지', '책상 위에 두기 좋은 작은 선물', '주인공 꽃 + 곁들임 꽃 조합을 원하는 분'],
    },
    {
        'id': 'bouquet', 'name': '편지 + 꽃다발', 'short': '꽃다발', 'price': 52000,
        'img': 'assets/img/bouquet-lover.png', 'alt': '리시안셔스와 빨간 장미로 만든 꽃다발 그림',
        'summary': '주인공·곁들임·채움 꽃을 풍성하게 담아, 매장에서 직접 엮은 꽃다발과 편지를 함께 보내요.',
        'includes': ['보내주신 편지 1통', '주인공·곁들임·채움 꽃으로 엮은 꽃다발', '실링 왁스 봉인 봉투', '꽃말 카드', '생화 보호 포장'],
        'good': ['고백, 기념일, 프러포즈', '부모님·선생님께 드리는 감사', '오래 기억에 남을 선물'],
    },
]
SHIPPING = 4000

FLOWERS = [
    {'id': 'lisianthus', 'name': '리시안셔스', 'en': 'Lisianthus', 'meaning': '변치 않는 사랑', 'role': '주인공 꽃', 'source': '10월의 꽃 · 농림축산식품부 자료',
     'color': '#B79BD6', 'center': '#F2E4A6', 'petals': 8,
     'desc': '장미를 닮은 여러 겹의 꽃잎이 부드럽게 겹쳐 피어요. 화려하기보다 단정한 분위기라 어떤 꽃과도 잘 어울립니다.',
     'when': ['오래 만난 연인에게', '결혼기념일', '변함없는 우정을 전할 때'], 'theme': 'love'},
    {'id': 'freesia', 'name': '프리지아', 'en': 'Freesia', 'meaning': '순진 · 천진난만', 'role': '곁들임 꽃', 'source': '2월의 꽃 · 농림축산식품부 자료',
     'color': '#F2C94C', 'center': '#E2A72E', 'petals': 6,
     'desc': '맑은 노란빛과 은은한 향이 봄을 먼저 알리는 꽃이에요. 졸업과 입학 시즌에 특히 많이 찾아요.',
     'when': ['졸업 · 입학 축하', '새로운 시작을 응원할 때', '설레는 첫 고백'], 'theme': 'flutter'},
    {'id': 'rose', 'name': '빨간 장미', 'en': 'Red Rose', 'meaning': '열렬한 사랑 · 사랑의 고백', 'role': '주인공 꽃', 'source': '일반적으로 알려진 꽃말',
     'color': '#B3263A', 'center': '#7E1626', 'petals': 10,
     'desc': '사랑을 말할 때 가장 먼저 떠오르는 꽃이에요. 한 송이만으로도 마음이 충분히 전해집니다.',
     'when': ['고백', '기념일', '프러포즈'], 'theme': 'love'},
    {'id': 'carnation', 'name': '빨간 카네이션', 'en': 'Red Carnation', 'meaning': '어버이에 대한 사랑 · 존경', 'role': '주인공 꽃', 'source': '일반적으로 알려진 꽃말',
     'color': '#C8324A', 'center': '#9B1F35', 'petals': 12,
     'desc': '가장자리가 톱니처럼 갈라진 꽃잎이 특징이에요. 어버이날과 스승의날에 감사를 전하는 대표 꽃입니다.',
     'when': ['어버이날', '스승의날', '부모님 생신'], 'theme': 'thanks'},
    {'id': 'hydrangea', 'name': '수국', 'en': 'Hydrangea', 'meaning': '진심', 'role': '주인공 꽃', 'source': '일반적으로 알려진 꽃말',
     'color': '#8FA8D8', 'center': '#C9D6F0', 'petals': 4,
     'desc': '작은 꽃들이 모여 하나의 둥근 꽃송이를 이뤄요. 자라는 흙의 성질에 따라 꽃 색이 달라지기도 합니다.',
     'when': ['사과하고 싶을 때', '진심을 꼭 전하고 싶을 때', '부모님께 감사'], 'theme': 'sorry'},
    {'id': 'marigold', 'name': '메리골드', 'en': 'Marigold', 'meaning': '반드시 오고야 말 행복', 'role': '곁들임 꽃', 'source': '일반적으로 알려진 꽃말',
     'color': '#E8892B', 'center': '#B8601A', 'petals': 14,
     'desc': '주황과 노랑의 따뜻한 색이 눈에 띄는 꽃이에요. 힘든 시간을 보내는 사람에게 건네는 응원으로 잘 어울려요.',
     'when': ['시험 · 취업 응원', '힘든 시기를 지나는 친구에게', '새해 인사'], 'theme': 'cheer'},
    {'id': 'delphinium', 'name': '델피니움', 'en': 'Delphinium', 'meaning': '당신을 행복하게 해줄게요', 'role': '곁들임 꽃', 'source': '일반적으로 알려진 꽃말',
     'color': '#4F6FB8', 'center': '#E9EEF8', 'petals': 5,
     'desc': '긴 꽃대를 따라 푸른 꽃이 층층이 피어요. 꽃다발에 높이와 시원한 색감을 더해 줍니다.',
     'when': ['연인에게 하는 약속', '응원의 메시지', '여름 꽃다발'], 'theme': 'cheer'},
    {'id': 'forgetmenot', 'name': '물망초', 'en': 'Forget-me-not', 'meaning': '나를 잊지 마세요', 'role': '채움 꽃', 'source': '일반적으로 알려진 꽃말',
     'color': '#7DA7E0', 'center': '#F2D35B', 'petals': 5,
     'desc': '작고 파란 꽃잎 가운데 노란 점이 있는 꽃이에요. 꽃다발 사이사이를 채워 섬세한 느낌을 더해요.',
     'when': ['멀리 떠나는 친구에게', '오래 기억되고 싶을 때', '화해의 편지'], 'theme': 'sorry'},
    {'id': 'statice', 'name': '스타티스', 'en': 'Statice', 'meaning': '변치 않는 마음', 'role': '채움 꽃', 'source': '일반적으로 알려진 꽃말',
     'color': '#9B7BC4', 'center': '#F4F0F8', 'petals': 6,
     'desc': '말려도 색이 오래 남아 드라이플라워로도 사랑받아요. 받은 꽃다발을 오래 간직하고 싶을 때 좋아요.',
     'when': ['오래 간직할 선물', '연인에게', '기념일'], 'theme': 'love'},
    {'id': 'daisy', 'name': '데이지', 'en': 'Daisy', 'meaning': '희망 · 순수', 'role': '곁들임 꽃', 'source': '일반적으로 알려진 꽃말',
     'color': '#FFFFFF', 'center': '#F2C94C', 'petals': 16,
     'desc': '하얀 꽃잎과 노란 꽃술이 맑고 귀여운 인상을 줘요. 친구에게 가볍게 마음을 전하기 좋아요.',
     'when': ['친구와의 화해', '새 출발 응원', '가벼운 안부'], 'theme': 'cheer'},
    {'id': 'cotton', 'name': '목화', 'en': 'Cotton', 'meaning': '어머니의 사랑', 'role': '채움 꽃', 'source': '일반적으로 알려진 꽃말',
     'color': '#F4EFE6', 'center': '#8A6A55', 'petals': 5,
     'desc': '포근한 솜뭉치 모양으로, 오래 두어도 모양이 변하지 않아요. 따뜻한 겨울 꽃다발에 자주 쓰여요.',
     'when': ['어머니께', '겨울 선물', '집들이'], 'theme': 'thanks'},
]
FL = {f['id']: f for f in FLOWERS}

THEMES = [
    {'id': 'love', 'label': '사랑', 'flowers': ['lisianthus', 'rose', 'statice']},
    {'id': 'thanks', 'label': '감사', 'flowers': ['carnation', 'hydrangea', 'cotton']},
    {'id': 'sorry', 'label': '사과 · 진심', 'flowers': ['hydrangea', 'daisy', 'forgetmenot']},
    {'id': 'cheer', 'label': '응원', 'flowers': ['marigold', 'delphinium', 'daisy']},
    {'id': 'flutter', 'label': '설렘', 'flowers': ['freesia', 'lisianthus', 'statice']},
]
TH = {t['id']: t for t in THEMES}

RECIPIENTS = [
    {'id': 'lover', 'label': '연인'}, {'id': 'friend', 'label': '친구'}, {'id': 'family', 'label': '가족'},
    {'id': 'teacher', 'label': '선생님'}, {'id': 'me', 'label': '나에게'},
]

GIFTS = [
    {'id': 'lover', 'to': '연인에게', 'msg': '앞으로도 변함없이 사랑해', 'img': 'assets/img/bouquet-lover.png',
     'flowers': ['lisianthus', 'rose', 'statice'], 'theme': 'love', 'recipient': 'lover', 'product': 'bouquet',
     'story': '오래 함께한 사람에게는 화려한 말보다 변하지 않겠다는 약속이 더 크게 들려요. 리시안셔스의 "변치 않는 사랑"을 주인공으로, 빨간 장미로 마음의 온도를 더하고 스타티스로 오래 남는 여운을 채웠어요.',
     'tips': ['편지 첫 줄에 처음 만난 날을 적어 보세요.', '꽃다발 구성을 추천해요. 한 송이 편지로도 충분히 전해져요.', '기념일 이틀 전까지 주문하면 여유롭게 받을 수 있어요.']},
    {'id': 'mom', 'to': '엄마에게', 'msg': '엄마 키워줘서 고마워요', 'img': 'assets/img/bouquet-mom.png',
     'flowers': ['carnation', 'hydrangea', 'cotton'], 'theme': 'thanks', 'recipient': 'family', 'product': 'bouquet',
     'story': '쑥스러워서 미뤄 둔 "고마워요"를 꽃말로 대신 전해요. 빨간 카네이션의 존경, 수국의 진심, 목화의 "어머니의 사랑"을 한 다발에 담았어요.',
     'tips': ['어버이날이 아니어도 좋아요. 평범한 날의 꽃이 더 오래 기억돼요.', '매장 픽업을 선택하면 직접 들고 찾아갈 수 있어요.', '편지에는 구체적인 추억 하나를 적어 보세요.']},
    {'id': 'friend', 'to': '친구에게', 'msg': '미안해, 오해였어. 진심이야', 'img': 'assets/img/bouquet-friend.png',
     'flowers': ['hydrangea', 'daisy', 'forgetmenot'], 'theme': 'sorry', 'recipient': 'friend', 'product': 'mini',
     'story': '말로 꺼내기 어려운 사과는 꽃이 먼저 문을 두드려 줘요. 수국의 진심, 데이지의 희망, 물망초의 "나를 잊지 마세요"로 다시 가까워지고 싶은 마음을 전해요.',
     'tips': ['미니 꽃다발이 부담 없이 건네기 좋아요.', '편지는 길지 않아도 괜찮아요. 진심 한 문장이면 돼요.', '받는 분 주소를 모르면 매장 픽업 후 직접 전해 주세요.']},
]

SHORTS = [
    {'no': 1, 'title': '훅 · 브랜드 소개', 'line': '말로 하기 쑥스러운 진심, 꽃말에 담아 대신 전해드립니다', 'file': 'media/short-1.mp4'},
    {'no': 2, 'title': '꽃말 소개 · 리시안셔스', 'line': '‘변치 않는 사랑’을 전하고 싶다면 리시안셔스를 편지에 곁들여 보세요', 'file': 'media/short-2.mp4'},
    {'no': 3, 'title': '참여 유도 · 주문', 'line': '누구에게 마음을 전하고 싶으신가요? 지금 사연을 보내주세요', 'file': 'media/short-3.mp4'},
]

NAV = [
    ('home', 'index.html', '홈'),
    ('about', 'about.html', '브랜드 이야기'),
    ('how', 'how.html', '이용 안내'),
    ('shop', 'shop.html', '상품'),
    ('gift', 'gift.html', '선물 가이드'),
    ('flowers', 'flowers.html', '꽃말 사전'),
    ('media', 'media.html', '홍보 영상'),
]

e = html.escape
def won(n): return f'{n:,}원'

# ---------------------------------------------------------------- 그림
def flower_svg(f, label=True):
    """꽃잎 수와 색으로 그린 단순한 꽃 그림"""
    n = f['petals']; c = f['color']; stroke = '#6B2C3B' if c.upper() in ('#FFFFFF', '#F4EFE6') else 'none'
    petals = ''.join(
        f'<ellipse cx="50" cy="30" rx="{max(6, 40 // n + 5)}" ry="20" fill="{c}" stroke="{stroke}" stroke-width="1" transform="rotate({i * 360 / n:.1f} 50 50)"/>'
        for i in range(n))
    aria = f'role="img" aria-label="{e(f["name"])} 그림"' if label else 'aria-hidden="true"'
    return (f'<svg viewBox="0 0 100 100" {aria}>'
            f'<circle cx="50" cy="50" r="48" fill="#F5E3E0"/>{petals}'
            f'<circle cx="50" cy="50" r="11" fill="{f["center"]}"/></svg>')

ICON = {
    'flower': '<svg viewBox="0 0 24 24" fill="none" stroke="#6B2C3B" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><path d="M12 13c-2-3-6-3-6 0s4 3 6 0zm0 0c2-3 6-3 6 0s-4 3-6 0zm0 0c-3-2-3-6 0-6s3 4 0 6zm0 0v8"/></svg>',
    'letter': '<svg viewBox="0 0 24 24" fill="none" stroke="#6B2C3B" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="6" width="18" height="13" rx="1.5"/><path d="M3 7l9 6 9-6"/><circle cx="12" cy="14" r="2.2" fill="#6B2C3B"/></svg>',
    'box': '<svg viewBox="0 0 24 24" fill="none" stroke="#6B2C3B" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><path d="M3 8l9-4 9 4v8l-9 4-9-4z"/><path d="M3 8l9 4 9-4M12 12v8"/></svg>',
    'store': '<svg viewBox="0 0 24 24" fill="none" stroke="#6B2C3B" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><path d="M4 10h16v10H4z"/><path d="M3 10l2-6h14l2 6"/><path d="M10 20v-5h4v5"/></svg>',
    'play': '<svg width="26" height="26" viewBox="0 0 24 24" fill="#FFFDFA" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>',
    'check': '<svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="#FFFDFA" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>',
    'x': '<svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="#FFFDFA" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>',
}

# ---------------------------------------------------------------- 레이아웃
def page(fname, title, active, body, desc='말로 하기 쑥스러운 진심, 꽃말에 담아 대신 전해드립니다.', head_extra='', scripts='', body_class=''):
    nav = ''.join(
        f'<li><a href="{href}"{" aria-current=\"page\"" if key == active else ""}>{label}</a></li>'
        for key, href, label in NAV)
    doc = f'''<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="assets/img/logo.png">
<link rel="icon" href="assets/img/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=Noto+Sans+KR:wght@400;500;700&display=swap">
<link rel="stylesheet" href="assets/css/style.css">
{head_extra}
</head>
<body class="{body_class}">
<a class="skip" href="#main">본문 바로가기</a>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="index.html"><img src="assets/img/logo.png" alt=""><span>꽃말 우체국</span></a>
    <nav class="nav" aria-label="주요 메뉴"><ul>{nav}</ul></nav>
    <div class="header-cta"><a class="btn sm" href="checkout.html"{" aria-current=\"page\"" if active == "checkout" else ""}>주문하기</a></div>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="stack" style="gap:12px">
        <h2>꽃말 우체국 · FLOWER POST</h2>
        <p>직접 쓴 편지와 꽃말을 담은 꽃을 함께 보내는 꽃집이에요.<br>매장: 경기도 안양시 동안구 · 택배 배송 및 매장 픽업</p>
      </div>
      <div>
        <p class="footer-title">둘러보기</p>
        <ul>{''.join(f'<li><a href="{h}">{l}</a></li>' for k, h, l in NAV[1:])}</ul>
      </div>
      <div>
        <p class="footer-title">주문</p>
        <ul>
          <li><a href="checkout.html">바로 주문하기</a></li>
          {''.join(f'<li><a href="product-{p["id"]}.html">{p["name"]}</a></li>' for p in PRODUCTS)}
          <li><a href="how.html#faq">자주 묻는 질문</a></li>
        </ul>
      </div>
    </div>
    <p class="footer-note">수업 과제로 만든 가상 브랜드이며 실제 판매 정보가 아닙니다. 결제는 토스페이먼츠 테스트 환경으로, 실제로 돈이 빠져나가지 않습니다.<br>로고·이미지는 AI(Claude) 생성물입니다 · 꽃말 출처: 시대일보(2014.2.6 / 2014.10.2) 농식품부·농진청 ‘이달의 꽃’ 프리지아·리시안셔스, 그 외는 일반적으로 알려진 꽃말</p>
  </div>
</footer>
<script src="assets/js/data.js"></script>
<script src="assets/js/main.js"></script>
{scripts}
</body>
</html>
'''
    with open(os.path.join(DIST, fname), 'w', encoding='utf-8') as fh:
        fh.write(doc)
    return fname

def head(eyebrow, h, lead='', crumbs=None):
    cr = ''
    if crumbs:
        cr = '<nav class="crumbs" aria-label="현재 위치">' + ' › '.join(
            f'<a href="{h_}">{e(l)}</a>' if h_ else f'<span>{e(l)}</span>' for l, h_ in crumbs) + '</nav>'
    return f'''<section class="page-hero"><div class="wrap">{cr}<div class="stack" style="gap:12px">
<p class="eyebrow">{eyebrow}</p><h1>{h}</h1>{f'<p class="lead">{lead}</p>' if lead else ''}</div></div></section>'''

def product_card(p):
    return f'''<article class="product-card">
<a class="thumb" href="product-{p['id']}.html"><img src="{p['img']}" alt="{e(p['alt'])}" loading="lazy"></a>
<div class="body"><h3>{p['name']}</h3><p class="muted small">{p['summary']}</p><p class="price">{won(p['price'])}</p>
<div class="actions"><a class="btn sm ghost" href="product-{p['id']}.html">자세히</a><a class="btn sm" href="checkout.html?product={p['id']}">바로 주문</a></div></div>
</article>'''

def flower_card(f):
    return f'''<a class="flower-card" href="flower-{f['id']}.html">{flower_svg(f, label=False)}
<span><strong>{f['name']}</strong><span class="meaning">{f['meaning']}</span></span></a>'''

def steps_block():
    items = [
        ('편지 쓰기', '전하고 싶은 마음을 직접 편지로 써 주세요. 매장에 맡기거나 우편으로 보내도, 주문서에 적어도 돼요.'),
        ('꽃 고르기', '편지에 담긴 마음과 어울리는 꽃말의 꽃으로 조합을 골라요.'),
        ('매장에서 제작', '안양 매장에서 꽃을 직접 엮고, 편지를 실링 왁스로 봉인해요.'),
        ('배송 · 픽업', '생화가 상하지 않게 포장해 택배로 보내거나, 매장에서 바로 찾아가요.'),
    ]
    return '<ol class="steps">' + ''.join(
        f'<li><span class="num">STEP {i + 1:02d}</span><strong>{t}</strong><span>{d}</span></li>' for i, (t, d) in enumerate(items)) + '</ol>'

FEATURES = [
    ('flower', '마음을 꽃말로 번역', '편지에 담긴 말과 어울리는 꽃말의 꽃을 골라 곁에 담아요.'),
    ('letter', '직접 쓴 편지를 그대로', '보내주신 편지를 와인색 실링 왁스로 한 통씩 봉인해 동봉해요.'),
    ('store', '매장에서 직접 만든 꽃', '안양 매장에서 꽃을 엮어 택배로 보내거나, 매장 픽업도 가능해요.'),
]
def features_block():
    return '<div class="grid c3">' + ''.join(
        f'<div class="card"><div class="icon-circle">{ICON[i]}</div><h3>{t}</h3><p class="muted">{d}</p></div>' for i, t, d in FEATURES) + '</div>'

# ---------------------------------------------------------------- 페이지
def build():
    os.makedirs(DIST, exist_ok=True)
    pages = []

    # data.js
    data = {
        'products': [{k: p[k] for k in ('id', 'name', 'short', 'price', 'img', 'alt')} for p in PRODUCTS],
        'shipping': SHIPPING,
        'themes': [{'id': t['id'], 'label': t['label'], 'flowers': [FL[x]['name'] for x in t['flowers']],
                    'meanings': [FL[x]['meaning'] for x in t['flowers']]} for t in THEMES],
        'recipients': RECIPIENTS,
        'flowers': {f['id']: f['name'] for f in FLOWERS},
        'siteUrl': SITE_URL,
    }
    with open(os.path.join(DIST, 'assets/js/data.js'), 'w', encoding='utf-8') as fh:
        fh.write('window.FP = ' + json.dumps(data, ensure_ascii=False, indent=1) + ';\n')

    # ---- 홈
    theme_links = ''.join(f'<a class="chip" href="checkout.html?theme={t["id"]}">{t["label"]}</a>' for t in THEMES)
    gifts = ''.join(f'''<a class="product-card" href="gift-{g['id']}.html" style="text-decoration:none;color:inherit">
<span class="thumb"><img src="{g['img']}" alt="{e(g['to'])} 보내는 추천 꽃다발 그림" loading="lazy"></span>
<span class="body"><span class="eyebrow">{g['to']}</span><span class="quote" style="font-size:20px">“{g['msg']}”</span>
<span class="muted small">{' · '.join(FL[x]['name'] for x in g['flowers'])}</span></span></a>''' for g in GIFTS)
    body = f'''
<section class="hero"><div class="wrap hero-grid">
  <div class="stack" style="gap:18px">
    <p class="eyebrow">FLOWER POST — ANYANG</p>
    <h1>꽃말 우체국</h1>
    <p class="tagline">말로 하기 쑥스러운 진심,<br>꽃말에 담아 대신 전해드립니다.</p>
    <p class="lead">직접 쓴 편지에 꼭 맞는 꽃말의 꽃을 골라, 매장에서 엮은 꽃과 함께 보내드려요.</p>
    <div class="btn-row" style="margin-top:6px"><a class="btn lg" href="checkout.html">지금 주문하기</a><a class="btn lg ghost" href="media.html">홍보 영상 보기</a></div>
  </div>
  <div class="hero-art" aria-hidden="true"><div class="disc"></div><img src="assets/img/logo.png" alt=""><span class="petal p1"></span><span class="petal p2"></span><span class="petal p3"></span></div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head"><p class="eyebrow">QUICK ORDER</p><h2 class="h-section">어떤 마음을 전하고 싶나요?</h2>
  <p class="lead">마음을 누르면 어울리는 꽃이 담긴 주문서가 바로 열려요.</p></div>
  <div class="chips">{theme_links}</div>
</div></section>

<section class="section" style="padding-top:0"><div class="wrap">
  <div class="section-head row"><div class="stack" style="gap:10px"><p class="eyebrow">PROMOTION FILM</p><h2 class="h-section">30초로 보는 꽃말 우체국</h2></div><a class="btn ghost sm" href="media.html">숏폼 · QR 보기</a></div>
  <div class="video-frame wide"><video controls playsinline preload="metadata" poster="media/promo.jpg" aria-label="꽃말 우체국 홍보 영상"><source src="media/promo.mp4" type="video/mp4"></video></div>
</div></section>

<section class="section white"><div class="wrap">
  <div class="section-head row"><div class="stack" style="gap:10px"><p class="eyebrow">PRODUCTS</p><h2 class="h-section">세 가지 구성</h2></div><a class="btn ghost sm" href="shop.html">상품 전체 보기</a></div>
  <div class="grid c3">{''.join(product_card(p) for p in PRODUCTS)}</div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head"><p class="eyebrow">WHY FLOWER POST</p><h2 class="h-section">꽃말 우체국만의 세 가지</h2></div>
  {features_block()}
</div></section>

<section class="section tint"><div class="wrap">
  <div class="section-head row"><div class="stack" style="gap:10px"><p class="eyebrow">GIFT GUIDE</p><h2 class="h-section">받는 사람마다 다른 꽃다발</h2></div><a class="btn ghost sm" href="gift.html">선물 가이드</a></div>
  <div class="grid c3">{gifts}</div>
</div></section>

<section class="section"><div class="wrap">
  <div class="section-head row"><div class="stack" style="gap:10px"><p class="eyebrow">HOW IT WORKS</p><h2 class="h-section">편지 한 통이 도착하기까지</h2></div><a class="btn ghost sm" href="how.html">이용 안내</a></div>
  {steps_block()}
</div></section>

<section class="section" style="padding-top:0"><div class="wrap">
  <div class="banner"><div class="stack" style="gap:8px"><h2>누구에게 마음을 전하고 싶으신가요?</h2><p>오늘 주문하면 모레부터 받을 수 있어요. 매장 픽업도 가능해요.</p></div>
  <a class="btn light lg" href="checkout.html">꽃 편지 주문하기</a></div>
</div></section>'''
    pages.append(page('index.html', '꽃말 우체국 · FLOWER POST', 'home', body))

    # ---- 브랜드 이야기
    body = head('ABOUT', '꽃이 아니라,<br>편지를 보내는 꽃집', '기념일이 아니어도 마음을 전하고 싶은 사람들을 위한 작은 우체국이에요.') + f'''
<section class="section"><div class="wrap split">
  <div class="stack" style="gap:20px">
    <p class="quote">마음을 꽃말로 번역해<br>편지와 함께 보냅니다.</p>
    <p>연인, 친구, 가족, 선생님, 그리고 나 자신에게. 말로 꺼내기 쑥스러운 진심은 편지에 적어 두면 오래 남아요. 꽃말 우체국은 그 편지에 꼭 맞는 꽃말의 꽃을 골라 함께 보내드립니다.</p>
    <p>편지는 의뢰인이 직접 써요. 우리는 그 편지를 읽고, 어울리는 꽃을 고르고, 안양 매장에서 꽃을 엮어 실링 왁스로 봉인한 편지와 함께 포장합니다.</p>
  </div>
  <div class="figure"><img src="assets/img/logo.png" alt="꽃말 우체국 로고: 편지 봉투에서 피어난 세 송이 꽃"></div>
</div></section>
<section class="section white"><div class="wrap">
  <div class="section-head"><p class="eyebrow">BRAND</p><h2 class="h-section">한눈에 보는 꽃말 우체국</h2></div>
  <dl class="dl">
    <dt>타깃</dt><dd>기념일이 아니어도 마음을 전하고 싶은 사람 (연인 · 친구 · 가족)</dd>
    <dt>차별점</dt><dd>직접 쓴 편지와 어울리는 꽃말의 꽃을 함께 보내는 꽃집</dd>
    <dt>포인트</dt><dd>실링 왁스로 봉인한 편지, 매장에서 직접 엮은 꽃</dd>
    <dt>매장</dt><dd>경기도 안양시 동안구 · 택배 배송과 매장 픽업</dd>
    <dt>한 줄 소개</dt><dd>말로 하기 쑥스러운 진심, 꽃말에 담아</dd>
  </dl>
</div></section>
<section class="section"><div class="wrap">
  <div class="section-head"><p class="eyebrow">WHY FLOWER POST</p><h2 class="h-section">우리가 지키는 세 가지</h2></div>
  {features_block()}
  <div class="btn-row" style="margin-top:32px"><a class="btn" href="checkout.html">주문하기</a><a class="btn ghost" href="flowers.html">꽃말 사전 보기</a></div>
</div></section>'''
    pages.append(page('about.html', '브랜드 이야기 · 꽃말 우체국', 'about', body))

    # ---- 이용 안내
    faqs = [
        ('편지는 어떻게 보내나요?', '세 가지 방법 중 고를 수 있어요. ① 주문서에 편지 내용을 적으면 편지지에 옮겨 동봉해요. ② 직접 쓴 편지를 안양 매장에 맡겨도 되고, ③ 우편으로 보내셔도 돼요. 우편 주소는 주문 완료 후 안내해 드려요.'),
        ('꽃은 제가 고를 수 있나요?', '네. 주문서에서 전하고 싶은 마음을 고르면 추천 조합이 나오고, 꽃말 사전에서 원하는 꽃을 골라 요청할 수도 있어요. 계절에 따라 비슷한 꽃말의 꽃으로 바뀔 수 있어요.'),
        ('언제 받을 수 있나요?', '주문일로부터 2일 뒤부터 원하는 날짜를 고를 수 있어요. 택배는 지정일 전날 발송하고, 매장 픽업은 지정일에 준비해 둬요.'),
        ('배송비는 얼마인가요?', f'택배 배송비는 {won(SHIPPING)}이고, 매장 픽업은 무료예요.'),
        ('취소나 환불이 되나요?', '제작 시작 전에는 전액 취소할 수 있어요. 생화 특성상 제작이 시작된 뒤에는 취소가 어려워요.'),
        ('결제는 어떻게 하나요?', '주문 페이지에서 카드, 간편결제(토스페이 · 카카오페이 등), 계좌이체로 결제할 수 있어요. 이 사이트는 테스트 결제 환경이라 실제로 돈이 빠져나가지 않아요.'),
    ]
    body = head('HOW IT WORKS', '이용 안내', '편지 한 통이 꽃과 함께 도착하기까지의 과정과 배송 · 픽업 안내예요.') + f'''
<section class="section"><div class="wrap">{steps_block()}</div></section>
<section class="section white"><div class="wrap">
  <div class="section-head"><p class="eyebrow">DELIVERY</p><h2 class="h-section">받는 방법</h2></div>
  <div class="grid c2">
    <div class="card"><div class="icon-circle">{ICON['box']}</div><h3>택배 배송</h3><p class="muted">생화가 상하지 않게 단단히 포장해 지정일에 맞춰 보내요. 배송비 {won(SHIPPING)}.</p></div>
    <div class="card"><div class="icon-circle">{ICON['store']}</div><h3>매장 픽업</h3><p class="muted">경기도 안양시 동안구 매장에서 지정일에 찾아가요. 배송비 없음.</p></div>
  </div>
</div></section>
<section class="section" id="faq"><div class="wrap" style="max-width:860px">
  <div class="section-head"><p class="eyebrow">FAQ</p><h2 class="h-section">자주 묻는 질문</h2></div>
  {''.join(f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs)}
  <div class="btn-row" style="margin-top:32px"><a class="btn" href="checkout.html">바로 주문하기</a></div>
</div></section>'''
    pages.append(page('how.html', '이용 안내 · 꽃말 우체국', 'how', body))

    # ---- 상품 목록
    theme_rows = ''.join(
        f'<tr><td><a href="checkout.html?theme={t["id"]}">{t["label"]}</a></td><td>{" · ".join(f"<a href=\"flower-{x}.html\">{FL[x]["name"]}</a>" for x in t["flowers"])}</td><td class="muted">{", ".join(FL[x]["meaning"] for x in t["flowers"])}</td></tr>'
        for t in THEMES)
    body = head('PRODUCTS', '상품', '모든 구성에는 직접 쓴 편지와 실링 왁스 봉투, 꽃말 카드가 함께 들어가요.') + f'''
<section class="section"><div class="wrap"><div class="grid c3">{''.join(product_card(p) for p in PRODUCTS)}</div></div></section>
<section class="section white"><div class="wrap">
  <div class="section-head"><p class="eyebrow">BY FEELING</p><h2 class="h-section">마음별 추천 꽃 조합</h2><p class="lead">마음 이름을 누르면 그 조합으로 주문서가 열려요.</p></div>
  <div class="table-box"><table class="tbl"><thead><tr><th scope="col">마음</th><th scope="col">꽃</th><th scope="col">꽃말</th></tr></thead><tbody>{theme_rows}</tbody></table></div>
</div></section>'''
    pages.append(page('shop.html', '상품 · 꽃말 우체국', 'shop', body))

    # ---- 상품 상세 3
    for p in PRODUCTS:
        others = ''.join(product_card(o) for o in PRODUCTS if o['id'] != p['id'])
        chips = ''.join(f'<a class="chip" href="checkout.html?product={p["id"]}&amp;theme={t["id"]}">{t["label"]}</a>' for t in THEMES)
        body = f'''
<section class="section"><div class="wrap">
  <nav class="crumbs" aria-label="현재 위치"><a href="index.html">홈</a> › <a href="shop.html">상품</a> › <span>{p['name']}</span></nav>
  <div class="split media-left">
    <div class="figure"><img src="{p['img']}" alt="{e(p['alt'])}"></div>
    <div class="stack" style="gap:20px">
      <p class="eyebrow">PRODUCT</p><h1 style="font-size:clamp(32px,4.5vw,46px)">{p['name']}</h1>
      <p class="lead">{p['summary']}</p>
      <p class="price" style="font-size:28px">{won(p['price'])} <span class="muted small" style="font-weight:400">+ 배송비 {won(SHIPPING)} (매장 픽업 무료)</span></p>
      <div class="stack" style="gap:10px"><p style="font-weight:700">마음을 고르면 바로 주문서로 이동해요</p><div class="chips">{chips}</div></div>
      <a class="btn lg block" href="checkout.html?product={p['id']}">이 구성으로 주문하기</a>
    </div>
  </div>
</div></section>
<section class="section white"><div class="wrap grid c2">
  <div class="stack"><h2 style="font-size:26px">구성</h2><ul class="list-check">{''.join(f'<li>{x}</li>' for x in p['includes'])}</ul></div>
  <div class="stack"><h2 style="font-size:26px">이럴 때 좋아요</h2><ul class="list-check">{''.join(f'<li>{x}</li>' for x in p['good'])}</ul></div>
</div></section>
<section class="section"><div class="wrap">
  <div class="section-head"><h2 class="h-section">안내</h2></div>
  <dl class="dl">
    <dt>편지</dt><dd>주문서에 적기 · 매장에 맡기기 · 우편 보내기 중 선택</dd>
    <dt>꽃</dt><dd>고른 마음에 맞춰 매장에서 직접 엮어요. 계절에 따라 같은 꽃말의 다른 꽃으로 바뀔 수 있어요.</dd>
    <dt>받는 날</dt><dd>주문일로부터 2일 뒤부터 지정 가능</dd>
    <dt>취소</dt><dd>제작 시작 전까지 전액 취소 가능</dd>
  </dl>
</div></section>
<section class="section tint"><div class="wrap"><div class="section-head"><h2 class="h-section">다른 구성</h2></div><div class="grid c2">{others}</div></div></section>'''
        pages.append(page(f'product-{p["id"]}.html', f'{p["name"]} · 꽃말 우체국', 'shop', body, desc=p['summary']))

    # ---- 선물 가이드 + 상세 3
    cards = ''.join(f'''<article class="product-card"><a class="thumb" href="gift-{g['id']}.html"><img src="{g['img']}" alt="{e(g['to'])} 보내는 추천 꽃다발 그림" loading="lazy"></a>
<div class="body"><p class="eyebrow">{g['to']}</p><h3>“{g['msg']}”</h3><p class="muted small">{' · '.join(FL[x]['name'] for x in g['flowers'])}</p>
<div class="actions"><a class="btn sm ghost" href="gift-{g['id']}.html">자세히</a><a class="btn sm" href="checkout.html?product={g['product']}&amp;theme={g['theme']}&amp;to={g['recipient']}">이 조합 주문</a></div></div></article>''' for g in GIFTS)
    rec_rows = ''.join(f'<a class="chip" href="checkout.html?to={r["id"]}">{r["label"]}</a>' for r in RECIPIENTS)
    body = head('GIFT GUIDE', '선물 가이드', '받는 사람과 하고 싶은 말에 맞춘 추천 꽃다발이에요.') + f'''
<section class="section"><div class="wrap"><div class="grid c3">{cards}</div></div></section>
<section class="section white"><div class="wrap">
  <div class="section-head"><h2 class="h-section">받는 사람으로 바로 주문</h2></div><div class="chips">{rec_rows}</div>
</div></section>'''
    pages.append(page('gift.html', '선물 가이드 · 꽃말 우체국', 'gift', body))
    for g in GIFTS:
        fl = ''.join(flower_card(FL[x]) for x in g['flowers'])
        order = f'checkout.html?product={g["product"]}&amp;theme={g["theme"]}&amp;to={g["recipient"]}'
        body = f'''
<section class="section"><div class="wrap">
  <nav class="crumbs" aria-label="현재 위치"><a href="index.html">홈</a> › <a href="gift.html">선물 가이드</a> › <span>{g['to']}</span></nav>
  <div class="split media-left">
    <div class="figure"><img src="{g['img']}" alt="{e(g['to'])} 보내는 추천 꽃다발 그림"></div>
    <div class="stack" style="gap:20px">
      <p class="eyebrow">{g['to']}</p><h1 class="quote" style="font-size:clamp(30px,4.5vw,44px)">“{g['msg']}”</h1>
      <p>{g['story']}</p>
      <ul class="list-check">{''.join(f'<li>{t}</li>' for t in g['tips'])}</ul>
      <a class="btn lg block" href="{order}">이 조합으로 주문하기</a>
    </div>
  </div>
</div></section>
<section class="section white"><div class="wrap"><div class="section-head"><h2 class="h-section">이 꽃다발의 꽃</h2></div><div class="grid c3">{fl}</div></div></section>
<section class="section"><div class="wrap"><div class="section-head"><h2 class="h-section">다른 추천</h2></div><div class="btn-row">{''.join(f'<a class="btn ghost" href="gift-{o["id"]}.html">{o["to"]}</a>' for o in GIFTS if o['id'] != g['id'])}</div></div></section>'''
        pages.append(page(f'gift-{g["id"]}.html', f'{g["to"]} 꽃다발 · 꽃말 우체국', 'gift', body, desc=g['story']))

    # ---- 꽃말 사전 + 상세 11
    rows = ''.join(f'<tr><td><a href="flower-{f["id"]}.html">{f["name"]}</a></td><td style="font-family:var(--serif);color:var(--wine)">{f["meaning"]}</td><td class="muted">{f["role"]} · {f["source"]}</td></tr>' for f in FLOWERS)
    body = head('DICTIONARY', '꽃말 사전', '꽃을 누르면 꽃말과 어울리는 상황, 함께 쓰기 좋은 꽃을 볼 수 있어요.') + f'''
<section class="section"><div class="wrap"><div class="grid c3">{''.join(flower_card(f) for f in FLOWERS)}</div></div></section>
<section class="section white"><div class="wrap">
  <div class="section-head"><h2 class="h-section">한눈에 보기</h2></div>
  <div class="table-box"><table class="tbl"><thead><tr><th scope="col">꽃</th><th scope="col">꽃말</th><th scope="col">역할 · 출처</th></tr></thead><tbody>{rows}</tbody></table></div>
  <p class="muted small" style="margin-top:16px">꽃말은 자료마다 조금씩 다를 수 있어요. 리시안셔스와 프리지아는 농림축산식품부 · 농촌진흥청 자료로 확인했고, 나머지는 일반적으로 알려진 꽃말이에요.</p>
</div></section>'''
    pages.append(page('flowers.html', '꽃말 사전 · 꽃말 우체국', 'flowers', body))
    for f in FLOWERS:
        th = TH[f['theme']]
        pals = [FL[x] for x in th['flowers'] if x != f['id']][:2]
        body = f'''
<section class="section"><div class="wrap">
  <nav class="crumbs" aria-label="현재 위치"><a href="index.html">홈</a> › <a href="flowers.html">꽃말 사전</a> › <span>{f['name']}</span></nav>
  <div class="split media-left">
    <div class="flower-art">{flower_svg(f)}</div>
    <div class="stack" style="gap:18px">
      <p class="eyebrow">{f['en']}</p><h1 style="font-size:clamp(34px,5vw,52px)">{f['name']}</h1>
      <p class="quote">“{f['meaning']}”</p>
      <p>{f['desc']}</p>
      <dl class="dl"><dt>꽃다발 역할</dt><dd>{f['role']}</dd><dt>추천 마음</dt><dd>{th['label']}</dd><dt>출처</dt><dd>{f['source']}</dd></dl>
      <a class="btn lg block" href="checkout.html?theme={th['id']}&amp;flower={f['id']}">{f['name']} 넣어서 주문하기</a>
    </div>
  </div>
</div></section>
<section class="section white"><div class="wrap grid c2">
  <div class="stack"><h2 style="font-size:26px">이럴 때 보내요</h2><ul class="list-check">{''.join(f'<li>{w}</li>' for w in f['when'])}</ul></div>
  <div class="stack"><h2 style="font-size:26px">함께 쓰면 좋은 꽃</h2><div class="stack" style="gap:12px">{''.join(flower_card(x) for x in pals)}</div></div>
</div></section>'''
        pages.append(page(f'flower-{f["id"]}.html', f'{f["name"]} 꽃말 · 꽃말 우체국', 'flowers', body, desc=f'{f["name"]}의 꽃말: {f["meaning"]}'))

    # ---- 홍보 영상 · 숏폼 · QR
    shorts = ''.join(f'''<figure style="margin:0"><div class="video-frame tall">
<video controls playsinline preload="metadata" poster="media/short-{s['no']}.jpg" aria-label="숏폼 {s['no']}: {s['title']}"><source src="{s['file']}" type="video/mp4"></video></div>
<figcaption class="short-meta"><strong>#{s['no']} {s['title']}</strong><span class="muted small">{s['line']}</span></figcaption></figure>''' for s in SHORTS)
    body = head('MEDIA', '홍보 영상', '꽃말 우체국을 소개하는 모션 그래픽 영상과 숏폼, 홈페이지 QR 코드예요.') + f'''
<section class="section"><div class="wrap">
  <div class="section-head"><p class="eyebrow">PROMOTION FILM</p><h2 class="h-section">홈페이지 홍보 영상</h2></div>
  <div class="video-frame wide">
    <video controls playsinline preload="metadata" poster="media/promo.jpg" aria-label="꽃말 우체국 홍보 영상"><source src="media/promo.mp4" type="video/mp4"></video>
  </div>
  <p class="muted small" style="margin-top:12px">30초 · 모션 그래픽 · 소리 없음</p>
</div></section>
<section class="section white"><div class="wrap">
  <div class="section-head"><p class="eyebrow">SHORTS</p><h2 class="h-section">숏폼 3편</h2><p class="lead">인스타그램 릴스 · 유튜브 쇼츠용 세로 영상이에요.</p></div>
  <div class="shorts-grid">{shorts}</div>
</div></section>
<section class="section"><div class="wrap">
  <div class="section-head"><p class="eyebrow">QR CODE</p><h2 class="h-section">휴대폰으로 바로 열기</h2></div>
  <div class="qr-box">
    <div id="qr" role="img" aria-label="꽃말 우체국 홈페이지 QR 코드"></div>
    <div class="stack" style="gap:12px;min-width:0;flex:1 1 260px">
      <p style="font-weight:700;font-size:18px">카메라로 QR 코드를 비추면 홈페이지가 열려요.</p>
      <p class="url-text" id="site-url">{SITE_URL}</p>
      <div class="btn-row"><button class="btn sm ghost" type="button" id="copy-url">주소 복사</button><a class="btn sm" href="checkout.html">주문하기</a></div>
      <p class="muted small" id="copy-msg" aria-live="polite"></p>
    </div>
  </div>
</div></section>'''
    pages.append(page('media.html', '홍보 영상 · 꽃말 우체국', 'media', body,
                      scripts='<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script><script src="assets/js/media.js"></script>'))

    # ---- 주문 / 결제
    popts = ''.join(f'''<div class="opt"><input type="radio" name="product" id="p-{p['id']}" value="{p['id']}"{' checked' if i == 0 else ''}>
<label for="p-{p['id']}"><img src="{p['img']}" alt=""><span class="t"><b>{p['name']}</b><small>{won(p['price'])}</small></span></label></div>''' for i, p in enumerate(PRODUCTS))
    topts = ''.join(f'<span class="chip-radio"><input type="radio" name="theme" id="t-{t["id"]}" value="{t["id"]}"{" checked" if i == 0 else ""}><label class="chip" for="t-{t["id"]}">{t["label"]}</label></span>' for i, t in enumerate(THEMES))
    ropts = ''.join(f'<span class="chip-radio"><input type="radio" name="to" id="r-{r["id"]}" value="{r["id"]}"{" checked" if i == 0 else ""}><label class="chip" for="r-{r["id"]}">{r["label"]}</label></span>' for i, r in enumerate(RECIPIENTS))
    body = f'''
<section class="page-hero" style="padding-block:clamp(28px,4vw,44px)"><div class="wrap"><div class="stack" style="gap:8px">
<p class="eyebrow">ORDER</p><h1>주문 · 결제</h1><p class="lead">한 페이지에서 고르고, 적고, 바로 결제해요.</p></div></div></section>
<section class="section" style="padding-top:32px"><div class="wrap">
<form id="order-form" class="checkout" novalidate>
  <div class="panel">
    <fieldset class="fs"><legend><span class="n">1</span>구성</legend>
      <div class="opt-grid">{popts}</div>
      <div style="display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap">
        <span style="font-weight:700">수량</span>
        <div class="qty"><button type="button" id="qty-dec" aria-label="수량 줄이기">−</button><output id="qty" aria-live="polite">1</output><button type="button" id="qty-inc" aria-label="수량 늘리기">+</button></div>
      </div>
    </fieldset>

    <fieldset class="fs"><legend><span class="n">2</span>담고 싶은 마음</legend>
      <div class="chips">{topts}</div>
      <div class="note" id="theme-note"></div>
      <p class="pay-badge" id="flower-req" hidden></p>
      <p style="font-weight:700;margin-top:6px">받는 사람</p>
      <div class="chips">{ropts}</div>
    </fieldset>

    <fieldset class="fs"><legend><span class="n">3</span>편지</legend>
      <div class="opt-grid">
        <div class="opt"><input type="radio" name="letterWay" id="lw-type" value="type" checked><label for="lw-type"><span class="t"><b>여기에 적기</b><small>편지지에 옮겨 동봉해요</small></span></label></div>
        <div class="opt"><input type="radio" name="letterWay" id="lw-store" value="store"><label for="lw-store"><span class="t"><b>매장에 맡기기</b><small>안양 매장에 직접 가져와요</small></span></label></div>
        <div class="opt"><input type="radio" name="letterWay" id="lw-mail" value="mail"><label for="lw-mail"><span class="t"><b>우편 보내기</b><small>주소는 주문 후 안내해요</small></span></label></div>
      </div>
      <div class="field" id="letter-field"><label for="letter">편지 내용 <span class="req">*</span></label>
        <textarea id="letter" rows="5" maxlength="400" placeholder="예) 엄마, 늘 고맙다는 말을 못 했어요. 키워줘서 고마워요."></textarea>
        <span class="hint" id="letter-count">0 / 400자</span></div>
    </fieldset>

    <fieldset class="fs"><legend><span class="n">4</span>받는 방법 · 정보</legend>
      <div class="opt-grid c2">
        <div class="opt"><input type="radio" name="receive" id="rv-ship" value="ship" checked><label for="rv-ship"><span class="t"><b>택배 배송</b><small>배송비 {won(SHIPPING)}</small></span></label></div>
        <div class="opt"><input type="radio" name="receive" id="rv-pickup" value="pickup"><label for="rv-pickup"><span class="t"><b>매장 픽업</b><small>경기도 안양시 동안구 · 무료</small></span></label></div>
      </div>
      <div class="row2">
        <div class="field"><label for="sname">주문하는 분 <span class="req">*</span></label><input id="sname" autocomplete="name"></div>
        <div class="field"><label for="sphone">연락처 <span class="req">*</span></label><input id="sphone" type="tel" inputmode="numeric" autocomplete="tel" placeholder="010-0000-0000"></div>
      </div>
      <div id="ship-fields" class="stack" style="gap:14px">
        <div class="row2">
          <div class="field"><label for="rname">받는 분 <span class="req">*</span></label><input id="rname"></div>
          <div class="field"><label for="rphone">받는 분 연락처 <span class="req">*</span></label><input id="rphone" type="tel" inputmode="numeric" placeholder="010-0000-0000"></div>
        </div>
        <div class="field"><label for="addr">배송 주소 <span class="req">*</span></label><input id="addr" autocomplete="street-address" placeholder="도로명 주소, 상세 주소"></div>
      </div>
      <div class="row2">
        <div class="field"><label for="date" id="date-label">도착 희망일 <span class="req">*</span></label><input id="date" type="date"></div>
        <div class="field"><label for="memo">요청 사항 (선택)</label><input id="memo" placeholder="예) 부재 시 문 앞에 놓아주세요"></div>
      </div>
    </fieldset>

    <fieldset class="fs"><legend><span class="n">5</span>결제</legend>
      <div id="payment-method"></div>
      <div id="agreement"></div>
      <div id="demo-pay" hidden class="stack" style="gap:12px">
        <p class="note">미리보기 화면에서는 토스페이먼츠 결제창을 불러올 수 없어 데모 결제로 진행돼요. GitHub Pages에 올리면 테스트 결제창이 열려요.</p>
        <div class="demo-pay">
          <span class="chip-radio"><input type="radio" name="demoPay" id="dp-card" value="신용·체크카드" checked><label class="chip" for="dp-card" style="width:100%;justify-content:center">신용·체크카드</label></span>
          <span class="chip-radio"><input type="radio" name="demoPay" id="dp-toss" value="토스페이"><label class="chip" for="dp-toss" style="width:100%;justify-content:center">토스페이</label></span>
          <span class="chip-radio"><input type="radio" name="demoPay" id="dp-kakao" value="카카오페이"><label class="chip" for="dp-kakao" style="width:100%;justify-content:center">카카오페이</label></span>
          <span class="chip-radio"><input type="radio" name="demoPay" id="dp-bank" value="계좌이체"><label class="chip" for="dp-bank" style="width:100%;justify-content:center">계좌이체</label></span>
        </div>
      </div>
      <label style="display:flex;gap:10px;align-items:flex-start;cursor:pointer"><input type="checkbox" id="agree" style="width:22px;height:22px;margin:3px 0 0;accent-color:#6B2C3B;flex:none"><span>생화 특성상 제작 시작 후에는 취소가 어려운 점을 확인했어요. (필수)</span></label>
      <p class="alert" id="form-error" role="alert" hidden></p>
    </fieldset>
  </div>

  <aside class="summary" aria-label="주문 요약">
    <h2>주문 요약</h2>
    <img id="sum-img" src="{PRODUCTS[0]['img']}" alt="">
    <div class="sum-row"><span>구성</span><span id="sum-product"></span></div>
    <div class="sum-row"><span>꽃</span><span id="sum-flowers"></span></div>
    <div class="sum-row"><span>받는 사람</span><span id="sum-to"></span></div>
    <div class="sum-row"><span>받는 방법</span><span id="sum-receive"></span></div>
    <div class="sum-row"><span>상품 금액</span><span id="sum-sub"></span></div>
    <div class="sum-row"><span>배송비</span><span id="sum-ship"></span></div>
    <div class="sum-total"><span style="font-weight:700">총 결제 금액</span><b id="sum-total"></b></div>
    <button class="btn lg block pay-btn" type="submit">결제하기</button>
    <p class="muted small">테스트 결제 환경이에요. 실제로 돈이 빠져나가지 않아요.</p>
  </aside>
  <div class="mobile-paybar"><span><span class="muted small">총 결제 금액</span><br><b id="bar-total"></b></span><button class="btn pay-btn" type="submit">결제하기</button></div>
</form>
</div></section>'''
    pages.append(page('checkout.html', '주문 · 결제 · 꽃말 우체국', 'checkout', body, body_class='has-paybar',
                      scripts='<script src="https://js.tosspayments.com/v2/standard"></script><script src="assets/js/checkout.js"></script>'))

    # ---- 결제 성공 / 실패
    body = f'''<section class="section"><div class="wrap">
<div class="result-card"><div class="mark">{ICON['check']}</div>
<h1 style="font-size:clamp(26px,4vw,34px)">편지가 우체국에 접수되었어요</h1>
<p class="muted" id="ok-msg">마음을 담은 꽃을 정성껏 준비할게요.</p>
<div class="result-list" id="ok-list"></div>
<p class="pay-badge" id="ok-mode"></p>
<div class="btn-row" style="justify-content:center"><a class="btn" href="index.html">홈으로</a><a class="btn ghost" href="checkout.html">새 편지 보내기</a></div>
</div></div></section>'''
    pages.append(page('success.html', '주문 완료 · 꽃말 우체국', 'checkout', body, scripts='<script src="assets/js/result.js"></script>'))
    body = f'''<section class="section"><div class="wrap">
<div class="result-card"><div class="mark fail">{ICON['x']}</div>
<h1 style="font-size:clamp(26px,4vw,34px)">결제가 완료되지 않았어요</h1>
<p class="muted" id="fail-msg">결제를 취소했거나 문제가 생겼어요. 입력한 내용은 그대로 남아 있어요.</p>
<div class="btn-row" style="justify-content:center"><a class="btn" href="checkout.html" id="retry">다시 결제하기</a><a class="btn ghost" href="how.html#faq">자주 묻는 질문</a></div>
</div></div></section>'''
    pages.append(page('fail.html', '결제 실패 · 꽃말 우체국', 'checkout', body, scripts='<script src="assets/js/result.js"></script>'))

    # ---- 404 (GitHub Pages용)
    body = '''<section class="section"><div class="wrap"><div class="result-card"><h1>페이지를 찾을 수 없어요</h1><p class="muted">주소가 바뀌었거나 없는 페이지예요.</p><div class="btn-row" style="justify-content:center"><a class="btn" href="index.html">홈으로</a></div></div></div></section>'''
    pages.append(page('404.html', '페이지 없음 · 꽃말 우체국', '', body))

    with open(os.path.join(DIST, '.nojekyll'), 'w') as fh:
        fh.write('')
    return pages

if __name__ == '__main__':
    out = build()
    print(len(out), 'pages:', ' '.join(out))
