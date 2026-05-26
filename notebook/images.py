# Copyright 2024 Marimo. All rights reserved.

import marimo

__generated_with = "0.17.6"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    _src = (
        "static/owl.jpeg"
        # "/Users/annyhe/workspace/py_examples/notebook/static/owl.jpeg"
    )
    mo.image(src=_src, width="180px", height="180px", rounded=True)
    return (mo,)


@app.cell
def _(mo):
    _src = "https://upload.wikimedia.org/wikipedia/commons/8/8c/Ivan_Ili%C4%87-Chopin_-_Prelude_no._1_in_C_major.ogg"
    mo.audio(_src)
    return

@app.cell
def _(mo, pl):
    chick_df = pl.read_csv('static/chickweight.csv')
    mo.inspect(chick_df)
    return (chick_df,)


@app.cell
def _(chick_df, pl):
    import altair as alt
    agg = chick_df.group_by("Time", "Diet").agg(pl.col("weight").mean())

    p1 = alt.Chart(chick_df).mark_point(color="gray", fill="gray").encode(x="Time", y="weight")
    p2 = alt.Chart(agg).mark_line().encode(x="Time", y="weight", color="Diet:N")

    chicken_chart = (p1 + p2).properties(title="weight distribution over time")
    chicken_chart.interactive()
    return (alt,)


@app.cell
def _(alt, chick_df, pl):
    df_doom = chick_df.with_columns(indicator=pl.len().over(pl.col("Chick")) != 12)

    _p1 = alt.Chart(df_doom).mark_line(color="gray").encode(x="Time", y="weight", detail="Chick")
    _p2 = (
        alt.Chart(df_doom.filter(pl.col("indicator")))
        .mark_line(color="red")
        .encode(x="Time", y="weight", detail="Chick")
    )

    (_p1 + _p2).properties(title="Good use of the color red here.")
    return


@app.cell
def _():
    import anywidget
    import traitlets

    class CounterWidget(anywidget.AnyWidget):
        _esm = "index.js"
        _css = "index.css"
        count = traitlets.Int(0).tag(sync=True)

    CounterWidget(count=42)
    return


if __name__ == "__main__":
    app.run()
