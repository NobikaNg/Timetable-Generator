import PyInstaller.__main__
import os
import tkcalendar

# Get the path to the tkcalendar library
tkcalendar_path = os.path.dirname(tkcalendar.__file__)

# Define paths for data files
# Note: The separator for --add-data is platform-specific (';' on Windows, ':' on others)
# PyInstaller handles this correctly when using os.pathsep
db_path = os.path.join('src', 'database', 'timetable_generator.db')
db_dest_folder = 'src/database'

# Run PyInstaller
PyInstaller.__main__.run([
    'main.py',
    '--name', 'TimeTableAdmin',
    '--onefile',
    # f'--add-data={db_path}{os.pathsep}{db_dest_folder}',
    f'--add-data={tkcalendar_path}{os.pathsep}tkcalendar',
    '--hidden-import', 'babel.numbers',
    '--hidden-import', 'pytz.zoneinfo',  # For babel/tkcalendar',
    '--paths', 'src',
    '--clean',
    '--specpath', '.'
])
