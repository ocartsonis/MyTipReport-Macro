import PyInstaller.__main__

PyInstaller.__main__.run([
    'macro.py',
    '--onefile',
    '--icon=macro.ico'
])