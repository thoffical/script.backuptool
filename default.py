import xbmc
import xbmcaddon
import xbmcgui
import shutil
import os
import platform

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
BACKUP_PATH = xbmc.translatePath('special://home')  # Kodi's home directory

def show_ios_disclaimer():
    """Display a disclaimer for iOS users."""
    if platform.system() == "Darwin" and "iOS" in xbmc.getInfoLabel("System.OSVersionInfo"):
        xbmcgui.Dialog().ok(
            "Incompatible Platform",
            "This add-on does not work on iOS due to strict file system restrictions. "
            "Please use an alternative device to back up your Kodi setup."
        )
        return True
    return False

def get_external_storage():
    """Detects external storage devices across platforms."""
    external_paths = []
    
    if os.name == 'nt':  # Windows
        # Scan for external drives (D:, E:, F:, etc.)
        for drive in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            drive_path = f'{drive}:\\'
            if os.path.exists(drive_path) and os.path.isdir(drive_path):
                external_paths.append(drive_path)
    elif os.name == 'posix':  # Linux/Android/macOS
        # Common mount points for external storage
        possible_mounts = ['/media', '/mnt', '/storage']
        for mount in possible_mounts:
            if os.path.exists(mount):
                for folder in os.listdir(mount):
                    full_path = os.path.join(mount, folder)
                    if os.path.isdir(full_path):
                        external_paths.append(full_path)
    return external_paths

def backup_to_external_storage():
    """Backs up Kodi data to selected external storage."""
    external_devices = get_external_storage()
    if not external_devices:
        xbmcgui.Dialog().notification('Backup to External Storage', 'No external storage found!', xbmcgui.NOTIFICATION_ERROR)
        return

    selected_device = xbmcgui.Dialog().select('Select External Storage', external_devices)
    if selected_device == -1:
        return

    target_path = os.path.join(external_devices[selected_device], 'KodiBackup')

    try:
        shutil.copytree(BACKUP_PATH, target_path, dirs_exist_ok=True)
        xbmcgui.Dialog().notification('Backup Complete', f'Backup saved to: {target_path}', xbmcgui.NOTIFICATION_INFO)
    except Exception as e:
        xbmcgui.Dialog().notification('Backup Failed', f'Error: {str(e)}', xbmcgui.NOTIFICATION_ERROR)

if __name__ == '__main__':
    if not show_ios_disclaimer():
        backup_to_external_storage()
