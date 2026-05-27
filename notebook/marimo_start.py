# Copyright 2024 Marimo. All rights reserved.

import marimo

__generated_with = "0.17.6"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    # Read a local file and render its content
    with open("static/page.html", "r") as f:
       content = f.read()
    renderedContent = mo.Html(content)
    renderedContent
    return (mo,)


@app.cell
def _(mo):
    # Initialize state with 0
    get_count, set_count = mo.state(0)
    return get_count, set_count


@app.cell
def _(mo, set_count):

    # A button to increment the count
    increment = mo.ui.button(label="Increment", on_click=lambda _: set_count(lambda c: c + 1))
    increment
    return


@app.cell
def _(mo):
    slider = mo.ui.slider(start=20, stop=100, step=5, value=50, label="Font Size")
    return (slider,)


@app.cell
def _(get_count, mo, slider):
    # Create a reactive markdown block that updates when the slider moves
    size_config = mo.md(
        f"""
        <h1 style="font-size: {slider.value}px;">Current count: <span class="highlight">{get_count()}</span></h1>
        {slider}
        """
    )
    size_config
    return


@app.cell
def _(mo):


    text = mo.ui.text(placeholder="Search...", label="Filter")
    text
    return (text,)


@app.cell
def _(text):
    f"The current value is {text.value}"
    return


@app.cell
def _(text):
    def repeat(s, exclaim):
        """
        Returns the string 's' repeated 3 times.
        If exclaim is true, add exclamation marks.
        """

        result = s + s + s # can also use "s * 3" which is faster (Why?)
        if exclaim:
            result = result + '!!!'
        return result
    f"The current value is {repeat(text.value, '!')}"
    return


@app.cell
def _():
    squares = [1, 4, 9, 16]
    sum = 0
    for num in squares:
        sum += num
    print(sum) 
    return


@app.cell
def _(mo):
    import polars as pl


    df = pl.read_csv('static/chickweight.csv')
    mo.inspect(df)
    return


@app.cell
def _(mo):
    import time

    for i in mo.status.progress_bar(range(10)):
        time.sleep(1)
    return


@app.cell
def _(mo):
    mo.ui.date()
    return


if __name__ == "__main__":
    app.run()
