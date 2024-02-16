#importing libraries
import cv2
from mido import MidiFile, MidiTrack, Message

# Open the video file
video_capture = cv2.VideoCapture(r"videos/HH24.mp4")
frames = []

while True:
    ret, frame = video_capture.read()
    if not ret:
        break
    frames.append(frame)

# Create a new MIDI file
midi_file = MidiFile()
track = MidiTrack()
midi_file.tracks.append(track)


#Creating notes
current_note0 = None
current_note1 = None
current_note2 = None
current_note3 = None

note_start_time0 = 0
note_start_time1 = 0
note_start_time2 = 0
note_start_time3 = 0

def rgb_brightness(note_start_time,current_note,i):

    if i==3:
        # Calculate the average brightness of the frame
        brightness = int(frame.mean())
    else:
        # Calculate the brightness of rgp channels
        brightness = int(frame[:,:,i].mean())
    
    # Map brightness to a MIDI note value within a specific range 
    # The notes change with as the brightness changes
    if (i==0):
        note = 45 + int(brightness % 49)  
    elif(i==1):
        note = 52 + int(brightness % 49)
    elif(i==2):
        note = 60 + int(brightness % 49)
    else:
        note = 40 + int(brightness % 49)

    if current_note is None:
        current_note = note
        note_start_time = 0
    else:
        # Calculate time difference between frames (adjust as needed)
        time_difference = 120  # You can adjust this value for smoother or faster transitions
        
        if note != current_note:
            # Add a Note Off message for the previous note
            track.append(Message('note_off', note=current_note, velocity=64, time=note_start_time))
            # Add a Note On message for the new note
            track.append(Message('note_on', note=note, velocity=64, time=0))
            current_note = note
            note_start_time = 0
        else:
            note_start_time += time_difference
    return note_start_time,current_note

# looping over each frame in the video
for frame_number, frame in enumerate(frames):
    
    #Downsampling the frame count
    if frame_number % 8 != 0:
        continue
    note_start_time0,current_note0 = rgb_brightness(note_start_time0,current_note0,0)
    note_start_time1,current_note1 = rgb_brightness(note_start_time1,current_note1,1)
    note_start_time2,current_note2 = rgb_brightness(note_start_time2,current_note2,2)
    note_start_time3,current_note3 = rgb_brightness(note_start_time3,current_note3,3)
    
print("Finished")   

# Add a final Note Off message to release the last note
track.append(Message('note_off', note=current_note0, velocity=64, time=note_start_time0))
track.append(Message('note_off', note=current_note1, velocity=64, time=note_start_time1))
track.append(Message('note_off', note=current_note2, velocity=64, time=note_start_time2))
track.append(Message('note_off', note=current_note3, velocity=64, time=note_start_time3))

# Save the file
midi_file.save('ses/HH24_2.mid')