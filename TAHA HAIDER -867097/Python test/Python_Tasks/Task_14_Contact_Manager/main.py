from manager import *

while True:

    print("\n1 Add")
    print("2 Search")
    print("3 Update")
    print("4 Delete")
    print("5 List")
    print("6 Exit")

    choice = input("Enter choice: ")

    if choice == "1":

        cid = input("ID: ")
        name = input("Name: ")
        phone = input("Phone: ")
        email = input("Email: ")

        add_contact(cid, name, phone, email)

    elif choice == "2":

        name = input("Search name: ")
        search_contact(name)

    elif choice == "3":

        cid = input("ID: ")
        name = input("New name: ")
        phone = input("New phone: ")
        email = input("New email: ")

        update_contact(cid, name, phone, email)

    elif choice == "4":

        cid = input("ID: ")
        delete_contact(cid)

    elif choice == "5":

        list_contacts()

    elif choice == "6":

        break

    else:

        print("Invalid choice")
