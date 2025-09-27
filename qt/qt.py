from .common.help import *

###################################
######     CONFIGURATION  #########
###################################

pd.options.display.max_columns = None
pd.options.display.max_rows = 35
pd.options.display.float_format = '{:,.2f}'.format
pd.options.plotting.backend = "plotly"
InteractiveShell.ast_node_interactivity = "all"

###################################
######     TEST FUNCTION  #########
###################################

def hello_world():
	print("justy says hi!")