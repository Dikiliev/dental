
document.getElementById('profile-nav').addEventListener('mouseover', () => {
  const sideMenu = document.getElementById('side-menu')

  sideMenu.classList.toggle('active', true);
});

document.getElementById('profile-nav').addEventListener('mouseout', () => {
  const sideMenu = document.getElementById('side-menu')

  sideMenu.classList.toggle('active', false);
});