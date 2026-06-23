import marimo

__generated_with = "0.17.6"
app = marimo.App()


@app.cell
def _():
    import polars as pl
    import matplotlib.pyplot as plt

    # 1. Load data from your local CSV file using Polars
    csv_path = "static/chapters_book_1.csv"
    df = pl.read_csv(csv_path)

    # 2. Process data using Polars expressions
    # Split the comma-separated strings into a list, explode them to individual rows, and strip whitespace
    df_exploded = (
        df.with_columns(
            pl.col("characters involved").str.split(",")
        )
        .explode("characters involved")
        .with_columns(
            pl.col("characters involved").str.strip_chars()
        )
        .rename({"characters involved": "Character"})
    )

    # [Optional] If you still have variations like "Queen Berki" vs "Berki" in your CSV,
    # you can uncomment this block to standardize them:
    # name_mapping = {"Queen Berki": "Berki", "Princess Miri": "Miri", "BatBayar": "Batbayar"}
    # df_exploded = df_exploded.with_columns(pl.col("Character").replace(name_mapping))

    # 3. Compute Character Frequency and Sort (Most frequent at the top)
    character_counts = (
        df_exploded.group_by("Character")
        .agg(pl.len().alias("count"))
        .sort("count", descending=True)
    )

    # Extract coordinates for the plotting matrix
    events = df["name"].to_list()
    characters_by_frequency = character_counts["Character"].to_list()

    # 4. Native Matplotlib Categorical Color Mapping
    cmap = plt.colormaps.get_cmap('tab20')
    colors = [cmap(i % 20) for i in range(len(characters_by_frequency))] # % 20 wraps around safely if you have >20 characters
    char_color_map = dict(zip(characters_by_frequency, colors))

    # 5. Build the custom grid matrix
    # Dynamically scale the size of the canvas to fit your total number of chapters/characters
    fig, ax = plt.subplots(figsize=(max(10, len(events) * 1.2), max(6, len(characters_by_frequency) * 0.4)))

    for c_idx, char in enumerate(characters_by_frequency):
        for e_idx, event in enumerate(events):
            # Filter matching rows to check for presence
            presence = df_exploded.filter(
                (pl.col("Character") == char) & (pl.col("name") == event)
            )
        
            if not presence.is_empty():
                color = char_color_map[char]
                alpha = 1.0
            else:
                color = (0.95, 0.95, 0.95)  # Soft neutral gray background for absence
                alpha = 0.5
            
            # Draw the individual grid square cell
            rect = plt.Rectangle((e_idx - 0.45, c_idx - 0.45), 0.9, 0.9, color=color, alpha=alpha, ec='white', lw=1.5)
            ax.add_patch(rect)

    # 6. Format axes, labels, and ticks
    ax.set_xlim(-0.6, len(events) - 0.4)
    ax.set_ylim(-0.6, len(characters_by_frequency) - 0.4)
    ax.set_xticks(range(len(events)))
    ax.set_xticklabels(events, rotation=20, ha='right', fontsize=11)
    ax.set_yticks(range(len(characters_by_frequency)))
    ax.set_yticklabels(characters_by_frequency, fontsize=11)

    ax.set_title("Character Presence Matrix (Sorted by Frequency)", fontsize=80, pad=20, fontweight='bold')
    ax.set_xlabel("Chapters / Timeline", fontsize=80, labelpad=10)
    ax.set_ylabel("Characters (Most Frequent at Top)", fontsize=80, labelpad=10)

    ax.invert_yaxis()  # Keep the highest-frequency character at the top row
    plt.tight_layout()

    # CRITICAL FOR MARIMO: End the cell by evaluating the 'fig' variable explicitly.
    # Do not add plt.close() or plt.show() here.
    fig
    return


if __name__ == "__main__":
    app.run()
