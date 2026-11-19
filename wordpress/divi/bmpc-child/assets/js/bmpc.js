/* Objectives page: filter long-term objectives by topic. */
(function () {
  var chips = [].slice.call(document.querySelectorAll('.chip[data-f]'));
  if (!chips.length) return;
  var BN = '০১২৩৪৫৬৭৮৯', bn = function (n) { return String(n).replace(/\d/g, function (d) { return BN[d]; }); };
  var rows = [].slice.call(document.querySelectorAll('.long-list li')), count = document.getElementById('count');
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      var f = c.getAttribute('data-f'), n = 0;
      chips.forEach(function (x) { x.setAttribute('aria-pressed', x === c ? 'true' : 'false'); });
      rows.forEach(function (r) { var on = f === 'all' || r.getAttribute('data-cat') === f; r.hidden = !on; if (on) n++; });
      if (count) count.textContent = bn(n) + 'টি উদ্দেশ্য দেখানো হচ্ছে';
    });
  });
})();
