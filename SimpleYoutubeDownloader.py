import PySimpleGUI as gui
import pytube
import urllib.request                        
from PIL import Image
import clipboard
import os

#Get current working directory
OSPATH = os.getcwd()

def main():
    gui.theme("Material2")

    #GUI Widgets
    header  = [gui.Text("Simple YouTube Downloader", font=("Arial", 16), size=(24,1))]
    browser = [gui.Text("Target DIR:", font=("Arial", 11),size=(10,1)), gui.Input(OSPATH, enable_events=True, key="-Target-", font=("Arial", 11), size=(45,1)), gui.FolderBrowse("Open", font=("Arial", 11), size=(8,1))]
    url     = [gui.Text("Video URL:",font=("Arial", 11), size=(10,1)), gui.Input(key="-URL-", font=("Arial", 11), size=(45,1), change_submits=True), gui.Button("Paste", enable_events=True, font=("Arial", 11), size=(8,1))]
    v_name  = [gui.Text("YouTube Video Name",text_color="green", font=("Arial", 10),size=(23,9), key="-VNAME-"), gui.Image("default_thumb.png",key="-THUMB-", size=(259,150))]
    proz    = [gui.Text("Progress...   ", key="percent",font=("Courier New", 10)), gui.ProgressBar(1, key="progress", orientation="h", size=(40,25))]
    line    = [gui.Text()]
    down    = [gui.Button("Download",font=("Arial", 11), size=(66,2))]
    
    #making frame layout from widgets
    framelayout     = [browser, url, v_name, line, 
    down] 
    #generating frame with caption
    frame   = [gui.Frame('Simple YouTube Downloader', framelayout, font=("Arial", 11), title_color='DarkBlue')]
    #gui layout creation
    layout  = [header, frame, proz]
    
    #Generating window from layout
    mainwindow = gui.Window("Simple YouTube Downloader v1").Layout(layout)

    #update thumbnail image
    def update_thumb(link):          
        yt = pytube.YouTube(link)   
        mainwindow["-VNAME-"].update(yt.title)
        url = yt.thumbnail_url #url for thumbnail
        urllib.request.urlretrieve(url,'thumb.jpg') #download thumbnail as thumb.jpg
        image = Image.open('thumb.jpg') #convert jpg to png and resize image
        image = image.resize([259,150])
        image.save('thumb.png')
        mainwindow["-THUMB-"].update("thumb.png") #update image
    
    #progressbar fuction (update progress)
    def progress_function(stream, chunk, bytes_remaining):
        percent = round((1-bytes_remaining/stream.filesize)*100)
        if( percent%1 == 0):
            progress_bar = mainwindow.FindElement('progress')
            progress_bar.UpdateBar(percent, 100)
            mainwindow["percent"].update("Loading: " + str(percent) + "% ")
   
    while True:
        event, values = mainwindow.read()

        if event in (None, 'Exit'):
            break

        if event in "-URL-":
            if "you" in values["-URL-"]:
                update_thumb(values["-URL-"])
            else:
                pass

        if event in "Download":
            ytdown = pytube.YouTube(values["-URL-"],on_progress_callback=progress_function)
            ytdown.streams.first().download(values["-Target-"])
            gui.PopupAutoClose("Download", ytdown.title, "finished!")

        if event in "Paste":
            clip = clipboard.paste()
            mainwindow["-URL-"].update(clip)
            if "you" in clip:
                update_thumb(clipboard.paste())
            else:
                pass
  
    mainwindow.Close()

if __name__ == "__main__":
    main()