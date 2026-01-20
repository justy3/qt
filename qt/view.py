from .common.help import *
from ipyaggrid import Grid

css_rules = """
	.number-cell {
		text-align: left;
		width: 10;
	}

	.left-align {
		text-align: left;
	}

	.ag-cell {
		padding-left: 1px; /* Adjust to the minimum necessary */
		padding-right: 1px;
	}

	/* Reduce padding inside header cells */
	.ag-header-cell {
		padding-left: 1px;
		padding-right: 1px;
	}
"""

formatNumerics = """
	function formatNumber(params){
		if (params.value !== undefined && params.value !== null){
			if (params.value === 0){
				return "0.";
			}
			else{
				if (Math.abs(params.value) < 0.0001) {
					return params.value.toExponential(2);
				}
				else if (Math.abs(params.value) < 0.01) {
					return params.value.toPrecision(4);
				}
				else if (Number.isInteger(params.value)) {
					return params.value.toLocaleString('en-US', { maximumFractionDigits: 0 });
				}
				else {
					return params.value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
				}
			}
		}
		return "-";
	}
	"""

url_renderer = """
	function(params) {
		var link = document.createElement("a");
		link.href = params.value;
		link.innerText = params.value;
		return link;
	}
	"""

stddev_func = {
	'std'	: {
		'name' : 'Std Dev',
		'func' : """
		function(params) {
			var data = params.values;
			var n = data.length;
			if (n === 0) return null;
			var mean = data.reduce((a, b) => a + b, 0) / n;
			var variance = data.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / n;
			return Math.sqrt(variance);
		}
		"""
	}
}


aggridlicensekey = 'DUMMY_AGGRID_KEY_DO_NOT_USE'

def view(df=None, url_columns=[], show_menu=True, **kw_aggrid):
	"""Creates a new AGGrid wrapped object

	Args:
		df (Union[str, DataFrame], Optional): Either a DataFrame or an Amadis query. Defaults to None.
		amadis_url (str, Optional): The Amadis web API URL to use if applicable
		**_ag_grid (dict, optional): A list of grid options overrides to allow customization
	"""

	if df is None or not isinstance(df, pd.DataFrame):
		log.warning("DataFrame is None or type(df) isn’t pd.DataFrame")
		return pd.DataFrame()

	if isinstance(df, pd.DataFrame):
		column_defs = []
		dataframe = df.reset_index()
		dataframe.columns = [str(c).replace('.', '_') for c in dataframe.columns]  # . represents a JSON parent to child relationship that AG Grid would misunderstand
		types = dataframe.dtypes

		for field in types.index:

			field_name = str(field)

			if (np.issubdtype(types[field], np.number) or "int" in str(types[field])):

				# value_formatter = formatNumerics if field_name in dataframe and dataframe[field_name].abs().max() > 10_000 else "formatNumber"
				value_formatter = formatNumerics

				column_def = {
					"cellClass"	:	"number-cell",
					"headerName":	field_name,
					"field"		:	field_name,
					"filter"	:	"agNumberColumnFilter",
					"resizable"	:	True,
					"rowGroup"	:	False,
					"sortable"	:	True,
					# "suppressMenu":	True,
					"type": "numberValue",
					"valueFormatter": value_formatter,
					"width": 130
				}

			else:
				column_def = {
					"cellClass": "left-align",
					"enableRowGroup": True,
					"enablePivot": True,
					"headerName": field_name,
					"field": field_name,
					"filter": "agSetColumnFilter",
					"resizable": True,
					"rowGroup" : False,
					"sortable": True,
					"width": 200,
					"pinned": "left" if field == types.index[0] else None
				}

			# add url columns
			if field_name in url_columns:
				column_def["cellRenderer"] = url_renderer

			# add column definition
			if not show_menu:
				column_def["suppressMenu"] = True
			column_defs.append(column_def)

	statusBar = {
		"statusPanels": [
			{
				"statusPanel": "agAggregationComponent",
				"align": "right",
				"statusPanelParams": {
					"aggFuncs": [
						"count",
						"avg",
						"min",
						"max",
						"sum"
					]
				}
			}
		]
	}

	sidebar = {
		"hiddenByDefault": False,
		"toolPanels": [
			{"iconKey" : "columns", "id": "columns", "labelDefault": "Columns", "labelKey": "columns", "toolPanel": "agColumnsToolPanel"},
			{"iconKey" : "filter",	"id": "filters", "labelDefault": "Filters", "labelKey": "filters", "toolPanel": "agFiltersToolPanel"}
		]
	}

	grid_options = {
		"animateRows": True,
		"columnDefs": column_defs,
		"enableRangeSelection": True,
		"enableCharts": True,
		"groupIncludeFooter": True,
		"groupIncludeTotalFooter": True,
		"rowGroupPanelShow" : "always",
		# "groupUseEntireRow": False,
		"sideBar": sidebar,
		"statusBar": statusBar,
		"suppressAggFuncInHeader": True,
	}

	defaults = dict(
		columns_fit = "auto",
		css_rules = css_rules,
		export_mode = "disabled",
		# export_csv = True,
		# export_excel = False,
		grid_options = grid_options,
		height = 600,
		index=True,
		menu = {"buttons" : []},
		# paste_from_excel = True,
		quick_filter = True,
		# show_toggle_edit = True,
		# show_toggle_delete = False,
		# sync_on_edit = True,
		theme = "ag-theme-balham-dark",
	)

	# merge defaults with user args
	grid_options = {**defaults, **kw_aggrid}

	return Grid(
		grid_data=dataframe,
		# license = aggridlicensekey,
		**grid_options
	)

