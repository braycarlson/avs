from pathlib import Path


# The current-working directory of the project
CWD = Path.cwd().parent

# The drive of the project
ROOT = Path(CWD.anchor)

# The icon for avs
ICON = CWD.joinpath('asset/avs.ico')

# The root directory for the package
PACKAGE = CWD.joinpath('avs')

# The file for all parameter settings
SETTINGS = PACKAGE.joinpath('settings')

# The directory for warbler.py
WARBLER = Path('E:/code/personal/warbler.py/')

# The directory for pickled recordings
PICKLE = WARBLER.joinpath('output/pickle')
