/* 공통: 저장소 접근 도우미 */
window.FPStore = {
  get: function (k) { try { return JSON.parse(sessionStorage.getItem(k)); } catch (e) { return null; } },
  set: function (k, v) { try { sessionStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
};
window.FPwon = function (n) { return Number(n).toLocaleString('ko-KR') + '원'; };
