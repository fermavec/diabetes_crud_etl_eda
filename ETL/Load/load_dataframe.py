import psycopg2
import pandas as pd

DROP_TABLE_AIGDA = "DROP TABLE IF EXISTS aigda"
AIGDA_TABLE  = "CREATE TABLE aigda(id_glucose SERIAL, register_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, mood CHARACTER VARYING(10), anxiety_level INT, glucose INT NOT NULL, g_level CHARACTER VARYING NOT NULL)"


if __name__ == "__main__":
    df = pd.read_csv('../Transform/diabetes_transformed.csv')

    try:
        connect = psycopg2.connect(f"dbname='aida' user='' password='' host='localhost'")
        print('Succesfully Connected')

        with connect.cursor() as cursor:
            cursor.execute(DROP_TABLE_AIGDA)
            print('AIGDA dropped')

            cursor.execute(AIGDA_TABLE)
            print('Database AIGDA created')

            insert_query = 'INSERT INTO aigda(register_date, mood, anxiety_level, glucose, g_level) VALUES(%s, %s, %s, %s, %s)'
            for row in df.itertuples():
                date = row.register_dt
                mood = row.mood
                al = row.anxiety_level
                glucose = row.glucose
                g_level = row.g_level

                values_insert_query = (date, mood, al, glucose, g_level)
                cursor.execute(insert_query, values_insert_query)
                connect.commit()
                print('Values inserted')

    except Exception as e:
        print(e)
    finally:
        connect.close()
        print('Connection ended')