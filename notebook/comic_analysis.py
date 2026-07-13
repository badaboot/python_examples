# Copyright 2024 Marimo. All rights reserved.

import marimo

__generated_with = "0.17.6"
app = marimo.App()


@app.cell
def _():
    import altair as alt
    import polars as pl
    import urllib.request
    import json

    url = 'https://raw.githubusercontent.com/badaboot/gatsby-starter-minimal-ts/refs/heads/master/src/metadata/comics.json'

    with urllib.request.urlopen(url) as response:
        raw_data = json.loads(response.read().decode())

    # View the JSON structure reactively using marimo's native tree viewer
    # mo.tree(raw_data)

    # 2. Process data with Polars
    df = (
        pl.DataFrame(raw_data)
        # Explode the nested category arrays into individual rows
        .explode("categories")
        # Group by date and category to count occurrences
        .group_by(["created", "categories"])
        .agg(pl.len().alias("count"))
        # Ensure chronological sorting
        .sort("created")
    )

    sorted_categories = sorted(df["categories"].unique().to_list())

    # 3. Build the Altair Stacked Bar Chart with explicit ordering
    stacked_bar = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X(
                "created:O", 
                title="Created Date",
                axis=alt.Axis(labelAngle=-45)
            ),
            y=alt.Y(
                "count:Q", 
                title="Comic count"
            ),
            color=alt.Color(
                "categories:N", 
                title="Category", 
                scale=alt.Scale(
                    scheme="category10",
                    domain=sorted_categories  # Forces alphabetical order in the legend
                )
            ),
            order=alt.Order(
                "categories:N",
                sort="descending"  # Forces identical alphabetical stacking order inside the bars
            ),
            tooltip=[
                alt.Tooltip("created:O", title="Date"),
                alt.Tooltip("categories:N", title="Category"),
                alt.Tooltip("count:Q", title="Count")
            ]
        )
        .properties(
            width=500,
            height=400,
            title=alt.TitleParams(
                text="Comic Category Over Time",
                subtitle="Read comics at https://annyh.co/all",
                anchor="middle",
                fontSize=16,
            )
        )
    )

    # Render the chart
    stacked_bar

    return


if __name__ == "__main__":
    app.run()
