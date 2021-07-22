import numpy as np
import cv2

palette = (2 ** 11 - 1, 2 ** 15 - 1, 2 ** 20 - 1)


def compute_color_for_labels(label):
    """
    Simple function that adds fixed color depending on the class
    """
    color = [int((p * (label ** 2 - label + 1)) % 255) for p in palette]
    return tuple(color)


Store = dict()
TOTAL = 0

def draw_boxes(img, bbox, identities=None, offset=(0,0),P=None,Cx=None,R=None):
    global TOTAL
    global Store
    


    n,m,_ = img.shape
    xx1 = int(P[0]*m)
    xx2 = int(P[1]*m)
    yy1 = int(P[2]*n)
    yy2 = int(P[3]*n)


    a1 = (yy2-yy1)/(xx2-xx1)
    b1 = yy1 -a1*xx1

    color = (0, 0, 0)
    Cx *=m 
    Cy =  a1*Cx+b1
    r = int(R*m)
    img = cv2.circle(img, (int(Cx),int(Cy)), r, color, 2)


    for i,box in enumerate(bbox):
        x1,y1,x2,y2 = [int(i) for i in box]
        x1 += offset[0]
        x2 += offset[0]
        y1 += offset[1]
        y2 += offset[1]


    

        X,Y = (int(x2-(x2-x1)/2),y2)
        
        is_in = a1*X+b1<Y
        

        center_coordinates = (int(x2-(x2-x1)/2),y2)




        if is_in:color = (255, 0, 0)
        else:color = (0, 255, 0)
        img = cv2.circle(img, center_coordinates, 10, color, 2)



        # box text and bar
        id = int(identities[i]) if identities is not None else 0   

        # print(TOTAL,is_in)
        #  center_coordinates (m,n)
        if abs(pow(Cx - center_coordinates[0],2)+pow(Cy - center_coordinates[1],2))<r*r and center_coordinates[0]<m and center_coordinates[0]>=0 and center_coordinates[1]<m and center_coordinates[1]>=0:
            if id in Store:
                if is_in !=Store[id]:
                    # print("######")
                    if is_in:TOTAL+=1
                    else:TOTAL-=1

            Store[id] = is_in

        color = compute_color_for_labels(id)
        label = '{}{:d}'.format("", id)
        t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 2 , 2)[0]
        cv2.rectangle(img,(x1, y1),(x2,y2),color,3)
        cv2.rectangle(img,(x1, y1),(x1+t_size[0]+3,y1+t_size[1]+4), color,-1)
        cv2.putText(img,label,(x1,y1+t_size[1]+4), cv2.FONT_HERSHEY_PLAIN, 2, [255,255,255], 2)
    cv2.putText(img,"PEOPLE INSIDE : %d"%TOTAL,(40,100), cv2.FONT_HERSHEY_PLAIN, 5, [255,0,0], 4)
    

    return img

def just_draw(img):
    cv2.putText(img,"PEOPLE INSIDE : %d"%TOTAL,(40,100), cv2.FONT_HERSHEY_PLAIN, 5, [255,0,0], 4)
    return img
def draw_line(img,x1,x2,y1,y2):
    n,m,_ = img.shape
    x1 = int(x1*m)
    x2 = int(x2*m)
    y1 = int(y1*n)
    y2 = int(y2*n)

    cv2.line(img, (x1,y1), (x2,y2), (0, 255, 0), thickness=3, lineType=8)
    return img


if __name__ == '__main__':
    for i in range(82):
        print(compute_color_for_labels(i))
