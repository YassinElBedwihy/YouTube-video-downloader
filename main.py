from pytube import YouTube
import os
import re
import moviepy.editor as mpe


link = input("Insert your video's link: ").strip()
format = input("MP4 or MP3? ").strip()

def combine_vid_with_aud(vidpath, audpath, outname):
    clip = mpe.VideoFileClip(vidpath)
    audclip = mpe.AudioFileClip(audpath)

    final_aud = mpe.CompositeAudioClip([audclip])
    clip.audio = final_aud
    
    clip.write_videofile(outname + '.mp4')


if(format.lower() == "mp4"):
    print('Getting available qualities...')
    yt_obj = YouTube(link).streams
    qualities = []
    qualitynums = []
    for i, stream in enumerate(yt_obj):
        #get all available qualities for the vid and choose the best fps
        vidpattern = r'<Stream: itag="\d+" mime_type="video\/mp4" res="\d+p" fps="\d+fps" vcodec="avc\d+\.(?:.+)" progressive="False" type="video">'
        stream = str(stream)
        current_match = re.match(vidpattern, stream)
        if(current_match):  # if there's a match, run another regex to capture(match) only the quality part(e.g. 720p)

            #this whole next section is a little dirty, for reference though:
            #qualitynums is a reference for the index of the stream of the specified quality number, so basically,
            #if qualities[0] == "720p", qualitynums[0] == "4" (for example), and yt_obj[4] is equal to a stream with the quality 720p, it all connects together

            current_match = current_match.group()
            quality_pattern = r'\d+p'
            qualities.append(re.findall(quality_pattern, current_match)[0])
            qualitynums.append(i)
    


    qualities_without_duplicates = [] #check if there are duplicates
    duplicate_nums = []
    for i, quality in enumerate(qualities):
        if quality not in qualities_without_duplicates:
            qualities_without_duplicates.append(quality)
        else:
            arrofduplicates = [qualities_without_duplicates.index(quality), i]
            duplicate_nums.append(arrofduplicates)

    
    for arr in duplicate_nums: #compare the duplicates and choose the one with the highest fps
        first_array_fps = re.findall(r'\d+fps', str(yt_obj[qualitynums[arr[0]]]))[0]
        second_array_fps = re.findall(r'\d+fps', str(yt_obj[qualitynums[arr[1]]]))[0]
        if int(re.findall(r'\d+', first_array_fps)[0]) > int(re.findall(r'\d+', first_array_fps)[0]):
            qualitynums.pop(arr[1])
            qualities.pop(arr[1])
        else:
            qualitynums.pop(arr[0])
            qualities.pop(arr[0])
        
    string = 'Choose a quality (' + ', '.join(qualities) + '): '
    quality = input(string).strip()

    print("Downloading...")

    for i, stream in enumerate(yt_obj): #iterate over all the available streams and choose only the audio
        audpattern = r'<Stream: itag="\d+" mime_type="audio\/mp4" abr="\d+kbps" acodec="(?:.+)" progressive="False" type="audio">'
        stream = str(stream)
        if(re.findall(audpattern, stream)): #make pytube objects for the vid and aud streams
            curregaud = yt_obj[i]
    curregvid = yt_obj[qualitynums[(qualities.index(quality))]]
            
    if(curregvid and curregaud): #download the aud and vid, then combine them using moviepy
        outvid = curregvid.download(filename = curregvid.title + 'video')
        unedited_aud = curregaud.download(filename = curregaud.title + 'audio')
        
        base, ext = os.path.splitext(unedited_aud)
        outaud = base + '.mp3'
        os.rename(unedited_aud, outaud)
        outaud_path = os.path.abspath(outaud)
        outvid_path = os.path.abspath(outvid)
    else:
        raise ValueError('An error has occurred, try reaching out to me on github or choosing a different video to see if the problem is with the script or the video.')

    combine_vid_with_aud(outvid_path, outaud_path, curregvid.title) #make the final combined video.

    os.remove(outvid_path) #remove the seperated video and audio files, only leave the combined vid
    os.remove(outaud_path)
    print('Successfully downloaded.')


elif(format.lower() == "mp3"):
    print("Downloading...")
    try:
        yt_obj = YouTube(link).streams.filter(only_audio=True).first() 
        output = yt_obj.download() #download the audio
        name, extension = os.path.splitext(output)
        final_name = name + '.mp3' 

        os.rename(output, final_name) #turn it into an mp3 file, since pytube downloads audio files as mp4.
        
        print('Successfully downloaded.')
    except:
        print('error')