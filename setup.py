from cx_Freeze import setup, Executable

executables = [Executable('main.py', base = "Win32GUI")]

options = {
    'build_exe': {
        'include_msvcr': True,
    }
}

setup(name='Nitshe game',
      version='0.0.1',
      description='test game',
      executables=executables)
