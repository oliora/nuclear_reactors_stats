```python
import json
import pandas as pd
import matplotlib.pyplot as plt

import seaborn
seaborn.set_theme()

orig_input_df = pd.read_csv('./reactors.csv').convert_dtypes()
```


```python
with open('regions-m49.json') as f:
    regions = json.load(f)['regions']
    regions = {v: n for n, v in regions.items()}

with open('countries-m49.json') as f:
    countries = json.load(f)['countries']
    country_subregions = {c['name']: regions[c['subRegion']] for c in countries}
    country_regions = {c['name']: regions[c['region']] for c in countries}
```


```python
country_mapping = {
    'Czech Republic': 'Czechia',
    'Iran': 'Iran (Islamic Republic of)',
    'Russia': 'Russian Federation',
    'South Korea': 'Republic of Korea',
    'Taiwan': 'China',  # UN is an abomination
    'Turkey': 'T\u00fcrkiye',
    'United Kingdom': 'United Kingdom of Great Britain and Northern Ireland',
    'United States': 'United States of America',
}

max_year = 2023
years = range(1954, max_year + 1)

copyright_text = 'CC BY-SA 4.0 Andrey Upadyshev (image) and\nWikipedia, List of commercial nuclear reactors (data)'
copyright_font_size = 10
```


```python
input_df = orig_input_df[orig_input_df['Begin building'].notna() & orig_input_df['Begin building'] <= max_year].reset_index(drop=True)
input_df.loc[input_df['Commercial operation'] > max_year, 'Commercial operation'] = None
input_df.loc[input_df['Closed'] > max_year, 'Closed'] = None

input_df['SubRegion'] = input_df['Country'].map(lambda x: country_subregions[country_mapping.get(x, x)])
input_df['Region'] = input_df['Country'].map(lambda x: country_regions[country_mapping.get(x, x)])
input_df['Operated closed'] = input_df['Closed'].where(input_df['Commercial operation'].notna(), None)
```


```python
def format_years_ticks(ax):
    for label in ax.get_xticklabels():
        if label.get_text() in ('1957', '1979', '1986', '2011'):
            label.set_color('red')


def format_number_plants_ticks(ax, ymin, ymax):
    def fmt(val, pos):
        return int(abs(val))
    ax.yaxis.set_major_formatter(fmt)
    ax.set_ylim(-ymin, ymax)
```


