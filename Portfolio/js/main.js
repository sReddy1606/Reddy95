var hero = document.getElementById('hero');
var replayBtn = document.getElementById('replay');
var intro = document.getElementById('intro');
var introPixels = document.getElementById('introPixels');
var nameShatterLabel = document.getElementById('nameShatterLabel');
var canvas = document.getElementById('lightfall-canvas');
var ctx = canvas.getContext('2d');
var introTimers = [];
var rafId = null;
var beams = [];
var ACCENT = [207, 122, 82]; /* matches site accent #cf7a52 */
var BG = '#0b0d12';

function measureFontPx() {
  var size = window.getComputedStyle(nameShatterLabel).fontSize;
  return parseFloat(size) || 60;
}

function sizeCanvas() {
  var dpr = Math.min(window.devicePixelRatio || 1, 2);
  canvas.width = Math.round(window.innerWidth * dpr);
  canvas.height = Math.round(window.innerHeight * dpr);
  canvas.style.width = '100%';
  canvas.style.height = '100%';
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
}

function seedBeams() {
  var count = window.innerWidth < 640 ? 26 : 46;
  beams = [];
  for (var i = 0; i < count; i++) {
    beams.push({
      x: Math.random() * window.innerWidth,
      y: Math.random() * window.innerHeight - window.innerHeight,
      len: 60 + Math.random() * 160,
      speed: 1.2 + Math.random() * 3.2,
      width: 1 + Math.random() * 2.2,
      alpha: 0.18 + Math.random() * 0.4
    });
  }
}

function drawLightfall() {
  var w = window.innerWidth, h = window.innerHeight;
  ctx.fillStyle = 'rgba(11,13,18,0.22)';
  ctx.fillRect(0, 0, w, h);

  beams.forEach(function (b) {
    var grad = ctx.createLinearGradient(b.x, b.y, b.x, b.y + b.len);
    grad.addColorStop(0, 'rgba(' + ACCENT.join(',') + ',0)');
    grad.addColorStop(0.5, 'rgba(' + ACCENT.join(',') + ',' + b.alpha + ')');
    grad.addColorStop(1, 'rgba(' + ACCENT.join(',') + ',0)');
    ctx.fillStyle = grad;
    ctx.fillRect(b.x, b.y, b.width, b.len);
    b.y += b.speed;
    if (b.y > h) {
      b.y = -b.len - Math.random() * 200;
      b.x = Math.random() * w;
    }
  });

  var vign = ctx.createRadialGradient(w / 2, h * 0.45, h * 0.15, w / 2, h * 0.45, h * 0.75);
  vign.addColorStop(0, 'rgba(11,13,18,0)');
  vign.addColorStop(1, 'rgba(6,7,10,0.55)');
  ctx.fillStyle = vign;
  ctx.fillRect(0, 0, w, h);

  ctx.save();
  ctx.fillStyle = '#f5f1ea';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.font = "700 " + measureFontPx() + "px 'Space Grotesk', sans-serif";
  ctx.fillText('SHASHANK REDDY', w / 2, h / 2);
  ctx.restore();

  rafId = requestAnimationFrame(drawLightfall);
}

function buildIntroPixels(snapshotURL, w, h) {
  introPixels.innerHTML = '';
  var cols = window.innerWidth < 640 ? 9 : 16;
  var tileW = w / cols;
  var rows = Math.max(5, Math.round(h / tileW));
  var tileH = h / rows;
  var tiles = [];
  for (var r = 0; r < rows; r++) {
    for (var c = 0; c < cols; c++) {
      var tile = document.createElement('div');
      tile.className = 'intro-pixel';
      tile.style.left = (c * tileW) + 'px';
      tile.style.top = (r * tileH) + 'px';
      tile.style.width = Math.ceil(tileW) + 'px';
      tile.style.height = Math.ceil(tileH) + 'px';
      tile.style.backgroundImage = 'url(' + snapshotURL + ')';
      tile.style.backgroundSize = w + 'px ' + h + 'px';
      tile.style.backgroundPosition = (-c * tileW) + 'px ' + (-r * tileH) + 'px';
      introPixels.appendChild(tile);
      tiles.push(tile);
    }
  }
  return tiles;
}

