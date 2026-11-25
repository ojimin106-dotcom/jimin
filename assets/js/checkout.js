/* 주문 · 결제 — 토스페이먼츠 결제위젯 v2 (테스트 키) */
(function () {
  // 토스페이먼츠 문서용 공개 테스트 키. 실제 판매 시 본인 상점의 클라이언트 키로 교체하세요.
  var CLIENT_KEY = 'test_gck_docs_Ovk5rk1EwkEbP0W43n07xlzm';
  var FP = window.FP;
  var $ = function (id) { return document.getElementById(id); };
  var form = $('order-form');
  var qty = 1;
  var widgets = null;
  var tossReady = false;
  var flowerReq = null;

  // ---- 주소창 값으로 미리 선택 (상품·마음·받는 사람·꽃)
  var q = new URLSearchParams(location.search);
  function pick(name, val) {
    if (!val) return;
    var el = form.querySelector('input[name="' + name + '"][value="' + CSS.escape(val) + '"]');
    if (el) el.checked = true;
  }
  pick('product', q.get('product'));
  pick('theme', q.get('theme'));
  pick('to', q.get('to'));
  if (q.get('flower') && FP.flowers[q.get('flower')]) flowerReq = FP.flowers[q.get('flower')];

  // 실패 후 돌아왔을 때 입력값 복원
  var saved = FPStore.get('fp-draft');
  if (saved && q.get('restore') === '1') {
    ['letter', 'sname', 'sphone', 'rname', 'rphone', 'addr', 'date', 'memo'].forEach(function (k) { if (saved[k]) $(k).value = saved[k]; });
    pick('product', saved.product); pick('theme', saved.theme); pick('to', saved.to);
    pick('letterWay', saved.letterWay); pick('receive', saved.receive);
    qty = saved.qty || 1; if (saved.flowerReq) flowerReq = saved.flowerReq;
  }

  // ---- 날짜: 오늘 + 2일부터
  var d = new Date(); d.setDate(d.getDate() + 2);
  var minDate = d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
  $('date').min = minDate;
  if (!$('date').value) $('date').value = minDate;

  function val(name) { var el = form.querySelector('input[name="' + name + '"]:checked'); return el ? el.value : null; }
  function find(list, id) { return list.filter(function (x) { return x.id === id; })[0] || list[0]; }

  function state() {
    var p = find(FP.products, val('product'));
    var t = find(FP.themes, val('theme'));
    var r = find(FP.recipients, val('to'));
    var receive = val('receive');
    var ship = receive === 'pickup' ? 0 : FP.shipping;
    var sub = p.price * qty;
    return { p: p, t: t, r: r, receive: receive, ship: ship, sub: sub, total: sub + ship, letterWay: val('letterWay') };
  }

  function render() {
    var s = state();
    $('qty').textContent = qty;
    $('theme-note').innerHTML = '<b style="color:var(--wine)">추천 꽃</b> ' + s.t.flowers.join(' · ') + '<br><span>' + s.t.meanings.join(', ') + '</span>';
    var fr = $('flower-req');
    if (flowerReq) { fr.hidden = false; fr.textContent = '요청한 꽃: ' + flowerReq; } else { fr.hidden = true; }
    $('letter-field').hidden = s.letterWay !== 'type';
    $('ship-fields').hidden = s.receive === 'pickup';
    $('date-label').firstChild.textContent = s.receive === 'pickup' ? '픽업 희망일 ' : '도착 희망일 ';
    $('sum-img').src = s.p.img; $('sum-img').alt = s.p.alt;
    $('sum-product').textContent = s.p.name + ' × ' + qty;
    $('sum-flowers').textContent = s.t.flowers.join(' · ') + (flowerReq ? ' + ' + flowerReq : '');
    $('sum-to').textContent = s.r.label;
    $('sum-receive').textContent = s.receive === 'pickup' ? '매장 픽업' : '택배 배송';
    $('sum-sub').textContent = FPwon(s.sub);
    $('sum-ship').textContent = FPwon(s.ship);
    $('sum-total').textContent = FPwon(s.total);
    $('bar-total').textContent = FPwon(s.total);
    document.querySelectorAll('.pay-btn').forEach(function (b) { b.textContent = FPwon(s.total) + ' 결제하기'; });
    $('letter-count').textContent = $('letter').value.length + ' / 400자';
    if (widgets && tossReady) widgets.setAmount({ currency: 'KRW', value: s.total }).catch(function () {});
  }

  form.addEventListener('change', function () { hideError(); render(); });
  $('letter').addEventListener('input', render);
  $('qty-inc').addEventListener('click', function () { qty = Math.min(10, qty + 1); render(); });
  $('qty-dec').addEventListener('click', function () { qty = Math.max(1, qty - 1); render(); });

  function showError(msg, focusId) {
    var el = $('form-error'); el.textContent = msg; el.hidden = false;
    if (focusId && $(focusId)) $(focusId).focus();
    else el.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }
  function hideError() { $('form-error').hidden = true; }

  function validate(s) {
    var need = [];
    if (s.letterWay === 'type' && !$('letter').value.trim()) need.push(['편지 내용', 'letter']);
    if (!$('sname').value.trim()) need.push(['주문하는 분', 'sname']);
    if ($('sphone').value.replace(/\D/g, '').length < 9) need.push(['연락처', 'sphone']);
    if (s.receive === 'ship') {
      if (!$('rname').value.trim()) need.push(['받는 분', 'rname']);
      if ($('rphone').value.replace(/\D/g, '').length < 9) need.push(['받는 분 연락처', 'rphone']);
      if (!$('addr').value.trim()) need.push(['배송 주소', 'addr']);
    }
    if (!$('date').value || $('date').value < minDate) need.push([s.receive === 'pickup' ? '픽업 희망일(오늘로부터 2일 뒤부터)' : '도착 희망일(오늘로부터 2일 뒤부터)', 'date']);
    if (need.length) { showError(need.map(function (n) { return n[0]; }).join(', ') + '을(를) 확인해 주세요.', need[0][1]); return false; }
    if (!$('agree').checked) { showError('취소 안내에 동의해 주세요.', 'agree'); return false; }
    return true;
  }

  function orderRecord(s, orderId, mode, method) {
    return {
      orderId: orderId, mode: mode, method: method || '',
      product: s.p.name, qty: qty, flowers: s.t.flowers.join(' · ') + (flowerReq ? ' + ' + flowerReq : ''),
      theme: s.t.label, to: s.r.label, receive: s.receive === 'pickup' ? '매장 픽업' : '택배 배송',
      date: $('date').value, rname: s.receive === 'pickup' ? $('sname').value.trim() : $('rname').value.trim(),
      letterWay: { type: '주문서에 작성', store: '매장에 맡기기', mail: '우편 보내기' }[s.letterWay],
      total: s.total
    };
  }

  function saveDraft(s) {
    var o = { product: s.p.id, theme: s.t.id, to: s.r.id, letterWay: s.letterWay, receive: s.receive, qty: qty, flowerReq: flowerReq };
    ['letter', 'sname', 'sphone', 'rname', 'rphone', 'addr', 'date', 'memo'].forEach(function (k) { o[k] = $(k).value; });
    FPStore.set('fp-draft', o);
  }

  form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    var s = state();
    if (!validate(s)) return;
    var orderId = 'FP' + Date.now() + Math.random().toString(36).slice(2, 8);
    var base = location.href.replace(/[^/]*([?#].*)?$/, '');
    saveDraft(s);

    if (tossReady) {
      FPStore.set('fp-order', orderRecord(s, orderId, 'toss'));
      var btns = document.querySelectorAll('.pay-btn');
      btns.forEach(function (b) { b.disabled = true; });
      widgets.requestPayment({
        orderId: orderId,
        orderName: s.p.name + (qty > 1 ? ' 외 ' + (qty - 1) + '건' : ''),
        successUrl: base + 'success.html',
        failUrl: base + 'fail.html',
        customerName: $('sname').value.trim()
      }).catch(function (err) {
        showError('결제창을 열지 못했어요. ' + (err && err.message ? err.message : '잠시 후 다시 시도해 주세요.'));
      }).finally(function () { btns.forEach(function (b) { b.disabled = false; }); });
    } else {
      var m = form.querySelector('input[name="demoPay"]:checked');
      FPStore.set('fp-order', orderRecord(s, orderId, 'demo', m ? m.value : ''));
      location.href = 'success.html?orderId=' + encodeURIComponent(orderId) + '&amount=' + s.total + '&demo=1';
    }
  });

  // ---- 토스페이먼츠 위젯 불러오기 (불러올 수 없으면 데모 결제)
  function useDemo() { tossReady = false; $('demo-pay').hidden = false; }
  async function initToss() {
    if (!window.TossPayments) { useDemo(); return; }
    try {
      var tp = TossPayments(CLIENT_KEY);
      widgets = tp.widgets({ customerKey: TossPayments.ANONYMOUS });
      await widgets.setAmount({ currency: 'KRW', value: state().total });
      await Promise.all([
        widgets.renderPaymentMethods({ selector: '#payment-method', variantKey: 'DEFAULT' }),
        widgets.renderAgreement({ selector: '#agreement', variantKey: 'AGREEMENT' })
      ]);
      tossReady = true;
    } catch (e) {
      console.warn('TossPayments 위젯을 불러오지 못했어요:', e);
      $('payment-method').innerHTML = ''; $('agreement').innerHTML = '';
      useDemo();
    }
  }

  render();
  initToss();
})();
