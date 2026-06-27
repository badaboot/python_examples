import marimo

__generated_with = "0.17.6"
app = marimo.App()


@app.cell
def _():
    import polars as pl
    import altair as alt

    # 1. Load data from local CSV
    csv_path = "static/chapters_book_1.csv"
    df = pl.read_csv(csv_path)

    # 2. Process data with Polars expressions
    df_exploded = (
        df.with_columns([
            # Extract everything before the colon for the clean X-axis label
            pl.col("name").str.split_exact(":", 0).struct.field("field_0").str.strip_chars().alias("chapter_num"),
            # Split the comma-separated strings into a list
            pl.col("characters involved").str.split(",")
        ])
        .explode("characters involved")
        .with_columns(
            pl.col("characters involved").str.strip_chars()
        )
        .rename({"characters involved": "Character"})
    )

    # 3. Calculate frequencies to get an ordered list for the Y-axis
    character_counts = (
        df_exploded.group_by("Character")
        .agg(pl.len().alias("count"))
        .sort("count", descending=True)
    )

    # Extract unique list of clean chapter numbers in chronological order
    events_order = df_exploded["chapter_num"].unique(maintain_order=True).to_list()
    characters_by_frequency = character_counts["Character"].to_list()

    # 4. Define a fixed color scale for consistent character identity
    color_scale = alt.Scale(domain=characters_by_frequency, scheme='tableau20')

    # 5. Build the Interactive Altair Grid
    heatmap_chart = alt.Chart(df_exploded).mark_rect(
        stroke='white',
        strokeWidth=1.5
    ).encode(
        x=alt.X('chapter_num:N', 
                sort=events_order, 
                title='Chapter #',
                axis=alt.Axis(labelAngle=-30, labelAlign='center')), # Set angle to 0 since short numbers fit perfectly
        y=alt.Y('Character:N', 
                sort=characters_by_frequency, 
                title='Characters (Most Frequent at Top)'),
        color=alt.Color('Character:N', 
                        scale=color_scale, 
                        legend=None),
        tooltip=[
            alt.Tooltip('Character:N', title='Character Name'),
            alt.Tooltip('name:N', title='Chapter Name') 
        ]
    ).properties(
        width="container",
        height=400, 
        title="Character frequency per Chapter"
    ).configure_view(
        strokeWidth=0
    )
    # 6. Explicitly evaluate the chart object at the end for Marimo rendering
    heatmap_chart
    return


if __name__ == "__main__":
    app.run()
