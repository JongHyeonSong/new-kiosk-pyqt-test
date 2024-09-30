import cv2
import subprocess

# Specify the RTSP server URL (local network or localhost)
# rtsp_url = "rtsp://localhost:8554/mystream"
rtsp_url = "rtsp://192.168.0.5:8554/mystream"
 
# Start capturing video from the USB camera
cap = cv2.VideoCapture(0)  # 0 is usually the default camera

# Define the command for FFmpeg to stream video over RTSP
ffmpeg_command = [
    'ffmpeg',
    '-y',  # Overwrite output files
    '-f', 'rawvideo',  # Input format
    '-vcodec', 'rawvideo',  # Input codec
    '-pix_fmt', 'bgr24',  # Input pixel format
    '-s', f"{int(cap.get(3))}x{int(cap.get(4))}",  # Frame size: width x height
    '-r', '30',  # Frame rate
    '-i', '-',  # Input from stdin (pipe)
    '-c:v', 'libx264',  # Video codec
    '-preset', 'ultrafast',  # Compression preset (ultrafast has the least compression)
    '-f', 'rtsp',  # Output format
    rtsp_url  # Output URL
]

# Start FFmpeg as a subprocess
process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)

# Continuously read frames from the camera and send them to FFmpeg
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Write the frame to the FFmpeg process stdin
    process.stdin.write(frame.tobytes())

# Release resources
cap.release()
process.stdin.close()
process.wait()
