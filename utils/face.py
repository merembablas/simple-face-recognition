import pickle
import cv2
import face_recognition

DATA_ENCODINGS = { "names": [], "encodings": [] }
FILE_PATH = None
DETECTOR = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
DETECT_CONF = {
    "scaleFactor": 1.1,
    "minNeighbors": 5,
    "minSize": (100, 100)
}

def load(file):
    global DATA_ENCODINGS, FILE_PATH
    FILE_PATH = file

    try:
        f = open(file, 'rb')
        DATA_ENCODINGS = pickle.load(f)
        f.close()
    except (EOFError, FileNotFoundError):
        DATA_ENCODINGS = { "names": [], "encodings": [] }

    return DATA_ENCODINGS

def save(name, image):
    global DATA_ENCODINGS, FILE_PATH

    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb, model='cnn')
    encodings = face_recognition.face_encodings(rgb, boxes)
    for encoding in encodings:
        DATA_ENCODINGS['names'].append(name)
        DATA_ENCODINGS['encodings'].append(encoding)

    f = open(FILE_PATH, "wb")
    f.write(pickle.dumps(DATA_ENCODINGS))
    f.close()

def detect(image):
    global DETECT_CONF, DATA_ENCODINGS, DETECTOR
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    rects = DETECTOR.detectMultiScale(gray, scaleFactor=DETECT_CONF['scaleFactor'], 
        minNeighbors=DETECT_CONF['minNeighbors'], minSize=DETECT_CONF['minSize'],
        flags=cv2.CASCADE_SCALE_IMAGE)

    boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]
    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []
    for encoding in encodings:
        matches = face_recognition.compare_faces(DATA_ENCODINGS['encodings'], encoding)
        name = "Unknown"

        if True in matches:
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            for i in matchedIdxs:
                name = DATA_ENCODINGS['names'][i]
                counts[name] = counts.get(name, 0) + 1

            name = max(counts, key=counts.get)

        names.append(name)

    return zip(boxes, names)