function beginDissolve(reduce) {
  var w = window.innerWidth, h = window.innerHeight;
  if (rafId) cancelAnimationFrame(rafId);
  var snapshotURL = canvas.toDataURL('image/png');
  canvas.style.display = 'none';

  var tiles = buildIntroPixels(snapshotURL, w, h);
  void intro.offsetWidth;

  var order = tiles.map(function (_, i) { return i; });
  for (var i = order.length - 1; i > 0; i--) {
    var j = Math.floor(Math.random() * (i + 1));
    var tmp = order[i]; order[i] = order[j]; order[j] = tmp;
  }
  var dissolveWindow = reduce ? 0 : 950;
  order.forEach(function (idx, pos) {
    var delay = reduce ? 0 : ((pos / tiles.length) * dissolveWindow + Math.random() * 40);
    tiles[idx].style.transitionDelay = delay.toFixed(0) + 'ms';
  });

  intro.classList.add('dissolve');
  hero.classList.add('opened');

  introTimers.push(setTimeout(function () {
    intro.classList.add('cleared');
    document.body.classList.remove('intro-active');
  }, dissolveWindow + 600));
}

function playIntro() {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  introTimers.forEach(function (id) { clearTimeout(id); });
  introTimers = [];

  hero.classList.remove('opened');
  intro.classList.remove('dissolve', 'cleared');
  canvas.style.display = 'block';
  document.body.classList.add('intro-active');
  void intro.offsetWidth;

  sizeCanvas();
  seedBeams();

  var start = function () {
    if (rafId) cancelAnimationFrame(rafId);
    if (reduce) {
      drawLightfall();
      if (rafId) cancelAnimationFrame(rafId);
      beginDissolve(true);
      return;
    }
    drawLightfall();
    var holdDelay = 1300;
    introTimers.push(setTimeout(function () { beginDissolve(false); }, holdDelay));
  };

  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(start).catch(start);
  } else {
    start();
  }
}

window.addEventListener('DOMContentLoaded', playIntro);
replayBtn.addEventListener('click', playIntro);
window.addEventListener('resize', function () {
  if (!intro.classList.contains('dissolve') && !intro.classList.contains('cleared')) {
    sizeCanvas();
  }
});

document.querySelectorAll('.h-logos-row .h-logo').forEach(function (el, i) {
  el.style.animationDelay = (-(i * 0.6)).toFixed(2) + 's';
});

document.querySelectorAll('.h-timeline-section').forEach(function (section) {
  var body = section.querySelector('.h-detail-body');
  var contents = section.querySelectorAll('.h-detail-content');
  var activeIdx = null;

  function setActive(idx) {
    section.querySelectorAll('.h-node').forEach(function (n) {
      n.classList.toggle('active', n.getAttribute('data-idx') === idx);
    });
    section.querySelectorAll('.h-point').forEach(function (n) {
      n.classList.toggle('h-point-active', n.getAttribute('data-idx') === idx);
    });
    contents.forEach(function (c) {
      c.classList.toggle('active', c.getAttribute('data-idx') === idx);
    });
  }

  section.querySelectorAll('.h-logo, .h-point').forEach(function (trigger) {
    trigger.addEventListener('click', function () {
      var idx = trigger.getAttribute('data-idx');
      if (activeIdx === idx) {
        activeIdx = null;
        body.classList.remove('open');
        section.querySelectorAll('.h-node').forEach(function (n) { n.classList.remove('active'); });
        contents.forEach(function (c) { c.classList.remove('active'); });
        return;
      }
      activeIdx = idx;
      setActive(idx);
      body.classList.add('open');
    });
  });
});

var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
var morphStates = new Map();
document.querySelectorAll('.morph-wrap').forEach(function (wrap) {
  morphStates.set(wrap, { cur: reduceMotion ? 1 : 0 });
});

var progressBar = document.getElementById('scroll-progress');
var trackWraps = document.querySelectorAll('.h-track-wrap .h-track');
var trackDrift = new Map();
trackWraps.forEach(function (el) { trackDrift.set(el, 0); });

