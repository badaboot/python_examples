import marimo

__generated_with = "0.17.6"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import io
    return mo, plt, io


@app.cell
def _(mo):
    import numpy as np
    # Create interactive widgets for the artist
    num_petals = mo.ui.slider(start=3, stop=30, step=1, value=8, label="Number of Petals")
    frequency = mo.ui.slider(start=1, stop=10, step=0.1, value=3.0, label="Wave Frequency")
    color_theme = mo.ui.dropdown(options=["magma", "viridis", "plasma", "inferno", "ocean"], value="plasma", label="Color Palette")

    # Group them together in a nice sidebar or stack
    controls = mo.vstack([
        mo.md("### 🎨 Art Controls"),
        num_petals,
        frequency,
        color_theme
    ])
    controls
    return num_petals, frequency, color_theme


@app.cell
def spiral_logic(np, plt, io, num_petals, frequency, color_theme, mo):
    theta = np.linspace(0, 2 * np.pi, 1000)
    r = np.sin(num_petals.value * theta) + 0.5 * np.cos(frequency.value * num_petals.value * theta)


    x = r * np.cos(theta)
    y = r * np.sin(theta)


    fig, ax = plt.subplots(figsize=(6, 6))


    cmap = plt.get_cmap(color_theme.value)
    art_color = cmap(0.6)


    ax.plot(x, y, color='white', linewidth=1.5)
    ax.fill(x, y, color=art_color, alpha=0.4)


    ax.set_facecolor('#111111')
    fig.patch.set_facecolor('#111111')
    ax.axis('off')  # Instantly hides all borders, ticks, and labels


    ax.set_aspect('equal') 

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, facecolor='#111111')
    buf.seek(0)
    plt.close(fig)


    mo.center(mo.image(src=buf))

if __name__ == "__main__":
    app.run()
