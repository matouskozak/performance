'''
pre-command
'''
import shutil
import sys
from performance.logger import setup_loggers, getLogger
from shared import const
from shared.mauisharedpython import remove_aab_files, install_latest_maui
from shared.precommands import PreCommands
from shared.versionmanager import versions_write_json, get_version_from_dll_powershell
from test import EXENAME

setup_loggers(True)
logger = getLogger(__name__)
logger.info("Starting pre-command for MAUI Android sample app (dotnet new maui)")

precommands = PreCommands()

install_latest_maui(precommands)
precommands.print_dotnet_info()

# Setup the Maui folder
precommands.new(template='maui',
                output_dir=const.APPDIR,
                bin_dir=const.BINDIR,
                exename=EXENAME,
                working_directory=sys.path[0],
                no_restore=False)

# Build the APK
precommands.execute([])

# Remove the aab files as we don't need them, this saves space
output_dir = const.PUBDIR
if precommands.output:
    output_dir = precommands.output
remove_aab_files(output_dir)

# Copy the MauiVersion to a file so we have it on the machine
maui_version = get_version_from_dll_powershell(rf".\{const.APPDIR}\obj\Release\{precommands.framework}\android-arm64\linked\Microsoft.Maui.dll")
version_dict = { "mauiVersion": maui_version }
versions_write_json(version_dict, rf"{output_dir}\versions.json")
print(f"Versions: {version_dict}")
