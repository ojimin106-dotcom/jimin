(function () {
  var q = new URLSearchParams(location.search);
  var order = FPStore.get('fp-order');
  var $ = function (id) { return document.getElementById(id); };
  var esc = function (s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); };

  // 결제 성공 페이지
  if ($('ok-list')) {
    var amount = Number(q.get('amount') || (order && order.total) || 0);
    var orderId = q.get('orderId') || (order && order.orderId) || '';
    if (order && order.total !== amount) {
      $('ok-msg').textContent = '결제 금액이 주문 금액과 달라요. 매장으로 문의해 주세요.';
    } else if (order && order.rname) {
      $('ok-msg').textContent = order.rname + '님께 보낼 꽃을 정성껏 준비할게요.';
    }
    var rows = [['주문번호', orderId]];
    if (order) rows = rows.concat([
      ['구성', order.product + ' × ' + order.qty], ['꽃', order.flowers], ['받는 사람', order.to],
      ['편지', order.letterWay], ['받는 방법', order.receive], [order.receive === '매장 픽업' ? '픽업일' : '도착 희망일', order.date]
    ]);
    if (order && order.method) rows.push(['결제 수단', order.method]);
    rows.push(['결제 금액', FPwon(amount)]);
    $('ok-list').innerHTML = rows.map(function (r, i) {
      var last = i === rows.length - 1;
      return '<div class="sum-row"' + (last ? ' style="border-top:1px solid var(--line);padding-top:10px;font-weight:700"' : '') + '><span>' + esc(r[0]) + '</span><span>' + esc(r[1]) + '</span></div>';
    }).join('');
    $('ok-mode').textContent = q.get('demo') === '1' ? '데모 결제 · 실제 결제 아님' : '토스페이먼츠 테스트 결제 · 실제 출금 없음';
    try { sessionStorage.removeItem('fp-draft'); } catch (e) {}
  }

  // 결제 실패 페이지
  if ($('fail-msg')) {
    if (q.get('message')) $('fail-msg').textContent = q.get('message') + ' 입력한 내용은 그대로 남아 있어요.';
    $('retry').href = 'checkout.html?restore=1';
  }
})();
