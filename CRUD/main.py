import psycopg2
import os

def clear():
    """Cleans the console in UNIX systems or OS systems
    """
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def start_connection():
    """The initialization to connect with Postgresql Database

    Returns:
        object: A connection object
    """
    username = input('Database user: ')
    password = input('Database password: ')

    try:
        connect = psycopg2.connect(f"dbname='aida' user={username} password={password} host='localhost'")
        print('Succesfully Connected')
    except Exception as e:
        print(e)

    return connect


def set_register():
    """Function to set all records in order to create or update

    Returns:
        tuple: A tuple of values to set at Postgresql queries
    """
    c_date = input('Register de date in the next format "YYYY-MM-DD HH:mm:ss": ')
    c_mood = input('What was your mood at the moment of testing: ')
    c_mood = c_mood.capitalize()
    c_anxiety = int(input('What was your anxierty level: '))
    c_glucose = int(input('Register your glucose level in mg/dl: '))
    c_g_level = ''

    if c_glucose > 180:
        c_g_level = 'High'
    elif c_glucose < 80:
        c_g_level = 'Low'
    else:
        c_g_level = 'in Range'

    return (c_date, c_mood, c_anxiety, c_glucose, c_g_level)


def create(connect):
    """The create new register function

    Args:
        connect (object): A connection object to execute Postgresql queries
    """
    values_insert = set_register()
    tuple_values_insert = (values_insert[0], values_insert[1], values_insert[2], values_insert[3], values_insert[4])
    print(tuple_values_insert)
    query = 'INSERT INTO aigda(register_date, mood, anxiety_level, glucose, g_level) VALUES(%s, %s, %s, %s, %s)'

    
    with connect.cursor() as cursor:
        cursor.execute(query, tuple_values_insert)
        connect.commit()
        print('Values inserted')


def read(connect):
    """The read values function

    Args:
        connect (object): A connection object to execute Postgresql queries
    """
    print("""How many registers do you want to read?
    a) Last 10 registers
    b) First 10 registers
    c) All registers""")
    read_user = input('Select an option: ')
    read_user.lower()

    with connect.cursor() as cursor:
        if read_user == 'a':
            query = 'SELECT * FROM aigda ORDER BY id_glucose DESC LIMIT 10'
            cursor.execute(query)
            records = cursor.fetchall()

            for row in records:
                print('-'*10)
                print(f'register: {row[0]}')
                print(f'date: {row[1]}')
                print(f'mood: {row[2]}')
                print(f'Anxiety Level: {row[3]}')
                print(f'glucose: {row[4]}')
                print(f'glucose status: {row[5]}')
                
        elif read_user == 'b':
            query = 'SELECT * FROM aigda LIMIT 10'
            cursor.execute(query)
            records = cursor.fetchall()

            for row in records:
                print('-'*10)
                print(f'register: {row[0]}')
                print(f'date: {row[1]}')
                print(f'mood: {row[2]}')
                print(f'Anxiety Level: {row[3]}')
                print(f'glucose: {row[4]}')
                print(f'glucose status: {row[5]}')

        elif read_user == 'c':
            query = 'SELECT * FROM aigda'
            cursor.execute(query)
            records = cursor.fetchall()

            for row in records:
                print(f'{row[0]} - {row[1]} - {row[2]} - {row[3]} - {row[4]} - {row[5]}')

        else:
            print('Wrong option')


def updating_process(connect, cursor):
    """A function which updates a value.

    Args:
        connect (object): The connection object to work in a Postgresql Database
        cursor (method): The method of connect objecto to execute queries
    """
    register_to_change = int(input('Enter the number of the register to chage: '))
    update_query = 'UPDATE aigda SET register_date = %s, mood = %s, anxiety_level = %s, glucose = %s, g_level = %s WHERE id_glucose = %s'
    updated_values = set_register()
    updated_values = (updated_values[0], updated_values[1], updated_values[2], updated_values[3], updated_values[4], register_to_change)

    cursor.execute(update_query, updated_values)
    connect.commit()


def update(connect):
    """The update register function

    Args:
        connect (object): A connection object to execute Postgresql Queries
    """
    print("""Do you want to see all the registers or you already know what is the number of the register to update?""")
    option_selected = input("See[s] | I know [k]: ")
    option_selected.lower()

    with connect.cursor() as cursor:
        if option_selected == 's':
            cursor.execute('SELECT * FROM aigda')
            records = cursor.fetchall()

            for row in records:
                print(f'{row[0]} - {row[1]} - {row[2]} - {row[3]} - {row[4]} - {row[5]}')
            
            updating_process(connect, cursor)

        elif option_selected == 'k':
            updating_process(connect, cursor)

        else:
            print('Wrong Option')

    print('register updated')


def deleting_process(connect, cursor):
    """A function which deletes an entire row.

    Args:
        connect (object): The connection object to work in a Postgresql Database
        cursor (method): The method of connect objecto to execute queries
    """
    register_to_delete = int(input('Enter the number of the register to delete: '))
    delete_query = f'DELETE FROM aigda WHERE id_glucose = {register_to_delete}'

    cursor.execute(delete_query)
    connect.commit()


def delete(connect):
    """The delete register function

    Args:
        connect (object): A connection object to execute Postgresql Queries
    """
    print("""Do you want to see all the registers or you already know what is the number of the register to delete?""")
    option_selected = input("See[s] | I know [k]: ")
    option_selected.lower()

    with connect.cursor() as cursor:
        if option_selected == 's':
            cursor.execute('SELECT * FROM aigda')
            records = cursor.fetchall()

            for row in records:
                print(f'{row[0]} - {row[1]} - {row[2]} - {row[3]} - {row[4]} - {row[5]}')
            
            deleting_process(connect, cursor)

        elif option_selected == 'k':
            deleting_process(connect, cursor)

        else:
            print('Wrong Option')

    print('Register deleted')


def close_connection(connect):
    """This function ends the Postgresql connection

    Args:
        connect (object): An object which allows the connection with the Postgresql Database
    """
    connect.close()
    print('Connection ended')


def run(connect):
    """
    This is the main function which receives the connection object that allows us to enable the Postgresql database interaction
    """
    print("""What do you want to do?
        c) Create
        r) Read
        u) Update
        d) Delete""")
    user_selection = input("Select an option: ")
    user_selection = user_selection.lower()

    if user_selection == 'c':
        create(connect)
    elif user_selection == 'r':
        read(connect)
    elif user_selection == 'u':
        update(connect)
    elif user_selection == 'd':
        delete(connect)
    else:
        print('Wrong option general menu')

    
    print('Do you want to make another request?: ')
    another_request = input('Yes [y] | No [n]: ').lower()

    if another_request == 'y':
        clear()
        run(connect)
    elif another_request == 'n':
        clear()
        close_connection(connect)
        print('See you')
    else:
        clear()
        print('Wrong Value')
        close_connection(connect)
        print('See you')


if __name__ == '__main__':
    connect = start_connection()
    
    run(connect)