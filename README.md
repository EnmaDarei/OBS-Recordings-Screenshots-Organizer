# Enma's Recording & Screenshot Organizer
### [**[Download]**](https://github.com/EnmaDarei/OBS-Recordings-Screenshots-Organizer/releases/latest)

A script to automatically organize OBS Recordings, Replays and Screenshots into dated folders based on the game being played using the following folder structure:

```\RecordingsFolder\GameName\YYYY\MM\DD\Screenshots```

```\RecordingsFolder\GameName\YYYY\MM\DD\Videos```

![image](https://github.com/EnmaDarei/OBS-Recordings-Screenshots-Organizer/assets/14081432/45ec6cd6-121b-4047-8117-da516c442aec)
![image](https://github.com/EnmaDarei/OBS-Recordings-Screenshots-Organizer/assets/14081432/4c831016-c9d7-4d01-b1aa-15ab900ebe04)



## Configuration
The script needs to be configured via the OBS Script Properties window:
![image](https://github.com/EnmaDarei/OBS-Recordings-Screenshots-Organizer/assets/14081432/b9fa92ab-65b3-4988-8cf0-27e34422cc4d)

**Origin Folder** - Where OBS is currently saving videos/replays and screenshots.

**Output Folder** - Top level folder where organized game folders will be created.

**Game Text File** - Text file that contains just the name of the current game. This will be read to determine/create destination folder.

**Video Format** - The format OBS saves videos as [mkv or mp4].

## Usage
Just record, save replays, and take screenshots as normal. The script will organize your media automatically as soon as a video or a screenshot are created on the **Origin Folder**.

This script is very much tailored to work with my workflow, it reads from a text file that contains the name of the game you're currently playing. 
I keep that text file updated automatically with Touch Portal, you must find a way to automate updating it or do it manually (or feel free to modify the python script to do that part for you).

I recommend setting your output filename to `[%MM-%DD] %H-%M-%S` on `Advanced>Recording>Filename Formatting`
![image](https://github.com/EnmaDarei/OBS-Recordings-Screenshots-Organizer/assets/14081432/e5fe3b5d-68eb-4f43-a9d3-52569bed8feb)

The script should still work with other file naming conventions, but it checks for that.

<sup>If you find this script useful consider [leaving a tip](https://ko-fi.com/enmadarei)</sup>
