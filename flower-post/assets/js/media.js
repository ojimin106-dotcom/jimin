(function () {
  // 홈페이지 주소: GitHub Pages에서 열면 현재 주소, 그 밖에서는 기본 주소
  var url = window.FP.siteUrl;
  if (/github\.io$/.test(location.hostname)) {
    url = location.origin + location.pathname.replace(/[^/]*$/, '');
  }
  var urlEl = document.getElementById('site-url');
  if (urlEl) urlEl.textContent = url;

  var qr = document.getElementById('qr');
  if (qr && window.QRCode) {
    new QRCode(qr, { text: url, width: 400, height: 400, colorDark: '#4E1F2B', colorLight: '#FFFFFF', correctLevel: QRCode.CorrectLevel.M });
  } else if (qr) {
    qr.textContent = 'QR 코드를 불러오지 못했어요.';
  }

  var copyBtn = document.getElementById('copy-url');
  var msg = document.getElementById('copy-msg');
  if (copyBtn) copyBtn.addEventListener('click', function () {
    var done = function () { msg.textContent = '주소를 복사했어요.'; };
    var fallback = function () {
      var r = document.createRange(); r.selectNodeContents(urlEl);
      var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
      msg.textContent = '주소를 선택했어요. 길게 눌러 복사하세요.';
    };
    try { navigator.clipboard.writeText(url).then(done, fallback); } catch (e) { fallback(); }
  });
})();
