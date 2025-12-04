import pygame as pg
import cv2
import math

class Point():
    def __init__(self, x, y, z, color=(0, 0, 0), size=5):
        self.x, self.y, self.z = x, y, z
        self.color = color
        self.size = size
    
    def get_pos(self, eye_x, eye_y, eye_z):
        x = self.z * (self.x-eye_x) / (eye_z-self.z)
        y = self.z * (self.y-eye_y) / (eye_z-self.z)
        return x, y
    
class Line():
    def __init__(self, a, b, color, width):
        self.a = a
        self.b = b
        self.color = color
        self.width = width

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

camera = cv2.VideoCapture(0)
frame_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

pg.init()

WIDTH, HEIGHT = 640, 480
screen = pg.display.set_mode((WIDTH, HEIGHT))

l = Line(Point(0, 0, 0), Point(0, 0, 500), (0, 0, 255), 2)

def detect_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return face_cascade.detectMultiScale(gray, 1.3, 5)

def convert_point(a):
    return -a[0]+WIDTH/2, a[1]+HEIGHT/2

face_distance = 1000 # pixels
face_y_offset = -30

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill((255, 255, 255))

    ret, img = camera.read() 
    face_coords = detect_face(img)
    face_center_x = WIDTH/2
    face_center_y = HEIGHT/2
    for x, y, w, h in face_coords:
        face_center_x = float(x+w/2)
        face_center_y = float(y+h/2)+face_y_offset
    
    #pg.draw.circle(screen, (0, 0, 0), (WIDTH - face_center_x, face_center_y), 5)

    face_x, face_y, face_z = (face_center_x-WIDTH/2, face_center_y-HEIGHT/2, face_distance)

    la = l.a.get_pos(face_x, face_y, face_z)
    lb = l.b.get_pos(face_x, face_y, face_z)

    pg.draw.line(screen, l.color, convert_point(la), convert_point(lb), l.width)

    pg.display.flip()

# Close the window
camera.release()

# De-allocate any associated memory usage
cv2.destroyAllWindows()

pg.quit()