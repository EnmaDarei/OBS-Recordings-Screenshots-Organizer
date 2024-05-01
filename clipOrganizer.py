import obspython as S
from datetime import datetime
import glob, os, re, os.path, shutil
from pathlib import Path

class Data:
    Origin = None
    Destination = None
    CurrentGame = None
    VideoType = None
    ImageType = "png"
    CurrentGameTxt = None

def CreateDestinationPath(CurrentGame):
    current_date = datetime.now()
    DateString = current_date.strftime("%Y\\%m\\%d\\")
    DestinationPath = f"{Data.Destination}{CurrentGame}\\{DateString}"
    return DestinationPath

def FindNewestFile(filepath, extension):
    fileType = f"*.{extension}"
    # print(f"looking for all {fileType} files")
    files = glob.glob(filepath + fileType)
    if files:
        max_file = max(files, key=os.path.getctime)
        return max_file
    else:
        print(f"Error: couldn't find any {extension} files!")
        return None

def CheckDestinationDirectory(destination):
    if not Path(destination).exists():
        Path(destination).mkdir(parents=True, exist_ok=True)

def ReadGameName():
    try:
        with open(Data.CurrentGameTxt, 'r') as file:
            rawGameName = file.read()
            Data.CurrentGame = re.sub(r':', ' -', rawGameName)
            Data.CurrentGame = re.sub(r'[<>"/\\|?*\x00-\x1F\x7F]', '_', Data.CurrentGame)
    except FileNotFoundError:
            print(f"File '{Data.CurrentGameTxt}' not found.")

def MoveFile(source,destination):
    try:
        CheckDestinationDirectory(destination)
        fileName = os.path.basename(source)
        newName = re.sub(r'(Screenshot )?\[.*?\] ', '', fileName)
        shutil.move(source, destination)
        os.rename(os.path.join(destination, fileName), os.path.join(destination, newName))
        print(f"{source} -> {destination}{newName}")
        print("File moved successfully!")
    except FileNotFoundError:
        print("Source file not found")
    except PermissionError:
        print("Permission denied to move the file")
    except Exception as e:
        print(f"An error occurred: {e}")

def on_event(event):

    if event == S.OBS_FRONTEND_EVENT_SCREENSHOT_TAKEN:
        print("Screenshot taken...")
        ReadGameName()
        if Data.CurrentGame != "":
            LatestFile = FindNewestFile(Data.Origin,Data.ImageType)
            if LatestFile:
                Output = CreateDestinationPath(Data.CurrentGame)+"Screenshots\\"
                MoveFile(LatestFile,Output)

    if event == S.OBS_FRONTEND_EVENT_REPLAY_BUFFER_SAVED or event == S.OBS_FRONTEND_EVENT_RECORDING_STOPPED:
        print("Video saved...")
        ReadGameName()
        if Data.CurrentGame != "":
            LatestFile = FindNewestFile(Data.Origin,Data.VideoType)
            if LatestFile:
                Output = CreateDestinationPath(Data.CurrentGame)+"Video\\"
                MoveFile(LatestFile,Output)

def script_load(settings):
    S.obs_frontend_add_event_callback(on_event)

def script_description():
    desc = "Sorts Replays and Screenshots based on current game.\n\nAuthor: Enma Darei"
    return desc

def script_update(settings):
    Data.Origin = S.obs_data_get_string(settings,"origindir")
    if not re.search(r'/$',Data.Origin):
        Data.Origin = Data.Origin+"/"
    Data.Origin = Data.Origin.replace('/','\\')
    Data.Destination = S.obs_data_get_string(settings,"outputdir")
    if not re.search(r'/$',Data.Destination):
        Data.Destination = Data.Destination+"/"
    Data.Destination = Data.Destination.replace('/','\\')
    Data.VideoType = S.obs_data_get_string(settings,"vidExt")
    Data.CurrentGameTxt =  S.obs_data_get_string(settings,"gameTxt")

def script_properties():
    props = S.obs_properties_create()
    S.obs_properties_add_path(
        props, "origindir", "Origin Folder", S.OBS_PATH_DIRECTORY,
        None, str(Path.home()))
    S.obs_properties_add_path(
        props, "outputdir", "Output Folder", S.OBS_PATH_DIRECTORY,
        None, str(Path.home()))
    S.obs_properties_add_path(
        props, "gameTxt", "Game Text File", S.OBS_PATH_FILE,
        "*.txt", None)
    VidList = S.obs_properties_add_list(props, "vidExt", "Video Format", S.OBS_COMBO_TYPE_LIST, S.OBS_COMBO_FORMAT_STRING)
    S.obs_property_list_add_string(VidList, "mkv", "mkv")
    S.obs_property_list_add_string(VidList, "mp4", "mp4")
    return props

print("Recording & Screenshot Organizer Started")
