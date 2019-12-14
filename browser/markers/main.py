import bokeh.io
import bokeh.layouts
import bokeh.models
import bokeh.palettes
import bokeh.plotting
import numpy as np
import pandas as pd
import sqlite3

db = '/project2/mstephens/aksarkar/projects/singlecell-modes/browser/browser.db'

def update_gene(attr, old, new):
  global gene_df
  global gene_data
  with sqlite3.connect(db) as conn:
    x = pd.read_sql(sql="""select n_mols, n_cells, cell_type from markers where name == ?""",
                    con=conn, params=(gene_df.iloc[new[0]]['name'],))
    count_data.data = {
      'n_mols': [list(g['n_mols']) for k, g in x.groupby('cell_type')],
      'n_cells': [list(g['n_cells']) for k, g in x.groupby('cell_type')],
      'cell_type': [k for k, g in x.groupby('cell_type')],
      'color': bokeh.palettes.Paired[10][:len(x.groupby('cell_type').groups)],
      }
    print(count_data.data)
      
def init():
  global gene_df
  global gene_data
  with sqlite3.connect(db) as conn:
    gene_df = pd.read_sql(
        sql="""select distinct name from markers order by name;""",
        con=conn)
    gene_data.data = bokeh.models.ColumnDataSource.from_df(gene_df)
  
gene_df = pd.DataFrame(
  columns=['name'])

gene_data = bokeh.models.ColumnDataSource(gene_df)
gene_data.selected.on_change('indices', update_gene)

count_data = bokeh.models.ColumnDataSource(pd.DataFrame(
  columns=['n_mols', 'n_cells', 'cell_type', 'color']))

genes = bokeh.models.widgets.DataTable(
    source=gene_data,
    columns=[bokeh.models.widgets.TableColumn(field=x, title=x) for x in gene_df.columns],
    width=400,
    height=400)

counts = bokeh.plotting.figure(title='Molecule counts', width=400, height=400, tools=['wheel_zoom', 'reset'])
ml = counts.multi_line(source=count_data, xs='n_mols', ys='n_cells', line_color='color')
counts.xaxis.axis_label = "Number of molecules"
counts.yaxis.axis_label = "Number of cells"

# Hack
cell_types = ['b_cells', 'cd14_monocytes', 'cd34', 'cd4_t_helper', 'cd56_nk',
              'cytotoxic_t', 'memory_t', 'naive_cytotoxic', 'naive_t', 'regulatory_t']

legend = bokeh.models.Legend(items=[
  bokeh.models.LegendItem(label=k, renderers=[ml], index=i) for i, k in enumerate(cell_types)
])
counts.add_layout(legend)

layout = bokeh.layouts.layout([[genes, counts]], sizing_mode='fixed')

doc = bokeh.io.curdoc()
doc.title = 'Marker genes in in-silico mixtures'
doc.add_root(layout)

init()
