"""Version of hollerith module.

On the ``main`` branch, use 'dev0' to denote a development version.
For example:

version_info = 0, 7, 'dev0'

"""
# major, minor, patch
version_info = 0, 7, "dev0"

# Nice string for the version
__version__ = ".".join(map(str, version_info))
