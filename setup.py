from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in shift_rotation/__init__.py
from shift_rotation import __version__ as version

setup(
	name="shift_rotation",
	version=version,
	description="Many businesses have operations and business hours that require staffing outside of a traditional 9 a.m. to 5 p.m. schedule. These organizations often use rotating shifts to meet their staffing demands. These shifts allow employees to learn about different facets of the business while helping employers meet production or service goals.",
	author="preciholesports",
	author_email="azhar@preciholesports.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
