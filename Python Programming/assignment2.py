score_list = []
subject_list = ["Korean:", "English:", "Math:"]

MENU_RETRIEVE = 1
MENU_ADD = 2
MENU_UPDATE = 3
MENU_DELETE = 4
MENU_QUIT = 5


def print_menu():
    print("**************************")
    print("1. Retrieve")
    print("2. Add")
    print("3. Update")
    print("4. Delete")
    print("5. Quit")
    print("**************************")


def print_list():
    print("INDEX  KOR  ENG  MAT")
    print("********************")
    for j in range(len(score_list)):
        print((str(j+1)+".").ljust(5), " ", str(score_list[j][0]).rjust(4), " ",  str(score_list[j][1]).rjust(4), " ", str(score_list[j][2]).rjust(4), sep="")


def sort_list():
    global score_list
    score_list = sorted(score_list, key=lambda x: x[0] + x[1] + x[2], reverse=True)


print_menu()
while True:
    if score_list:
        sort_list()
    try:
        input_num = int(input(">"))

    except ValueError as e:
        print("The input has errors.")
        continue

    if 1 <= input_num <= 5:
        if input_num == MENU_RETRIEVE:
            if not score_list:
                print("There are no data.")
                print()

            else:
                print_list()
                print()

        elif input_num == MENU_ADD:
            if len(score_list) >= 9999:
                print("No more data is accepted.")
                continue

            else:
                add_list_temp = []

                while len(add_list_temp) < len(subject_list):
                    try:
                        subject_score = int(input(subject_list[len(add_list_temp)]))

                    except ValueError as e:
                        print("The input has errors.")
                        for i in range(len(add_list_temp)):
                            print(subject_list[i], add_list_temp[i], sep="")
                        continue

                    if 0 <= subject_score <= 100:
                        add_list_temp.append(subject_score)

                    else:
                        print("The input has errors.")
                        for i in range(len(add_list_temp)):
                            print(subject_list[i], add_list_temp[i], sep="")

                score_list.append(add_list_temp)
                print("Added.")
                print()

        elif input_num == MENU_UPDATE:
            if not score_list:
                print("There are no data.")
                print()

            else:
                update_list_temp = []
                print_list()

                while True:
                    try:
                        update_num = int(input("Update>"))

                        if 1 <= update_num <= len(score_list):
                            while len(update_list_temp) < len(subject_list):
                                try:
                                    subject_score = int(input(subject_list[len(update_list_temp)]))

                                except ValueError as e:
                                    print("The input has errors.")
                                    for i in range(len(update_list_temp)):
                                        print(subject_list[i], update_list_temp[i], sep="")
                                    continue

                                if 0 <= subject_score <= 100:
                                    update_list_temp.append(subject_score)

                                else:
                                    print("The input has errors.")
                                    for i in range(len(update_list_temp)):
                                        print(subject_list[i], update_list_temp[i], sep="")

                            score_list[update_num-1] = update_list_temp
                            print("Updated.")
                            print()
                            break

                        else:
                            print("The input has errors.")

                    except ValueError as e:
                        print("The input has errors.")
                        continue

        elif input_num == MENU_DELETE:
            if not score_list:
                print("There are no data.")
                print()

            else:
                print_list()

                while True:
                    try:
                        delete_num = int(input("Delete>"))

                        if 1 <= delete_num <= len(score_list):
                            del score_list[delete_num-1]
                            print("Deleted.")
                            print()
                            break

                        else:
                            print("The input has errors.")

                    except ValueError as e:
                        print("The input has errors.")
                        continue

        elif input_num == MENU_QUIT:
            print("Bye Bye!!")
            break

    else:
        print("The input has errors.")
        continue

    print_menu()
