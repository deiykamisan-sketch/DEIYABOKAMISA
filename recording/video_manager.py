"""Safe recording filenames and directories."""
from datetime import datetime,timezone
from pathlib import Path
def recording_path(root,extension='mp4'):
    folder=Path(root)/'recordings'; folder.mkdir(parents=True,exist_ok=True)
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    return folder/f'lecture_{stamp}.{extension}'
