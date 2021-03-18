from pytube import YouTube
import os
import re




link = input("Insert your video's link: ")
format = input("MP4 or MP3? ")




if(format.lower() == "mp4"):
    quality = input('What quality do you want?(1080, 720, 480, 360) ').strip()
    fps = input('FPS? (60, 30) ').strip()

    print("Downloading...")

    yt_obj = YouTube(link).streams.filter(progressive=True)
    print(yt_obj)
    try:
        for i, stream in enumerate(yt_obj):
            pattern = '<Stream: itag="\d+" mime_type="video\/mp4" res="' + re.escape(quality) +'p" fps="' + re.escape(fps) + 'fps" vcodec="avc1\.(?:.+)" acodec="(?:.+)" progressive="True" type="video"'
            stream = str(stream)
            curreg = re.findall(pattern, stream)
            yt_obj[i].download() if curreg else 0
        print('Successfully downloaded.')
    except:
        print('An error has occurred, Try using a different fps/quality or check if the link you entered is correct.')

elif(format.lower() == "mp3"):
    print("Downloading...")
    try:
        yt_obj = YouTube(link).streams.filter(only_audio=True).first()
        output = yt_obj.download()
        name, extension = os.path.splitext(output)
        final_name = name + '.mp3'

        os.rename(output, final_name)
        
        print('Successfully downloaded.')
    except:
        print('error')





