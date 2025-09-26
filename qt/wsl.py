import os
import platform

def is_wsl() -> bool:
	"""
	Detects if the script is running inside Windows Subsystem for Linux (WSL).
	:return : True if running in WSL, False otherwise.
	"""

	if os.name == "posix":  # UNIX-based OS (Linux, MacOS, WSL)
		try:
			with open("/proc/version", "r") as f:
				version_info = f.read().lower()
				if "microsoft" in version_info or "wsl" in version_info:
					return True

		except FileNotFoundError:
			return False

	return False

def host_os() -> str:
	"""
	Returns the host operating system.
	:return: 'Windows' if running in WSL, otherwise the current OS.
	"""
	if is_wsl():
		return "WSL"

	elif os.name == "nt":
		return "Windows"

	elif os.name == "posix":
		return "Linux"

	else:
		return "Unknown"

if __name__ == "__main__":
	print(f"Running in WSL: {is_wsl()}")
	print(f"Host OS: {host_os()}")
	print(f"Platform: {platform.system()} {platform.release()}")