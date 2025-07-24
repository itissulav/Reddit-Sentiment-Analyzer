document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('analyze-form');
  const loadingBarSection = document.getElementById('loading-bar');

  form.addEventListener('submit', () => {
    // Show the loading bar when the form is submitted
    loadingBarSection.classList.remove('hidden');
  });
});
