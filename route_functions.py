import pymysql.cursors
import json
import urllib
from flask import request,Request, Response
from config import connect,commit

def server_insert_type(id):
    global jsonData
    url = "https://pokeapi.co/api/v2/pokemon/" + str(id)
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    operUrl = urllib.request.urlopen(req).read()
    if operUrl != None:
        data = operUrl
        jsonData = json.loads(data)
        try:
            cur = connect()
            cur1 = connect()
            for i in jsonData['types']:
                cur1.execute(f'select count(pokeman_id) from types where pokeman_id = {jsonData["id"]} and name="{i["type"]["name"]}" ')
                output = cur1.fetchall()
                a = output[0]
                if 0 != int(a[0]):
                    pass
                else:
                    sql = f"INSERT INTO types (pokeman_id,name) VALUES ({jsonData['id']},'{i['type']['name']}') "
                    cur.execute(sql)
        except Exception as e:
            print("error", e)
        commit()
    else:
        print("Error receiving data")
    return "the types was inserted succefully"

def server_Evolve():
    global jsonData
    req_from_json = request.get_json()
    url = "https://pokeapi.co/api/v2/pokemon/" + str(req_from_json["id"])
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    operUrl = urllib.request.urlopen(req).read()
    if operUrl != None:
        data = operUrl
        jsonData = json.loads(data)
    url1 = jsonData['species']['url']
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url1, headers=headers)
    operUrl = urllib.request.urlopen(req).read()
    if operUrl != None:
        data = operUrl
        jsonData1 = json.loads(data)
    url2 = jsonData1['evolution_chain']['url']
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url2, headers=headers)
    operUrl = urllib.request.urlopen(req).read()
    if operUrl != None:
        data = operUrl
        jsonData2 = json.loads(data)
    if len(jsonData2['chain']['evolves_to']) == 0:
        return "can't conitiue any more"
    else:
        try:
            cur = connect()
            cur1 = connect()
            cur2 = connect()
            cur3 = connect()
            cur1.execute(
                f'select count(pokeman_id) from owned_by where pokeman_id = {req_from_json["id"]} and owner_name= "{req_from_json["name"]}"')
            output = cur1.fetchall()
            a = output[0]
            if 0 == int(a[0]):
                return "error, there is no such pokeman and trainer"
            else:
                cur.execute(
                    f'UPDATE owned_by SET pokeman_id = {jsonData2["id"]} WHERE  owner_name="{req_from_json["name"]}" and pokeman_id = {req_from_json["id"]}')
                cur2.execute(f'select count(id) from pokeman where id = {jsonData2["id"]}')
                output = cur2.fetchall()
                b = output[0]
                if 0 == int(b[0]):
                    cur3.execute(
                        f"INSERT INTO Pokeman (id,name,height,weight) VALUES ({jsonData2['id']},'{jsonData2['name']}',{jsonData2['height']},{jsonData2['weight']}) ")
        except Exception as e:
            print("error", e)
        commit()
        return "the pokeman evolve a level"

def server_add_pokeman_from_pokapi(id):
    global jsonData
    url = "https://pokeapi.co/api/v2/pokemon/"+str(id)
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    operUrl = urllib.request.urlopen(req).read()
    if operUrl != None:
        data = operUrl
        jsonData = json.loads(data)
        try:
            cur = connect()
            cur1=connect()
            cur1.execute(f'select count(id) from pokeman where id = {jsonData["id"]} ')
            output = cur1.fetchall()
            a = output[0]
            if 0 != int(a[0]):
                pass
            else:
                sql = f"INSERT INTO pokeman (id,name,height,weight) VALUES ({jsonData['id']},'{jsonData['name']}',{jsonData['height']},{jsonData['weight']}) "
                cur.execute(sql)
        except Exception as e:
            print("error", e)
        commit()
    else:
        print("Error receiving data")
    return "the pokemaon inserted into the local data from the api data"

