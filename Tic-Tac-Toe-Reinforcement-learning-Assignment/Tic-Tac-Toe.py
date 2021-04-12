import numpy as np
import matplotlib.pyplot as plt
import copy
import math
from tqdm import tqdm


class Environment33to3():  # 3x3 환경 승리조건 3개

    def __init__(self):
        # 보드는 0으로 초기화된 9개의 배열로 준비
        # 게임종료 : done = True
        self.board_a = np.zeros(9)
        self.done = False
        self.reward = 0
        self.winner = 0
        self.print = False

    def move(self, p1, p2, player):
        # 각 플레이어가 선택한 행동을 표시 하고 게임 상태(진행 또는 종료)를 판단
        # p1 = 1, p2 = -1로 정의
        # 각 플레이어는 행동을 선택하는 select_action 메서드를 가짐
        if player == 1:
            pos = p1.select_action(env, player)
        else:
            pos = p2.select_action(env, player)

        # 보드에 플레이어의 선택을 표시
        self.board_a[pos] = player
        if self.print:
            print(player)
            self.print_board()
        # 게임이 종료상태인지 아닌지를 판단
        self.end_check(player)

        return self.reward, self.done

    # 현재 보드 상태에서 가능한 행동(둘 수 있는 장소)을 탐색하고 리스트로 반환
    def get_action(self):
        observation = []
        for i in range(9):
            if self.board_a[i] == 0:
                observation.append(i)
        return observation

    # 게임이 종료(승패 또는 비김)됐는지 판단
    def end_check(self, player):
        # 0 1 2
        # 3 4 5
        # 6 7 8
        # 승패 조건은 가로, 세로, 대각선 이 -1 이나 1 로 동일할 때
        end_condition = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
        for line in end_condition:
            if self.board_a[line[0]] == self.board_a[line[1]] \
                    and self.board_a[line[1]] == self.board_a[line[2]] \
                    and self.board_a[line[0]] != 0:
                # 종료됐다면 누가 이겼는지 표시
                self.done = True
                self.reward = player
                return
        # 비긴 상태는 더는 보드에 빈 공간이 없을때
        observation = self.get_action()
        if (len(observation)) == 0:
            self.done = True
            self.reward = 0
        return

    # 현재 보드의 상태를 표시 p1 = O, p2 = X
    def print_board(self):
        print("+----+----+----+")
        for i in range(3):
            for j in range(3):
                if self.board_a[3 * i + j] == 1:
                    print("|  O", end=" ")
                elif self.board_a[3 * i + j] == -1:
                    print("|  X", end=" ")
                else:
                    print("|   ", end=" ")
            print("|")
            print("+----+----+----+")

class Environment44to4():  # 4x4환경 승리조건 4개

    def __init__(self):
        # 보드는 0으로 초기화된 25개의 배열로 준비
        # 게임종료 : done = True
        self.board_a = np.zeros(16)
        self.done = False
        self.reward = 0
        self.winner = 0
        self.print = False


    def move(self, p1, p2, player):
        # 각 플레이어가 선택한 행동을 표시 하고 게임 상태(진행 또는 종료)를 판단
        # p1 = 1, p2 = -1로 정의
        # 각 플레이어는 행동을 선택하는 select_action 메서드를 가짐
        if player == 1:
            pos = p1.select_action(env, player)
        else:
            pos = p2.select_action(env, player)

        # 보드에 플레이어의 선택을 표시
        self.board_a[pos] = player
        if self.print:
            print(player)
            self.print_board()
        # 게임이 종료상태인지 아닌지를 판단
        self.end_check(player)

        return self.reward, self.done

    # 현재 보드 상태에서 가능한 행동(둘 수 있는 장소)을 탐색하고 리스트로 반환
    def get_action(self):
        observation = []
        for i in range(16):
            if self.board_a[i] == 0:
                observation.append(i)
        return observation

    # 게임이 종료(승패 또는 비김)됐는지 판단
    def end_check(self, player):
        # 0 1 2
        # 3 4 5
        # 6 7 8
        # 승패 조건은 가로, 세로, 대각선 이 -1 이나 1 로 동일할 때
        end_condition = ((0, 1, 2, 3), (4, 5, 6, 7), (8, 9, 10, 11), (12, 13, 14, 15),
                         (0, 4, 8, 12), (1, 5, 9, 13), (2, 6, 10, 14), (3, 7, 11, 15),
                         (0, 5, 10, 15), (3, 6, 9, 12))
        for line in end_condition:
            if self.board_a[line[0]] == self.board_a[line[1]] \
                    and self.board_a[line[1]] == self.board_a[line[2]] \
                    and self.board_a[line[2]] == self.board_a[line[3]] \
                    and self.board_a[line[0]] != 0:
                # 종료됐다면 누가 이겼는지 표시
                self.done = True
                self.reward = player
                return
        # 비긴 상태는 더는 보드에 빈 공간이 없을때
        observation = self.get_action()
        if (len(observation)) == 0:
            self.done = True
            self.reward = 0
        return

    # 현재 보드의 상태를 표시 p1 = O, p2 = X
    def print_board(self):
        print("+----+----+----+----+")
        for i in range(4):
            for j in range(4):
                if self.board_a[4 * i + j] == 1:
                    print("|  O", end=" ")
                elif self.board_a[4 * i + j] == -1:
                    print("|  X", end=" ")
                else:
                    print("|   ", end=" ")
            print("|")
            print("+----+----+----+----+")

