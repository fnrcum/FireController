from distutils.core import setup
import py2exe, sys, os
import cmd, code, pdb
import orm

setup(
    options={'py2exe': {'bundle_files': 1, 'compressed': True, 'includes': ["sqlalchemy", "pymysql",
                                                                            "sqlalchemy.sql.default_comparator"]}},
    windows=[{'script': "FireController.py"}],
    zipfile=None,
)

# from cx_Freeze import setup, Executable
#
# base = None
#
#
# executables = [Executable("FireController.py", base=base)]
#
# packages = ["idna"]
# options = {
#     'build_exe': {
#         'packages': packages,
#     },
#
# }
#
# setup(
#     name="FireController",
#     options=options,
#     version="0.1",
#     description='Test Application',
#     executables=executables
# )