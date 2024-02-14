import PySimpleGUI as sg
import csv
import re

sg.theme('DarkPurple1')
sg.set_options(font='Arial 16')

CONTACTS_FILE = "contacts.csv"

def validate_contact(values):
    fname = values['-fname-']
    lname = values['-lname-']
    phone = values['-phone-']
    email = values['-email-']
    address = values['-address-']

    if not all((fname, lname, phone, email, address)):
        sg.Popup("Please fill in all fields.")
        return False

    if not re.match(r'^\d{10}$', phone):
        sg.Popup("Invalid phone number. Please enter a 10-digit integer.") 
        return False

    if not re.match(r'^\w+@\w+\.\w+$', email):
        sg.Popup("Invalid email. Please enter a valid email address.")
        return False

    return True

def add_contact(values):
    if not validate_contact(values):
        return

    contact = [values['-fname-'], values['-lname-'], values['-phone-'], values['-email-'], values['-address-']]

    with open(CONTACTS_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(contact)

    sg.Popup("Contact added successfully!")
    clear_input_fields()

def search_contact(values):
    search_text = values['-searchText-'].lower()

    found_contacts = []
    with open(CONTACTS_FILE, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if (row[0].lower().startswith(search_text) or 
                row[1].lower().startswith(search_text) or 
                search_text in row[2]):  # search in phone numbers
                found_contacts.append(row)

    update_search_output(found_contacts)

def view_contacts():
    all_contacts = []
    with open(CONTACTS_FILE, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            all_contacts.append(row)

    update_search_output(all_contacts)

def delete_contact(values):
    delete_text = values['-deleteText-'].lower()

    deleted_contacts = []
    remaining_contacts = []
    with open(CONTACTS_FILE, "r") as file:
        reader = csv.reader(file)
        for contact in reader:
            if contact[0].lower().startswith(delete_text) or contact[1].lower().startswith(delete_text):
                deleted_contacts.append(contact)
            else:
                remaining_contacts.append(contact)

    if not deleted_contacts:
        sg.Popup("No contacts found!")
        return

    layout_delete = [[sg.Text("Delete the following contacts?")]] + [[sg.Text(", ".join(contact))] for contact in deleted_contacts] + [[sg.Button('Delete'), sg.Button('Cancel')]]
    window_delete = sg.Window('Delete Contacts', layout_delete)

    event_delete, _ = window_delete.read()
    window_delete.close()

    if event_delete == 'Delete':
        with open(CONTACTS_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            for contact in remaining_contacts:
                writer.writerow(contact)

        sg.Popup("Contacts deleted successfully!")
    else:
        sg.Popup("Delete canceled!")

def update_contacts(values):
    updated_contacts_text = values['-searchOutput-']
    updated_contacts = [line.strip().split(', ') for line in updated_contacts_text.split('\n') if line.strip()]
    
    with open(CONTACTS_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        for contact in updated_contacts:
            writer.writerow(contact)

    sg.Popup("Contacts updated successfully!")
    view_contacts()

def clear_input_fields():
    window['-fname-'].update('')
    window['-lname-'].update('')
    window['-phone-'].update('')
    window['-email-'].update('')
    window['-address-'].update('')

def update_search_output(contacts):
    output = ''
    for contact in contacts:
        output += ', '.join(contact) + '\n'
    window['-searchOutput-'].update(output)

layout = [
    [sg.Text('Enter First Name'), sg.InputText(key='-fname-')],
    [sg.Text('Enter Last Name'), sg.InputText(key='-lname-')],
    [sg.Text('Enter Phone Number'), sg.InputText(key='-phone-')],
    [sg.Text('Enter Email'), sg.InputText(key='-email-')],
    [sg.Text('Enter Address'), sg.InputText(key='-address-')],
    [sg.Button('Save'), sg.Button('Search'), sg.Button('View Contacts')],
    [sg.Text("Search by Starting Letter, Full Name, or Phone Number"), sg.InputText(key='-searchText-')],
    [sg.Text("Search Results:")],
    [sg.Multiline(size=(50, 5), key='-searchOutput-')],
    [sg.Button('Update Contacts')],
    [sg.Text("Enter Name to Delete"), sg.InputText(key='-deleteText-'), sg.Button('Delete Contact')],
]

window = sg.Window('Contact Book', layout, icon='favicon.ico')

while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Save':
        add_contact(values)
        clear_input_fields()
    elif event == 'Search':
        search_contact(values)
    elif event == 'View Contacts':
        view_contacts()
    elif event == 'Delete Contact':
        delete_contact(values)
    elif event == 'Update Contacts':
        update_contacts(values)

window.close()
