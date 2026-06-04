# Copyright 2024 Marimo. All rights reserved.

import marimo

__generated_with = "0.17.6"
app = marimo.App()


@app.cell
def _():
    import altair as alt
    import polars as pl

    # 1. Load the data from the CSV file
    # (And add the constant column 'one' to enable dynamic circle stacking)
    data = pl.read_csv("static/name_ethnicity.csv").with_columns(
        pl.lit(1).alias("one")
    )

    dot_plot = (
        alt.Chart(data)
        .mark_circle(
            size=600,  # Size of the dots
            opacity=0.9,
            stroke="white",  # Crisp white outline to separate stacked circles
            strokeWidth=1,
        )
        .encode(
            # X-Axis is now grouped by Ethnicity
            x=alt.X(
                "ethnicity:N",
                title="Ethnicity",
                axis=alt.Axis(
                    labelAngle=-30, grid=False
                ),  # Angled slightly for readability
            ),
            # Y-Axis stacks the circles perfectly on top of each other
            y=alt.Y("sum(one):Q", title=None, stack=True, axis=None),
            # Color breakdown is now by Category
            color=alt.Color(
                "category:N", title="Category", scale=alt.Scale(scheme="tableau10")
            ),
            # Ensures identical categories clump together sequentially inside each stack
            order=alt.Order("category:N", sort="ascending"),
            tooltip=[
                alt.Tooltip("name:N", title="Name"),
                alt.Tooltip("ethnicity:N", title="Ethnicity"),
                alt.Tooltip("category:N", title="Category"),
            ],
        )
        .properties(
            width=600,
            height=300,
            title=alt.TitleParams(
                text="Character Ethnicity + Category",
                anchor="start",
                frame="group",
            ),
        )
        .configure_view(strokeWidth=0)
        .configure_legend(offset=-50, titleFontSize=16, labelFontSize=14)
        .configure_title(dy=-20, fontSize=24, anchor="middle")
    ).configure_axis(
        labelFontSize=14,
        titleFontSize=16
    )

    dot_plot.show()
    return alt, pl


@app.cell
def _(alt, pl):
    import marimo as mo
    # import polars as pl
    # import altair as alt
    import numpy as np

    # 1. Load and clean the dataset
    df = pl.read_csv("static/name_ethnicity.csv")
    df = df.with_columns([
        pl.col("name").str.strip_chars(),
        pl.col("ethnicity").str.strip_chars()
    ]).sort('ethnicity')

    # 2. Compute the base grid geometry
    columns = 5
    num_rows = df.height

    grid_x = [i % columns for i in range(num_rows)]
    grid_y = [i // columns for i in range(num_rows)]

    df = df.with_columns([
        pl.Series('grid_x', grid_x),
        pl.Series('grid_y', grid_y)
    ])

    # 3. Calculate raw hexagonal packing positions
    df = df.with_columns([
        pl.when(pl.col('grid_y') % 2 == 1)
        .then(pl.col('grid_x') + 0.5)
        .otherwise(pl.col('grid_x'))
        .alias('raw_x'),
    
        (pl.col('grid_y') * 0.82).alias('raw_y') # Adjusted vertical spacing
    ])

    # 4. CENTER THE COORDINATES (New Step)
    # Find the midpoints of the generated cluster and shift them to zero
    mean_x = df['raw_x'].mean()
    mean_y = df['raw_y'].mean()

    df = df.with_columns([
        (pl.col('raw_x') - mean_x).alias('x'),
        (pl.col('raw_y') - mean_y).alias('y')
    ])

    # 5. Build the tight-packed Bubble Chart
    # We set symmetric scale domains around 0 so the chart container centers the data
    max_range = 3.5  # This creates an invisible boundary window from -3.5 to +3.5

    bubbles = alt.Chart(df).mark_circle(size=5200, opacity=1.0).encode(
        x=alt.X('x:Q', axis=None, scale=alt.Scale(domain=[-2, max_range])),
        y=alt.Y('y:Q', axis=None, scale=alt.Scale(reverse=True, domain=[-2, max_range])),
        color=alt.Color(
            'ethnicity:N', 
            scale=alt.Scale(scheme='category10'), 
            title="Ethnicity"
        ),
        tooltip=['name', 'ethnicity']
    )

    # 6. Build the Text Label Layer
    labels = alt.Chart(df).mark_text(
        baseline='middle', 
        align='center',
        color='white', 
        fontWeight='bold', 
        fontSize=12
    ).encode(
        x='x:Q',
        y=alt.Y('y:Q', scale=alt.Scale(reverse=True)),
        text='name:N'
    )

    # 7. Combine layers
    packing_plot = (bubbles + labels).properties(
        width=480,
        height=400,
        title=alt.TitleParams(
            text="Character Name + Ethnicity",
            anchor='middle',
            fontSize=24
        )
    ).configure_view(
        strokeWidth=0
    ).configure_legend(
        offset=-40 ,
         titleFontSize=16,  
        labelFontSize=14   
    ).configure_title(
        dy=-20,
    )

    packing_plot.show()
    return


if __name__ == "__main__":
    app.run()
