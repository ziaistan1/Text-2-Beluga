import os
import glob

def gen_vid(filename, background_audio_path):
    input_folder = 'chat/'

    # Get all image files in the input folder
    image_files = sorted([f for f in os.listdir(input_folder) if f.endswith('.png')])

    durations = []
    with open(filename, encoding="utf8") as f:
        name_up_next = True
        
        lines = f.read().splitlines()
        for line in lines:
            if line == '':
                name_up_next = True
                continue
            elif line[0] == '#' and not line[1] == '!':
                continue
            elif name_up_next == True:
                name_up_next = False
                continue
            else:
                durations.append(line.split('$^')[1])
                
    # Create a text file to store the image paths and durations
    with open('image_paths.txt', 'w') as file:    
        count = 0
        for image_file, duration in zip(image_files, durations):
            file.write(f"file '{input_folder}{image_file}'\noutpoint {duration}\n")
            count += 1

    video_width = 1920
    video_height = 1920

    # Generate the video using the text file containing image paths and calculated frame rate
    os.system(f"ffmpeg -f concat -i image_paths.txt -vcodec libx264 -crf 25 -vf 'scale={video_width}:{video_height}:force_original_aspect_ratio=decrease,pad={video_width}:{video_height}:(ow-iw)/2:(oh-ih)/2' -pix_fmt yuv420p -y output.mp4")

    if background_audio_path:
        # Add the background audio to the video
        os.system(f"ffmpeg -i output.mp4 -i {background_audio_path} -c:v copy -c:a aac -strict experimental -map 0:v:0 -map 1:a:0 -shortest final_output.mp4")
        os.remove('output.mp4')
    else:
        os.rename('output.mp4', 'final_output.mp4')

    # Remove the temporary text file
    os.remove('image_paths.txt')

if __name__ == '__main__':
    # Input paths for audio addition
    directoryback = "mybackground"
    mp3_files_back = glob.glob(os.path.join(directoryback, "*.mp3"))
    background_audio_path = mp3_files_back[0] if mp3_files_back else None
    print(background_audio_path)

    # Call gen_vid with the background audio path
    gen_vid('your_filename.txt', background_audio_path)
