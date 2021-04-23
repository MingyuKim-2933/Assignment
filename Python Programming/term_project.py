import pickle
import os
import datetime


score_list = []
user_input_list = ["Name:", "Flavor:", "Hygiene:", "Price:"]

MENU_RETRIEVE = 1
MENU_ADD = 2
MENU_UPDATE = 3
MENU_DELETE = 4
MENU_SAVE = 5
MENU_LOAD = 6
MENU_QUIT = 7

INDEX_NAME = 0
INDEX_FLAVOR = 1
INDEX_HYGIENE = 2
INDEX_PRICE = 3
INDEX_TIME = 4


def print_menu():
    print("**************************")
    print("1. Retrieve")
    print("2. Add")
    print("3. Update")
    print("4. Delete")
    print("5. Save")
    print("6. Load")
    print("7. Quit")
    print("**************************")


def print_list():
    custom_sort_list()
    flavor_total, hygiene_total, price_total = calculate_total()
    flavor_average, hygiene_average, price_average = calculate_average()
    print("INDEX                 NAME  FLAVOR  HYGIENE  PRICE                    ADD TIME")
    print("******************************************************************************")
    for j in range(len(score_list)):
        print((str(j+1)+".").ljust(5), " ", str(score_list[j][INDEX_NAME]).rjust(20), " ", str(score_list[j][INDEX_FLAVOR]).rjust(7), " ",  str(score_list[j][INDEX_HYGIENE]).rjust(8), " ", str(score_list[j][INDEX_PRICE]).rjust(6), " ", str(score_list[j][INDEX_TIME]).rjust(27), sep="")
    print("******************************************************************************")
    print("TOTAL".ljust(26), str(flavor_total).rjust(7), str(hygiene_total).rjust(8), str(price_total).rjust(6))
    print("AVG.".ljust(27), str(round(flavor_average, 1)).rjust(7), str(round(hygiene_average, 1)).rjust(8), str(round(price_average, 1)).rjust(6))
    print()
    print("TOPS: 1", end='')

    for k in range(2, check_top()+1):
        print(",", k, end='')
    print()


def sort_list():
    global score_list

    score_list.sort(key=lambda x: x[1] + x[2] + x[3], reverse=True)


def custom_sort_list():
    global score_list

    print("정렬 기준을 선택하세요.")
    print("1.TOTAL SCORE 2. FLAVOR 3. HYGIENE 4.PRICE 5.ADD TIME")
    while True:
        try:
            sort_num = int(input(">"))

            if sort_num == 1:
                score_list.sort(key=lambda x: x[INDEX_FLAVOR] + x[INDEX_HYGIENE] + x[INDEX_PRICE], reverse=True)
                break

            elif sort_num == 2:
                score_list.sort(key=lambda x: x[INDEX_FLAVOR], reverse=True)
                break

            elif sort_num == 3:
                score_list.sort(key=lambda x: x[INDEX_HYGIENE], reverse=True)
                break

            elif sort_num == 4:
                score_list.sort(key=lambda x: x[INDEX_PRICE], reverse=True)
                break

            elif sort_num == 5:
                score_list.sort(key=lambda x: x[INDEX_TIME], reverse=True)
                break

            else:
                print("The input has errors.")
                continue

        except ValueError:
            print("The input has errors.")
            continue


def calculate_total():
    flavor_total = 0
    hygiene_total = 0
    price_total = 0

    for j in range(len(score_list)):
        flavor_total += score_list[j][INDEX_FLAVOR]
        hygiene_total += score_list[j][INDEX_HYGIENE]
        price_total += score_list[j][INDEX_PRICE]

    return flavor_total, hygiene_total, price_total


def calculate_average():
    flavor_average, hygiene_average, price_average = calculate_total()

    flavor_average = flavor_average / len(score_list)
    hygiene_average = hygiene_average / len(score_list)
    price_average = price_average / len(score_list)

    return flavor_average, hygiene_average, price_average


def check_top():
    top_count = 1
    for j in range(1, len(score_list)):
        if score_list[j][INDEX_FLAVOR] + score_list[j][INDEX_HYGIENE] + score_list[j][INDEX_PRICE] == score_list[j-1][INDEX_FLAVOR] + score_list[j-1][INDEX_HYGIENE] + score_list[j-1][INDEX_PRICE]:
            top_count += 1

        else:
            break

    return top_count


