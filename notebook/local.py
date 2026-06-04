# Copyright 2024 Marimo. All rights reserved.

import marimo

__generated_with = "0.17.6"
app = marimo.App()


@app.cell
def _(mo):
    mo.md("""
    <h1>Project 100 reach outs</h1>
    """)
    return


@app.cell
def _():
    import polars as pl
    df = pl.read_csv('static/reach_out_anonymized.csv')
    # 2. Cast string column to Date with a specific format
    df = df.with_columns(
        pl.col("date").str.to_date("%m/%d/%Y"),
    )
    return df, pl


@app.cell
def _(df):
    import marimo as mo
    # chart_data = (
    #     df.with_columns(
    #         (pl.col("reaction (y/n)") == "y").alias("reaction_bool")
    #     )
    #     .group_by("reaction_bool")
    #     .agg(pl.len().alias("count"))
    # )

    # Displaying the variable in a large font
    earliest = df["date"].min()
    mo.md(f"<h3>Since <span style='background-color: #FFFF00'>{earliest}</span> I have reached out to <span style='background-color: #FFFF00'>{df.height}</span> people</h3>")
    return (mo,)


@app.cell
def _(df, pl):
    import altair as alt

    # df = pl.read_csv("networking.csv")
    chart_data = (
        df.with_columns(
            (pl.col("reaction (y/n)") == "y").alias("reaction_bool")
        )
        .group_by("reaction_bool")
        .agg(pl.len().alias("count"))
        .with_columns(
            pl.when(pl.col("reaction_bool"))
            .then(pl.lit("Yes"))
            .otherwise(pl.lit("No reaction"))
            .alias("label")
        )
    )
 
    base_1 = alt.Chart(chart_data).encode(
        theta=alt.Theta("count:Q", stack=True),
        color=alt.Color(
            "label:N",
            scale=alt.Scale(
                domain=["Yes", "No reaction"],
                range=["#1a7fb8", "#cce5f5"],
            ),
            legend=alt.Legend(
                title=None,
                orient="right",
                labelFontSize=13,
                symbolSize=150,
            ),
        ),
        tooltip=[
            alt.Tooltip("label:N", title="Reaction"),
            alt.Tooltip("count:Q", title="Count"),
        ],
    )
 
    pie = base_1.mark_arc(outerRadius=150, color="black")
 
    text = base_1.mark_text(radius=180, fontSize=14, fontWeight="bold").encode(
        text=alt.Text("count:Q"),
         color=alt.value("black")
    )
 
    chart = (
        (pie + text)
        .properties(
            title=alt.TitleParams(
                text="Networking Contacts: Reaction Breakdown",
                fontSize=16,
                anchor="middle",
            ),
            width=400,
            height=400,
        )
    )
    chart.show()
    return (alt,)


@app.cell
def _(alt, df, pl):
    max_val = 10  # Adjust this depending on your absolute maximum expected reach-outs

    result = (
        df.sort("date")
        .group_by(pl.col("date").dt.week().alias("week"))
        .agg(
            # 1. Get a representative date from the group to calculate the week boundaries
            pl.col("date").first().alias("temp_date"),
            pl.len().alias("len")
        )
        .with_columns(
            # 2. Truncate to Monday (start of week)
            pl.col("temp_date").dt.truncate("1w").alias("start_of_week"),
        )
        .with_columns(
            # 3. Add 6 days to get Sunday (end of week)
            pl.col("start_of_week").dt.offset_by("6d").alias("end_of_week")
        )
        .with_columns(
            # 4. Format them into the "M/D/YYYY - M/D/YYYY" format
            pl.format(
                "{}/{} - {}/{}",
                pl.col("start_of_week").dt.month(),
                pl.col("start_of_week").dt.day(),
                pl.col("end_of_week").dt.month(),
                pl.col("end_of_week").dt.day(),
            ).alias("date")
        )
        # 5. Clean up temporary columns
        # .drop("temp_date", "start_of_week", "end_of_week")
    ) 

    # 2. Base chart split by weeks on the Y-axis
    base = alt.Chart(result).encode(
        y=alt.Y("week:N", title="Week", axis=alt.Axis(labels=True, tickSize=0))
    )

    # 3. Layer 1: Background bands (Red, Yellow, Green)
    # We map the ranges: 0-3 (Red), 3-6 (Yellow), 6-max_val (Green)
    background_bands = base.mark_bar(opacity=0.35, size=30).encode(
        x=alt.X("start:Q", scale=alt.Scale(domain=[0, max_val]), title="Reach outs count"),
        x2="end:Q",
        color=alt.Color("color:N", scale=None)  # scale=None reads hex codes directly
    ).transform_calculate(
        # Create 3 rows of data structurally for every week to layer the colors
        start="[0, 3, 6]",
        end=f"[3, 6, {max_val}]",
        color="['#ff4d4d', '#ffcc00', '#2bc443']" # Red, Yellow, Green hex values
    ).transform_flatten(["start", "end", "color"])

    # 4. Layer 2: Actual Performance Bar (The "Bullet")
    # This is a thinner, dark bar sitting perfectly centered on top of the bands
    actual_bar = base.mark_bar(color="#2a2a2a", size=12).encode(
        x=alt.X("len:Q"),
        tooltip=["week", "len", "date"]
    )

    # 5. Combine the layers using the '+' operator
    bullet_chart = (
        (background_bands + actual_bar)
        .properties(
            title="Reach outs by Week (Bullet Chart)",
            width=500,
            height=alt.Step(50)  # Dynamically scales the chart height based on number of weeks
        )
        .configure_view(strokeWidth=0)
    )
    bullet_chart.show()
    return


if __name__ == "__main__":
    app.run()