function updatePins() {
  var doc = document.documentElement;
  var scrollTop = window.scrollY || doc.scrollTop;
  var docHeight = doc.scrollHeight - window.innerHeight;
  var pct = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
  if (progressBar) progressBar.style.width = pct.toFixed(2) + '%';

  if (!reduceMotion) {
    trackWraps.forEach(function (el) {
      var rect = el.getBoundingClientRect();
      var vh = window.innerHeight;
      var centerDist = (rect.top + rect.height / 2) - vh / 2;
      var target = Math.max(-1, Math.min(1, -centerDist / vh)) * 14;
      var cur = trackDrift.get(el);
      cur += (target - cur) * 0.08;
      trackDrift.set(el, cur);
      el.style.transform = 'translateY(' + cur.toFixed(2) + 'px)';
    });
  }

  if (!reduceMotion) {
    morphStates.forEach(function (state, wrap) {
      var rect = wrap.getBoundingClientRect();
      var vh = window.innerHeight;
      var scrollable = wrap.offsetHeight - vh;
      var raw = scrollable > 0 ? (-rect.top) / scrollable : 0;
      raw = Math.max(0, Math.min(1, raw));
      var t = raw < 0.3 ? 0 : (raw - 0.3) / 0.7;
      var target = t * t * (3 - 2 * t);
      state.cur += (target - state.cur) * 0.09;
      if (Math.abs(target - state.cur) < 0.0006) state.cur = target;

      var photo = wrap.querySelector('.morph-photo');
      var content = wrap.querySelector('.morph-content');
      var img = wrap.querySelector('.photo-frame-img');

      photo.style.opacity = String(1 - state.cur);
      photo.style.transform = 'scale(' + (1 + state.cur * 0.1).toFixed(4) + ')';
      if (img) img.style.transform = 'translateY(' + (state.cur * 30 - 15).toFixed(2) + 'px)';

      content.style.opacity = String(state.cur);
      content.style.transform = 'translateY(' + ((1 - state.cur) * 26).toFixed(2) + 'px)';
      content.style.pointerEvents = state.cur > 0.5 ? 'auto' : 'none';
    });
  } else {
    morphStates.forEach(function (state, wrap) {
      var photo = wrap.querySelector('.morph-photo');
      var content = wrap.querySelector('.morph-content');
      photo.style.opacity = '0';
      content.style.opacity = '1';
      content.style.transform = 'none';
      content.style.pointerEvents = 'auto';
    });
  }
  requestAnimationFrame(updatePins);
}
requestAnimationFrame(updatePins);

if ('IntersectionObserver' in window) {
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) e.target.classList.add('in-view');
    });
  }, { threshold: 0.15 });
  document.querySelectorAll('.reveal-up').forEach(function (el) { io.observe(el); });
} else {
  document.querySelectorAll('.reveal-up').forEach(function (el) { el.classList.add('in-view'); });
}