def add_list():
    global score_list

    add_list_temp = []

    while len(add_list_temp) < len(user_input_list):
        if len(add_list_temp) == 0:
            restaurant_name = input(user_input_list[len(add_list_temp)])

            if 1 <= len(restaurant_name) < 20:
                add_list_temp.append(restaurant_name)

            elif len(restaurant_name) == 0:
                print("The input has errors.")
                continue

            else:
                print("The length of name should be less than 20")
                print("The input has errors.")
                continue
        try:
            print("1~5점 사이의 점수를 입력해주세요.")
            restaurant_score = int(input(user_input_list[len(add_list_temp)]))

        except ValueError as e:
            print("The input has errors.")
            for i in range(len(add_list_temp)):
                print(user_input_list[i], add_list_temp[i], sep="")
            continue

        if 1 <= restaurant_score <= 5:
            add_list_temp.append(restaurant_score)

        else:
            print("The input has errors.")
            for i in range(len(add_list_temp)):
                print(user_input_list[i], add_list_temp[i], sep="")

    add_list_temp.append(datetime.datetime.now())
    score_list.append(add_list_temp)
    print("Added.")


def update_list():
    global score_list
    update_list_temp = []
    print_list()

    while True:
        try:
            update_num = int(input("Update>"))

            if 1 <= update_num <= len(score_list):
                while len(update_list_temp) < len(user_input_list):
                    if len(update_list_temp) == 0:
                        restaurant_name = input(user_input_list[len(update_list_temp)])

                        if 1 <= len(restaurant_name) < 20:
                            update_list_temp.append(restaurant_name)

                        elif len(restaurant_name) == 0:
                            print("The input has errors.")
                            continue

                        else:
                            print("The length of name should be less than 20")
                            print("The input has errors.")
                            continue

                    try:
                        print("1~5점 사이의 점수를 입력해주세요.")
                        restaurant_score = int(input(user_input_list[len(update_list_temp)]))

                    except ValueError:
                        print("The input has errors.")
                        for i in range(len(update_list_temp)):
                            print(user_input_list[i], update_list_temp[i], sep="")
                        continue

                    if 1 <= restaurant_score <= 5:
                        update_list_temp.append(restaurant_score)

                    else:
                        print("The input has errors.")
                        for i in range(len(update_list_temp)):
                            print(user_input_list[i], update_list_temp[i], sep="")

                update_list_temp.append(datetime.datetime.now())
                score_list[update_num - 1] = update_list_temp
                print("Updated.")
                break

            else:
                print("The input has errors.")

        except ValueError:
            print("The input has errors.")
            continue


def delete_list():
    global score_list
    print_list()

    while True:
        try:
            delete_num = int(input("Delete>"))

            if 1 <= delete_num <= len(score_list):
                del score_list[delete_num - 1]
                print("Deleted.")
                break

            else:
                print("The input has errors.")

        except ValueError as e:
            print("The input has errors.")
            continue


def save_list():
    global score_list

    save_score_list = score_list

    file = open('DATA.dat', 'wb')
    pickle.dump(save_score_list, file)
    file.close()
    print("Saved.")


def load_list():
    global score_list

    file = open('DATA.dat', 'rb')
    save_score_list = pickle.load(file)
    file.close()
    score_list = save_score_list

    print("Loaded.")


print_menu()
while True:
    if len(score_list) >= 2:
        sort_list()

    try:
        input_num = int(input(">"))

    except ValueError as e:
        print("The input has errors.")
        continue

    if 1 <= input_num <= 7:
        if input_num == MENU_RETRIEVE:
            if not score_list:
                print("There are no data.")

            else:
                print_list()

        elif input_num == MENU_ADD:
            if len(score_list) >= 9999:
                print("No more data is accepted.")
                continue

            else:
                add_list()

        elif input_num == MENU_UPDATE:
            if not score_list:
                print("There are no data.")

            else:
                update_list()

        elif input_num == MENU_DELETE:
            if not score_list:
                print("There are no data.")

            else:
                delete_list()

        elif input_num == MENU_SAVE:
            if not score_list:
                print("There are no data.")

            else:
                print_list()
                save_list()

        elif input_num == MENU_LOAD:
            if not os.path.isfile('DATA.dat'):
                print("There is no files.")

            else:
                load_list()

        elif input_num == MENU_QUIT:
            print("Bye Bye!!")
            break

    else:
        print("The input has errors.")
        continue

    print()
    print_menu()
