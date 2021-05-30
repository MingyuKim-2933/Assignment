import sys
import numpy as np
import math
from random import randint
import cv2
import timeit

# Hr, Hs, ERR 값 설정
Hr = 90
Hs = 90
ERR = 90

window_size = 11

# Global Variables
src = cv2.imread('image6.png')
src1 = cv2.imread('image6.png', cv2.IMREAD_GRAYSCALE)
src2 = cv2.imread('image7.png', cv2.IMREAD_GRAYSCALE)

if src1 is None or src2 is None:
    print('Image load failed!')
    sys.exit()

dst = np.zeros(src.shape, np.uint8)


# Gaussian Kernel
def gaussian_kernel(x_norm):
    if x_norm <= 1:
        return math.exp(1) ** (-1 * x_norm ** 2)
    else:
        return 0


def get_weight(y_current, y_prev):
    # 현재 픽셀의 값들을 거리에 따라 차등 영향을 주도록 Gaussian kernel을 사용한다.
    k_r = gaussian_kernel(np.linalg.norm((y_current[:3] - y_prev[:3]) / Hr))
    k_s = gaussian_kernel(np.linalg.norm((y_current[3:5] - y_prev[3:5]) / Hs))

    weight = k_r * k_s

    return weight


# 비슷한 값을 가진 픽셀들을 구한다.
def get_neighbors(y_prev, matrix):
    neighbors = []
    neighbors_temp = neighbors.append

    for i in range(len(matrix)):
        y_current = matrix[i]

        xk_sum = 0.0
        k_sum = 0.0

        r = math.sqrt(sum((y_current[:3] - y_prev[:3]) ** 2))
        s = math.sqrt(sum((y_current[3:5] - y_prev[3:5]) ** 2))

        weight = get_weight(y_current, y_prev)
        xk_sum += y_current * weight

        k_sum += weight

        if s < Hs and r < Hr:
            neighbors_temp(i)

    y_current = xk_sum / (k_sum+1e-5)

    return neighbors


# 특정 픽셀 neighbors에 속한 픽셀들의 r, g, b 각각의 평균 색으로 채워 영상을 만든다.
def mark_pixels(neighbors, mean, matrix):

    for i in neighbors:
        y_current = matrix[i]
        h = y_current[3]
        w = y_current[4]

        dst[h][w] = np.array(mean[:3], np.uint8)

    return np.delete(matrix, neighbors, axis=0)  # 영상을 만든 후 사용된 neighbors를 삭제한다.


# r, g, b, x, y의 각각의 평균값을 구한다.
def calculate_mean(neighbors, matrix):
    neighbors = matrix[neighbors]

    r = neighbors[:, 0]
    g = neighbors[:, 1]
    b = neighbors[:, 2]
    y = neighbors[:, 3]
    x = neighbors[:, 4]

    mean = np.array([np.mean(r), np.mean(g), np.mean(b), np.mean(y), np.mean(x)])
    return mean


# img 사이즈에 맞춰 각 픽셀의 r, g, b, y, x의 값을 포함한 Feature Matrix를 만든다.
def create_feature_matrix(img):
    h, w, d = img.shape

    feature_matrix = []
    feature_matrix_temp = feature_matrix.append

    for y in range(0, h):
        for x in range(0, w):
            r, g, b = img[y][x]
            feature_matrix_temp([r, g, b, y, x])

    feature_matrix = np.array(feature_matrix)
    return feature_matrix


