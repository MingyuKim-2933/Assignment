import pickle
import os
import datetime


restaurant_list = []
user_input_list = ["Name:", "Flavor:", "Hygiene:", "Price:", "Menu:", "Location:", "Business hours:"]

MENU_RETRIEVE = 1
MENU_ADD = 2
MENU_UPDATE = 3
MENU_EDIT = 4
MENU_DELETE = 5
MENU_SAVE = 6
MENU_LOAD = 7
MENU_QUIT = 8

INDEX_NAME = 0
INDEX_FLAVOR = 1
INDEX_HYGIENE = 2
INDEX_PRICE = 3
INDEX_MENU = 4
INDEX_LOCATION = 5
INDEX_BUSINESS_HOURS = 6
INDEX_TIME = 7


def print_menu():
    """menu를 출력하는 함수"""
    print("**************************")
    print("1. Retrieve")
    print("2. Add")
    print("3. Update")
    print("4. Edit")
    print("5. Delete")
    print("6. Save")
    print("7. Load")
    print("8. Quit")
    print("**************************")


def print_retrieve_list():
    """프로그램에 저장 되어 있는 식당의 정보(이름, 점수 + 상세정보)를 보여주는 함수"""
    custom_sort_list()
    flavor_total, hygiene_total, price_total = calculate_total()
    flavor_average, hygiene_average, price_average = calculate_average()
    print("INDEX                 NAME  FLAVOR  HYGIENE  PRICE                    ADD TIME")
    print("******************************************************************************")
    for j in range(len(restaurant_list)):
        print((str(j+1)+".").ljust(5), " ", str(restaurant_list[j][INDEX_NAME]).rjust(20), " ", str(restaurant_list[j][INDEX_FLAVOR]).rjust(7), " ",  str(restaurant_list[j][INDEX_HYGIENE]).rjust(8), " ", str(restaurant_list[j][INDEX_PRICE]).rjust(6), " ", str(restaurant_list[j][INDEX_TIME]).rjust(27), sep="")
    print("******************************************************************************")
    print("TOTAL".ljust(26), str(flavor_total).rjust(7), str(hygiene_total).rjust(8), str(price_total).rjust(6))
    print("AVG.".ljust(27), str(round(flavor_average, 1)).rjust(7), str(round(hygiene_average, 1)).rjust(8), str(round(price_average, 1)).rjust(6))
    print()
    print("TOPS: 1", end='')

    for k in range(2, check_top()+1):
        print(",", k, end='')
    print()

    print("식당의 추가 정보를 보고 싶으시다면 식당의 INDEX를 입력하세요. 추가 정보가 필요 없으시면 0을 입력하면 메뉴로 돌아갑니다.")

    while True:
        try:
            additional_information_index = int(input(">"))
            if 0 < additional_information_index <= len(restaurant_list):
                pass
            elif additional_information_index == 0:
                break
            else:
                print("The input has errors.")
                continue

        except ValueError:
            print("The input has errors.")
            continue

        print("INDEX                 NAME                 MENU             LOCATION  BUSINESS HOURS")
        print("************************************************************************************")
        print((str(additional_information_index) + ".").ljust(5), " ", str(restaurant_list[additional_information_index-1][INDEX_NAME]).rjust(20), " ", str(restaurant_list[additional_information_index-1][INDEX_MENU]).rjust(20), " ", str(restaurant_list[additional_information_index-1][INDEX_LOCATION]).rjust(20), " ", str(restaurant_list[additional_information_index-1][INDEX_BUSINESS_HOURS]).rjust(15), " ", sep="")
        print("************************************************************************************")
        break