/* ============ SKILLS: MASONRY (React Bits port, vanilla JS + GSAP) ============ */
(function () {
  var hasGsap = typeof gsap !== 'undefined';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var container = document.getElementById('skillsMasonry');
  if (!container) return;

  var items = [
    { id: 'python', name: 'Python', img: 'assets/tool-logos/python.svg', url: 'https://www.python.org/' },
    { id: 'sql', name: 'PostgreSQL', img: 'assets/tool-logos/postgresql.svg', url: 'https://www.postgresql.org/' },
    { id: 'mysql', name: 'MySQL', img: 'assets/tool-logos/mysql.svg', url: 'https://www.mysql.com/' },
    { id: 'powerbi', name: 'Power BI', badge: true, url: 'https://powerbi.microsoft.com/' },
    { id: 'tableau', name: 'Tableau', badge: true, url: 'https://www.tableau.com/' },
    { id: 'looker', name: 'Looker', img: 'assets/tool-logos/looker.svg', url: 'https://www.looker.com/' },
    { id: 'snowflake', name: 'Snowflake', img: 'assets/tool-logos/snowflake.svg', url: 'https://www.snowflake.com/' },
    { id: 'dbt', name: 'dbt', badge: true, url: 'https://www.getdbt.com/' },
    { id: 'spark', name: 'Apache Spark', img: 'assets/tool-logos/apachespark.svg', url: 'https://spark.apache.org/' },
    { id: 'databricks', name: 'Databricks', img: 'assets/tool-logos/databricks.svg', url: 'https://www.databricks.com/' },
    { id: 'azure', name: 'Azure', badge: true, url: 'https://azure.microsoft.com/' },
    { id: 'aws', name: 'AWS', badge: true, url: 'https://aws.amazon.com/' },
    { id: 'gcp', name: 'Google Cloud', img: 'assets/tool-logos/googlecloud.svg', url: 'https://cloud.google.com/' },
    { id: 'oci', name: 'Oracle Cloud', badge: true, url: 'https://www.oracle.com/cloud/' },
    { id: 'docker', name: 'Docker', img: 'assets/tool-logos/docker.svg', url: 'https://www.docker.com/' },
    { id: 'git', name: 'Git', img: 'assets/tool-logos/git.svg', url: 'https://git-scm.com/' },
    { id: 'linux', name: 'Linux', img: 'assets/tool-logos/linux.svg', url: 'https://www.linux.org/' },
    { id: 'java', name: 'Java', img: 'assets/tool-logos/openjdk.svg', url: 'https://openjdk.org/' },
    { id: 'mongodb', name: 'MongoDB', img: 'assets/tool-logos/mongodb.svg', url: 'https://www.mongodb.com/' },
    { id: 'splunk', name: 'Splunk', img: 'assets/tool-logos/splunk.svg', url: 'https://www.splunk.com/' },
    { id: 'jira', name: 'Jira', img: 'assets/tool-logos/jira.svg', url: 'https://www.atlassian.com/software/jira' },
    { id: 'confluence', name: 'Confluence', img: 'assets/tool-logos/confluence.svg', url: 'https://www.atlassian.com/software/confluence' },
    { id: 'hubspot', name: 'HubSpot', img: 'assets/tool-logos/hubspot.svg', url: 'https://www.hubspot.com/' }
  ];
  /* Uniform card size for every item, per request (source height / 2 = rendered height). */
  var CARD_H = 236;
  items.forEach(function (it) { it.height = CARD_H; });

  var ease = 'power3.out', duration = 0.6, stagger = 0.05;
  var animateFrom = 'bottom', scaleOnHover = true, hoverScale = 0.95, blurToFocus = true;

  function getColumns() {
    var w = window.innerWidth;
    if (w >= 1500) return 5;
    if (w >= 1000) return 4;
    if (w >= 600) return 3;
    if (w >= 400) return 2;
    return 1;
  }

  var wrappers = [];
  var hasMounted = false;

  function buildDom() {
    container.innerHTML = '';
    wrappers = [];
    items.forEach(function (it) {
      var wrap = document.createElement('div');
      wrap.className = 'skl-item-wrapper';
      wrap.setAttribute('data-key', it.id);
      var img = document.createElement('div');
      img.className = 'skl-item-img' + (it.badge ? ' skl-badge' : '');
      if (it.badge) {
        var label = document.createElement('span');
        label.className = 'skl-item-name';
        label.textContent = it.name;
        img.appendChild(label);
      } else {
        var el = document.createElement('img');
        el.src = it.img;
        el.alt = it.name + ' logo';
        el.loading = 'lazy';
        var cap = document.createElement('span');
        cap.className = 'skl-item-name';
        cap.textContent = it.name;
        img.appendChild(el);
        img.appendChild(cap);
      }
      wrap.appendChild(img);
      wrap.addEventListener('click', function () { window.open(it.url, '_blank', 'noopener'); });
      if (hasGsap && scaleOnHover && !reduce) {
        wrap.addEventListener('mouseenter', function () {
          gsap.to(wrap, { scale: hoverScale, duration: 0.3, ease: 'power2.out' });
        });
        wrap.addEventListener('mouseleave', function () {
          gsap.to(wrap, { scale: 1, duration: 0.3, ease: 'power2.out' });
        });
      }
      container.appendChild(wrap);
      wrappers.push(wrap);
    });
  }

  function getInitialPosition(item) {
    var rect = container.getBoundingClientRect();
    switch (animateFrom) {
      case 'top': return { x: item.x, y: -200 };
      case 'left': return { x: -200, y: item.y };
      case 'right': return { x: window.innerWidth + 200, y: item.y };
      case 'center': return { x: rect.width / 2 - item.w / 2, y: rect.height / 2 - item.h / 2 };
      default: return { x: item.x, y: window.innerHeight + 200 };
    }
  }

  function layout(animate) {
    var width = container.getBoundingClientRect().width;
    if (!width) return;
    var cols = getColumns();
    var colHeights = new Array(cols).fill(0);
    var columnWidth = width / cols;
    var grid = items.map(function (child) {
      var col = colHeights.indexOf(Math.min.apply(null, colHeights));
      var x = columnWidth * col;
      var h = child.height / 2;
      var y = colHeights[col];
      colHeights[col] += h;
      return Object.assign({}, child, { x: x, y: y, w: columnWidth, h: h });
    });
    var maxH = Math.max.apply(null, colHeights);
    container.style.height = maxH + 'px';

    grid.forEach(function (item, index) {
      var wrap = wrappers[index];
      if (!wrap) return;
      var animProps = { x: item.x, y: item.y, width: item.w, height: item.h };
      if (!hasGsap || reduce) {
        wrap.style.transform = 'translate(' + item.x + 'px,' + item.y + 'px)';
        wrap.style.width = item.w + 'px';
        wrap.style.height = item.h + 'px';
        wrap.style.opacity = '1';
        return;
      }
      if (!hasMounted && animate) {
        var initial = getInitialPosition(item);
        var initState = Object.assign({ opacity: 0, x: initial.x, y: initial.y, width: item.w, height: item.h }, blurToFocus ? { filter: 'blur(10px)' } : {});
        gsap.fromTo(wrap, initState, Object.assign({ opacity: 1 }, animProps, blurToFocus ? { filter: 'blur(0px)' } : {}, { duration: 0.8, ease: 'power3.out', delay: index * stagger }));
      } else {
        gsap.to(wrap, Object.assign({}, animProps, { duration: duration, ease: ease, overwrite: 'auto' }));
      }
    });
    hasMounted = true;
  }

  buildDom();
  var laidOutOnce = false;
  function runLayout(animate) { layout(animate); laidOutOnce = true; }

  if ('IntersectionObserver' in window) {
    var msIo = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting && !laidOutOnce) runLayout(true);
      });
    }, { threshold: 0.1 });
    msIo.observe(container);
  } else {
    runLayout(true);
  }

  var resizeTimer;
  window.addEventListener('resize', function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function () { if (laidOutOnce) layout(false); }, 120);
  });
})();