# Mean Shift를 수행한다.
def perform_mean_shift_with_optical_flow(img):
    clusters = 0
    feature_matrix = create_feature_matrix(img)

    while len(feature_matrix) > 0:
        print('remPixelsCount: ' + str(len(feature_matrix)))  # 남은 픽셀들의 개수를 출력한다.

        random_index = randint(0, len(feature_matrix) - 1)  # index를 random으로 설정한다.
        seed_point = feature_matrix[random_index]  # seed_point로 랜덤한 값을 배정한다.

        initial_mean = seed_point

        neighbors = get_neighbors(seed_point, feature_matrix)  # seed_point에서의 neighbors를 구한다.
        print('found neighbors: ' + str(len(neighbors)))  # 찾은 neighbors의 개수를 출력한다.

        mean_u, mean_v = extract_mean_motion_vector(src1, src2, window_size, neighbors, feature_matrix)

        # neighbors가 1인 경우 Mean Shift를 하지 않는다.
        if len(neighbors) == 1:
            feature_matrix = mark_pixels([random_index], initial_mean, feature_matrix)
            clusters += 1

            continue

        # neighbors가 1개보다 많은 경우 mean를 구한다.
        mean = calculate_mean(neighbors, feature_matrix)
        # Mean Shift를 구한다.
        mean_shift = abs(mean - initial_mean)

        if np.mean(mean_shift) < ERR:  # mean_shift의 산술 평균을 구해서 ERR보다 낮을 때 실행한다.
            feature_matrix = mark_pixels(neighbors, mean, feature_matrix)
            clusters += 1

    return clusters, mean_u, mean_v


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
def lukas_kanade(delta_y, delta_x, delta_t, window_size, w, neighbors, feature_matrix):
    count = 0
    nb_count = 0

    delta_height, delta_width = delta_y.shape

    # 모션 벡터를 저장할 numpy 배열을 초기화한다.
    u = np.zeros(src1.shape)
    v = np.zeros(src1.shape)

    v_temp = []
    u_temp = []
    # window_size * window_size만큼 주변 픽셀을 돌며 A와 b를 구한다.
    for y in range(w, delta_height-w):
        for x in range(w, delta_width-w):

            if nb_count in neighbors:

                transpose_A = np.zeros((2, (window_size**2)))  # (2, (window_size ** 2)) matrix
                b = np.zeros(((window_size**2), 1))  # ((window_size ** 2), 1) matrix

                for i in range(-w, w+1):
                    for j in range(-w, w+1):
                        b[count][0] = delta_t[y+i][x+j]

                        transpose_A[0][count] = delta_y[y+i][x+j]
                        transpose_A[1][count] = delta_x[y+i][x+j]

                        count = count + 1

                A = transpose_A.T  # ((window_size ** 2), 2) matrix
                front = np.linalg.pinv(np.matmul(transpose_A, A))  # (2, 2) matrix
                behind = np.matmul(transpose_A, b)  # (2, 1) matrix

                v_t = np.matmul(front, behind)

                v_temp.append(v_t[0])
                u_temp.append(v_t[1])
                v[y-w, x-w] = v_t[0]
                u[y-w, x-w] = v_t[1]

            count = 0

    v_mean = np.mean(v_temp)
    u_mean = np.mean(u_temp)

    for i in neighbors:
        y_current = feature_matrix[i]
        y = y_current[3]
        x = y_current[4]
        v[y - w, x - w] = v_mean
        u[y - w, x - w] = u_mean

    return u, v


# 모션 벡터를 추출한다.
def extract_mean_motion_vector(img1, img2, window_size, neighbors, feature_matrix):
    w = int(window_size / 2)

    # 사용할 window size에 맞게 이미지를 패딩시켜준다.
    padding_image1 = cv2.copyMakeBorder(src1, w + 1, w + 1, w + 1, w + 1, cv2.BORDER_WRAP)
    padding_image2 = cv2.copyMakeBorder(src2, w + 1, w + 1, w + 1, w + 1, cv2.BORDER_WRAP)

    delta_y, delta_x, delta_t = get_delta(padding_image1, padding_image2)

    u, v = lukas_kanade(delta_y, delta_x, delta_t, window_size, w, neighbors, feature_matrix)

    return u, v


# Optical Flow를 그린다.
def draw_optical_flow(img, u, v):
    img_height, img_width, d = img.shape

    min_th = 1
    max_th = 7

    # img1 사이즈로 검정색 mask 영상 초기화.
    mask = np.zeros_like(img)

    # 가로, 세로 5pixel씩 건너 뛰면서 그린다.
    for y in range(0, img_height, 5):
        for x in range(0, img_width, 5):
            if min_th <= abs(u[y][x]) or min_th <= abs(v[y][x]):
                if abs(u[y][x]) <= max_th and abs(v[y][x]) <= max_th:
                    mask = cv2.line(mask, (x, y), (int(x + round(u[y][x])), int(y + round(v[y][x]))), (255, 255, 255))

    dst = cv2.add(mask, img)

    return mask, dst


def main():
        global dst
        start_time = timeit.default_timer()  # 시작 시간 체크
        clusters, u, v = perform_mean_shift_with_optical_flow(src)
        terminate_time = timeit.default_timer()  # 종료 시간 체크

        print("%f초 걸렸습니다." % (terminate_time - start_time))

        mask, dst = draw_optical_flow(dst, u, v)  # Optical Flow를 그린다.
        print('Number of clusters: ', clusters)

        cv2.imshow("dst", dst)
        cv2.waitKey()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

