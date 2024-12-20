import csv
import sqlite3

def create_connection():
    try:
        con = sqlite3.connect('users.sqlite3')
        return con
    except Exception as e:
        print(e)

INPUT_STRING = '''
    Enter the option:
    1.CREATE TABLE
    2.DUMP USERS FROM CSV INTO USERS TABLE
    3.ADD NEW USER INTO USER TABLE
    4.QUERY ALL USERS FROM TABLE
    5.QUERY ALL USERS BY ID FROM TABLE
    6.QUERY SPECIFIED  NO OF RECORDS FROM TABLE
    7.DELETE ALL USERS
    8.DELETE USER BY ID 
    9.UPDATE USER
    10.PRESS ANY KEY TO EXIT
'''

def create_table(con):
    CREATE_USERS_TABLE_QUERY = '''
        create table if not exists users(
            id integer primary key autoincrement,
            first_name char(100) not null,
            last_name char(100) not null,
            company_name char(100) not null,
            address char(100) not null,
            city char(100) not null,
            state char(100) not null,
            county char(100) not null,
            zip real not null,
            phone1 char(100) not null,
            phone2 char(100) not null,
            email char(100) not null,
            web text
        );
    '''
    cur = con.cursor()
    cur.execute(CREATE_USERS_TABLE_QUERY)
    print("User table was created sucssfully!")

def read_csv():
    users = []
    with open("sample_users.csv","r") as f:
        data = csv.reader(f)
        for user in data:
            users.append(tuple(user))
    return users[1:]

def insert_users(con, users):
    user_add_query = '''
    insert into users (
        first_name,
        last_name,
        company_name,
        address,
        city,
        state,
        county,
        zip,
        phone1,
        phone2,
        email,
        web
    )
    values(?,?,?,?,?,?,?,?,?,?,?,?);
'''
    cur = con.cursor()
    cur.executemany(user_add_query,users)
    con.commit()
    print("{} users were imported sucessfully".format(len(users)))

def select_users(con,no_of_records=None):
    cur = con.cursor()
    if no_of_records:
        users = cur.execute("select * from users limit ?;",(no_of_records,))
    else:
        users = cur.execute("select * from users;")
    for user in users:
        print(user)

def select_users_id(con,user_id):
    cur = con.cursor()
    users = cur.execute("select * from users where id=?",(user_id,))
    for user in users:
        print(user)

def delete_users(con):
    cur = con.cursor()
    cur.execute("delete from users;")
    con.commit()
    print("All users were deleted sucessfully!")

def delete_by_id(con,user_id):
    cur = con.cursor()
    cur.execute("Delete from users where id=?",(user_id,))
    con.commit()
    print("User with id {} is deleted!".format(user_id))

def update_user(con,field,user_id):
    cur = con.cursor()
    cur.execute("update table set field=? where id=?",(field))

columns = (
    "first_name",
    "last_name",
    "company_name",
    "address",
    "city",
    "state",
    "county",
    "zip",
    "phone1",
    "phone2",
    "email",
    "web"
)

def update_user_by_id(con,user_id,column_name,column_value):
    update_query = "update users set {}=? where id = ?;".format(column_name)
    cur = con.cursor()
    cur.execute(update_query,(column_value,user_id))
    con.commit()
    print("{} was updated with value {} !".format(column_name,column_value))

def main():

    con = create_connection()
    user_input  = input(INPUT_STRING)
    if user_input == '1':
        create_table(con)
    elif user_input == '2':
        users = read_csv()
        insert_users(con,users)
    elif user_input == '3':
        user_data = []
        for column in columns:
            value = input("Enter the value of:{}".format(column))
            user_data.append(value)
        insert_users(con,[tuple(user_data)])
    elif user_input == '4':
        select_users(con)
    elif user_input == '5':
        user_id = input("Enter the id")
        if user_id.isnumeric():
            select_users_id(con,user_id)
    elif user_input == '6':
        no_of_users =  input ("Enter number of users:")
        if no_of_users.isnumeric():
            select_users(con,no_of_users)
    elif user_input == '7':
        confirm = input("Are you sure to delete all users?(y/n)")
        if confirm=='y':
            delete_users(con)
        else:
            print("operation terminated!")
    elif user_input == '8':
        user_id = input("Enter the id of the user:")
        delete_by_id(con,user_id)
    elif user_input == '9':
        user_id = input("Enter the id of user:")
        if user_id.isnumeric():
            column_name = input(
                "Enter the column you want to edit.Please make sure the column is within{}:".format(columns)
            )
            if column_name in columns:
                column_value = input("Enter the value of {}:".format(column_name))
                update_user_by_id(con,user_id,column_name,column_value)
    elif user_input == '10':
        exit
main()
######THIS IS A BASIC CRUD OPERATION######