/* ============ COMPETENCE: FLOWING MENU (React Bits port, vanilla JS + GSAP) ============ */
(function () {
  var hasGsap = typeof gsap !== 'undefined';
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var menu = document.getElementById('competenceMenu');
  if (!menu) return;

  var competence = [
    { text: 'AI & LLM Engineering' },
    { text: 'Data & Business Intelligence', image: 'assets/tool-logos/looker.svg' },
    { text: 'Data Engineering & ETL', image: 'assets/tool-logos/snowflake.svg' },
    { text: 'Databases & SQL', image: 'assets/tool-logos/postgresql.svg' },
    { text: 'Cloud & Infrastructure', image: 'assets/tool-logos/googlecloud.svg' },
    { text: 'Solution & Product Architecture' },
    { text: 'Agile Delivery & Leadership', image: 'assets/tool-logos/jira.svg' },
    { text: 'Business & Analytical Acumen' }
  ];
  var speed = 15;

  function distMetric(x, y, x2, y2) { var dx = x - x2, dy = y - y2; return dx * dx + dy * dy; }
  function closestEdge(mx, my, w, h) {
    return distMetric(mx, my, w / 2, 0) < distMetric(mx, my, w / 2, h) ? 'top' : 'bottom';
  }

  competence.forEach(function (entry) {
    var item = document.createElement('div');
    item.className = 'fm-item';

    var link = document.createElement('div');
    link.className = 'fm-item-link';
    link.textContent = entry.text;
    item.appendChild(link);

    var marquee = document.createElement('div');
    marquee.className = 'fm-marquee';
    var innerWrap = document.createElement('div');
    innerWrap.className = 'fm-marquee-inner-wrap';
    var inner = document.createElement('div');
    inner.className = 'fm-marquee-inner';

    function addParts(n) {
      for (var i = 0; i < n; i++) {
        var part = document.createElement('div');
        part.className = 'fm-marquee-part';
        var span = document.createElement('span');
        span.textContent = entry.text;
        part.appendChild(span);
        if (entry.image) {
          var imgWrap = document.createElement('div');
          imgWrap.className = 'fm-marquee-img';
          var img = document.createElement('img');
          img.src = entry.image;
          img.alt = '';
          imgWrap.appendChild(img);
          part.appendChild(imgWrap);
        }
        inner.appendChild(part);
      }
    }
    addParts(4);
    innerWrap.appendChild(inner);
    marquee.appendChild(innerWrap);
    item.appendChild(marquee);
    menu.appendChild(item);

    var tween = null;
    function setupLoop() {
      var part = inner.querySelector('.fm-marquee-part');
      if (!part) return;
      var contentWidth = part.offsetWidth;
      var viewportWidth = window.innerWidth;
      var needed = Math.ceil(viewportWidth / contentWidth) + 2;
      var reps = Math.max(4, needed);
      var current = inner.querySelectorAll('.fm-marquee-part').length;
      if (reps > current) addParts(reps - current);
      var w = inner.querySelector('.fm-marquee-part').offsetWidth;
      if (hasGsap && !reduce) {
        if (tween) tween.kill();
        tween = gsap.to(inner, { x: -w, duration: speed, ease: 'none', repeat: -1 });
      }
    }
    setTimeout(setupLoop, 60);
    window.addEventListener('resize', function () {
      clearTimeout(item._fmResizeT);
      item._fmResizeT = setTimeout(setupLoop, 150);
    });

    if (hasGsap && !reduce) {
      link.addEventListener('mouseenter', function (ev) {
        var rect = item.getBoundingClientRect();
        var edge = closestEdge(ev.clientX - rect.left, ev.clientY - rect.top, rect.width, rect.height);
        gsap.timeline({ defaults: { duration: 0.6, ease: 'expo' } })
          .set(marquee, { y: edge === 'top' ? '-101%' : '101%' }, 0)
          .set(inner, { y: edge === 'top' ? '101%' : '-101%' }, 0)
          .to([marquee, inner], { y: '0%' }, 0);
      });
      link.addEventListener('mouseleave', function (ev) {
        var rect = item.getBoundingClientRect();
        var edge = closestEdge(ev.clientX - rect.left, ev.clientY - rect.top, rect.width, rect.height);
        gsap.timeline({ defaults: { duration: 0.6, ease: 'expo' } })
          .to(marquee, { y: edge === 'top' ? '-101%' : '101%' }, 0)
          .to(inner, { y: edge === 'top' ? '101%' : '-101%' }, 0);
      });
    }
  });
})();