def print_list():
    """프로그램에 저장 되어 있는 식당의 정보(이름, 점수)를 보여주는 함수"""
    custom_sort_list()
    flavor_total, hygiene_total, price_total = calculate_total()
    flavor_average, hygiene_average, price_average = calculate_average()
    print("INDEX                 NAME  FLAVOR  HYGIENE  PRICE                    ADD TIME")
    print("******************************************************************************")
    for j in range(len(restaurant_list)):
        print((str(j+1)+".").ljust(5), " ", str(restaurant_list[j][INDEX_NAME]).rjust(20), " ", str(restaurant_list[j][INDEX_FLAVOR]).rjust(7), " ",  str(restaurant_list[j][INDEX_HYGIENE]).rjust(8), " ", str(restaurant_list[j][INDEX_PRICE]).rjust(6), " ", str(restaurant_list[j][INDEX_TIME]).rjust(27), sep="")
    print("******************************************************************************")
    print("TOTAL".ljust(26), str(flavor_total).rjust(7), str(hygiene_total).rjust(8), str(price_total).rjust(6))
    print("AVG.".ljust(27), str(round(flavor_average, 1)).rjust(7), str(round(hygiene_average, 1)).rjust(8), str(round(price_average, 1)).rjust(6))
    print()
    print("TOPS: 1", end='')

    for k in range(2, check_top()+1):
        print(",", k, end='')
    print()


def custom_sort_list():
    """유저가 선택한 정렬 기준에 따라 식당의 정보를 정렬할 수 있게 해주는 함수, 메뉴 출력에 사용"""
    global restaurant_list

    print("정렬 기준을 선택하세요.")
    print("1.TOTAL SCORE 2. FLAVOR 3. HYGIENE 4.PRICE 5.ADD TIME")
    while True:
        try:
            sort_num = int(input(">"))

            if sort_num == 1:
                restaurant_list.sort(key=lambda x: x[INDEX_FLAVOR] + x[INDEX_HYGIENE] + x[INDEX_PRICE], reverse=True)
                break

            elif sort_num == 2:
                restaurant_list.sort(key=lambda x: x[INDEX_FLAVOR], reverse=True)
                break

            elif sort_num == 3:
                restaurant_list.sort(key=lambda x: x[INDEX_HYGIENE], reverse=True)
                break

            elif sort_num == 4:
                restaurant_list.sort(key=lambda x: x[INDEX_PRICE], reverse=True)
                break

            elif sort_num == 5:
                restaurant_list.sort(key=lambda x: x[INDEX_TIME], reverse=True)
                break

            else:
                print("The input has errors.")
                continue

        except ValueError:
            print("The input has errors.")
            continue


def calculate_total():
    """식당의 맛, 위생, 가격의 합을 구해주는 함수"""
    flavor_total = 0
    hygiene_total = 0
    price_total = 0

    for j in range(len(restaurant_list)):
        flavor_total += restaurant_list[j][INDEX_FLAVOR]
        hygiene_total += restaurant_list[j][INDEX_HYGIENE]
        price_total += restaurant_list[j][INDEX_PRICE]

    return flavor_total, hygiene_total, price_total


def calculate_average():
    """식당의 맛, 위생, 가격의 평균을 구해주는 함수"""
    flavor_average, hygiene_average, price_average = calculate_total()

    flavor_average = flavor_average / len(restaurant_list)
    hygiene_average = hygiene_average / len(restaurant_list)
    price_average = price_average / len(restaurant_list)

    return flavor_average, hygiene_average, price_average


def check_top():
    """맛, 위생, 가격의 합을 비교하여 가장 큰 식당이 어떤 것인지 보여주는 함수"""
    top_count = 1
    for j in range(1, len(restaurant_list)):
        if restaurant_list[j][INDEX_FLAVOR] + restaurant_list[j][INDEX_HYGIENE] + restaurant_list[j][INDEX_PRICE] == restaurant_list[j-1][INDEX_FLAVOR] + restaurant_list[j-1][INDEX_HYGIENE] + restaurant_list[j-1][INDEX_PRICE]:
            top_count += 1

        else:
            break

    return top_count