# displays a scrollable table vertically and horizontally
def view2(df, h=30, w=None, **kwargs):
	CSS_VIEW = """
	<style>
		.table {
			text-align: left;
			position: relative;
			border-collapse: collapse;
			border-spacing: 0;
			white-space: nowrap;
		}

		th,
		td {
			padding: 0.25rem;
		}

		tr.red th {
			background: red;
			color: white;
		}

		tr.green th {
			background: green;
			color: white;
		}

		tr.purple th {
			background: purple;
			color: white;
		}

		th {
			background: black;
			position: sticky;
			top: 0;
			/* Don't forget this, required for the stickiness */
			box-shadow: 0 2px 2px -1px rgba(0, 0, 0, 0.4);
		}
	</style>
	"""

	hstr = "100%"
	wstr = "100%"

	if h is not None:
		h = min(h, len(df)+2)
		hstr = f"{h*27}px"

	if w is not None:
		w = f"{w}px"

	# html form of dataframe
	df_html = df.to_html(classes='table')

	# add scrollability
	scrollable_df = CSS_VIEW + f"""
	<html>
	<head><title>HTML Pandas Dataframe with CSS </title></head>
	<link rel = "stylesheet" type = "text/css" href = "df_style.css"/>
	<div style="height:{hstr}; width:{wstr}; overflow:auto;">
		{df_html}
	</div>
	</html>.
	"""
	display(HTML(scrollable_df))


def view3(df, get_str=False, **kwargs):
	df_s = df.to_markdown(tablefmt = 'psql', index=False)

	if get_str:
		return df_s

	else:
		print(df_s)

def fmt_dict(d: dict):
	return json.dumps(d, indent=4, sort_keys=True)


from IPython.core.display import HTML

#Acceps a list of IpyTable objects and returns a table which contains each IpyTable in a cell
def vc_counts(df, column_list=None):
	if column_list is None:
		column_list = df.columns.tolist()
	table_list = [pd.DataFrame(df[c].value_counts()) for c in column_list]
	return HTML('<table>' +  ''.join(['<td>' + table._repr_html_() + '</td>' for table in table_list]) +'</tr></table>')