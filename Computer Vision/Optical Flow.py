import sys
import numpy as np
import cv2
import timeit

# Global Variables
src1 = cv2.imread('image6.png', cv2.IMREAD_GRAYSCALE)
src2 = cv2.imread('image7.png', cv2.IMREAD_GRAYSCALE)

if src1 is None or src2 is None:
    print('Image load failed!')
    sys.exit()


# delta 값들을 구한다.
def get_delta(padding_img1, padding_img2):
    padding_height, padding_width = padding_img1.shape

    # delta값들을 임시 저장할 temp를 만든다.
    temp_y = []
    temp_x = []
    temp_t = []

    # delta값들을 저장할 numpy 배열을 초기화한다.
    delta_y = np.zeros((0, padding_width - 2))
    delta_x = np.zeros((0, padding_width - 2))
    delta_t = np.zeros((0, padding_width - 2))

    # delta 값들을 구해 각 numpy 배열에 넣는다.
    for y in range(1, padding_height - 1):
        for x in range(1, padding_width - 1):
            temp_y.append(np.int(padding_img1[y + 1, x]) - np.int(padding_img1[y, x]))
            temp_x.append(np.int(padding_img1[y, x + 1]) - np.int(padding_img1[y, x]))
            temp_t.append(np.int(padding_img2[y, x]) - np.int(padding_img1[y, x]))
        delta_y = np.append(delta_y, [temp_y], axis=0)
        delta_x = np.append(delta_x, [temp_x], axis=0)
        delta_t = np.append(delta_t, [temp_t], axis=0)
        temp_y = []
        temp_x = []
        temp_t = []

    return delta_y, delta_x, delta_t


# lukas-kanade algorithm을 구현한다.
def lukas_kanade(delta_y, delta_x, delta_t, window_size, w):
    count = 0

    delta_height, delta_width = delta_y.shape

    # 모션 벡터를 저장할 numpy 배열을 초기화한다.
    u = np.zeros(src1.shape)
    v = np.zeros(src1.shape)

    # window_size만큼 주변 픽셀을 돌며 A와 b를 구한다.
    for y in range(w, delta_height-w):
        for x in range(w, delta_width-w):
            transpose_A = np.zeros((2, (window_size**2)))  # (2, (window_size ** 2)) matrix
            b = np.zeros(((window_size**2), 1))  # ((window_size ** 2), 1) matrix

            for i in range(-w, w+1):
                for j in range(-w, w+1):
                    b[count][0] = delta_t[y+i][x+j]

                    transpose_A[0][count] = delta_y[y+i][x+j]
                    transpose_A[1][count] = delta_x[y+i][x+j]

                    if count <= (window_size**2) - 2:
                        count = count + 1

            A = transpose_A.T  # ((window_size ** 2), 2) matrix
            front = np.linalg.pinv(np.matmul(transpose_A, A))  # (2, 2) matrix
            behind = np.matmul(transpose_A, b)  # (2, 1) matrix

            v_t = np.matmul(front, behind)

            v[y-w, x-w] = v_t[0]
            u[y-w, x-w] = v_t[1]

            count = 0

    return u, v


# 모션 벡터를 추출한다.
def extract_motion_vector(img1, img2, window_size):
    w = int(window_size / 2)

    # 사용할 window size에 맞게 이미지를 패딩시켜준다.
    padding_image1 = cv2.copyMakeBorder(img1, w+1, w+1, w+1, w+1, cv2.BORDER_WRAP)
    padding_image2 = cv2.copyMakeBorder(img2, w+1, w+1, w+1, w+1, cv2.BORDER_WRAP)

    delta_y, delta_x, delta_t = get_delta(padding_image1, padding_image2)

    u, v = lukas_kanade(delta_y, delta_x, delta_t, window_size, w)

    return u, v


# Optical Flow를 그린다.
def draw_optical_flow(img1, u, v):
    img_height, img_width = img1.shape

    min_th = 1
    max_th = 7

    # img1 사이즈로 검정색 mask 영상 초기화.
    mask = np.zeros_like(img1)

    # 가로, 세로 5pixel씩 건너 뛰면서 그린다.
    for y in range(0, img_height, 5):
        for x in range(0, img_width, 5):
            if min_th <= abs(u[y][x]) or min_th <= abs(v[y][x]):
                if abs(u[y][x]) <= max_th and abs(v[y][x]) <= max_th:
                    mask = cv2.line(mask, (x, y), (int(x + round(u[y][x])), int(y + round(v[y][x]))), 255)

    dst = cv2.add(mask, img1)

    return mask, dst


def main():

        mask_list = []
        dst_list = []

        for i in range(3, 22, 2):

            start_time = timeit.default_timer()  # 시작 시간 체크
            u, v = extract_motion_vector(src1, src2, i)  # 모션 벡터 추출
            terminate_time = timeit.default_timer()  # 종료 시간 체크

            print("window", i, "%f초 걸렸습니다." % (terminate_time - start_time))

            mask, dst = draw_optical_flow(src1, u, v)  # Optical Flow를 그린다.

            mask_list.append(mask)
            dst_list.append(dst)

        for j in range(10):
            cv2.imshow("mask {}".format(2*j+3), mask_list[j])
            cv2.imshow("dst {}".format(2*j+3), dst_list[j])
        cv2.waitKey()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
