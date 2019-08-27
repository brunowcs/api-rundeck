#!flask/bin/python
# -*- coding: utf-8 -*-
import requests, re, os
from flask import Flask, jsonify, abort, json, request, Response

app = Flask(__name__)

#### API para criar automaticamente opcoes para rundeck utilizando json ######

@app.route('/rundeck/api/v1.0/<torre>', methods=['GET'])


def get_options(torre):

    #Var parametros recebidos da url
    hostname = request.args.get("hostname")
    response = requests.get(request.args.get("url"))
    value = request.args.get("value")
    file_json = json.loads(response.text)

    #for no json carregado pela URL
    for i in file_json:

        #verificar se o host do json e igual host recebido pelo parametro da url
        if i['hostname'] == hostname:

           #trata o valor e realizar o dump para transforma em string
           json_query = i[value]
           json_query = json.dumps(json_query)
           json_query = re.split(r'\s', json_query)

            #se for um parametro apenas executa esse bloco montando o json
           if len(json_query) == 1:

                json_query = json.dumps(json_query)
                json_query = json_query.replace('"', '').replace('[', '').replace(',', '').replace(']', '').replace(
                    '\\', '')
                json_rundeck = ("{'%s':'%s'}" % (json_query,json_query ))
                break

           else:

                #se for 2 ou mais executa esse for montando o json
                for index, item in enumerate(json_query):

                   lista = []

                   #limpa caracteres da variavel
                   item = item.replace('"', '').replace('[', '').replace(',', '').replace(']', '')

                   #monta a variavel do json
                   var =("{'%s':'%s'}," % (item,item))

                   #em cada passagem do for adiciona a uma lista
                   lista.append(var)

                   #transforma em string
                   lista = json.dumps(lista)
                   json_rundeck = lista

                   #escreve o json e um arquivo local - nescessario por conta da versao flesk nao retorna lista
                   with open('data.'+hostname+'.json', 'a') as outfile:
                       json.dump(json_rundeck, outfile)
                       outfile.close()

                   #ler o json do arquivo local
                   arq = open('data.'+hostname+'.json', 'r')
                   texto = arq.read()

                   #transforma em string
                   json_query = json.dumps(texto)

                   #limpa string para montar o json corretamente
                   json_query = json_query.replace('"', '').replace('[', '').replace(']', '').replace('\\\\', '').replace('}\\\\\\{', ',').replace(',\\\\', '').replace('},{',',').replace('},','}')
                   print json_query
                   json_rundeck = json_query
                   arq.close()

        #remove o json criado local
        if os.path.exists("data." + hostname + ".json"):
            os.remove("data." + hostname + ".json")

    #retornar como json
    return Response(json_rundeck, mimetype='application/json')


@app.route('/rundeck/api/v1.0/get_hosts', methods=['GET'])

#pega todos hosts do json pelo ambiente
def get_hosts():

    #Var parametros recebidos da url
    environment = request.args.get("env")
    response = requests.get(request.args.get("url"))
    value = request.args.get("value")
    file_json = json.loads(response.text)

    for i in file_json:
        if i['environment'] == environment:
            # trata o valor e realizar o dump para transforma em string
            json_query = i[value]
            json_query = json.dumps(json_query)
            json_query = re.split(r'\s', json_query)

            for index, item in enumerate(json_query):
                lista = []

                # limpa caracteres da variavel
                item = item.replace('"', '').replace('[', '').replace(',', '').replace(']', '')

                # monta a variavel do json
                var = ("{'%s':'%s'}," % (item, item))

                # em cada passagem do for adiciona a uma lista
                lista.append(var)

                # transforma em string
                lista = json.dumps(lista)
                json_rundeck_hosts = lista

                # escreve o json e um arquivo local - nescessario por conta da versao flesk nao retorna lista
                with open('get.' + environment + '.json', 'a') as outfile:
                    json.dump(json_rundeck_hosts, outfile)
                    outfile.close()

                # ler o json do arquivo local
                arq = open('get.' + environment + '.json', 'r')
                texto = arq.read()

                # transforma em string
                json_query = json.dumps(texto)

                # limpa string para montar o json corretamente
                json_query = json_query.replace('"', '').replace('[', '').replace(']', '').replace('\\\\', '').replace(
                    '}\\\\\\{', ',').replace(',\\\\', '').replace('},{', ',').replace('},', '}')
                json_rundeck_hosts = json_query
                arq.close()

    #remove o json criado local
    if os.path.exists("get." + environment + ".json"):
        os.remove("get." + environment + ".json")


    return Response(json_rundeck_hosts, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=8080)
    app.run()
