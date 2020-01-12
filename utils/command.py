import cv2
from . import face

STATE = {
    "is_start_input": False,
    "is_display_names": False,
    "name": "",
    "selected_image": None,
    "parent_window": "Main",
    "child_window": "Child",
    "key": None
}

def removeChildWindow():
    global STATE

    STATE['is_start_input'] = False
    STATE['name'] = ''
    cv2.destroyWindow(STATE['child_window'])
    # make parent window focus / on top
    cv2.setWindowProperty(STATE['parent_window'], cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setWindowProperty(STATE['parent_window'], cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)
    return cv2.waitKey(1) & 0xFF

def updateChildWindow():
    global STATE

    tmp_image = STATE['selected_image'].copy()
    cv2.putText(tmp_image, STATE['name'], (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 234, 255), 1)
    cv2.imshow(STATE['child_window'], tmp_image)

def listen(key, frame):
    global STATE

    STATE['key'] = key

    if STATE['is_start_input']:
        if (key >= 97 and key <= 122) or key == 32:
            STATE['name'] = STATE['name'] + chr(key)
            updateChildWindow()
        elif key == 8: # BACKSPACE
            STATE['name'] = STATE['name'][:-1]
            updateChildWindow()
        elif key == 13: # ENTER
            # save encoding
            face.save(STATE['name'], STATE['selected_image'])
            STATE['key'] = removeChildWindow()
        elif key == 27: # ESC
            STATE['key'] = removeChildWindow()

    if not STATE['is_start_input']:
        if STATE['key'] == ord('	'):
            r = cv2.selectROI(STATE['parent_window'], frame, fromCenter=False, showCrosshair=False)
            if r[0] > 0:
                STATE['selected_image'] = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
                # Display cropped image
                tmp_image = STATE['selected_image'].copy()
                cv2.putText(tmp_image, "{ Insert Label }", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 234, 255), 1)
                cv2.imshow(STATE['child_window'], tmp_image)
                cv2.setWindowProperty(STATE['child_window'], cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
                cv2.setWindowProperty(STATE['child_window'], cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)

                STATE['is_start_input'] = True
        elif STATE['key'] == ord('f'):
            STATE['is_display_names'] = not STATE['is_display_names']

    if STATE['is_display_names']:
        box_of_faces = face.detect(frame)
        for ((top, right, bottom, left), name) in box_of_faces:
            cv2.rectangle(frame, (left, top), (right, bottom), (111, 240, 242), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (111, 240, 242), 2)

    return STATE