```python
# Totals
total_constructed = input_df.groupby(['Country'])[['Begin building', 'Commercial operation', 'Closed']].count().reset_index().sort_values('Begin building', ascending=False).reset_index(drop=True)
total_constructed
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Country</th>
      <th>Begin building</th>
      <th>Commercial operation</th>
      <th>Closed</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>United States</td>
      <td>140</td>
      <td>134</td>
      <td>46</td>
    </tr>
    <tr>
      <th>1</th>
      <td>China</td>
      <td>81</td>
      <td>55</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>France</td>
      <td>69</td>
      <td>68</td>
      <td>12</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Japan</td>
      <td>62</td>
      <td>59</td>
      <td>26</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Russia</td>
      <td>62</td>
      <td>47</td>
      <td>10</td>
    </tr>
    <tr>
      <th>5</th>
      <td>United Kingdom</td>
      <td>46</td>
      <td>44</td>
      <td>35</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Germany</td>
      <td>39</td>
      <td>36</td>
      <td>39</td>
    </tr>
    <tr>
      <th>7</th>
      <td>India</td>
      <td>31</td>
      <td>23</td>
      <td>1</td>
    </tr>
    <tr>
      <th>8</th>
      <td>South Korea</td>
      <td>30</td>
      <td>27</td>
      <td>2</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Canada</td>
      <td>25</td>
      <td>25</td>
      <td>6</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Ukraine</td>
      <td>25</td>
      <td>19</td>
      <td>8</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Sweden</td>
      <td>14</td>
      <td>13</td>
      <td>8</td>
    </tr>
    <tr>
      <th>12</th>
      <td>Spain</td>
      <td>14</td>
      <td>10</td>
      <td>7</td>
    </tr>
    <tr>
      <th>13</th>
      <td>Slovakia</td>
      <td>9</td>
      <td>8</td>
      <td>3</td>
    </tr>
    <tr>
      <th>14</th>
      <td>Belgium</td>
      <td>8</td>
      <td>8</td>
      <td>3</td>
    </tr>
    <tr>
      <th>15</th>
      <td>Bulgaria</td>
      <td>8</td>
      <td>6</td>
      <td>4</td>
    </tr>
    <tr>
      <th>16</th>
      <td>Taiwan</td>
      <td>8</td>
      <td>6</td>
      <td>6</td>
    </tr>
    <tr>
      <th>17</th>
      <td>Pakistan</td>
      <td>7</td>
      <td>7</td>
      <td>1</td>
    </tr>
    <tr>
      <th>18</th>
      <td>Italy</td>
      <td>6</td>
      <td>4</td>
      <td>6</td>
    </tr>
    <tr>
      <th>19</th>
      <td>Switzerland</td>
      <td>6</td>
      <td>6</td>
      <td>2</td>
    </tr>
    <tr>
      <th>20</th>
      <td>Czech Republic</td>
      <td>6</td>
      <td>6</td>
      <td>0</td>
    </tr>
    <tr>
      <th>21</th>
      <td>Finland</td>
      <td>5</td>
      <td>5</td>
      <td>0</td>
    </tr>
    <tr>
      <th>22</th>
      <td>Turkey</td>
      <td>4</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>23</th>
      <td>United Arab Emirates</td>
      <td>4</td>
      <td>3</td>
      <td>0</td>
    </tr>
    <tr>
      <th>24</th>
      <td>Argentina</td>
      <td>4</td>
      <td>3</td>
      <td>0</td>
    </tr>
    <tr>
      <th>25</th>
      <td>Belarus</td>
      <td>4</td>
      <td>2</td>
      <td>2</td>
    </tr>
    <tr>
      <th>26</th>
      <td>Hungary</td>
      <td>4</td>
      <td>4</td>
      <td>0</td>
    </tr>
    <tr>
      <th>27</th>
      <td>Brazil</td>
      <td>3</td>
      <td>2</td>
      <td>0</td>
    </tr>
    <tr>
      <th>28</th>
      <td>Egypt</td>
      <td>3</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>29</th>
      <td>Netherlands</td>
      <td>2</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <th>30</th>
      <td>Armenia</td>
      <td>2</td>
      <td>2</td>
      <td>1</td>
    </tr>
    <tr>
      <th>31</th>
      <td>Bangladesh</td>
      <td>2</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>32</th>
      <td>Cuba</td>
      <td>2</td>
      <td>0</td>
      <td>2</td>
    </tr>
    <tr>
      <th>33</th>
      <td>Iran</td>
      <td>2</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <th>34</th>
      <td>South Africa</td>
      <td>2</td>
      <td>2</td>
      <td>0</td>
    </tr>
    <tr>
      <th>35</th>
      <td>Lithuania</td>
      <td>2</td>
      <td>2</td>
      <td>2</td>
    </tr>
    <tr>
      <th>36</th>
      <td>Mexico</td>
      <td>2</td>
      <td>2</td>
      <td>0</td>
    </tr>
    <tr>
      <th>37</th>
      <td>Romania</td>
      <td>2</td>
      <td>2</td>
      <td>0</td>
    </tr>
    <tr>
      <th>38</th>
      <td>Poland</td>
      <td>2</td>
      <td>0</td>
      <td>2</td>
    </tr>
    <tr>
      <th>39</th>
      <td>Philippines</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>40</th>
      <td>Slovenia</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
    </tr>
    <tr>
      <th>41</th>
      <td>Austria</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>42</th>
      <td>Kazakhstan</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>




```python
num_building_started = input_df.groupby(['Country', 'Begin building'])['Begin building'].count()
num_connected = input_df.groupby(['Country', 'Commercial operation'])['Commercial operation'].count()
num_closed = input_df.groupby(['Country', 'Closed'])['Closed'].count()
num_operated_closed = input_df.groupby(['Country', 'Operated closed'])['Operated closed'].count()

countries = sorted(c for c in input_df['Country'].unique() if c in num_building_started)
#top_countries = total_constructed[total_constructed['Begin building'] >= 10]['Country'].to_list()
top_countries = total_constructed['Country'].to_list()

max_building_started = num_building_started.max()
max_num_closed = num_closed.max()
ymax = (max_building_started + 4) // 5 * 5
ymin = (max_num_closed + 4) // 5 * 5
tot_ymax = 110  # TODO: calculate from data


