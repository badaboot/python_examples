import marimo

__generated_with = "0.17.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    # Define the HTML and JavaScript together
    c_note_component = mo.iframe(
        """
<style>
  .star-btn {
    background: none;
    border: none;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    padding: 0;
    transition: transform 0.1s ease-out;
  }
  .star-btn svg {
    transition: transform 0.1s;
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
  }
  .star-btn:active svg {
    transform: scale(1.25);
    filter: drop-shadow(0 0 14px currentColor);
  }
  .star-label {
    font-size: 20px;
    font-weight: bold;
    font-family: sans-serif;
  }
  .animate {
    animation: growAndFly 0.6s forwards ease-in;
  }
  /* The animation class */
  @keyframes growAndFly {
    0% {
      transform: scale(1) translateY(0);
      opacity: 1;
    }
    50% {
      transform: scale(1.5) translateY(-20px);
      opacity: 1;
    }
    100% {
      transform: scale(1) translateY(0);
      opacity: 1;
    }
  }
</style>

<div style="text-align: center; font-family: sans-serif; padding: 24px">
  <h2>✨ Twinkle Twinkle Little Star ✨</h2>
  <p style="color: #888; font-size: 14px">
    Press and hold a star to play its note, or play using keyboard
  </p>

  <div
    style="
      display: flex;
      justify-content: center;
      gap: 20px;
      flex-wrap: wrap;
      margin: 28px 0;
    "
  >
    <!-- C - Red -->
    <button class="star-btn" id="C">
      <svg width="80" height="80" viewBox="0 0 100 100">
        <polygon
          points="50,5 61,35 95,35 68,57 79,91 50,70 21,91 32,57 5,35 39,35"
          fill="#FF4444"
        />
      </svg>
      <span class="star-label" style="color: #ff4444">C</span>
    </button>

    <!-- D - Orange -->
    <button class="star-btn" id="D">
      <svg width="80" height="80" viewBox="0 0 100 100">
        <polygon
          points="50,5 61,35 95,35 68,57 79,91 50,70 21,91 32,57 5,35 39,35"
          fill="#FF8C00"
        />
      </svg>
      <span class="star-label" style="color: #ff8c00">D</span>
    </button>

    <!-- E - Yellow -->
    <button class="star-btn" id="E">
      <svg width="80" height="80" viewBox="0 0 100 100">
        <polygon
          points="50,5 61,35 95,35 68,57 79,91 50,70 21,91 32,57 5,35 39,35"
          fill="#FFD700"
        />
      </svg>
      <span class="star-label" style="color: #ffd700">E</span>
    </button>

    <!-- F - Green -->
    <button class="star-btn" id="F">
      <svg width="80" height="80" viewBox="0 0 100 100">
        <polygon
          points="50,5 61,35 95,35 68,57 79,91 50,70 21,91 32,57 5,35 39,35"
          fill="#44BB44"
        />
      </svg>
      <span class="star-label" style="color: #44bb44">F</span>
    </button>

    <!-- G - Blue -->
    <button class="star-btn" id="G">
      <svg width="80" height="80" viewBox="0 0 100 100">
        <polygon
          points="50,5 61,35 95,35 68,57 79,91 50,70 21,91 32,57 5,35 39,35"
          fill="#4488FF"
        />
      </svg>
      <span class="star-label" style="color: #4488ff">G</span>
    </button>

    <!-- A - Purple -->
    <button class="star-btn" id="A">
      <svg width="80" height="80" viewBox="0 0 100 100">
        <polygon
          points="50,5 61,35 95,35 68,57 79,91 50,70 21,91 32,57 5,35 39,35"
          fill="#9B59B6"
        />
      </svg>
      <span class="star-label" style="color: #9b59b6">A</span>
    </button>
  </div>
  <div>
    <div
      style="
        background: #f5f5f5;
        border-radius: 12px;
        padding: 16px;
        display: inline-block;
      "
    >
      <p
        style="
          margin: 0 0 6px 0;
          font-weight: bold;
          font-size: 13px;
          color: #555;
        "
      >
        🎵 Song sequence:
      </p>
      <p style="margin: 0; font-size: 15px; letter-spacing: 1px; color: #333">
        C C G G A A G — F F E E D D C — G G F F E E D — G G F F E E D — C C G G
        A A G — F F E E D D C
      </p>

      <script>
        // Ensure context is initialized inside the marimo environment
        let audioCtx = new (window.AudioContext || window.webkitAudioContext)();

        const notes = {
          C: 261.63,
          D: 293.66,
          E: 329.63,
          F: 349.23,
          G: 392.0,
          A: 440.0,
        };
        const buttons = document.querySelectorAll("button");
        for (let button of buttons) {
          button.addEventListener("click", () => {
            playTone(notes[button.id.toUpperCase()]);
            button.classList.add("animate");

            // remove the class after the animation finishes
            button.addEventListener(
              "animationend",
              () => {
                button.classList.remove("animate");
              },
              { once: true },
            ); // {once: true} ensures this listener only runs once
          });
        }

        function playTone(frequency) {
          const oscillator = audioCtx.createOscillator();
          const gainNode = audioCtx.createGain();

          oscillator.type = "sine";
          oscillator.frequency.setValueAtTime(frequency, audioCtx.currentTime);

          oscillator.connect(gainNode);
          gainNode.connect(audioCtx.destination);

          oscillator.start();

          gainNode.gain.setValueAtTime(0.5, audioCtx.currentTime);
          gainNode.gain.exponentialRampToValueAtTime(
            0.001,
            audioCtx.currentTime + 0.5,
          );

          oscillator.stop(audioCtx.currentTime + 0.5);
        }
        // need this otherwise app mode does not listen for keyboard events
        const targetWindows = [window, window.parent];
        targetWindows.forEach((win) => {
          try {
            win.addEventListener("keydown", (event) => {
              const key = event.key.toUpperCase();
              if (notes[key]) {
                document.getElementById(key).click();
              }
            });
          } catch (e) {
            // Catch SecurityErrors if origins differ during local dev testing
            console.warn("Could not attach listener to parent window:", e);
          }
        });
      </script>
    </div>
  </div>
</div>
        """
    )

    # Display the component in the notebook
    c_note_component
    return


if __name__ == "__main__":
    app.run()