class Environment55to5():  # 5x5환경 승리조건 5개

    def __init__(self):
        # 보드는 0으로 초기화된 25개의 배열로 준비
        # 게임종료 : done = True
        self.board_a = np.zeros(25)
        self.done = False
        self.reward = 0
        self.winner = 0
        self.print = False


    def move(self, p1, p2, player):
        # 각 플레이어가 선택한 행동을 표시 하고 게임 상태(진행 또는 종료)를 판단
        # p1 = 1, p2 = -1로 정의
        # 각 플레이어는 행동을 선택하는 select_action 메서드를 가짐
        if player == 1:
            pos = p1.select_action(env, player)
        else:
            pos = p2.select_action(env, player)

        # 보드에 플레이어의 선택을 표시
        self.board_a[pos] = player
        if self.print:
            print(player)
            self.print_board()
        # 게임이 종료상태인지 아닌지를 판단
        self.end_check(player)

        return self.reward, self.done

    # 현재 보드 상태에서 가능한 행동(둘 수 있는 장소)을 탐색하고 리스트로 반환
    def get_action(self):
        observation = []
        for i in range(25):
            if self.board_a[i] == 0:
                observation.append(i)
        return observation

    # 게임이 종료(승패 또는 비김)됐는지 판단
    def end_check(self, player):
        # 0 1 2
        # 3 4 5
        # 6 7 8
        # 승패 조건은 가로, 세로, 대각선 이 -1 이나 1 로 동일할 때
        end_condition = ((0, 1, 2, 3, 4), (5, 6, 7, 8, 9), (10, 11, 12, 13, 14), (15, 16, 17, 18, 19), (20, 21, 22, 23, 24),
                         (0, 5, 10, 15, 20), (1, 6, 11, 16, 21), (2, 7, 12, 17, 22), (3, 8, 13, 18, 23), (4, 9, 14, 19, 24),
                         (0, 6, 12, 18, 24), (4, 8, 12, 16, 20))
        for line in end_condition:
            if self.board_a[line[0]] == self.board_a[line[1]] \
                    and self.board_a[line[1]] == self.board_a[line[2]] \
                    and self.board_a[line[2]] == self.board_a[line[3]] \
                    and self.board_a[line[3]] == self.board_a[line[4]] \
                    and self.board_a[line[0]] != 0:
                # 종료됐다면 누가 이겼는지 표시
                self.done = True
                self.reward = player
                return
        # 비긴 상태는 더는 보드에 빈 공간이 없을때
        observation = self.get_action()
        if (len(observation)) == 0:
            self.done = True
            self.reward = 0
        return

    # 현재 보드의 상태를 표시 p1 = O, p2 = X
    def print_board(self):
        print("+----+----+----+----+----+")
        for i in range(5):
            for j in range(5):
                if self.board_a[5 * i + j] == 1:
                    print("|  O", end=" ")
                elif self.board_a[5 * i + j] == -1:
                    print("|  X", end=" ")
                else:
                    print("|   ", end=" ")
            print("|")
            print("+----+----+----+----+----+")

