import pymysql.cursors
import json
from config import connect, commit


def load_data(filename: str):
    with open(filename) as f_in:
        try:
            cur = connect()
            cur1 = connect()
            cur2 = connect()
            cur3 = connect()
            a = json.load(f_in)
            arrayNames = []
            for element in a:
                sql = f"INSERT INTO pokeman (id,name,height,weight) VALUES ({element['id']},'{element['name']}',{element['height']},{element['weight']}) "
                cur.execute(sql)
                for i in element['ownedBy']:
                    if i['name'] not in arrayNames:
                        sql1 = f"INSERT INTO owners  (name,town) VALUES ('{i['name']}','{i['town']}') "
                        cur1.execute(sql1)
                        arrayNames.append(i['name'])
                    sql2 = f"INSERT INTO owned_by(pokeman_id,owner_name) VALUES ({element['id']},'{i['name']}') "
                    cur2.execute(sql2)
                sql3 = f"INSERT INTO types(pokeman_id,name) VALUES ({element['id']},'{element['type']}') "
                cur3.execute(sql3)
        except Exception as e:
            print("error", e)
        commit()


def find_by_type(new_type):
    try:
        cur = connect()
        cur.execute(f"select p.name from pokeman p,types t where t.name ='{new_type}' and t.pokeman_id=p.id")
        output = cur.fetchall()
        temp = []
        for i in output:
            temp.append(i)
            print(i[0])
        return temp
    except Exception as e:
        print("error", e)
    commit()


def find_roster(trainer_name):
    try:
        cur = connect()
        cur.execute(
            f"select p.name from pokeman p, owned_by o where owner_name='{trainer_name}' and p.id=o.pokeman_id  ")
        output = cur.fetchall()
        temp = []
        for i in output:
            print(i[0])
            temp.append(i)
        return temp
    except Exception as e:
        print("error", e)
    commit()


def heaviest_pokemon():
    try:
        cursor = connect()
        query = "SELECT name FROM pokeman WHERE weight = (SELECT MAX(weight) AS weight FROM pokeman);"
        cursor.execute(query)
        result = cursor.fetchall()
    except Exception as e:
        print("error", e)
    commit()
    return result


def find_owners(pokemon_name):
    arr_owners = []
    try:
        cursor = connect()
        query = "SELECT o.name FROM owners o JOIN owned_by o_by ON o.name = o_by.owner_name JOIN pokeman p ON p.id = " \
                "o_by.pokeman_id AND p.name = 'bulbasaur';; "
        cursor.execute(query)
        result = cursor.fetchall()
        for i in result:
            arr_owners.append(i)
    except Exception as e:
        print("error", e)
    commit()
    return arr_owners


def finds_most_owned():
    try:
        cursor = connect()
        query = "SELECT query1.* FROM(SELECT pokeman.name,COUNT(*) AS counter FROM owned_by join pokeman on " \
                "owned_by.pokeman_id=pokeman.id join owners on owned_by.owner_name=owners.name  GROUP BY pokeman_id) " \
                "query1,(SELECT MAX(query2.counter)AS highest FROM(SELECT pokeman.name,COUNT(*) AS counter FROM " \
                "owned_by " \
                "join pokeman on owned_by.pokeman_id=pokeman.id join owners on owned_by.owner_name=owners.name  GROUP " \
                "BY " \
                "pokeman_id)query2)query3 WHERE query1.counter=query3.highest; "
        cursor.execute(query)
        result = cursor.fetchall()
    except Exception as e:
        print("error", e)
    commit()
    return result
