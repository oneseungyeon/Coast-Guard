from math import *
import numpy as np
import csv
import re

def img23d(input, output):
    f = open(input, 'r')
    file = csv.reader(f)
    output_list = {"name": [], "x": [], "y": [], "Alat": [], "Alon": [], "az": [], "el": [], "Date": [], "Time": []}
    output = {"name": [], "X": [], "Y": [], "Z" : []}
    for line in file:
        name = line[0]
        xmin = line[3]
        ymin = line[4]
        xmax = line[5]
        ymax = line[6]

        x = (int(xmin) + int(xmax)) / 2
        y = (int(ymin) + int(ymax)) / 2

        output_list["name"].append(name)
        output_list["x"].append(x)
        output_list["y"].append(y)

        Alat_re = re.compile('(\d{1,4})(\D+)(\d{1,4})(\D+)(\d{1,4})')
        az_re = re.compile('([+-]?\d{1,2})(\D+)(\d{1,2})')
        Date_re = re.compile('(\d{2})-([a-zA-Z]{3})-(\d{4})')
        Time_re = re.compile("(\d{2}):(\d{2}):(\d{2})")

        Alat = re.findall(Alat_re, line[7])
        Alon = re.findall(Alat_re, line[8])
        az = re.findall(az_re, line[12])
        el = re.findall(az_re, line[13])
        Date = re.findall(Date_re, line[14])
        Time = re.findall(Time_re, line[15])

        output_list["Alat"].append(Alat)
        output_list["Alon"].append(Alon)
        output_list["az"].append(az)
        output_list["el"].append(el)
        output_list["Date"].append(Date)
        output_list["Time"].append(Time)

        xp = 1
        yp = 1

    for i in range(10):
        om1 = float(output_list["az"][i][0][0]+'.'+output_list["az"][i][0][2])
        om = om1 * pi / 180
        ph = 0
        kp1 = float(output_list["el"][i][0][0] + '.' + output_list["el"][i][0][2])
        kp = kp1 * pi / 180

        # 회전행렬
        Rom = np.matrix([[1, 0, 0], [0, cos(om), -sin(om)], [0, sin(om), cos(om)]])
        Rph = np.matrix([[cos(ph), 0, sin(ph)], [0, 1, 0], [-sin(ph), 0, cos(ph)]])
        Rkp = np.matrix([[cos(kp), -sin(kp), 0], [sin(kp), cos(kp), 0], [0, 0, 1]])
        R = Rom * Rph * Rkp
        R_inv = np.linalg.inv(R)

        # 카메라 주점, 초점거리
        f = 1.5
        la = R_inv[2,0] / -f
        c = np.matrix([output_list["x"][i]-xp, output_list["y"][i]-yp, -f])

        # 비행기 위치 = 카메라 위치
        Xc = float(output_list["Alat"][i][0][0]) + float(output_list["Alat"][i][0][2]) /60 + float(output_list["Alat"][i][0][4]) /3600
        Yc = float(output_list["Alon"][i][0][0]) + float(output_list["Alon"][i][0][2]) /60 + float(output_list["Alon"][i][0][4]) /3600

        # 행렬 계산
        XYZ = c * la * R_inv + np.matrix([Xc, Yc, 100])

        for i in range(100):
            output["name"].append(line[0])
            output["X"].append(XYZ[0,0])
            output["Y"].append(XYZ[0,1])
            output["Z"].append(XYZ[0,2])
    print(output)

if __name__ == '__main__':
    img23d("./KSIS.csv", "./output.csv")