for c in top_countries:
    combined = pd.concat([
        num_building_started[c],
        num_connected[c] if c in num_connected else pd.DataFrame(columns=['Commercial operation']),
        num_closed[c] if c in num_closed else pd.DataFrame(columns=['Closed']),
        num_operated_closed[c] if c in num_operated_closed else pd.DataFrame(columns=['Operated closed']),
    ], axis=1)
    
    combined = combined.reindex(years, fill_value=0)

    combined['Commercial operation tot'] = combined['Commercial operation'].fillna(0).cumsum()
    combined['Operated closed tot'] = combined['Operated closed'].fillna(0).cumsum()
    combined['In operation'] = combined['Commercial operation tot'] - combined['Operated closed tot']

    fig, ax = plt.subplots(2, 1, figsize=(11, 10))

    ax1, ax2 = ax

    combined['Begin building'].plot.bar(ax=ax1, label='Construction started')
    (-combined['Closed']).plot.bar(ax=ax1, color='red', label='Closed')

    ax1.set_title(c)
    ax1.set_xlabel(None)
    format_years_ticks(ax1)
    format_number_plants_ticks(ax1, ymin, ymax)
    ax1.text(0, -ymin, copyright_text, fontsize=copyright_font_size, verticalalignment='bottom')
    ax1.legend()

    combined['In operation'].plot.bar(ax=ax2, label='Number in operation')
    combined['Commercial operation'].plot.bar(ax=ax2, color='black', label='Operation started')
    format_years_ticks(ax2)
    ax2.set_ylim(0, tot_ymax)
    #ax2.text(0, ax2.get_ylim()[1], copyright_text, fontsize=copyright_font_size, verticalalignment='top')
    ax2.legend()

    fig.tight_layout()
