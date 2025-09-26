from setuptools import find_packages, setup

setup(
	name="qt",
	version="0.0.1",
	packages=["qt"],
	description="simple package toolkit for python",
	author="justy",
	package_data={
		''  : [
			'*.css',
			'*.csv',
			'common/*',
		]
	}
)