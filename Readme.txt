NtdPlayer Packaging Instruction:

a. Please use Py2App to package NtdPlayer.

b. Tutorial for how to install Py2App
https://pythonhosted.org/py2app/tutorial.html

c. setup.py in already includes in the root of source tree.

d. Clean up build directories by “rm -r build dist”.

e. Run “python setup.py py2app” to start package the app.

P.S.: This app requires the external dylib named “tkdnd2.7”.


** For PC version, use cx_Freeze to pack the app:

a. Use PIP to download the latest cx_Freeze package.
PIP install cx_Freeze

b. Tutorial for detail configuration of cx_Freeze
http://cx-freeze.readthedocs.org/en/latest/distutils.html#distutils

c. Change the version number in both NtdNewsTool.py and info.plist

d. Use below cli command to build the app:
OSX CLI:
python setup_cx.py bdist_mac --iconfile=ntdplayer_512.icns --bundle-name=NtdPlayer --custom-info-plist=info.plist

Win Cli:
python setup_cx.py build