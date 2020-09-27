import cv2
import stack as st
import numpy as np
import statistics as stat
import random
import matplotlib.pyplot as plt


class BreakDetection:
    area_list=[]
    edges_list=[]

    def __init__(self, img_src,scale):   
        self.image_src = img_src
        self.scale=scale 

    def get_possiblebreak(self,contour,area_lst):
        possible_break=[]
        #remove contour that contain highest area(Basically terminal open edges contour)
        #and small area which is not usable for calculating avg
        temp_area_list=[x for x in area_lst if x>20 or x!=max(area_lst)]
        avg=sum(temp_area_list)/len(temp_area_list)
        print("average_value: ",avg)
        
        for i,cnt in enumerate(contour):
            if(area_lst[i]>=avg):
                if max(area_lst)!=area_lst[i]:
                    possible_break.append(cnt)
        return possible_break


    def get_edges(self,cnt):
        peri = cv2.arcLength(cnt, True)
        approx_edges = cv2.approxPolyDP(cnt, 0.04 * peri, True)
        return len(approx_edges)

    def get_area(self,cnt):
        return cv2.contourArea(cnt)

    def getContour(self,_img):
        contours, hierarchy = cv2.findContours(_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        return contours
        

    def run_algo(self):

        img = cv2.imread(self.image_src)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (7, 7), 1)
        canny = cv2.Canny(blur, 90, 100)
        kernel = np.ones((3, 3))
        dilated_img = cv2.dilate(canny, kernel, iterations=1)
        contours=self.getContour(dilated_img)
        contour_img=img.copy()
        breaks_img=img.copy()
        for cnt in contours:
            cv2.drawContours(contour_img, cnt, -1, (random.randint(0,256),random.randint(0,256),random.randint(0,256)), 2)
            #getting area of each contour
            area=self.get_area(cnt)
            self.area_list.append(area)
            #getting list of edges of detected contour
            self.edges_list.append(self.get_edges(cnt))
        
        cv2.drawContours(breaks_img, self.get_possiblebreak(contours,self.area_list), -1, (random.randint(0,256),random.randint(0,256),random.randint(0,256)), 2)
        
        image_matrix=[[img, gray, canny], [dilated_img, contour_img, breaks_img]]
        collage = st.image_matrix(image_matrix,self.scale)
        cv2.imshow("all images", collage)
        #plt.plot(var.area_list)
        #plt.plot(var.eges_list)
        plt.show()
        cv2.waitKey(0)


if __name__ == "__main__":
    var=BreakDetection("images/3.jpg",.6)
    var.run_algo()



