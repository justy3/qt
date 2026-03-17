import ipyaggrid
import pandas as pd
import ipywidgets as widgets
import plotly.graph_objects as go
import plotly.express as px

from IPython.display import display, HTML

def use_mp():
	pd.options.plotting.backend = 'matplotlib'

def use_pl():
	pd.options.plotting.backend = 'plotly'

def create_widget(plots, names=[], display_plot=True, mode="tab"):
	# 3 modes are supported - tab/vbox/hbox

	if isinstance(names, str):
		names = [names]

	if not isinstance(plots, list):
		plots = [plots]

	for i in range(len(plots)):
		plt = plots[i]

		if not isinstance(plt, ipyaggrid.grid.Grid):
			plots[i] = go.FigureWidget(plt)

	if len(names) == 0:
		names = [f"Plot {i+1}" for i in range(len(plots))]

	assert len(names) == len(plots), f"Length of names must match length of plots, len(plots) = {len(plots)} and len(names) = {len(names)}"

	# create tabs and add plots
	WO = {
		"tab"	:	widgets.Tab,
		"vbox"	:	widgets.VBox,
		"hbox"	:	widgets.HBox
	}

	wo = WO.get(mode, None)
	assert wo is not None, f"Mode {mode} not supported, only tab/vbox/hbox are supported"

	# plot
	wdg_layout = widgets.Layout(display='flex', flex_flow='column', align_items='stretch', width='100%')
	plt_wdg = wo(children=plots, layout=wdg_layout)

	# set tab titles
	if mode == "tab":
		for i in range(len(plots)):
			plt_wdg.set_title(i, names[i])

	if display_plot:
		display(plt_wdg)

	else:
		return plt_wdg