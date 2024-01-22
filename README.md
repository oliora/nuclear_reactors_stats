nuclear_reactors_stats
======================

Graphs with basic statistics about commercial nuclear reactors in the world.

Based on data from https://en.wikipedia.org/wiki/List_of_commercial_nuclear_reactors.

Requirements:

- Python 3 (almost any version should do)
- Python packages `requests`, `lxml`, `pandas`, `matplotlib`, `seaborn` and `jupyter`.
  To install run `python3 -m pip install -r requirements.txt`

How to generate graphs
----------------------

First, extract data from the wiki page into CSV file `reactors.csv`:

    python3 extract_reactors.py

Then run Jupyter notebook [`notebook.ipynb`](notebook.ipynb) and export it to to Markdown file `notebook.md`:

    jupyter nbconvert --to markdown --execute notebook.ipynb

Or run it and export to `notebook.html` which you can open in your browser:
    
    jupyter nbconvert --to html --execute notebook.ipynb

Repostitory contains CSV file [reactors.csv](reactors.csv), Markdown [notebook.md](notebook.md) and HTML [notebook.html](notebook.html) (you need to download it to view) generated on **January 22, 2024**.

Note that reactors data is distributed by Wikipedia under the [Creative Commons Attribution-ShareAlike License 4.0](https://en.wikipedia.org/wiki/Wikipedia:Text_of_the_Creative_Commons_Attribution-ShareAlike_4.0_International_License).
