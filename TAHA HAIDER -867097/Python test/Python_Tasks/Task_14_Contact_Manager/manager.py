from storage import load_contacts, save_contacts


def add_contact(contact_id, name, phone, email):

    contacts = load_contacts()

    for contact in contacts:

        if contact["id"] == contact_id:
            print("ID already exists")
            return

    contacts.append({
        "id": contact_id,
        "name": name,
        "phone": phone,
        "email": email
    })

    save_contacts(contacts)

    print("Contact added")


def search_contact(name):

    contacts = load_contacts()

    for contact in contacts:

        if name.lower() in contact["name"].lower():
            print(contact["name"], contact["phone"], contact["email"])


def update_contact(contact_id, name, phone, email):

    contacts = load_contacts()

    for contact in contacts:

        if contact["id"] == contact_id:

            contact["name"] = name
            contact["phone"] = phone
            contact["email"] = email

            save_contacts(contacts)

            print("Contact updated")
            return

    print("Contact not found")


def delete_contact(contact_id):

    contacts = load_contacts()

    for contact in contacts:

        if contact["id"] == contact_id:

            contacts.remove(contact)

            save_contacts(contacts)

            print("Contact deleted")
            return

    print("Contact not found")


def list_contacts():

    contacts = load_contacts()

    for contact in contacts:

        print(contact["id"], contact["name"], contact["phone"], contact["email"])
