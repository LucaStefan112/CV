/* ============================================
   Navbar scroll behavior
   ============================================ */
(function () {
  const navbar = document.getElementById('navbar');
  const navToggle = document.getElementById('navToggle');
  const navLinks = document.getElementById('navLinks');
  const allNavLinks = document.querySelectorAll('.nav-link');

  // Scroll — add background to navbar
  function handleNavScroll() {
    if (window.scrollY > 60) {
      navbar.classList.add('scrolled');
    } else {
      navbar.classList.remove('scrolled');
    }
  }

  window.addEventListener('scroll', handleNavScroll, { passive: true });
  handleNavScroll();

  // Mobile hamburger toggle
  navToggle.addEventListener('click', function () {
    navToggle.classList.toggle('open');
    navLinks.classList.toggle('open');
  });

  // Close mobile menu on link click
  allNavLinks.forEach(function (link) {
    link.addEventListener('click', function () {
      navToggle.classList.remove('open');
      navLinks.classList.remove('open');
    });
  });

  // Close mobile menu on outside click
  document.addEventListener('click', function (e) {
    if (
      navLinks.classList.contains('open') &&
      !navLinks.contains(e.target) &&
      !navToggle.contains(e.target)
    ) {
      navToggle.classList.remove('open');
      navLinks.classList.remove('open');
    }
  });

  /* ============================================
     Scroll spy — highlight active nav link
     ============================================ */
  var sections = document.querySelectorAll('.section');

  function updateActiveLink() {
    var scrollPos = window.scrollY + 150;

    sections.forEach(function (section) {
      var id = section.getAttribute('id');
      var top = section.offsetTop;
      var height = section.offsetHeight;

      if (scrollPos >= top && scrollPos < top + height) {
        allNavLinks.forEach(function (link) {
          link.classList.remove('active');
          if (link.getAttribute('href') === '#' + id) {
            link.classList.add('active');
          }
        });
      }
    });
  }

  window.addEventListener('scroll', updateActiveLink, { passive: true });
  updateActiveLink();

  /* ============================================
     Hero sequential fade-in
     ============================================ */
  var heroElements = document.querySelectorAll('.anim-hero');

  heroElements.forEach(function (el) {
    var delay = parseInt(el.getAttribute('data-delay'), 10) || 0;
    setTimeout(function () {
      el.classList.add('visible');
    }, 300 + delay * 200);
  });

  /* ============================================
     Intersection Observer — reveal on scroll
     ============================================ */
  var revealElements = document.querySelectorAll('.reveal');

  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1 }
    );

    revealElements.forEach(function (el) {
      observer.observe(el);
    });
  } else {
    // Fallback: show all elements immediately
    revealElements.forEach(function (el) {
      el.classList.add('visible');
    });
  }

  /* ============================================
     Smooth scroll for anchor links (fallback)
     ============================================ */
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      var targetId = this.getAttribute('href');
      if (targetId === '#') return;
      var target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
})();
