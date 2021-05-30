import sys
import numpy as np
import math
from random import randint
import cv2
import timeit

# Hr, Hs, ERR 값 설정
Hr = 300
Hs = 300
ERR = 20

# Global Variables
src = cv2.imread('image6.png')

if src is None:
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
def perform_mean_shift(img):
    clusters = 0
    feature_matrix = create_feature_matrix(img)

    while len(feature_matrix) > 0:
        print('remPixelsCount: ' + str(len(feature_matrix)))  # 남은 픽셀들의 개수를 출력한다.

        random_index = randint(0, len(feature_matrix) - 1)  # index를 random으로 설정한다.
        seed_point = feature_matrix[random_index]  # seed_point로 랜덤한 값을 배정한다.

        initial_mean = seed_point

        neighbors = get_neighbors(seed_point, feature_matrix)  # seed_point에서의 neighbors를 구한다.
        print('found neighbors: ' + str(len(neighbors)))  # 찾은 neighbors의 개수를 출력한다.

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

    return clusters


def main():
    start_time = timeit.default_timer()  # 시작 시간 체크
    clusters = perform_mean_shift(src)
    terminate_time = timeit.default_timer()  # 종료 시간 체크
    print("%f초 걸렸습니다." % (terminate_time - start_time))

    print('Number of clusters: ', clusters)

    # cv2.imshow('Hs: {}, Hr: {}'.format(Hs, Hr), src)
    cv2.imshow('Hs: {}, Hr: {}'.format(Hs, Hr), dst)
    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