```

    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/1497431667.py:28: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Operated closed tot'] = combined['Operated closed'].fillna(0).cumsum()


    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/1497431667.py:28: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Operated closed tot'] = combined['Operated closed'].fillna(0).cumsum()
    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/1497431667.py:31: RuntimeWarning: More than 20 figures have been opened. Figures created through the pyplot interface (`matplotlib.pyplot.figure`) are retained until explicitly closed and may consume too much memory. (To control this warning, see the rcParam `figure.max_open_warning`). Consider using `matplotlib.pyplot.close()`.
      fig, ax = plt.subplots(2, 1, figsize=(11, 10))


    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/1497431667.py:28: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Operated closed tot'] = combined['Operated closed'].fillna(0).cumsum()


    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/1497431667.py:27: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Commercial operation tot'] = combined['Commercial operation'].fillna(0).cumsum()
    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/1497431667.py:28: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Operated closed tot'] = combined['Operated closed'].fillna(0).cumsum()


    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/1497431667.py:28: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Operated closed tot'] = combined['Operated closed'].fillna(0).cumsum()


    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/1497431667.py:28: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Operated closed tot'] = combined['Operated closed'].fillna(0).cumsum()


    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/1497431667.py:28: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Operated closed tot'] = combined['Operated closed'].fillna(0).cumsum()


    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/1497431667.py:28: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Operated closed tot'] = combined['Operated closed'].fillna(0).cumsum()


    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/1497431667.py:28: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Operated closed tot'] = combined['Operated closed'].fillna(0).cumsum()


    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/1497431667.py:27: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Commercial operation tot'] = combined['Commercial operation'].fillna(0).cumsum()
    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/1497431667.py:28: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Operated closed tot'] = combined['Operated closed'].fillna(0).cumsum()


    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/1497431667.py:27: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Commercial operation tot'] = combined['Commercial operation'].fillna(0).cumsum()
    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/1497431667.py:28: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Operated closed tot'] = combined['Operated closed'].fillna(0).cumsum()


    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/1497431667.py:27: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Commercial operation tot'] = combined['Commercial operation'].fillna(0).cumsum()
    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/1497431667.py:28: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Operated closed tot'] = combined['Operated closed'].fillna(0).cumsum()


    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/1497431667.py:28: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Operated closed tot'] = combined['Operated closed'].fillna(0).cumsum()


    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/1497431667.py:28: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Operated closed tot'] = combined['Operated closed'].fillna(0).cumsum()


    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/1497431667.py:28: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Operated closed tot'] = combined['Operated closed'].fillna(0).cumsum()


    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/1497431667.py:28: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Operated closed tot'] = combined['Operated closed'].fillna(0).cumsum()


    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/1497431667.py:27: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Commercial operation tot'] = combined['Commercial operation'].fillna(0).cumsum()
    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/1497431667.py:28: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Operated closed tot'] = combined['Operated closed'].fillna(0).cumsum()


    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/1497431667.py:27: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Commercial operation tot'] = combined['Commercial operation'].fillna(0).cumsum()
    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/1497431667.py:28: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Operated closed tot'] = combined['Operated closed'].fillna(0).cumsum()


    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/1497431667.py:28: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Operated closed tot'] = combined['Operated closed'].fillna(0).cumsum()


    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/1497431667.py:27: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Commercial operation tot'] = combined['Commercial operation'].fillna(0).cumsum()
    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/1497431667.py:28: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Operated closed tot'] = combined['Operated closed'].fillna(0).cumsum()



    
![png](notebook_files/notebook_6_20.png)
    



    
![png](notebook_files/notebook_6_21.png)
    



    
![png](notebook_files/notebook_6_22.png)
    



    
![png](notebook_files/notebook_6_23.png)
    



    
![png](notebook_files/notebook_6_24.png)
    



    
![png](notebook_files/notebook_6_25.png)
    



    
![png](notebook_files/notebook_6_26.png)
    



    
![png](notebook_files/notebook_6_27.png)
    



    
![png](notebook_files/notebook_6_28.png)
    



    
![png](notebook_files/notebook_6_29.png)
    



    
![png](notebook_files/notebook_6_30.png)
    



    
![png](notebook_files/notebook_6_31.png)
    



    
![png](notebook_files/notebook_6_32.png)
    



    
![png](notebook_files/notebook_6_33.png)
    



    
![png](notebook_files/notebook_6_34.png)
    



    
![png](notebook_files/notebook_6_35.png)
    



    
![png](notebook_files/notebook_6_36.png)
    



    
![png](notebook_files/notebook_6_37.png)
    



    
![png](notebook_files/notebook_6_38.png)
    



    
![png](notebook_files/notebook_6_39.png)
    



    
![png](notebook_files/notebook_6_40.png)
    



    
![png](notebook_files/notebook_6_41.png)
    



    
![png](notebook_files/notebook_6_42.png)
    



    
![png](notebook_files/notebook_6_43.png)
    



    
![png](notebook_files/notebook_6_44.png)
    



    
![png](notebook_files/notebook_6_45.png)
    



    
![png](notebook_files/notebook_6_46.png)
    



    
![png](notebook_files/notebook_6_47.png)
    



    
![png](notebook_files/notebook_6_48.png)
    



    
![png](notebook_files/notebook_6_49.png)
    



    
![png](notebook_files/notebook_6_50.png)
    



    
![png](notebook_files/notebook_6_51.png)
    



    
![png](notebook_files/notebook_6_52.png)
    



    
![png](notebook_files/notebook_6_53.png)
    



    
![png](notebook_files/notebook_6_54.png)
    



    
![png](notebook_files/notebook_6_55.png)
    



    
![png](notebook_files/notebook_6_56.png)
    



    
![png](notebook_files/notebook_6_57.png)
    



    
![png](notebook_files/notebook_6_58.png)
    



    
![png](notebook_files/notebook_6_59.png)
    



    
![png](notebook_files/notebook_6_60.png)
    



    
![png](notebook_files/notebook_6_61.png)
    



    
![png](notebook_files/notebook_6_62.png)
    



```python
total_constructed_by_subregion = input_df.groupby(['SubRegion'])[['Begin building', 'Commercial operation', 'Closed']].count().reset_index().sort_values('Begin building', ascending=False).reset_index(drop=True)
total_constructed_by_subregion
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>SubRegion</th>
      <th>Begin building</th>
      <th>Commercial operation</th>
      <th>Closed</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Eastern Asia</td>
      <td>181</td>
      <td>147</td>
      <td>34</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Northern America</td>
      <td>165</td>
      <td>159</td>
      <td>52</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Western Europe</td>
      <td>125</td>
      <td>120</td>
      <td>58</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Eastern Europe</td>
      <td>122</td>
      <td>94</td>
      <td>29</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Northern Europe</td>
      <td>67</td>
      <td>64</td>
      <td>45</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Southern Asia</td>
      <td>42</td>
      <td>31</td>
      <td>2</td>
    </tr>
    <tr>
      <th>6</th>
      <td>Southern Europe</td>
      <td>21</td>
      <td>15</td>
      <td>13</td>
    </tr>
    <tr>
      <th>7</th>
      <td>Latin America and the Caribbean</td>
      <td>11</td>
      <td>7</td>
      <td>2</td>
    </tr>
    <tr>
      <th>8</th>
      <td>Western Asia</td>
      <td>10</td>
      <td>5</td>
      <td>1</td>
    </tr>
    <tr>
      <th>9</th>
      <td>Northern Africa</td>
      <td>3</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>10</th>
      <td>Sub-Saharan Africa</td>
      <td>2</td>
      <td>2</td>
      <td>0</td>
    </tr>
    <tr>
      <th>11</th>
      <td>Central Asia</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>12</th>
      <td>South-eastern Asia</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>




