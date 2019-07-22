"""Sequencing efficiency interactive simulation"""
import bokeh.io
import bokeh.layouts
import bokeh.models
import bokeh.plotting
import numpy as np
import pandas as pd
import scipy.stats as st

N_slider = bokeh.models.widgets.Slider(
  title='Total mols',
  value=1e5,
  start=1e5,
  end=1e6,
  step=1e5)
p1_slider = bokeh.models.widgets.Slider(
  title='Fraction mols gene 1',
  value=.05,
  start=.05,
  end=.95,
  step=0.05)
p_slider = bokeh.models.widgets.Slider(
  title='Fraction mols sequenced',
  value=.1,
  start=.05,
  end=.95,
  step=0.05)
controls = [N_slider, p1_slider, p_slider]

obs_data = bokeh.models.ColumnDataSource(pd.DataFrame(columns=['x', 'bin_llik', 'hyperg_llik']))

def update(attr, old, new):
  global obs_data
  N, p1, p = [x.value for x in controls]
  n1 = N * p1
  mean = n1 * p
  sd = np.sqrt(n1 * p * (1 - p))
  grid = np.arange(np.floor(mean - sd), np.ceil(mean + sd))
  bin_llik = st.binom(n=N * p, p=n1 / N).logpmf(grid)
  hyperg_llik = st.hypergeom(M=N, n=n1, N=N * p).logpmf(grid)
  obs_data.data = bokeh.models.ColumnDataSource.from_df(
    pd.DataFrame({'x': grid, 'bin_llik': bin_llik, 'hyperg_llik': hyperg_llik}))

for c in controls:
  c.on_change('value', update)

llik = bokeh.plotting.figure(width=600, height=400, tools=[])
l0 = llik.line(source=obs_data, x='x', y='bin_llik', color='black')
l1 = llik.line(source=obs_data, x='x', y='hyperg_llik', color='red')
legend = bokeh.models.Legend(items=[
  bokeh.models.LegendItem(label='Hypergeometric', renderers=[l1]),
  bokeh.models.LegendItem(label='Binomial', renderers=[l0]),
])
llik.add_layout(legend, 'right')
llik.xaxis.axis_label = 'Molecule count'
llik.yaxis.axis_label = 'Log likelihood'

layout = bokeh.layouts.layout([[
  bokeh.layouts.widgetbox(*controls, width=250),
  llik
]])

doc = bokeh.io.curdoc()
doc.title = 'Sequencing efficiency simulation'
doc.add_root(layout)

update(None, None, None)
