import cv2
import os

def avitoframe(videodir, framedir, frame):
    v_list = os.listdir(videodir)
    v_path_list = []
    for v_nm in v_list:
        v_path = os.path.join(videodir, v_nm)
        v_path_list.append(v_path)

    i = 0

    for v_path in v_path_list:
        vidcap = cv2.VideoCapture(v_path)
        count = 0
        while (vidcap.isOpened()):
            ret, image = vidcap.read()
            if (int(vidcap.get(1)) % frame == 0):
                print('Saved frame number : ' + str(int(vidcap.get(1))))
                file_nm = framedir + "\\" + "{0}_{1}.jpg".format(str(i), str(count))
                cv2.imwrite(file_nm, image)
                print('Saved frame%d.jpg' % count)
                count += 1
                print(vidcap.get(0))
            if not ret:
                i += 1
                print(i)
                break

if __name__ == '__main__':
    avitoframe("C:\\Users\\user\\Desktop\\video", "C:\\Users\\user\\Desktop\\image", 30)