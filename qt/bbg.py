from .common.help import *

# constants
DEFAULT_FIELDS = ["PX_LAST", "PX_OPEN", "PX_LOW", "PX_HIGH", "PX_VOLUME", "EQY_FLOAT", "EQY_SH_OUT", "EQY_WEIGHTED_AVG_PX" ]
DEFAULT_RENAME_DICT = {
	"date"						:	"obs_date",
	"security"					:	"ticker",
	"PX_LAST"					:	"close",
	"PX_OPEN"					:	"open",
	"PX_LOW"					:	"low",
	"PX_HIGH"					:	"high",
	"PX_VOLUME"					:	"volume",
	"EQY_FLOAT"					:	"float_shares",
	"EQY_SH_OUT"				:	"out_shares",
	"EQY_WEIGHTED_AVG_PX"		:	"vwap"
}

def get_bbg_query(set_aik=False):
	from blp import blp
	BBG_QUERY_OBJ = blp.BlpQuery(parser=blp.BlpParser(raise_security_errors=False)).start()

	# set AIK
	if set_aik:
		BBG_QUERY_OBJ.session_options.setApplicationIdentityKey("DUMMY_AIK_FOR_OPEN_SOURCE")

	return BBG_QUERY_OBJ

def bbg_query_fields(tickers, fields, start, end, BBG_QUERY_OBJ=None, options={}):

	# get bloomberg query object
	if BBG_QUERY_OBJ is None:
		BBG_QUERY_OBJ = get_bbg_query(set_aik=False)

	# format date to string
	if isinstance(start, dt.date): start = start.strftime("%Y%m%d")
	if isinstance(end, dt.date): end = end.strftime("%Y%m%d")

	# send query
	t = BBG_QUERY_OBJ.bdh(tickers, fields, start, end, options=options)
	return t