def add_list():
    """프로그램에 식당의 정보를 추가"""
    global restaurant_list

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
        elif 1<= len(add_list_temp) < 4:
            try:
                print("1~5점 사이의 점수를 입력해주세요.")
                restaurant_score = int(input(user_input_list[len(add_list_temp)]))

            except ValueError:
                print("The input has errors.")
                for i in range(len(add_list_temp)):
                    print(user_input_list[i], add_list_temp[i], sep="")
                continue

            if 1 <= restaurant_score <= 5:
                add_list_temp.append(restaurant_score)

        elif len(add_list_temp) == 4:
            print("식당의 대표 메뉴를 입력해주세요. (ex. Pasta, Pizza)")
            restaurant_menu = input(user_input_list[len(add_list_temp)])
            add_list_temp.append(restaurant_menu)

        elif len(add_list_temp) == 5:
            print("식당의 위치를 입력해주세요. (ex. Jangchung-dong)")
            restaurant_location = input(user_input_list[len(add_list_temp)])
            add_list_temp.append(restaurant_location)

        elif len(add_list_temp) == 6:
            print("식당의 영업시간을 입력해주세요. (ex. 9:00 ~ 20:00)")
            restaurant_business_hours = input(user_input_list[len(add_list_temp)])
            add_list_temp.append(restaurant_business_hours)

        else:
            print("The input has errors.")
            for i in range(len(add_list_temp)):
                print(user_input_list[i], add_list_temp[i], sep="")

    add_list_temp.append(datetime.datetime.now())
    restaurant_list.append(add_list_temp)
    print("Added.")


def update_list():
    """프로그램에 저장 되어 있는 기존 식당의 정보를 모두 업데이트 할 수 있게 해주는 함수"""
    global restaurant_list
    update_list_temp = []
    print_list()

    while True:
        try:
            update_num = int(input("Update>"))

            if 1 <= update_num <= len(restaurant_list):
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

                    if len(update_list_temp) == 4:
                        print("식당의 대표 메뉴를 입력해주세요. (ex. Pasta, Pizza)")
                        restaurant_menu = input(user_input_list[len(update_list_temp)])
                        update_list_temp.append(restaurant_menu)

                    if len(update_list_temp) == 5:
                        print("식당의 위치를 입력해주세요. (ex. Jangchung-dong)")
                        restaurant_location = input(user_input_list[len(update_list_temp)])
                        update_list_temp.append(restaurant_location)

                    if len(update_list_temp) == 6:
                        print("식당의 영업시간을 입력해주세요. (ex. 9:00 ~ 20:00)")
                        restaurant_business_hours = input(user_input_list[len(update_list_temp)])
                        update_list_temp.append(restaurant_business_hours)

                update_list_temp.append(datetime.datetime.now())
                restaurant_list[update_num - 1] = update_list_temp
                print("Updated.")
                break

            else:
                print("The input has errors.")

        except ValueError:
            print("The input has errors.")
            continue


