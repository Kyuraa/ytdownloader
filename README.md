# ytdownloader

### Requirements
* **kivy**
* **shutil**

youtube-dl is built-in. (more like included)


Using **youtube-dl** and **kivy** for UI.

Usage is pretty simple.
- Enter a valid youtube video link. If its a playlist provide a starting number. (i.e. if from start type 1)
- Pick if you want to extract audio or not. **Note**: If you tick extract audio, it will download the video and extract audio and delete the original video.

Additionally: It will also convert ".webm" and ".mkv" files to ".mp4" files while keeping the original file. This is due to my personal preference. If you wanna remove it, just comment out "converter(file)" in the code.


![UI](https://github.com/Kyuraa/ytdownloader/tree/main/image.png?raw=true)