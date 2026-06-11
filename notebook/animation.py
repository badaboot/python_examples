import marimo

__generated_with = "0.17.6"
app = marimo.App()


@app.cell
def _():
    import matplotlib.pyplot as plt
    import numpy as np
    return np, plt


@app.cell
def _():
    # Slider acts as a timeline tracking the drawing progression from 0% to 100%
    import marimo as mo
    time_slider = mo.ui.slider(
        start=0, stop=100, step=1, value=0, label="Time Progress"
    )

    mo.md(
        f"""
        # Inside-Out Procedural Spiral
        Move the slider forward to watch the outer edges draw first, shrinking down to a center point.

        {time_slider}
        """
    )
    return mo, time_slider


@app.cell
def spiral_logic(np, plt, time_slider):
    # 1. SETUP CLEAN MATPLOTLIB CANVAS
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-12, 12)
    ax.set_ylim(-12, 12)
    ax.set_aspect("equal")
    ax.axis("off")

    # 2. GENERATE PROCEDURAL SPIRAL COORDINATES
    current_step = time_slider.value

    if current_step == 0:
        # START STATE: No spiral line drawn yet. 
        # The dot starts at the outer edge (Radius = 10, Angle = 0)
        dot_x = 10.0
        dot_y = 0.0
    else:
        # Create a timeline array matching the current slider position
        t = np.linspace(0, current_step, current_step)

        # Radius shrinks from 10 down to 0 over the 100-step timeline
        radius = 10 - (t * 0.1)
        angle = t * 0.5 

        # Calculate all coordinate paths
        x_coords = radius * np.cos(angle)
        y_coords = radius * np.sin(angle)

        # Draw the trailing spiral line
        ax.plot(x_coords, y_coords, color="black", lw=2)

        # TIP TRACKING: Grab the last item [-1] in the array to get the moving tip
        dot_x = x_coords[-1]
        dot_y = y_coords[-1]

    # 3. DRAW THE DOT AT THE SPIRAL TIP
    # This renders at (10, 0) at the start and moves to (0, 0) at the end
    ax.plot(dot_x, dot_y, marker="o", color="black", markersize=10)

    # Output canvas object
    fig
    return


@app.cell
def _(mo):
    mo.image(src="static/duncan_opium.jpg")
    return


if __name__ == "__main__":
    app.run()
