import cv2
import stack as st
import numpy as np
import random
import matplotlib.pyplot as plt


class UsingEdges():
    area_list=[]
    eges_list=[]

    def get_possiblebreak(self,contour,area_lst):
        possible_break=[]
        temp_area_list=area_lst.copy()
        temp_area_list.remove(max(temp_area_list))
        avg=sum(temp_area_list)/len(temp_area_list)
        for i,cnt in enumerate(contour):
            if(area_lst[i]>=avg*3.1):
                possible_break.append(cnt)
        print(avg)
        return possible_break



    
    def get_edges(self,cnt):
        perl = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.04 * perl, True)
        return len(approx)

    def get_area(self,cnt):
        return cv2.contourArea(cnt)

    def getContour_and_edges(self,_img):
        contours, hierarchy = cv2.findContours(_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        return contours
        

    def run_algo(self):
        blur = cv2.GaussianBlur(gray, (7, 7), 1)
        canny = cv2.Canny(blur, 90, 100)
        kernel = np.ones((3, 3))
        dilated_img = cv2.dilate(canny, kernel, iterations=1)
        contours=self.getContour_and_edges(dilated_img)
        #possible_breaks=[]
        contour_img=img.copy()
        breaks_img=img.copy()
        for cnt in contours:
            cv2.drawContours(contour_img, cnt, -1, (random.randint(0,256),random.randint(0,256),random.randint(0,256)), 2)
            #getting area of each contour
            area=self.get_area(cnt)
            self.area_list.append(area)
            #if (area>=500):
            #    possible_breaks.append(cnt)
            #getting list of edges of detected contour
            self.eges_list.append(self.get_edges(cnt))
        
        cv2.drawContours(breaks_img, self.get_possiblebreak(contours,self.area_list), -1, (random.randint(0,256),random.randint(0,256),random.randint(0,256)), 2)
        
        return [[img, gray, canny], [dilated_img, contour_img, breaks_img]]


img = cv2.imread("images/0.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
var=UsingEdges()
image_matrix=var.run_algo()
area_list=var.area_list
area_list.remove(max(area_list))
collage = st.image_matrix(image_matrix, 1)
plt.plot(var.area_list)
plt.plot(var.eges_list)
cv2.imshow("all images", collage)
plt.show()
cv2.waitKey(0)