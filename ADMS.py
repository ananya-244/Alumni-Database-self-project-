import mysql.connector
from datetime import date
import time


def clear():
    print("\n" * 65)


# Context manager for database connection
def connect_db():
    return mysql.connector.connect(host='localhost', database='alumni', user='root', password='root')


def record_exists(name, fname, dob):
    query = "SELECT * FROM alumni WHERE name=%s AND fname=%s AND dob=%s;"
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query, (name, fname, dob))
        return cursor.fetchone()


def add_alumni():
    clear()
    alumni_data = {
        'name': input('Enter Alumni Name: ').upper(),
        'fname': input('Enter Alumni Father Name: ').upper(),
        'dob': input('Enter Alumni Date Of Birth (yyyy-mm-dd): '),
        'phone': input('Enter Alumni Phone No: '),
        'email': input('Enter Alumni Email ID: '),
        'stream': input('Enter Alumni Stream (Passed): ').upper(),
        'pass_year': input('Enter Alumni Pass Year: '),
        'quali': input('Enter Alumni Highest Qualification: ').upper(),
        'position': input('Enter Alumni Current Position: '),
        'city': input('Enter Alumni Current City: ').upper(),
        'country': input('Enter Alumni Current Country: ').upper(),
        'employ': input('Enter Alumni Currently Employed/Business: ')
    }

    if record_exists(alumni_data['name'], alumni_data['fname'], alumni_data['dob']) is None:
        query = '''INSERT INTO alumni(name, fname, phone, email, stream, pass_year, hqualification, current_position, dob, c_city, c_country, employement)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, tuple(alumni_data.values()))
            conn.commit()
        print('\n\n\n Alumni information added successfully.')
    else:
        print('\n\n\n Record already exists.')
    input('\n\n\n Press any key to continue.')


def modify_alumni():
    fields = {
        1: 'name', 2: 'fname', 3: 'phone', 4: 'email', 5: 'stream', 6: 'pass_year', 7: 'hqualification',
        8: 'current_position', 9: 'c_city', 10: 'c_country'
    }
    while True:
        clear()
        print('ALUMNI INFORMATION MODIFICATION MENU')
        print('*' * 100)
        for key, field in fields.items():
            print(f'{key}. Correction in {field.replace("_", " ").title()}')
        print('11. Back to main menu')

        choice = int(input('Enter your choice: '))
        if choice == 11:
            break
        field_name = fields.get(choice)
        if not field_name:
            print('Invalid choice.')
            continue

        idr = input('Enter Alumni ID: ')
        value = input(f'Enter new value for {field_name.replace("_", " ").title()}: ')
        query = f"UPDATE alumni SET {field_name}=%s WHERE id=%s;"

        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (value, idr))
            conn.commit()
        print(f'\n\n\n {field_name.replace("_", " ").title()} updated successfully.')
        input('\n\n\n Press any key to continue.')


def search_menu():
    fields = {
        1: 'id', 2: 'name', 3: 'fname', 4: 'phone', 5: 'email', 6: 'stream',
        7: 'pass_year', 8: 'hqualification', 9: 'current_position', 10: 'c_city', 11: 'c_country', 12: 'employement'
    }
    while True:
        clear()
        print('S E A R C H  M E N U')
        print('*' * 100)
        for key, field in fields.items():
            print(f'{key}. Search by {field.replace("_", " ").title()}')
        print('13. Back to main menu')

        choice = int(input('Enter your choice: '))
        if choice == 13:
            break
        field_name = fields.get(choice)
        if not field_name:
            print('Invalid choice.')
            continue

        value = input(f'Enter {field_name.replace("_", " ").title()}: ')
        query = f"SELECT * FROM alumni WHERE {field_name} LIKE %s;"

        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (f'%{value}%',))
            records = cursor.fetchall()

        clear()
        print(f'Search Results for {field_name.replace("_", " ").title()}: {value}')
        print('-' * 120)
        if not records:
            print(f'No results found for {field_name.replace("_", " ").title()}: {value}')
        for record in records:
            print(record)
        input('\n\n\n Press any key to continue.')


def report_alumni_list():
    query = "SELECT * FROM alumni;"
    with connect_db() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        records = cursor.fetchall()

    clear()
    print('Alumni List')
    print('_' * 140)
    print('{:10s} {:30s} {:30s} {:15s} {:30s} {:20s}'.format('ID', 'Name', 'Father Name', 'Email', 'Phone', 'Position'))
    print('_' * 140)
    for record in records:
        print('{:010d} {:30s} {:30s} {:15s} {:30s} {:20s}'.format(record[0], record[1], record[2], record[4], record[3],
                                                                  record[8]))
        print('_' * 140)
    input('\n\n\n Press any key to continue.')


# Other reporting functions like year_wise_alumni, city_wise_alumni_list, etc., can follow the same pattern.

def report_menu():
    while True:
        clear()
        print('A L U M N I  R E P O R T  M E N U')
        print('*' * 120)
        options = {
            1: report_alumni_list,
            # Similarly add other reporting functions here
            9: None
        }
        for key, _ in options.items():
            print(f"{key}. Report option {key}")
        choice = int(input('Enter your choice: '))
        if choice == 9:
            break
        action = options.get(choice)
        if action:
            action()


def main():

    while True:
        clear()
        print('A L U M N I  I N F O R M A T I O N  S Y S T E M')
        print('*' * 100)
        options = {
            1: add_alumni,
            2: modify_alumni,
            3: search_menu,
            4: report_menu,
            5: exit
        }
        for key, _ in options.items():
            print(f"{key}. Menu option {key}")
        choice = int(input('Enter your choice: '))
        action = options.get(choice)
        if action:
            action()


if __name__ == "__main__":
    main()
