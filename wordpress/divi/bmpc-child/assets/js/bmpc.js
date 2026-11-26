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

/* Join form (Fluent Forms): group each section into the design's lettered card.
   Section titles are written "ক. ব্যক্তিগত তথ্য"; the letter becomes the badge. Fields are moved, not copied,
   so Fluent's validation, uploads and conditional logic keep working. Without JS the form stays a plain list. */
(function () {
  [].forEach.call(document.querySelectorAll('form.frm-fluent-form'), function (form) {
    var breaks = [].slice.call(form.querySelectorAll('.ff-el-section-break'));
    breaks.forEach(function (br) {
      var title = br.querySelector('.ff-el-section-title');
      var text = title ? title.textContent.trim() : '';
      var m = text.match(/^(\S{1,3})\.\s*(.+)$/);
      var card = document.createElement('fieldset');
      card.className = 'bmpc-card';
      var legend = document.createElement('legend');
      if (m) {
        var b = document.createElement('b');
        b.textContent = m[1];
        b.setAttribute('aria-hidden', 'true');
        legend.appendChild(b);
        legend.appendChild(document.createTextNode(m[2]));
      } else {
        legend.textContent = text;
      }
      card.appendChild(legend);
      var desc = br.querySelector('.ff-section_break_desk');
      if (desc && desc.textContent.trim()) {
        var p = document.createElement('p');
        p.className = 'bmpc-hint';
        p.textContent = desc.textContent.trim();
        card.appendChild(p);
      }
      br.parentNode.insertBefore(card, br);
      var node = br.nextElementSibling;
      card.appendChild(br);
      while (node && !node.classList.contains('ff-el-section-break')) {
        var next = node.nextElementSibling;
        if (!node.classList.contains('ff-form-inline-style')) card.appendChild(node);
        node = next;
      }
    });
    var submit = form.querySelector('.ff_submit_btn_wrapper');
    if (submit && !submit.querySelector('.bmpc-submit-note')) {
      var note = document.createElement('p');
      note.className = 'bmpc-submit-note';
      note.textContent = 'জমা দেওয়ার পর অ্যাডমিন তথ্য যাচাই করে আপনার মোবাইল বা হোয়াটসঅ্যাপ নম্বরে যোগাযোগ করবেন।';
      submit.appendChild(note);
    }
  });
})();
