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
			} else if (Math.abs(params.value) < 0.01) {
				return params.value.toPrecision(4);
			} else if (Number.isInteger(params.value)) {
				return params.value.toLocaleString('en-US', { maximumFractionDigits: 0 });
			} else {
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
				value_formatter = formatNumerics if field_name in dataframe and dataframe[field_name].abs().max() > 10_000 else "formatNumber"
				column_def = {
					"cellClass": "number-cell",
					"headerName": field_name,
					"field": field_name,
					"filter": "agNumberColumnFilter",
					"resizable": True,
					"sortable": False,
					"suppressMenu": True,
					"type": "numericColumn",
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
					"filter": "agTextColumnFilter",
					"resizable": True,
					"sortable": False,
					"width": 220,
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
			{"id": "columns", "labelDefault": "Columns", "labelKey": "columns", "toolPanel": "agColumnsToolPanel"},
			{"id": "filters", "labelDefault": "Filters", "labelKey": "filters", "toolPanel": "agFiltersToolPanel"}
		]
	}

	grid_options = {
		"animateRows": True,
		"columnDefs": column_defs,
		"enableCharts": True,
		"enableRangeSelection": True,
		"groupIncludeFooter": True,
		"groupIncludeTotalFooter": True,
		"groupUseEntireRow": False,
		"sideBar": sidebar,
		"statusBar": statusBar,
		"suppressAggFuncInHeader": True,
	}

	defaults = dict(
		column_fit = "auto",
		css_rules = css_rules,
		export_mode = "disabled",
		# export_csv = True,
		# export_excel = False,
		grid_options = grid_options,
		height = 600,
		index=True,
		menu = {"buttons" : []},
		paste_from_excel = True,
		quick_filter = True,
		show_toggle_edit = True,
		show_toggle_delete = False,
		sync_on_edit = True,
		theme = "ag-theme-balham-dark",
	)

	# merge defaults with user args
	grid_options = {**defaults, **kw_aggrid}