class Environment55to3():  # 5x5환경 승리조건 3개

    def __init__(self):
        # 보드는 0으로 초기화된 25개의 배열로 준비
        # 게임종료 : done = True
        self.board_a = np.zeros(25)
        self.done = False
        self.reward = 0
        self.winner = 0
        self.print = False


    def move(self, p1, p2, player):
        # 각 플레이어가 선택한 행동을 표시 하고 게임 상태(진행 또는 종료)를 판단
        # p1 = 1, p2 = -1로 정의
        # 각 플레이어는 행동을 선택하는 select_action 메서드를 가짐
        if player == 1:
            pos = p1.select_action(env, player)
        else:
            pos = p2.select_action(env, player)

        # 보드에 플레이어의 선택을 표시
        self.board_a[pos] = player
        if self.print:
            print(player)
            self.print_board()
        # 게임이 종료상태인지 아닌지를 판단
        self.end_check(player)

        return self.reward, self.done

    # 현재 보드 상태에서 가능한 행동(둘 수 있는 장소)을 탐색하고 리스트로 반환
    def get_action(self):
        observation = []
        for i in range(25):
            if self.board_a[i] == 0:
                observation.append(i)
        return observation

    # 게임이 종료(승패 또는 비김)됐는지 판단
    def end_check(self, player):
        # 0 1 2
        # 3 4 5
        # 6 7 8
        # 승패 조건은 가로, 세로, 대각선 이 -1 이나 1 로 동일할 때
        end_condition = ((0, 1, 2), (1, 2, 3), (2, 3, 4), (5, 6, 7), (6, 7, 8), (7, 8, 9), (10, 11, 12), (11, 12, 13), (12, 13, 14), (15, 16, 17), (16, 17, 18), (17, 18, 19), (20, 21, 22), (21, 22, 23), (22, 23, 24),
                         (0, 6, 12), (6, 12, 18), (12, 18, 24), (5, 11, 17), (11, 17, 23), (10, 16, 22), (1, 7, 13), (7, 13, 19), (2, 8, 14),
                         (4, 8, 12), (8, 12, 16), (12, 16, 20), (3, 7, 11), (7, 11, 15), (2, 6, 10), (9, 13, 17), (13, 17, 21), (14, 18, 22),
                         (0, 5, 10), (5, 10, 15), (10, 15, 20), (1, 6, 11), (6, 11, 16), (11, 16, 21), (2, 7, 12), (7, 12, 17), (12, 17, 22), (3, 8, 13), (8, 13, 18), (13, 18, 23), (4, 9, 14), (9, 14, 19), (14, 19, 24))
        for line in end_condition:
            if self.board_a[line[0]] == self.board_a[line[1]] \
                    and self.board_a[line[1]] == self.board_a[line[2]] \
                    and self.board_a[line[0]] != 0:
                # 종료됐다면 누가 이겼는지 표시
                self.done = True
                self.reward = player
                return
        # 비긴 상태는 더는 보드에 빈 공간이 없을때
        observation = self.get_action()
        if (len(observation)) == 0:
            self.done = True
            self.reward = 0
        return

    # 현재 보드의 상태를 표시 p1 = O, p2 = X
    def print_board(self):
        print("+----+----+----+----+----+")
        for i in range(5):
            for j in range(5):
                if self.board_a[5 * i + j] == 1:
                    print("|  O", end=" ")
                elif self.board_a[5 * i + j] == -1:
                    print("|  X", end=" ")
                else:
                    print("|   ", end=" ")
            print("|")
            print("+----+----+----+----+----+")

class Random_player():

    def __init__(self):
        self.name = "Random player"
        self.print = False

    def select_action(self, env, player):
        # 가능한 행동 조사
        available_action = env.get_action()
        # 가능한 행동 중 하나를 무작위로 선택
        action = np.random.randint(len(available_action))
        #         print("Select action(random) = {}".format(available_action[action]))
        return available_action[action]

    class Monte_Carlo_player():

        def __init__(self):
            self.name = "MC player"
            self.num_playout = 1000

        def select_action(self, env, player):
            # 가능한 행동 조사
            available_action = env.get_action()
            V = np.zeros(len(available_action))

            for i in range(len(available_action)):
                # 플레이아웃을 1000번 반복
                for j in range(self.num_playout):
                    # 지금 상태를 복사해서 플레이 아웃에 사용
                    temp_env = copy.deepcopy(env)
                    # 플레이아웃의 결과는 승리 플레이어의 값으로 반환
                    # p1 이 이기면 1, p2 가 이기면 -1
                    self.playout(temp_env, available_action[i], player)
                    if player == temp_env.reward:
                        V[i] += 1

            return available_action[np.argmax(V)]

            # 플레이아웃 재귀함수

        # 게임이 종료상태 (승 또는 패 또는 비김) 가 될때까지 행동을 임의로 선택하는 것을 반복
        # 플레이어는 계속 바뀌기 때문에 (-)를 곱해서 -1, 1, -1 이 되게함
        def playout(self, temp_env, action, player):

            temp_env.board_a[action] = player
            temp_env.end_check(player)
            # 게임 종료 체크
            if temp_env.done == True:
                return
            else:
                # 플레이어 교체
                player = -player
                # 가능한 행동 조사
                available_action = temp_env.get_action()
                # 무작위로 행동을 선택
                action = np.random.randint(len(available_action))
                self.playout(temp_env, available_action[action], player)


