# Copyright 2024 Marimo. All rights reserved.

import marimo

__generated_with = "0.17.6"
app = marimo.App()


@app.cell
def _():
    import marimo as mo


    text = mo.ui.text(placeholder="Search...", label="Filter")
    text
    return mo, text


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
def _():
    import polars as pl


    # chick_df = pl.read_csv('data/chickenweight.csv')
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
