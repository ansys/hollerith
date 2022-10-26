"""Version of hollerith module.

On the ``master`` branch, use 'dev0' to denote a development version.
For example:

version_info = 0, 2, 'dev0'

"""
# major, minor, patch
version_info = 0, 1, 0

# Nice string for the version
__version__ = ".".join(map(str, version_info))