class MG_player():
    def __init__(self):
        self.name = "MG_player"
        self.v_table = np.zeros((3, 3, 3, 3, 3, 3, 3, 3, 3, 9))
        self.Itr_Policy(self.v_table)
        self.print = False

    def select_action(self, env, player):
        a = (int)(env.board_a[0])
        b = (int)(env.board_a[1])
        c = (int)(env.board_a[2])
        d = (int)(env.board_a[3])
        e = (int)(env.board_a[4])
        f = (int)(env.board_a[5])
        g = (int)(env.board_a[6])
        h = (int)(env.board_a[7])
        i = (int)(env.board_a[8])

        available_action = env.get_action()

        # v_table에서 현재 정보에 가장 값이 높은 action으로 결정
        max_Value = self.v_table[a][b][c][d][e][f][g][h][i][available_action[-1]]
        action = available_action[-1]

        if self.print:
            print("{} : select action".format(action))

        for j in available_action:
            if self.v_table[a][b][c][d][e][f][g][h][i][j] > max_Value:
                action = j
                max_Value = self.v_table[a][b][c][d][e][f][g][h][i][j]
        return action

    def Itr_Policy(self, v_table):
        env = Environment44to4() # 게임 환경 지정
        gamma = 0.9
        k = 0

        while True:
            k += 1
            # Δ←0
            delta = 0
            # 계산전 가치를 저장
            temp_v = copy.deepcopy(v_table)
            for a in [-1, 0, 1]:
                for b in [-1, 0, 1]:
                    for c in [-1, 0, 1]:
                        for d in [-1, 0, 1]:
                            for e in [-1, 0, 1]:
                                for f in [-1, 0, 1]:
                                    for g in [-1, 0, 1]:
                                        for h in [-1, 0, 1]:
                                            for i in [-1, 0, 1]:
                                                for action in range(9):
                                                    G = 0
                                                    env.reward = 0
                                                    # 모든 𝑠∈𝑆에 대해
                                                    env.board_a = np.asarray([a, b, c, d, e, f, g, h, i])
                                                    # action으로 인한 이동에 대한 계산
                                                    if action == 0 and env.board_a[0] == 0:
                                                        env.board_a[0] = 1
                                                        env.reward -= 1
                                                    elif action == 1 and env.board_a[1] == 0:
                                                        env.board_a[1] = 1
                                                        env.reward -= 1
                                                    elif action == 2 and env.board_a[2] == 0:
                                                        env.board_a[2] = 1
                                                        env.reward -= 1
                                                    elif action == 3 and env.board_a[3] == 0:
                                                        env.board_a[3] = 1
                                                        env.reward -= 1
                                                    elif action == 4 and env.board_a[4] == 0:
                                                        env.board_a[4] = 1
                                                        env.reward -= 0.5
                                                    elif action == 5 and env.board_a[5] == 0:
                                                        env.board_a[5] = 1
                                                        env.reward -= 1
                                                    elif action == 6 and env.board_a[6] == 0:
                                                        env.board_a[6] = 1
                                                        env.reward -= 1
                                                    elif action == 7 and env.board_a[7] == 0:
                                                        env.board_a[7] = 1
                                                        env.reward -= 1
                                                    elif action == 8 and env.board_a[8] == 0:
                                                        env.board_a[8] = 1
                                                        env.reward -= 1
                                                    else:
                                                        # 이미 둔 공간에 두는 경우
                                                        env.reward -= 5

                                                    end_condition = (
                                                    (0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8),
                                                    (0, 4, 8), (2, 4, 6))
                                                    for line in end_condition:
                                                        # 이길 경우
                                                        if env.board_a[line[0]] == 1 and env.board_a[line[0]] == \
                                                                env.board_a[line[1]] and env.board_a[line[1]] == \
                                                                env.board_a[line[2]] and env.board_a[line[0]] != 0:
                                                            env.reward += 3
                                                        # 질 경우
                                                        if env.board_a[line[0]] == -1 and env.board_a[line[0]] == \
                                                                env.board_a[line[1]] and env.board_a[line[1]] == \
                                                                env.board_a[line[2]] and env.board_a[line[0]] != 0:
                                                            env.reward -= 3

                                                    # 비길 경우
                                                    observation = env.get_action()
                                                    if (len(observation)) == 0:
                                                        env.reward -= 2

                                                    # 가능한 모든 행동으로 다음상태만 이용해 𝑉(𝑠) 계산
                                                    G += (1 / 9) * (env.reward + gamma * v_table[
                                                        a, b, c, d, e, f, g, h, i, action])
                                                    v_table[a, b, c, d, e, f, g, h, i, action] = G

            delta = np.max([delta, np.max(np.abs(temp_v - v_table))])
            print("Iteration " + (str)(k) + " delta : " + (str)(delta))
            if delta < 0.000001:
                break
        print("Iteration Complete")


