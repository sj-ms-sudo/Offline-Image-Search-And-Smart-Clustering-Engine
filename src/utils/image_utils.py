import cv2 as cv

def load_image(path):
    return cv.imread(path)

def draw_rectangle(image,faces):
    for face in faces:
        x1,y1,x2,y2 = face.bbox.astype(int)
        cv.rectangle(image,(x1,y1),(x2,y2),(0,255,0),2)
    return image
    
def save_image(image,path):
    cv.imwrite(path,image)