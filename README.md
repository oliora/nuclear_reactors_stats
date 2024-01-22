nuclear_reactors_stats
======================

Graphs with basic statistics about commercial nuclear reactors in the world.

Based on data from https://en.wikipedia.org/wiki/List_of_commercial_nuclear_reactors

Requirements:

- Python 3 (almost any version should do)
- Python packages `requests`, `lxml`, `pandas`, `matplotlib`, `seaborn` and `jupyter`.
  To install run `python3 -m pip install -r requirements.tx`

How to generate graphs
----------------------

First, extract data from the wiki page into a CSV file:

    python3 extract_reactors.py

Then run Jupyter notebook [`notebook.ipynb`](notebook.ipynb) and export it to HTML:
    
    jupyter nbconvert --to html --execute notebook.ipyn

Repostitory contains CSV file [reactors.csv](reactors.csv) and [HTML with graphs](notebook.html)) generated on January 22, 2024.
