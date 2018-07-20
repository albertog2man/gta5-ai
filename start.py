import numpy as np 
from PIL import ImageGrab
import cv2
import time
import pyautogui
from directKeyMaps import PressKey, ReleaseKey, W, A, S, D

last_time = time.time()

def roi(img, vertices): #region of interest
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(img, mask)
    return masked

def get_fps(last_time):
    time_value = time.time()
    if( time_value - last_time ):
        return round(1.0 / (time_value - last_time))
    else:
        return 0    

def grab_screen():
    return np.array(ImageGrab.grab(bbox=(0,40,800,640)))

def draw_lines(img, lines):
    try:
        for line in lines:
            coords = line[0]
            cv2.line(img, (coords[0],coords[1]), (coords[2],coords[3]), [255,255,255], 3)
    except:
        pass
        
def process_img(original_image):
    processed_img = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1=200, threshold2=300)
    processed_img = cv2.GaussianBlur(processed_img, (3,3),0)

    vertices = np.array([[10,500],[10,300],[300,200], [500,200], [800,300], [800, 500]])
    processed_img = roi(processed_img, [vertices])

    #finds lines and allows for a gap threshold
    lines = cv2.HoughLinesP(processed_img, 1, np.pi/180, 180, np.array([]), 200, 15)
    
    draw_lines(processed_img, lines)
    return processed_img


while(True):
    print('FPS: {}'.format(get_fps(last_time)))
    last_time = time.time()
    
    cv2.imshow('window', process_img(grab_screen()))

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