def server_Get_trainers_of_pokemon(pokeman_id):
    try:
        cur = connect()
        cur.execute(f"select owned_by.owner_name from owned_by where owned_by.pokeman_id={pokeman_id}  ")
        output = cur.fetchall()
        temp=[]
        for i in output:
            temp.append(json.dumps(i))
        return Response(temp)
    except Exception as e:
        return Response(json.dumps("error", e))
    connection.commit()

def server_add_pokeman():
    try:
        cur = connect()
        cur1 = connect()
        cur2 = connect()
        new_pokeman = request.get_json()
        cur1.execute(f"Select COUNT(id) from pokeman where id={new_pokeman['id']}")
        output = cur1.fetchall()
        a=output[0]
        if new_pokeman['id']== int(a[0]):
            return Response("The ID already exists")
        sql=(f"INSERT INTO pokeman (id,name,type,height,weight) VALUES ({new_pokeman['id']},'{new_pokeman['name']}','{new_pokeman['type']}',{new_pokeman['height']},{new_pokeman['weight']}) ")
        cur.execute(sql)
        sql2 = f"INSERT INTO types(id,name) VALUES ({new_pokeman['id']},'{new_pokeman['type']}') "
        cur2.execute(sql2)
    except Exception as e:
        print("error", e)
    commit()
    return Response("ok")

def server_Get_pokemon_by_type(pokeman_type):
    try:
        cur = connect()
        cur.execute(f"select p.name from pokeman p,types t where t.name ='{pokeman_type}' and t.id=p.id")
        output = cur.fetchall()
        temp=[]
        for i in output:
            temp.append(json.dumps(i))
        return Response(temp)
    except Exception as e:
        print("error", e)
    commit()
    return Response("ok")



def get_type_f(type):
    a = []
    try:
        cur1 = connect()
        cur2 = connect()
        cur1.execute(f"SELECT id from pokeman JOIN types ON types.pokeman_id=pokeman.id where types.name='{type}' ;")
        output1 = cur1.fetchall()
        for i in output1:
            print(i[0])
            cur2.execute(f"select * FROM pokeman where id={i[0]}")
            output = cur2.fetchall()
            a.append(output)
    except Exception as e:
        print("error", e)
    commit()
    return a


def get_trainer_f(id):
    owners=[]
    output=""
    try:
        cur1 = connect()
        cur1.execute(f"select owner_name from owned_by where pokeman_id={id};")
        output = cur1.fetchall()
        for i in output:
            owners.append(i)
    except Exception as e:
        print("error", e)
    commit()
    return owners


def delete_trainer_f(name):
    try:
        cur1 = connect()
        cur1.execute(f"Delete FROM owned_by WHERE owned_by.owner_name='{name}';")
        output = cur1.fetchall()
    except Exception as e:
        print("error", e)
    commit()
    return output


def return_pokemans(ownerName):
    pokemons=[]
    try:
        mycursor = connect()
        query = f"SELECT p.name FROM pokeman p JOIN owned_by o_by ON p.id = o_by.pokeman_id AND o_by.owner_name = '{ownerName}'; "
        mycursor.execute(query)
        result = mycursor.fetchall()
        for i in result:
            pokemons.append(i)
    except Exception as e:
        print("error", e)
    commit()
    return pokemons


def delelete_pokemans_by_id(id):
    try:
        curs1 = connect()
        curs2 = connect()
        curs3 = connect()
        query1 = f"DELETE FROM pokeman WHERE id = {id}; "
        query2 = f"Delete FROM owned_by WHERE owned_by.pokeman_id={id};"
        query3 = f"Delete from owners where owners.name IN (select owner_name from owned_by where pokeman_id ={id});"
        curs1.execute(query1)
        curs2.execute(query2)
        curs3.execute(query3)
    except Exception as e:
        print("error", e)
        return "error in deleation"
    commit()
    return "managed to delete"