(function () {
  var fab = document.getElementById('contact-fab');
  var card = document.getElementById('contact-card');
  var emailInput = document.getElementById('contact-email');
  var errorEl = document.getElementById('contact-error');
  var submitBtn = document.getElementById('contact-submit');
  var formWrap = card.querySelector('.contact-form-wrap');
  var greet = document.getElementById('contact-greet');
  var greetLine = document.getElementById('contact-greeting-line');
  var mailtoLink = document.getElementById('contact-mailto');

  fab.addEventListener('click', function () {
    var isOpen = document.body.classList.toggle('contact-open');
    fab.setAttribute('aria-expanded', String(isOpen));
  });

  function validEmail(v) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
  }

  function submit() {
    var val = emailInput.value.trim();
    if (!validEmail(val)) {
      emailInput.classList.add('error');
      errorEl.classList.add('show');
      return;
    }
    emailInput.classList.remove('error');
    errorEl.classList.remove('show');

    var hour = new Date().getHours();
    var greetText = hour < 12 ? 'Good morning' : (hour < 18 ? 'Good afternoon' : 'Good evening');
    greetLine.textContent = greetText + '! Thanks for saying hello.';

    var subject = encodeURIComponent('Hello from your portfolio');
    var body = encodeURIComponent('Hi Shashank,\n\nI came across your portfolio and wanted to reach out.\n\nMy email: ' + val + '\n\n');
    mailtoLink.href = 'mailto:shashankreddy1606@gmail.com?subject=' + subject + '&body=' + body;

    formWrap.classList.add('hidden');
    greet.classList.add('active');
  }

  submitBtn.addEventListener('click', submit);
  emailInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') submit();
  });

  document.addEventListener('click', function (e) {
    if (!document.body.classList.contains('contact-open')) return;
    if (card.contains(e.target) || fab.contains(e.target)) return;
    document.body.classList.remove('contact-open');
    fab.setAttribute('aria-expanded', 'false');
  });
})();
