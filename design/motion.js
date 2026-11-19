/* BMPC scroll motion. Everything is visible without JS; effects start on the first scroll. */
(function () {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var root = document.documentElement, BN = '০১২৩৪৫৬৭৮৯';
  var toBn = function (n) { return String(n).replace(/\d/g, function (d) { return BN[d]; }); };
  var fromBn = function (s) { return parseInt(s.replace(/[০-৯]/g, function (c) { return BN.indexOf(c); }), 10); };

  /* progress bar + compact header */
  var bar = document.createElement('div'); bar.className = 'scroll-bar'; bar.setAttribute('aria-hidden', 'true');
  document.body.appendChild(bar);
  var top = document.querySelector('.top');

  /* hero parallax layers */
  var L = function (sel) { return document.querySelector('.hero ' + sel); };
  var layers = [[L('.pl-burst'), function (y) { return 'rotate(' + (y * 0.035) + 'deg)'; }],
                [L('.pl-sun'), function (y) { return 'translateY(' + (-y * 0.14) + 'px)'; }],
                [L('.pl-crowd1'), function (y) { return 'translateY(' + (y * 0.05) + 'px)'; }],
                [L('.pl-crowd2'), function (y) { return 'translateY(' + (y * 0.09) + 'px)'; }],
                [L('.pl-mon'), function (y) { return 'translateY(' + (y * 0.02) + 'px)'; }],
                [L('.pl-birds'), function (y) { return 'translate(' + (y * 0.12) + 'px,' + (-y * 0.08) + 'px)'; }]]
               .filter(function (l) { return l[0]; });
  var heroText = document.querySelector('.hero .wrap > div:first-child');
  var bands = [].slice.call(document.querySelectorAll('.goals,.short,.slogan'));

  var ticking = false;
  function frame() {
    ticking = false;
    var y = scrollY, h = root.scrollHeight - innerHeight;
    bar.style.transform = 'scaleX(' + (h > 0 ? Math.min(1, y / h) : 0) + ')';
    if (top) top.classList.toggle('is-compact', y > 40);
    if (y < innerHeight * 1.2) {
      layers.forEach(function (l) { l[0].style.transform = l[1](y); });
      if (heroText && document.querySelector('.hero .hero-art')) heroText.style.transform = 'translateY(' + (y * 0.18) + 'px)';
    }
    bands.forEach(function (b) {
      var r = b.getBoundingClientRect();
      if (r.bottom > 0 && r.top < innerHeight) b.style.setProperty('--rot', ((innerHeight - r.top) * 0.04).toFixed(2) + 'deg');
    });
  }
  function onScroll() { if (!ticking) { ticking = true; requestAnimationFrame(frame); } }

  /* reveal-on-scroll: only elements still below the fold get the hidden start state, and only once the reader scrolls */
  var SEL = ['.sec-head', '.goals li', '.plan', '.lcard', '.nstory', '.day', '.acts span', '.steps li', '.join .wrap > div',
             '.about .big', '.about p.body', '.pill', '.rule', '.pledge', '.closing', '.slogan q', '.card', '.long-list li',
             '.mission li', '.intro figure', '.intro p.big', '.who', '.letter p', '.letter blockquote', '.sign', '.feat a.story',
             '.ngrid a.story', '.post figure', '.event', '.gallery figure', 'fieldset', '.aside .box', '.cta .wrap > *', '.ribbon .wrap>div'].join(',');
  var armed = false;
  function arm() {
    if (armed) return; armed = true;
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target; io.unobserve(el);
        var sibs = el.parentElement ? [].slice.call(el.parentElement.children).filter(function (c) { return c.classList.contains('rv'); }) : [];
        el.style.transitionDelay = Math.min(sibs.indexOf(el), 6) * 70 + 'ms';
        el.classList.add('rv-in');
        if (el.matches('.ribbon .wrap>div')) count(el.querySelector('b'));
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    document.querySelectorAll(SEL).forEach(function (el) {
      if (el.getBoundingClientRect().top > innerHeight) { el.classList.add('rv'); io.observe(el); }
    });
  }

  /* Bangla number count-up for the ribbon */
  function count(b) {
    if (!b) return; var txt = b.textContent, m = txt.match(/[০-৯]+/);
    if (!m) return; var end = fromBn(m[0]), t0 = null;
    if (!(end > 1) || end > 3000) return;
    (function step(t) {
      if (!t0) t0 = t; var k = Math.min(1, (t - t0) / 1100), v = Math.round(end * (1 - Math.pow(1 - k, 3)));
      b.textContent = txt.replace(m[0], toBn(v)); if (k < 1) requestAnimationFrame(step);
    })(performance.now());
  }

  addEventListener('scroll', function () { arm(); onScroll(); }, { passive: true });
  addEventListener('resize', onScroll);
})();
