// clickSound.js

let introPlayed = false;

// --- Play intro sound once after first interaction ---
document.addEventListener('click', () => {
  if (!introPlayed) {
    introPlayed = true;
    const intro = new Audio('/assets/intro.mp3');
    intro.volume = 0;
    intro.play().then(() => {
      // Fade in over 3 seconds
      const fadeDuration = 3000;
      const stepTime = 100;
      const volumeStep = 0.5 / (fadeDuration / stepTime);
      const fadeIn = setInterval(() => {
        if (intro.volume < 0.5) {
          intro.volume = Math.min(0.5, intro.volume + volumeStep);
        } else {
          clearInterval(fadeIn);
        }
      }, stepTime);
    }).catch(err => console.log("Intro play blocked:", err));
  }

  // --- Play gong sound on every click ---
  const gong = new Audio('/assets/gong.mp3');
  gong.volume = 0.3;
  gong.play().catch(err => {
    console.log("Gong play blocked:", err);
  });
});
