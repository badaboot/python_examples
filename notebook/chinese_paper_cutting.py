import marimo

__generated_with = "0.17.6"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import io
    import numpy as np
    return io, mo, np, plt


@app.cell
def _(mo):
    folds = mo.ui.slider(start=4, stop=12, step=2, value=8, label="Folds (Symmetry)")
    intricacy = mo.ui.slider(start=1, stop=5, step=1, value=3, label="Lattice Intricacy")
    edge_style = mo.ui.dropdown(options=["Smooth", "Spiked", "Scalloped"], value="Spiked", label="Border Cut")

    paper_controls = mo.vstack([
        mo.md("### ✂️ Jianzhi (剪纸) Studio"),
        folds,
        intricacy,
        edge_style
    ])
    paper_controls
    return edge_style, folds, intricacy


@app.cell
def _(edge_style, folds, intricacy, io, mo, np, plt):
    # 1. Base grid for the paper template
    theta = np.linspace(0, 2 * np.pi, 2000)

    # 2. Simulate the traditional border cuts
    if edge_style.value == "Spiked":
        r_border = 1.0 - 0.05 * np.abs(np.sin(folds.value * 2 * theta))
    elif edge_style.value == "Scalloped":
        r_border = 1.0 - 0.04 * (np.sin(folds.value * theta) ** 2)
    else: # Smooth
        r_border = np.ones_like(theta)

    # 3. Create negative space layers (the internal "cuts")
    # We overlay multiple frequency waves to simulate intricate lattice cutouts
    r_cuts = np.copy(r_border)
    for i in range(1, intricacy.value + 1):
        # This creates interconnected lace-like voids characteristic of paper cutting
        r_cuts -= 0.15 * (np.sin(folds.value * i * theta) ** 2) * (1 / i)

    # Convert our "cut" paper boundaries to Cartesian coordinates
    x = r_cuts * np.cos(theta)
    y = r_cuts * np.sin(theta)

    # 4. Render the paper cut
    fig, ax = plt.subplots(figsize=(7, 7))

    # Traditional Chinese Crimson Red on crisp white paper background
    paper_color = "#D32F2F" 
    ax.fill(x, y, color=paper_color, alpha=0.95, edgecolor=paper_color, linewidth=1)

    # Add a delicate inner gold or hollow core for depth if intricacy is high
    if intricacy.value > 2:
        ax.plot(x * 0.4, y * 0.4, color='white', linewidth=2)

    # Styling: clean canvas mimicking physical paper display
    fig.patch.set_facecolor('#FAFAFA') 
    ax.set_facecolor('#FAFAFA')
    ax.axis('off')
    ax.set_aspect('equal')

    # 5. Export to Marimo
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.2, facecolor=fig.get_facecolor())
    buf.seek(0)
    plt.close(fig)

    mo.center(mo.image(src=buf))
    return


if __name__ == "__main__":
    app.run()