```python
num_building_started = input_df.groupby(['SubRegion', 'Begin building'])['Begin building'].count()
num_connected = input_df.groupby(['SubRegion', 'Commercial operation'])['Commercial operation'].count()
num_closed = input_df.groupby(['SubRegion', 'Closed'])['Closed'].count()
num_operated_closed = input_df.groupby(['SubRegion', 'Operated closed'])['Operated closed'].count()

sub_regions = sorted(c for c in input_df['SubRegion'].unique() if c in num_building_started)
#top_regions = total_constructed_by_subregion[total_constructed_by_subregion['Begin building'] > 10]['SubRegion'].to_list()
top_regions = total_constructed_by_subregion['SubRegion'].to_list()

max_building_started = num_building_started.max()
max_num_closed = num_closed.max()
ymax = (max_building_started + 4) // 5 * 5
ymin = (max_num_closed + 4) // 5 * 5
tot_ymax = 130  # TODO: calculate from data


for c in top_regions:
    combined = pd.concat([
        num_building_started[c],
        num_connected[c] if c in num_connected else pd.DataFrame(columns=['Commercial operation']),
        num_closed[c] if c in num_closed else pd.DataFrame(columns=['Closed']),
        num_operated_closed[c] if c in num_operated_closed else pd.DataFrame(columns=['Operated closed']),
    ], axis=1)
    
    combined = combined.reindex(years, fill_value=0)

    combined['Commercial operation tot'] = combined['Commercial operation'].fillna(0).cumsum()
    combined['Operated closed tot'] = combined['Operated closed'].fillna(0).cumsum()
    combined['In operation'] = combined['Commercial operation tot'] - combined['Operated closed tot']

    fig, ax = plt.subplots(2, 1, figsize=(11, 10))

    ax1, ax2 = ax

    combined['Begin building'].plot.bar(ax=ax1, label='Construction started')
    (-combined['Closed']).plot.bar(ax=ax1, color='red', label='Closed')

    ax1.set_title(f'{c} (UN M49)')
    ax1.set_xlabel(None)
    format_years_ticks(ax1)
    format_number_plants_ticks(ax1, ymin, ymax)
    ax1.text(0, -ymin, copyright_text, fontsize=copyright_font_size, verticalalignment='bottom')
    ax1.legend()

    combined['In operation'].plot.bar(ax=ax2, label='Number in operation')
    combined['Commercial operation'].plot.bar(ax=ax2, color='black', label='Operation started')
    format_years_ticks(ax2)
    ax2.set_ylim(0, tot_ymax)
    #ax2.text(0, ax2.get_ylim()[1], copyright_text, fontsize=copyright_font_size, verticalalignment='top')
    ax2.legend()


    fig.tight_layout()
```

    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/2329359821.py:28: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Operated closed tot'] = combined['Operated closed'].fillna(0).cumsum()


    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/2329359821.py:27: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Commercial operation tot'] = combined['Commercial operation'].fillna(0).cumsum()
    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/2329359821.py:28: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Operated closed tot'] = combined['Operated closed'].fillna(0).cumsum()


    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/2329359821.py:28: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Operated closed tot'] = combined['Operated closed'].fillna(0).cumsum()


    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/2329359821.py:27: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Commercial operation tot'] = combined['Commercial operation'].fillna(0).cumsum()
    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/2329359821.py:28: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Operated closed tot'] = combined['Operated closed'].fillna(0).cumsum()



    
