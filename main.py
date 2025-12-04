import pygame as pg
import cv2 

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

camera = cv2.VideoCapture(0)
frame_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

pg.init()

WIDTH, HEIGHT = 640, 480
screen = pg.display.set_mode((WIDTH, HEIGHT))

def detect_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return face_cascade.detectMultiScale(gray, 1.3, 5)

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill((255, 255, 255))


    ret, img = camera.read() 
    face_coords = detect_face(img)
    face_center_x = 0
    face_center_y = 0
    for x, y, w, h in face_coords:
        face_center_x = x+w/2
        face_center_y = y+h/2
    
    pg.draw.circle(screen, (0, 0, 0), (WIDTH - face_center_x, face_center_y), 5)

    pg.display.flip()

# Close the window
camera.release()

# De-allocate any associated memory usage
cv2.destroyAllWindows()

pg.quit()