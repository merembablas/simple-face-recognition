from imutils.video import VideoStream, FileVideoStream
from imutils import resize
import argparse
import time
import cv2
from utils import command, face

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", 
    required=False, help="Streaming from file, webcam, or ipcam")
ap.add_argument("-d", "--data", 
    required=False, help="Face data encoding file", default="default")
args = vars(ap.parse_args())

# load data encoding
face.load('data/' +  args.get('data', 'default'))

if args.get('video', None) != None:
    vs = FileVideoStream(path=args["video"]).start()
else:
    vs = VideoStream(usePiCamera=False).start()

time.sleep(1.0)

while True:
    frame = vs.read()
    if frame is None:
        break

    frame = resize(frame, width=800)
    key = cv2.waitKey(1) & 0xFF

    # listen command
    state = command.listen(key, frame)

    # ESC to exit
    if not state['is_start_input'] and state['key'] == 27:
        break

    cv2.imshow("Main", frame)

vs.stop()

# close all windows
cv2.destroyAllWindows()