![png](notebook_files/notebook_8_4.png)
    



    
![png](notebook_files/notebook_8_5.png)
    



    
![png](notebook_files/notebook_8_6.png)
    



    
![png](notebook_files/notebook_8_7.png)
    



    
![png](notebook_files/notebook_8_8.png)
    



    
![png](notebook_files/notebook_8_9.png)
    



    
![png](notebook_files/notebook_8_10.png)
    



    
![png](notebook_files/notebook_8_11.png)
    



    
![png](notebook_files/notebook_8_12.png)
    



    
![png](notebook_files/notebook_8_13.png)
    



    
![png](notebook_files/notebook_8_14.png)
    



    
![png](notebook_files/notebook_8_15.png)
    



    
![png](notebook_files/notebook_8_16.png)
    



```python
total_constructed_by_region = input_df.groupby(['Region'])[['Begin building', 'Commercial operation', 'Closed']].count().reset_index().sort_values('Begin building', ascending=False).reset_index(drop=True)
total_constructed_by_region
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Region</th>
      <th>Begin building</th>
      <th>Commercial operation</th>
      <th>Closed</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Europe</td>
      <td>335</td>
      <td>293</td>
      <td>145</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Asia</td>
      <td>235</td>
      <td>184</td>
      <td>39</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Americas</td>
      <td>176</td>
      <td>166</td>
      <td>54</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Africa</td>
      <td>5</td>
      <td>2</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>




```python
num_building_started = input_df.groupby(['Region', 'Begin building'])['Begin building'].count()
num_connected = input_df.groupby(['Region', 'Commercial operation'])['Commercial operation'].count()
num_closed = input_df.groupby(['Region', 'Closed'])['Closed'].count()
num_operated_closed = input_df.groupby(['Region', 'Operated closed'])['Operated closed'].count()

#top_regions = total_constructed_by_region[total_constructed_by_region['Begin building'] > 10]['Region'].to_list()
top_regions = total_constructed_by_region['Region'].to_list()

regions = sorted(c for c in input_df['Region'].unique() if c in num_building_started)

max_building_started = num_building_started.max()
max_num_closed = num_closed.max()
ymax = (max_building_started + 4) // 5 * 5
ymin = (max_num_closed + 4) // 5 * 5
tot_ymax = 250  # TODO: calculate from data


for c in top_regions:
    combined = pd.concat([
        num_building_started[c],
        num_connected[c] if c in num_connected else pd.DataFrame(columns=['Commercial operation']),
        num_closed[c] if c in num_closed else pd.DataFrame(columns=['Closed']),
        num_operated_closed[c] if c in num_operated_closed else pd.DataFrame(columns=['Operated closed']),
    ], axis=1)
    
    combined = combined.reindex(years, fill_value=0)

    combined['Commercial operation tot'] = combined['Commercial operation'].fillna(0).cumsum()
    combined['Operated closed tot'] = combined['Operated closed'].fillna(0).cumsum()
    combined['In operation'] = combined['Commercial operation tot'] - combined['Operated closed tot']

    fig, ax = plt.subplots(2, 1, figsize=(11, 10))

    ax1, ax2 = ax

    combined['Begin building'].plot.bar(ax=ax1, label='Construction started')
    (-combined['Closed']).plot.bar(ax=ax1, color='red', label='Closed')

    ax1.set_title(f'{c} (UN M49)')
    ax1.set_xlabel(None)
    format_years_ticks(ax1)
    format_number_plants_ticks(ax1, ymin, ymax)
    ax1.text(0, -ymin, copyright_text, fontsize=copyright_font_size, verticalalignment='bottom')
    ax1.legend()

    combined['In operation'].plot.bar(ax=ax2, label='Number in operation')
    combined['Commercial operation'].plot.bar(ax=ax2, color='black', label='Operation started')
    format_years_ticks(ax2)
    ax2.set_ylim(0, tot_ymax)
    #ax2.text(0, ax2.get_ylim()[1], copyright_text, fontsize=copyright_font_size, verticalalignment='top')
    ax2.legend()


    fig.tight_layout()
```

    /var/folders/2z/kr9wj6s90nn6nkdsddywzyfw0000gn/T/ipykernel_25929/2047234876.py:29: FutureWarning: Downcasting object dtype arrays on .fillna, .ffill, .bfill is deprecated and will change in a future version. Call result.infer_objects(copy=False) instead. To opt-in to the future behavior, set `pd.set_option('future.no_silent_downcasting', True)`
      combined['Operated closed tot'] = combined['Operated closed'].fillna(0).cumsum()



    
![png](notebook_files/notebook_10_1.png)
    



    
![png](notebook_files/notebook_10_2.png)
    



    
![png](notebook_files/notebook_10_3.png)
    



    
![png](notebook_files/notebook_10_4.png)
    



```python
num_building_started = input_df.groupby(['Begin building'])['Begin building'].count()
num_connected = input_df.groupby(['Commercial operation'])['Commercial operation'].count()
num_closed = input_df.groupby(['Closed'])['Closed'].count()
num_operated_closed = input_df.groupby(['Operated closed'])['Operated closed'].count()

