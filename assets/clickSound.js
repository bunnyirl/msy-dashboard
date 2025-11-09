// clickSound.js

// --- Play intro sound with fade-in on page load ---
window.addEventListener('load', () => {
  const intro = new Audio('/assets/intro.mp3');
  intro.volume = 0; // start silent
  intro.play().catch(err => {
    console.log("Autoplay blocked until user interacts with the page.");
  });

  // Fade in over 3 seconds
  const fadeDuration = 3000; // milliseconds
  const stepTime = 100; // how often to increase volume (ms)
  const volumeStep = 0.5 / (fadeDuration / stepTime); // target 50% volume

  const fadeIn = setInterval(() => {
    if (intro.volume < 0.5) {
      intro.volume = Math.min(0.5, intro.volume + volumeStep);
    } else {
      clearInterval(fadeIn);
    }
  }, stepTime);
});

// --- Play gong sound on every click ---
document.addEventListener('click', () => {
  const gong = new Audio('/assets/gong.mp3');
  gong.volume = 0.3;
  gong.play().catch(err => {
    console.log("Audio play blocked until user interacts with the page.");
  });
});