def edit_list():
    """프로그램에 저장 되어 있는 기존 식당의 정보의 일부를 수정 할 수 있게 해주는 함수"""
    global restaurant_list
    print_list()

    while True:
        try:
            edit_list_num = int(input("Edit>"))

            if 1 <= edit_list_num <= len(restaurant_list):
                try:
                    while True:
                        edit_part_num = int(input("1:Name, 2:Flavor, 3:Hygiene:, 4:Price, 5:Menu, 6:Location, 7:Business hours > "))
                        if edit_part_num == 1:
                            while True:
                                restaurant_name = input(user_input_list[edit_part_num-1])
                                if 1 <= len(restaurant_name) < 20:
                                    restaurant_list[edit_list_num-1][0] = restaurant_name
                                    print("Edited")
                                    break
                                elif len(restaurant_name) == 0:
                                    print("The input has errors.")
                                    continue
                                else:
                                    print("The length of name should be less than 20")
                                    print("The input has errors.")
                                    continue
                        elif 2 <= edit_part_num <= 4:
                            while True:
                                try:
                                    print("1~5점 사이의 점수를 입력해주세요.")
                                    restaurant_score = int(input(user_input_list[edit_part_num-1]))

                                except ValueError:
                                    print("The input has errors.")
                                    continue

                                if 1 <= restaurant_score <= 5 :
                                    restaurant_list[edit_list_num-1][edit_part_num-1] = restaurant_score
                                    print("Edited")
                                    break
                                else:
                                    print("The input has errors.")
                                    continue
                        elif edit_part_num == 5:
                            print("식당의 대표 메뉴를 입력해주세요. (ex. Pasta, Pizza)")
                            restaurant_menu = input(user_input_list[edit_part_num-1])
                            restaurant_list[edit_list_num-1][edit_part_num-1] = restaurant_menu
                            print("Edited")
                        elif edit_part_num == 6:
                            print("식당의 위치를 입력해주세요. (ex. Jangchung-dong)")
                            restaurant_location = input(user_input_list[edit_part_num-1])
                            restaurant_list[edit_list_num-1][edit_part_num-1] = restaurant_location
                            print("Edited")
                        elif edit_part_num == 7:
                            print("식당의 영업시간을 입력해주세요. (ex. 9:00 ~ 20:00)")
                            restaurant_business_hours = input(user_input_list[edit_part_num-1])
                            restaurant_list[edit_list_num-1][edit_part_num-1] = restaurant_business_hours
                            print("Edited")
                        else:
                            print("The input has errors.")
                            continue
                        break
                except ValueError:
                    print("The input has errors.")
                    continue
                break

            else:
                print("The input has errors.")
                continue

        except ValueError:
            print("The input has errors.")
            continue


def delete_list():
    """프로그램에 저장 되어 있는 기존 식당의 정보를 삭제할 수 있게 해주는 함수"""
    global restaurant_list
    print_list()

    while True:
        try:
            delete_num = int(input("Delete>"))

            if 1 <= delete_num <= len(restaurant_list):
                del restaurant_list[delete_num - 1]
                print("Deleted.")
                break

            else:
                print("The input has errors.")

        except ValueError as e:
            print("The input has errors.")
            continue


def save_list():
    """프로그램에 저장 되어 있는 식당의 정보를 컴퓨터에 저장할 수 있게 해주는 함수"""
    global restaurant_list

    save_restaurant_list = restaurant_list

    file = open('DATA.dat', 'wb')
    pickle.dump(save_restaurant_list, file)
    file.close()
    print("Saved.")


def load_list():
    """컴퓨터에 저장 되어 있는 식당의 정보를 프로그램에 불러올 수 있게 해주는 함수"""
    global restaurant_list

    file = open('DATA.dat', 'rb')
    save_restaurant_list = pickle.load(file)
    file.close()
    restaurant_list = save_restaurant_list

    print("Loaded.")


print_menu()
while True:
    try:
        input_num = int(input(">"))

    except ValueError as e:
        print("The input has errors.")
        continue

    if 1 <= input_num <= 8:
        if input_num == MENU_RETRIEVE:
            if not restaurant_list:
                print("There are no data.")

            else:
                print_retrieve_list()

        elif input_num == MENU_ADD:
            if len(restaurant_list) >= 9999:
                print("No more data is accepted.")
                continue

            else:
                add_list()

        elif input_num == MENU_UPDATE:
            if not restaurant_list:
                print("There are no data.")

            else:
                update_list()

        elif input_num == MENU_DELETE:
            if not restaurant_list:
                print("There are no data.")

            else:
                delete_list()

        elif input_num == MENU_SAVE:
            if not restaurant_list:
                print("There are no data.")

            else:
                print_list()
                save_list()

        elif input_num == MENU_LOAD:
            if not os.path.isfile('DATA.dat'):
                print("There is no files.")

            else:
                load_list()

        elif input_num == MENU_EDIT:
            if not restaurant_list:
                print("There are no data.")
            else:
                edit_list()

        elif input_num == MENU_QUIT:
            print("Bye Bye!!")
            break

    else:
        print("The input has errors.")
        continue

    print()
    print_menu()