max_building_started = num_building_started.max()
max_num_closed = num_closed.max()
ymax = (max_building_started + 4) // 5 * 5
ymin = (max_num_closed + 4) // 5 * 5

combined = pd.concat([
        num_building_started,
        num_connected,
        num_closed,
        num_operated_closed,
    ], axis=1)

combined = combined.reindex(years, fill_value=0)

combined['Commercial operation tot'] = combined['Commercial operation'].fillna(0).cumsum()
combined['Operated closed tot'] = combined['Operated closed'].fillna(0).cumsum()
combined['In operation'] = combined['Commercial operation tot'] - combined['Operated closed tot']

fig, ax = plt.subplots(2, 1, figsize=(11, 10))

ax1, ax2 = ax

combined['Begin building'].plot.bar(ax=ax1, label='Construction started')
(-combined['Closed']).plot.bar(ax=ax1, color='red', label='Closed')

ax1.set_title('World')
ax1.set_xlabel(None)
format_years_ticks(ax1)
format_number_plants_ticks(ax1, ymin, ymax)
ax1.text(0, -ymin, copyright_text, fontsize=copyright_font_size, verticalalignment='bottom')
ax1.legend()

combined['In operation'].plot.bar(ax=ax2, label='Number in operation')
combined['Commercial operation'].plot.bar(ax=ax2, color='black', label='Operation started')
format_years_ticks(ax2)
#ax2.text(0, ax2.get_ylim()[1], copyright_text, fontsize=copyright_font_size, verticalalignment='top')
ax2.legend()

fig.tight_layout()
```


    
![png](notebook_files/notebook_11_0.png)
    



```python
# Never opened
never_opened_df = input_df[input_df['Commercial operation'].isna() & input_df['Begin building'].notna() & input_df['Closed'].notna()].sort_values('Closed')

num_building_started = never_opened_df.groupby(['Begin building'])['Begin building'].count()
num_closed = never_opened_df.groupby(['Closed'])['Closed'].count()

combined = pd.concat([
        num_building_started,
        num_closed,
    ], axis=1)

combined = combined.reindex(years, fill_value=0)

fig, ax = plt.subplots(figsize=(11, 5))

combined['Begin building'].plot.bar(ax=ax, label='Construction started')
(-combined['Closed']).plot.bar(ax=ax, color='red', label='Closed')

ax.set_title('Never operated reactors')
ax.set_xlabel(None)
format_years_ticks(ax)
ax.yaxis.set_major_formatter(lambda val, pos: int(val))
ax.text(0, ax.get_ylim()[0], copyright_text, fontsize=copyright_font_size, verticalalignment='bottom')
ax.legend()

fig.tight_layout()
```


    
![png](notebook_files/notebook_12_0.png)
    



```python
never_opened_df.groupby(['Country', 'Closed'])['Closed'].count().sort_values(ascending=False)
```




    Country        Closed
    Spain          1984      4
    United States  1984      3
    Belarus        1987      2
    Cuba           1992      2
    Germany        1990      2
    Italy          1988      2
    Poland         1990      2
    Taiwan         2014      2
    Ukraine        1987      2
                   1990      2
    United States  1983      2
    Austria        1978      1
    Germany        1985      1
    Philippines    1986      1
    Sweden         1970      1
    Name: Closed, dtype: Int64




```python
never_opened_df.groupby(['Country', 'Begin building'])['Begin building'].count().sort_values(ascending=False)
```




    Country        Begin building
    United States  1975              4
    Poland         1982              2
    Ukraine        1988              2
                   1984              2
    Germany        1983              2
    Italy          1982              2
    Taiwan         1999              2
    Belarus        1983              2
    Spain          1972              2
                   1975              2
    Sweden         1965              1
    Austria        1972              1
    Philippines    1976              1
    Germany        1972              1
    Cuba           1985              1
                   1983              1
    United States  1977              1
    Name: Begin building, dtype: Int64


