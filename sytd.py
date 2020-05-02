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
    header  = [gui.Text("Simple YouTube Downloader", font="Arial, 20", size=(33,1))]
    browser = [gui.Text("Target DIR:", font=(12),size=(10,1)), gui.Input(OSPATH, enable_events=True, key="-Target-", font=(12), size=(50,1)), gui.FolderBrowse("Open", font=(12), size=(6,1))]
    url     = [gui.Text("Video URL:",font=(12), size=(10,1)), gui.Input(key="-URL-", font=(12), size=(50,1), change_submits=True), gui.Button("Paste", enable_events=True, font=(12), size=(6,1))]
    v_name  = [gui.Text("YouTube Video Name",text_color="green", size=(70,1), font=("Arial Bold", 12), key="-VNAME-")]
    thumb   = [gui.Text(size=(23,1)), gui.Image("default_thumb.png",key="-THUMB-", size=(380,220))]
    down    = [gui.Button("Download",font=(12),size=(69,1))]
    proz    = [gui.Text("Download progress...", key="percent",size=(73,1)), gui.Text("Contact: p.mazela@icloud.com")]
    prog    = [gui.ProgressBar(1, auto_size_text=True, key="progress", orientation="h", size=(65,25))]
    
    #making frame layout from widgets
    framelayout     = [browser, url, v_name, thumb, down, proz, prog] 
    #generating frame with caption
    frame   = [gui.Frame('Simple YouTube Downloader', framelayout, font='Any 12', title_color='DarkBlue')]
    #gui layout creation
    layout  = [header, frame]
    
    #Generating window from layout
    mainwindow = gui.Window("Simple YouTube Downloader v1").Layout(layout)

    #update thumbnail image
    def update_thumb(link):          
        yt = pytube.YouTube(link)   
        mainwindow["-VNAME-"].update(yt.title)
        url = yt.thumbnail_url #url for thumbnail
        urllib.request.urlretrieve(url,'thumb.jpg') #download thumbnail as thumb.jpg
        image = Image.open('thumb.jpg') #convert jpg to png and resize image
        image = image.resize([380,220])
        image.save('thumb.png')
        mainwindow["-THUMB-"].update("thumb.png") #update image
    
    #progressbar fuction (update progress)
    def progress_function(stream, chunk, bytes_remaining):
        percent = round((1-bytes_remaining/stream.filesize)*100)
        if( percent%1 == 0):
            progress_bar = mainwindow.FindElement('progress')
            progress_bar.UpdateBar(percent, 100)
            mainwindow["percent"].update("Download: " + str(percent) + "%")
   
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
            ytdown.streams.get_highest_resolution().download(values["-Target-"])
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
