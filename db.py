import pandas as pd
import sqlite3
import datetime as dt

con = sqlite3.connect('/db/been_bot_db')
cursor = con.cursor()


def select(sql):
    return pd.read_sql(sql, con)


def init_db_regions():
    regions = pd.read_csv('regions.csv')
    regions.to_sql('regions', con, index=False)


def init_db_users():
    users = pd.read_csv('users.csv', sep=';')
    users.to_sql('users', con, index=False)


def log_user(callback, status):
    inputs = {'user_id': callback.from_user.id,
              'username': callback.from_user.username,
              'first_name': callback.from_user.first_name,
              'last_name': callback.from_user.last_name,
              'dt': dt.datetime.now(),
              'status': status}
    placeholders = ", ".join("?" * len(inputs.keys()))
    values = [tuple(inputs.values())]

    sql = (f"insert into users (user_id, username, first_name, last_name, dt, status) "
           f"values ({placeholders})")

    cursor.executemany(sql, values)
    con.commit()


def create_table(user_id):
    userid = str(user_id)
    sql = (f'drop table if exists {"id_" + userid}; '
           f'create table {"id_" + userid} ('
           f'id integer primary key, '
           f'concat text'
           f');')

    cursor.executescript(sql)
    con.commit()


def insert_question(user_id, question):
    userid = str(user_id)
    inputs = {'concat': question}
    question = [tuple(inputs.values())]
    sql = (f'insert into {"id_" + userid} (concat)'
           f'values (?)')

    cursor.executemany(sql, question)
    con.commit()


def delete_question(user_id):
    userid = str(user_id)
    sql = (f'delete '
           f'from {"id_" + userid} '
           f'where id = (select max(id) from {"id_" + userid})')

    cursor.execute(sql)
    con.commit()


def insert_answers(user_id, question, answers):
    userid = str(user_id)
    for i in range(len(answers)):
        inputs = {'concat': question + str(answers[i])}
        concat = [tuple(inputs.values())]
        sql = (f'insert into {"id_" + userid} (concat)'
               f'values (?)')

        cursor.executemany(sql, concat)
    con.commit()


def last_question(user_id):
    userid = str(user_id)
    sql = (f'select concat '
           f'from {"id_" + userid} '
           f'order by id desc '
           f'limit 1')

    df = pd.read_sql(sql, con)
    return df['concat'][0]


def finish(user_id):
    userid = str(user_id)
    sql = (f'select district, region_name, region_area, district_area, russia_area, region_id '
           f'from {"id_" + userid} as i '
           f'inner join regions as r on i.concat = r.concat_eng ')

    df = pd.read_sql(sql, con)
    return df


def send_stats(user_id):
    df = finish(user_id)

    total_russia = df['region_area'].sum() / df['russia_area'].max()
    region_cnt = df['region_name'].nunique()
    district_cnt = df['district'].nunique()

    message = (f'Here are your stats: \n'
               f'\n'
               f'been to % of Russia:     {total_russia :.1%} \n'
               f'been to # of regions:     {region_cnt} / 83 \n'
               f'been to # of districts:    {district_cnt} / 8 \n')

    return message


def check_db_exists():
    sql = """select * from sqlite_schema"""
    trial = select(sql)
    if ('regions' or 'users') not in trial['name'].values:
        init_db_regions()
        init_db_users()
    elif 'regions' not in trial['name'].values:
        init_db_regions()
    elif 'users' not in trial['name'].values:
        init_db_users()
    else:
        return
