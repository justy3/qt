import re
import os
from .common.help import *
from .common.constants import *
from .wsl import *

# mapping of Windows drives to WSL mounts
WINDOWS_TO_WSL_MOUNTS = {
	'C:': '/mnt/c',
	'D\\Custom\\justy:': '/mnt/d',
	'\\\\server\\Custom\\justy': '/mnt/e',	
}

def w2lp(win_path: str) -> str:
	"""
	Convert a Windows path to a WSL path.
	:param win_path: The Windows path to convert. (e.g. C:\\Users\\Username\\file.txt)
	returns: The corresponding WSL path (e.g. /mnt/c/Users/Username/file.txt)
	"""

	if not is_wsl():
		return win_path

	# normalizes slashes and handle case variations
	win_path = os.path.normpath(win_path)	# converts to "C:\Users\Username\file.txt"

	# match the custom mount points first (handle longer paths first)
	sorted_mounts = sorted(WINDOWS_TO_WSL_MOUNTS.keys(), key=len, reverse=True)
	for win_mount in sorted_mounts:
		if win_path.startswith(win_mount):
			wsl_mount = WINDOWS_TO_WSL_MOUNTS[win_mount]
			relative_path = win_path[len(win_mount):].lstrip('\\/')	# remove mount part and leading slashes
			wsl_path = os.path.join(wsl_mount, relative_path).replace('\\', '/')
			return wsl_path

	# return original if no conversion was possible
	return win_path