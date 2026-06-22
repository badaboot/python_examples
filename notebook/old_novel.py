import marimo

__generated_with = "0.17.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import polars as pl
    import matplotlib.pyplot as plt

    # 1. Load data into a Polars DataFrame
    data = [
        {"event": "1: Magical notebook", "characters": "Vivian, Mrs. Arda, Mandukai, Pontano, Queen Berki, Miri"},
        {"event": "2: Wedding night", "characters": "Vivian, Mandukai, Cecily, Princess Miri, Batbayar, Arban, Queen Berki"},
        {"event": "3: Intelligence gathering", "characters": "Mandukai, Batbayar, Jin, Pontano, Prince Darden, King Leon"},
        {"event": "4: Khan's proposal", "characters": "Miri, Queen Berki, Mandukai, Jin, Pontano, Prince Darden, King Leon"},
        {"event": "5: Golden ticket", "characters": "Mandukai, Jin, BatBayar, Miri, Berki, Willem, Xian, King Leon, Schemeisser"},
        {"event": "5.5 Surprise attack", "characters": "Mandukai, Jin, BatBayar, Xian, Willem, King Leon, Prince Darden, Queen Glor"}
    ]

    df = pl.DataFrame(data)

    # 2. Process data using Polars expressions
    df_exploded = (
        df.with_columns(
            pl.col("characters").str.split(", ")
        )
        .explode("characters")
        .rename({"characters": "Character"})
    )

    # Standardize names
    name_mapping = {
        "Queen Berki": "Berki",
        "Princess Miri": "Miri",
        "BatBayar": "Batbayar"
    }
    df_exploded = df_exploded.with_columns(
        pl.col("Character").replace(name_mapping)
    )

    # 3. Compute Character Frequency and Sort
    # We group by character, count occurrences, and sort descending
    character_counts = (
        df_exploded.group_by("Character")
        .agg(pl.len().alias("count"))
        .sort("count", descending=True)
    )

    # Extract lists for plotting coordinates
    events = df["event"].to_list()
    characters_by_frequency = character_counts["Character"].to_list()

    # 4. Native Matplotlib Color Mapping
    cmap = plt.colormaps.get_cmap('tab20')
    # Keep colors consistently mapped to the characters regardless of their frequency position
    colors = [cmap(i) for i in range(len(characters_by_frequency))]
    char_color_map = dict(zip(characters_by_frequency, colors))

    # 5. Build the custom grid matrix
    fig, ax = plt.subplots(figsize=(12, 8))

    for c_idx, char in enumerate(characters_by_frequency):
        for e_idx, event in enumerate(events):
            presence = df_exploded.filter(
                (pl.col("Character") == char) & (pl.col("event") == event)
            )
        
            if not presence.is_empty():
                color = char_color_map[char]
                alpha = 1.0
            else:
                color = (0.95, 0.95, 0.95)  # Soft gray background for absence
                alpha = 0.5
            
            rect = plt.Rectangle((e_idx - 0.45, c_idx - 0.45), 0.9, 0.9, color=color, alpha=alpha, ec='white', lw=1.5)
            ax.add_patch(rect)

    # 6. Format axes, labels, and display
    ax.set_xlim(-0.6, len(events) - 0.4)
    ax.set_ylim(-0.6, len(characters_by_frequency) - 0.4)
    ax.set_xticks(range(len(events)))
    ax.set_xticklabels(events, rotation=20, ha='right', fontsize=11)
    ax.set_yticks(range(len(characters_by_frequency)))
    ax.set_yticklabels(characters_by_frequency, fontsize=11)

    ax.set_title("Character Presence Grid (Sorted by Most Frequent)", fontsize=14, pad=20, fontweight='bold')
    ax.set_xlabel("Timeline / Events", fontsize=12, labelpad=10)
    ax.set_ylabel("Characters (Most Frequent at Top)", fontsize=12, labelpad=10)

    ax.invert_yaxis()  # Keeps the highest count at the top of the grid layout
    plt.tight_layout()
    plt.show()
    return


if __name__ == "__main__":
    app.run()
