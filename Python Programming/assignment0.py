while True:
    print("**************************")
    print("1. Retrieve")
    print("2. Add")
    print("3. Update")
    print("4. Delete")
    print("5. Quit")
    print("**************************")
    input_num = int(input(">"))

    if input_num == 1:
        print("Retrieve")
    elif input_num == 2:
        print("Add")
    elif input_num == 3:
        print("Update")
    elif input_num == 4:
        print("Delete")
    elif input_num == 5:
        print("Bye Bye!!")
        break
