import bokeh.io
import bokeh.layouts
import bokeh.models
import bokeh.plotting
import numpy as np
import pandas as pd
import sqlite3

db = '/project2/mstephens/aksarkar/projects/singlecell-modes/browser/browser.db'

def update_gene(attr, old, new):
  global gene_df
  global count_data
  params = gene_df.iloc[new[0]][['dataset', 'gene']]
  with sqlite3.connect(db) as conn:
    x = pd.read_sql(sql="""select count from counts where dataset == ? and gene == ?""",
                    con=conn, params=params).astype(int)
    n, edges = np.histogram(x['count'], bins=x['count'].max() + 1)
    count_data.data = bokeh.models.ColumnDataSource.from_df(
      pd.DataFrame({'left': edges[:-1], 'right': edges[1:], 'n': n}))
      
def init():
  global gene_df
  global gene_data
  with sqlite3.connect(db) as conn:
    gene_df = pd.read_sql(
        sql="""select * from genes order by dataset, p;""",
        con=conn)
    gene_data.data = bokeh.models.ColumnDataSource.from_df(gene_df)
  
gene_df = pd.DataFrame(
  columns=['dataset', 'gene', 'method', 'stat', 'p'])

gene_data = bokeh.models.ColumnDataSource(gene_df)
gene_data.selected.on_change('indices', update_gene)

count_data = bokeh.models.ColumnDataSource(pd.DataFrame(
  columns=['left', 'right', 'n']))

genes = bokeh.models.widgets.DataTable(
    source=gene_data,
    columns=[bokeh.models.widgets.TableColumn(field=x, title=x) for x in gene_df.columns],
    width=800,
    height=400)

counts = bokeh.plotting.figure(title='Molecule counts', width=400, height=400, tools=[])
counts.quad(source=count_data, left='left', right='right', bottom=0, top='n', fill_color='black', line_color='black')
counts.xaxis.axis_label = "Number of molecules"
counts.yaxis.axis_label = "Number of cells"

layout = bokeh.layouts.layout([[genes, counts]], sizing_mode='fixed')

doc = bokeh.io.curdoc()
doc.title = 'scRNA-seq goodness of fit'
doc.add_root(layout)

init()
