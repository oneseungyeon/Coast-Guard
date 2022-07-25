import os
import pytesseract # 그림 글씨인식 모듈 OCR
import math
import csv # csv 파일 사용
import re# 정규 표현 처리
import cv2  # 영상처리 모듈
import numpy as np # 행렬
import math # 복소수를 제외한 수학 함수
import matplotlib.pyplot as plt
from tqdm import tqdm
import time

class meta_info :

    def geo_info(self, frame_folder_dir, output) :
        # 해당 함수는 영상으로부터 1차적으로 추출한 문자데이터결과를 생성하는 함수로, 생성한 파일을 확인해보면, 많은 부분에서 후처리가 필요한 상태임

        # frame meta dict
        frame_meta_list = []
        meta_list = ["Filename", "Tlat_d", "Tlat_m", "Tlon_d", "Tlon_m", "Alat_d", "Alat_m", "Alon_d", "Alon_m", "Az", "El", "Date", "Time", "img"]

        # frame folder dir generation
        frame_nm_list = os.listdir(frame_folder_dir)
        for frame_nm in tqdm(frame_nm_list) :
            frame_dir = os.path.join(frame_folder_dir, frame_nm)
            frame = cv2.imread(frame_dir, cv2.IMREAD_GRAYSCALE)
            Az = frame[697:716, 770:845]
            El = frame[697:716, 918:989]
            Date = frame[697:716, 1010:1160]
            Time = frame[697:716, 1160:1277]
            img = frame[0:26, 0:60]
            Tlat_d = frame[668:690, 118:151]
            Tlat_m = frame[668:690, 166:251]
            Tlon_d = frame[668:690, 331:374]
            Tlon_m = frame[668:690, 391:468]
            Alat_d = frame[697:716, 75:109]
            Alat_m = frame[697:716, 122:203]
            Alon_d = frame[697:716, 341:388]
            Alon_m = frame[697:716, 403:481]

            # save meta info of a frame in dict type
            frame_dict = {}
            frame_dict[meta_list[0]] = frame_nm

            frame_dict[meta_list[1]] = pytesseract.image_to_string(Tlat_d, lang=None, config='--psm 8')
            if frame_dict[meta_list[1]] == "":
                frame_dict[meta_list[1]] = "None"
                print("Tlat None")

            frame_dict[meta_list[2]] = pytesseract.image_to_string(Tlat_m, lang=None, config='--psm 8')
            if frame_dict[meta_list[2]] == "":
                frame_dict[meta_list[2]] = "None"
                print("Tlat None")

            frame_dict[meta_list[3]] = pytesseract.image_to_string(Tlon_d, lang=None, config='--psm 8')
            if frame_dict[meta_list[3]] == "":
                frame_dict[meta_list[3]] = "None"
                print("Tlon None")

            frame_dict[meta_list[4]] = pytesseract.image_to_string(Tlon_m, lang=None, config='--psm 8')
            if frame_dict[meta_list[1]] == "":
                frame_dict[meta_list[4]] = "None"
                print("Tlon None")

            frame_dict[meta_list[5]] = pytesseract.image_to_string(Alat_d, lang=None, config='--psm 8')
            if frame_dict[meta_list[5]] == "":
                frame_dict[meta_list[5]] = "None"
                print("Alat None")

            frame_dict[meta_list[6]] = pytesseract.image_to_string(Alat_m, lang=None, config='--psm 8')
            if frame_dict[meta_list[6]] == "":
                frame_dict[meta_list[6]] = "None"
                print("Alat None")

            frame_dict[meta_list[7]] = pytesseract.image_to_string(Alon_d, lang=None, config='--psm 8')
            if frame_dict[meta_list[7]] == "":
                frame_dict[meta_list[7]] = "None"
                print("Alon None")

            frame_dict[meta_list[8]] = pytesseract.image_to_string(Alon_m, lang=None, config='--psm 8')
            if frame_dict[meta_list[8]] == "":
                frame_dict[meta_list[8]] = "None"
                print("Alon None")
            frame_dict[meta_list[9]] = pytesseract.image_to_string(Az, lang=None, config='--psm 8')
            if frame_dict[meta_list[9]] == "" :
                frame_dict[meta_list[9]] = "None"
                print("Az None")

            frame_dict[meta_list[10]] = pytesseract.image_to_string(El, lang=None, config='--psm 8')
            if frame_dict[meta_list[10]] == "" :
                frame_dict[meta_list[10]] = "None"
                print("El None")

            frame_dict[meta_list[11]] = pytesseract.image_to_string(Date, lang=None, config='--psm 8')
            if frame_dict[meta_list[11]] == "" :
                frame_dict[meta_list[11]] = "None"
                print("Date None")

            frame_dict[meta_list[12]] = pytesseract.image_to_string(Time, lang=None, config='--psm 8')
            if frame_dict[meta_list[12]] == "" :
                frame_dict[meta_list[12]] = "None"
                print("Time None")

            frame_dict[meta_list[13]] = pytesseract.image_to_string(img, lang=None, config='--psm 8')
            if frame_dict[meta_list[13]] == "":
                frame_dict[meta_list[13]] = "None"
                print("Img None")

            frame_meta_list.append(frame_dict)

        # dict to csv format file
        with open(output, "w", encoding='UTF-8-sig', newline='', ) as f:
            writer = csv.DictWriter(f, fieldnames=meta_list)
            writer.writeheader()
            for data in frame_meta_list:
                writer.writerow(data)

        return frame_meta_list

    def interpolation(self, input, output):
        """
        :param input: get the result from "def : get_info" function
        :param output: the results interpolated, and manipulated by the "def : interpolation"
        :param interpolation: False or True -> no meaning (deprecated after some testings.)
        :return:
        """
        f = open(input, 'r', encoding='UTF-8', newline="", errors="ignore")
        f = csv.reader(f)

        # pattern reg
        Loc_d_p = re.compile('(\d{2,3})')  # Tlat, Tlon, ALat, Alon
        Loc_m_p = re.compile('\d{1,2}.\d{3}')
        Pos_p = re.compile('([+-]?\d{1,2})(\D+)(\d{1,2})')  # Az, El
        Date_p = re.compile('(\d{2})-([a-zA-Z]{3})-(\d{4})')  # Date
        Time_p = re.compile("(\d{2}):(\d{2}):(\d{2})")  # Time
        img_p = re.compile('[a-zA-Z]{4}')
        # geo-data
        meta_list = ["Filename", "Tlat_d", "Tlat_m", "Tlon_d", "Tlon_m", "Alat_d", "Alat_m", "Alon_d", "Alon_m", "Az", "El", "Date", "Time", "img"]
        temp_meta = []

        for idx, line in enumerate(f) :
            if idx == 0 : continue # 맨 처음 열은 열 별 이름이므로 패스
            Tlat_d_re = re.findall(Loc_d_p, line[1])
            Tlat_m_re = re.findall(Loc_m_p, line[2])
            Tlon_d_re = re.findall(Loc_d_p, line[3])
            Tlon_m_re = re.findall(Loc_m_p, line[4])
            Alat_d_re = re.findall(Loc_d_p, line[5])
            Alat_m_re = re.findall(Loc_m_p, line[6])
            Alon_d_re = re.findall(Loc_d_p, line[7])
            Alon_m_re = re.findall(Loc_m_p, line[8])
            Az_re = re.findall(Pos_p, line[9])
            El_re = re.findall(Pos_p, line[10])
            Date_re = re.findall(Date_p, line[11])
            Time_re = re.findall(Time_p, line[12])
            img_re = re.findall(img_p, line[13])

            if Tlat_d_re == []:
                Tlat_d_re = [temp_meta[idx-2][1]]

            if Tlat_m_re == []:
                Tlat_m_re = [temp_meta[idx-2][2]]

            if Tlon_d_re == []:
                Tlon_d_re = [temp_meta[idx-2][3]]

            if Tlon_m_re == []:
                Tlon_m_re = [temp_meta[idx-2][4]]

            if Alat_d_re == []:
                Alat_d_re = [temp_meta[idx-2][5]]

            if Alat_m_re == []:
                Alat_m_re = [temp_meta[idx-2][6]]

            if Alon_d_re == []:
                Alon_d_re = [temp_meta[idx-2][7]]

            if Alon_m_re == []:
                Alon_m_re = [temp_meta[idx-2][8]]

            if Az_re != []:
                Az_re = str(Az_re[0][0]) + "." + str(Az_re[0][2]) + '°'
            else : Az_re = temp_meta[idx-2][9]

            if El_re != []:
                El_re = str(El_re[0][0]) + "." + str(El_re[0][2]) + '°'
            else : El_re = temp_meta[idx-2][10]

            if Date_re != [] :
                Date_re = str(Date_re[0][0])+"-"+str(Date_re[0][1])+"-"+str(Date_re[0][2])
            else : Date_re = temp_meta[idx-2][11]

            if Time_re != [] :
                Time_re = str(Time_re[0][0])+":"+str(Time_re[0][1])+":"+str(Time_re[0][2])
            else : Time_re = temp_meta[idx-2][12]

            if img_re != [] and img_re[0][2] == 'I':
                    img_re = 'RGB'
            else : img_re = 'Thermal'

            temp_meta.append([line[0], Tlat_d_re[0], Tlat_m_re[0], Tlon_d_re[0], Tlon_m_re[0], Alat_d_re[0],
                              Alat_m_re[0], Alon_d_re[0], Alon_m_re[0], Az_re, El_re, Date_re, Time_re, img_re])

            file = open(output, 'w', newline='')
            writer = csv.writer(file)
            writer.writerow(meta_list)
            for line in temp_meta:
                writer.writerow(line)

if __name__ == "__main__":

    i = meta_info()
    i.geo_info(frame_folder_dir="./test", output="./test.csv")
    i.interpolation(input="./test.csv",output="test_interpolation.csv")

