import cx_Freeze

executables = [cx_Freeze.Executable("pyPuzzle.py", base="Win32GUI", icon="assets/images/icon.ico")]

cx_Freeze.setup(
    name="pyPuzzle",
    options={"build_exe": {"packages":["pygame"],"include_files":["assets/"]}},
    
    executables = executables
)