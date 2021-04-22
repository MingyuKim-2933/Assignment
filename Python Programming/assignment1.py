score_list = []

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
    print("INDEX  KOR")
    print("**********")
    for i in range(len(score_list)):
        print((str(i+1)+".").ljust(5), " ", str(score_list[i]).rjust(4), sep="")


while True:
    print_menu()
    input_num = int(input(">"))

    if input_num == MENU_RETRIEVE:
        if not score_list:
            print("There are no data.")
            print()
        else:
            print_list()
            print()
    elif input_num == MENU_ADD:
        korean_value = int(input("Korean: "))
        score_list.append(korean_value)
        print("Added.")
        print()
    elif input_num == MENU_UPDATE:
        if not score_list:
            print("There are no data.")
            print()
        else:
            print_list()
            update_num = int(input("Update>"))
            update_value = int(input("Korean:"))
            score_list[update_num-1] = update_value
            print("Updated.")
            print()
    elif input_num == MENU_DELETE:
        if not score_list:
            print("There are no data.")
            print()
        else:
            print_list()
            delete_num = int(input("Delete>"))
            del score_list[delete_num-1]
            print("Deleted.")
            print()
    elif input_num == MENU_QUIT:
        print("Bye Bye!!")
        break