class KMGPlayer():

    def __init__(self):
        self.name = "KMG"
        self.num_play = 100

    def select_action(self, env, player):
        available_action = env.get_action()
        V = np.zeros(len(available_action))

        for i in range(len(available_action)):
            for j in range(self.num_play):
                temp_env = copy.deepcopy(env)
                self.play(temp_env, available_action[i], player)
                if len(available_action) == 25:
                    V[12] = 120

                elif player == temp_env.reward:
                    V[i] += 1

        return available_action[np.argmax(V)]

    def play(self, temp_env, action, player):
        temp_env.board_a[action] = player
        temp_env.end_check(player)

        if temp_env.done == True:
            return

        else:
            player = -player
            available_action = temp_env.get_action()
            action = np.random.randint(len(available_action))
            self.play(temp_env, available_action[action], player)

np.random.seed(0)

# p1 = KMG_player()
# p2 = MG_player()

# p1 = Human_player()
# p2 = Human_player()

# p1 = Random_player()
p2 = Random_player()

p1 = KMGPlayer()
# p1.num_playout = 100
# p2 = Monte_Carlo_player()
# p2.num_playout = 1000

# p1 = p1_Qplayer
# p1.epsilon = 0

# p2 = p2_Qplayer
# p2.epsilon = 0

# p1 = p1_DQN
# p1.epsilon = 0

# 지정된 게임 수를 자동으로 두게 할 것인지 한게임씩 두게 할 것인지 결정
# auto = True : 지정된 판수(games)를 자동으로 진행
# auto = False : 한판씩 진행

auto = False

# auto 모드의 게임수
games = 100

print("pl player : {}".format(p1.name))
print("p2 player : {}".format(p2.name))

# 각 플레이어의 승리 횟수를 저장
p1_score = 0
p2_score = 0
draw_score = 0

if auto:
    # 자동 모드 실행
    for j in tqdm(range(games)):

        np.random.seed(j)
        env = Environment55to5()  # 게임 환경 지정

        for i in range(10000):
            # p1 과 p2가 번갈아 가면서 게임을 진행
            # p1(1) -> p2(-1) -> p1(1) -> p2(-1) ...
            reward, done = env.move(p1, p2, (-1) ** i)
            # 게임 종료 체크
            if done == True:
                if reward == 1:
                    p1_score += 1
                elif reward == -1:
                    p2_score += 1
                else:
                    draw_score += 1
                break

else:
    # 한 게임씩 진행하는 수동 모드
    np.random.seed(1)
    while True:

        env = Environment55to5() # 게임 환경 지정
        env.print = False
        for i in range(10000):
            reward, done = env.move(p1, p2, (-1) ** i)
            env.print_board()
            if done == True:
                if reward == 1:
                    print("winner is p1({})".format(p1.name))
                    p1_score += 1
                elif reward == -1:
                    print("winner is p2({})".format(p2.name))
                    p2_score += 1
                else:
                    print("draw")
                    draw_score += 1
                break

        # 최종 결과 출력
        print("final result")
        env.print_board()

        # 한게임 더?최종 결과 출력
        answer = input("More Game? (y/n)")

        if answer == 'n':
            break

print("p1({}) = {} p2({}) = {} draw = {}".format(p1.name, p1_score, p2.name, p2_score, draw_score))
