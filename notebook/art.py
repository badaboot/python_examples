# Copyright 2024 Marimo. All rights reserved.

import marimo

__generated_with = "0.17.6"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import polars as pl
    objects_df = pl.read_csv('static/objects.csv')
    mo.inspect(objects_df)
    return mo, pl


@app.cell
def _(mo, pl):

    import altair as alt

    df = pl.read_csv('static/objects.csv')
    df_clean = df.with_columns(
        pl.col("beginyear").cast(pl.Float64, strict=False)
    ).filter(
        pl.col("beginyear").is_not_null() &
        (pl.col("beginyear") > 0) &
        (pl.col("beginyear") < 2100)
    )
    # Clean up - beginyear can have nulls or weird values
    df_clean = df.filter(pl.col("beginyear").is_not_null())

    chart = alt.Chart(df_clean).mark_bar().encode(
        alt.X("beginyear:Q", bin=alt.Bin(maxbins=50), title="Begin Year", scale=alt.Scale(domain=[1200, 2100])),
        alt.Y("count()", title="Number of Objects").scale(type="log"),
        tooltip=["count()"]
    ).properties(
        width=700,
        height=400,
        title="Collection Objects by Begin Year"
    )

    mo.ui.altair_chart(chart)
    return alt, df_clean


@app.cell
def _(df_clean, mo):
    # Cell 2: slider
    year_range = mo.ui.range_slider(
        start=int(df_clean["beginyear"].min()),
        stop=int(df_clean["beginyear"].max()),
        value=[1800, 2000],
        label="Year range",
        show_value=True,
        full_width=True,
        debounce=True  
    )
    year_range
    mo.hstack([
        mo.md(str(int(df_clean["beginyear"].min()))),
        year_range,
        mo.md(str(int(df_clean["beginyear"].max()))),
    ], align="center")
    return (year_range,)


@app.cell
def _():
    return


@app.cell
def _(alt, df_clean, mo, pl, year_range):
    # Cell 3: chart (reacts to slider automatically)
    top_classifications = (
        df_clean
        .group_by("classification")
        .len()
        .sort("len", descending=True)
        .head(8)
        .get_column("classification")
        .to_list()
    )


    df_filtered = (
        df_clean
        .filter(
            (pl.col("beginyear") >= year_range.value[0]) &
            (pl.col("beginyear") <= year_range.value[1]) &
            pl.col("classification").is_in(top_classifications)
        )
        .with_columns(pl.col("beginyear").cast(pl.Int32))
    )

    # define this once, outside the chart cell
    classification_colors = alt.Scale(
        domain=top_classifications,
        scheme="tableau10"
    )

    chart_two = alt.Chart(df_filtered).mark_bar().encode(
        alt.X("beginyear:Q", bin=alt.Bin(maxbins=50), title="Begin Year"),
        alt.Y("count()", title="Number of Objects"),
            alt.Color("classification:N",
                  legend=alt.Legend(title="Classification", orient="right", labelLimit=200),
                  scale=classification_colors),
        tooltip=["classification:N", "count()", "beginyear:Q"]
    ).properties(
        width=500,
        height=400,
        title="Collection Objects by Begin Year & Classification"
    )

    mo.ui.altair_chart(chart_two)
    return


if __name__ == "__main__":
    app.run()
