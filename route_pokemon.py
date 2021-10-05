import pymysql.cursors;
from route_functions import server_insert_type, server_Evolve, server_add_pokeman_from_pokapi, \
    server_Get_trainers_of_pokemon, server_add_pokeman, server_Get_pokemon_by_type
from flask import Flask, request, Response
import urllib
from route_functions import  get_type_f,return_pokemans,get_trainer_f,delete_trainer_f,delelete_pokemans_by_id

import json

app = Flask(__name__)

@app.route('/posteman_id/<pokeman_id>', methods=["GET"])
def Get_trainers_of_pokemon(pokeman_id):
    return server_Get_trainers_of_pokemon(pokeman_id)

@app.route('/add_pokeman', methods=["POST"])
def add_pokeman():
    server_add_pokeman()

@app.route("/insert_type/<id>")
def insert_type(id):
    return server_insert_type(id)

@app.route("/add_pokeman_from_pokapi/<id>")
def add_pokeman_from_pokapi(id):
    return server_add_pokeman_from_pokapi(id)

@app.route('/Get_pokeman_by_type/<pokeman_type>', methods=["GET"])
def Get_pokemon_by_type(pokeman_type):
    return server_Get_pokemon_by_type(pokeman_type)

@app.route("/Evolve")
def Evolve():
    return server_Evolve()

@app.route("/getTrainerByPokemon/<id>")
def get_trainer(id):
    return Response(json.dumps(get_trainer_f(id)))


@app.route("/getPokemanByType/<type>")
def get_type(type):
    return Response(json.dumps(get_type_f(type)))


@app.route("/deletepokemons/<id>")
def delete_pokemons(id):
    return Response(json.dumps(delete_trainer_f))


@app.route("/deleteTrainerPokeman/<name>")
def delete_trainer(name):
    return Response(json.dumps(delelete_pokemans_by_id(id)))


@app.route("/getpokemons/<ownerName>")
def return_pokemons(ownerName):
    return Response(json.dumps(return_pokemans(ownerName)))
