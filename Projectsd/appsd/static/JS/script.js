

const menuWrapper = document.getElementById('menuWrapper');
    const dropdownMenu = document.getElementById('dropdownMenu');

    menuWrapper.addEventListener('mouseenter', () => {
        dropdownMenu.style.display = 'block';
    });

    menuWrapper.addEventListener('mouseleave', () => {
        dropdownMenu.style.display = 'none';
    });

// User account dashboard Scripts

const navItems = document.querySelectorAll('.nav li');
const sections = document.querySelectorAll('.section');
const sidebar = document.getElementById('sidebar');
const toggleBtn = document.getElementById('toggleBtn');

navItems.forEach(item => {
  item.addEventListener('click', () => {
    const target = item.getAttribute('data-section');

    sections.forEach(section => {
      section.classList.remove('active');
    });

    document.getElementById(target).classList.add('active');

    // Hide sidebar on mobile after selection
    if (window.innerWidth <= 768) {
      sidebar.classList.add('hidden');
    }
  });
});

toggleBtn.addEventListener('click', () => {
  sidebar.classList.toggle('hidden');
});