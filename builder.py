from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder

import subprocess
import os
import time
from pathlib import Path
import shutil

from subprocess import PIPE

from threading import Thread

audioOnly = False
appel = Builder.load_file("suck.kv")

ytpath="\\youtube-dl"
vidlink=""
playliststartnumber=0

#fullargs=[
 #   "youtube-dl",
  #   "--extract-audio",
   #  "--audio-format",
   #  "mp3",
   #  "",
   #  "--output",
   #  " '\%\(title\)s.\%\(ext\)' "
#]


cp= 0
curpath= os.path.dirname(os.path.abspath(__file__))

#ss= "youtube-dl --extract-audio --audio-format mp3 -i https://www.youtube.com/playlist?list=PLhXjW6DZKEpwdDwFp6REjNi25KhJ26RUk --playlist-start 353 --output \"%(title)s.%(ext)s\" "


class Floaty(FloatLayout):

    def downloadvid(self):
        global audioOnly
        global vidlink
        global cp
        global playliststartnumber

        self.ids.linkInput.focus= True
        self.ids.numberInput.focus= True
        self.ids.linkInput.focus= False
        self.ids.numberInput.focus= False
        if not vidlink:
            self.ids.progresslabel.text= "Please enter a link"
            return
        
        if "ab_channel" in vidlink:
            sse= vidlink.split("&ab_channel")
            vidlink= sse[0]
        
        ##########playlist
        if "playlist" in vidlink:
            if not playliststartnumber or int(playliststartnumber) < 1:
                self.ids.progresslabel.text= "Please enter a starting number"
                return

            if audioOnly is True:
                #print(curpath)
                
                argu = "youtube-dl --extract-audio --audio-format mp3 -i " + vidlink +  " --playlist-start " + playliststartnumber + " --output \"%(title)s.%(ext)s\" "
                
                cp = subprocess.Popen(argu,shell=True, cwd=curpath+ytpath)
                #out, err = cp.communicate()
                
                t = Thread(target=self.thread_starter)
                t.daemon = True
                t.start()
            else:
                argu = "youtube-dl -i " + vidlink + " --playlist-start " + playliststartnumber + " --output \"%(title)s.%(ext)s\" "
                
                cp = subprocess.Popen(argu,shell=True, cwd=curpath+ytpath)
                #out, err = cp.communicate()
                
                t = Thread(target=self.thread_starter)
                t.daemon = True
                t.start()
            return
            
        ######### one video only
        #print(audioOnly)
        if audioOnly is True:
            #print(curpath)
            argu = "youtube-dl --extract-audio --audio-format mp3 " + vidlink + " --output \"%(title)s.%(ext)s\" "
            
            cp = subprocess.Popen(argu,shell=True, cwd=curpath+ytpath)
            #out, err = cp.communicate()
            
            t = Thread(target=self.thread_starter)
            t.daemon = True
            t.start()
        else:
            argu = "youtube-dl " + vidlink + " --output \"%(title)s.%(ext)s\" "
            
            cp = subprocess.Popen(argu,shell=True, cwd=curpath+ytpath)
            #out, err = cp.communicate()
            
            t = Thread(target=self.thread_starter)
            t.daemon = True
            t.start()
            
            

    def thread_starter(self):
        global cp
        self.ids.progresslabel.text= "Please wait while processing...."
        self.ids.downloadbutton.disabled= True
        while cp.poll() is None:
            time.sleep(0.5)
            
        exitcode = cp.returncode
        if exitcode == 0:
            self.ids.progresslabel.text= "Video/Audio successfully downloaded"
            makeNmove()
        else:
            self.ids.progresslabel.text= "ERROR!"
        self.ids.downloadbutton.disabled= False
        
    def checkbox_click(self, instance, val):
        
        global audioOnly
        if val:
            #print("Checkbox Checked")
            
            #self.ids.passLabel.text = "HeeHee"
            audioOnly = True
        else:
            #print("Checkbox Unchecked")
            #self.ids.passLabel.text = "Password"
            audioOnly= False

    def linkUpdate(self, instance, val):
        global vidlink
        if not val:
            vidlink = self.ids.linkInput.text
            #print(vidlink)
        
    def playlistnumberUpdate(self,instance,val):
        global playliststartnumber
        if not val:
            playliststartnumber = self.ids.numberInput.text
            #print(playliststartnumber)
    

def makeNmove():
    try:
        Path(curpath+"/downloads").mkdir()
        Path(curpath+"/downloads/mp3").mkdir()
    except:
        pass
    for file in os.listdir(curpath+ytpath):
        if file.endswith(".mp3"):
            shutil.move( os.path.join(curpath+ytpath,file) , os.path.join(curpath+"/downloads/mp3",file)  )
            #print(os.path.join("/mydir", file))
        elif file.endswith(".py") or file.endswith(".exe") or file.endswith(".dll"):
            pass
        else:
            shutil.move( os.path.join(curpath+ytpath,file) , os.path.join(curpath+"/downloads",file)  )
            converter(file)
            

def converter(file):
    if file.endswith(".webm"):
        tempa= file.split(".webm")

        path1=os.path.join(curpath+"/downloads",file)
        path2=os.path.join(curpath+"/downloads",tempa[0])
        #ss= "ffmpeg -i input.webm -c copy output.mp4"
        #ss= "ffmpeg -i \"{}\" -c:v libx264 -c:a aac -strict experimental -b:a 192k \"{}\".mp4".format(path1,path2)
        #ffmpegs= "ffmpeg -i \"{}\" -c copy -strict -2 \"{}\".mp4".format(path1,path2)
        ffmpegs= "ffmpeg -i \"{}\" -c:v libx264 -c:a aac -strict experimental -b:a 192k \"{}\".mp4".format(path1,path2)
        ccp = subprocess.Popen(ffmpegs,shell=True, cwd=curpath+ytpath)

        pass
    elif file.endswith(".mkv"): # after downloading and moving convert file to mp4 format
        tempa= file.split(".mkv")

        #comma="ffmpeg -i LostInTranslation.mkv -codec copy LostInTranslation.mp4"
        path1=os.path.join(curpath+"/downloads",file)
        path2=os.path.join(curpath+"/downloads",tempa[0])
        #ffmpegs="ffmpeg -i " + "\"{}\" ".format(path1) + " -codec copy " + os.path.join(curpath+"/downloads",tempa[0]) + ".mp4"
        ffmpegs= "ffmpeg -i \"{}\" -codec copy -c:a aac -strict -2 \"{}\".mp4".format(path1,path2)
        ccp = subprocess.Popen(ffmpegs,shell=True, cwd=curpath+ytpath)
        #print(file)
        pass
    pass
    
class Fook(App):
    def build(self):
        return Floaty()





if __name__ == '__main__':
    Fook().run()
