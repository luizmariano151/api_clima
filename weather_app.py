import requests
import json
from datetime import date
import urllib.parse
import pprint

accuweatherAPIKey = "qnnS7OAUEDRLsWAdKNC3HJG56W0RbS9f"
mapboxToken = "pk.eyJ1IjoibHVpem1hcmlhbm8iLCJhIjoiY2t0OG05cWxyMTNibjJucndueWtsajd5ayJ9.45AN4RR-bDxDMLGaMGrA3g"
dias_semanas = ["Domingo","Segunda-feira", "Terça-feira", "Quarta-feira","Quinta-feira","Sexta-feira","Sábado"]

def pegarCoordenadas():
    r = requests.get("http://www.geoplugin.net/json.gp")
    if(r.status_code != 200):
        print("Não foi possível obter a localização.")
        return None
    else:
        try:
            localizacao = json.loads(r.text)
            coordenadas = {}
            coordenadas['lat'] = localizacao['geoplugin_latitude']
            coordenadas['long']= localizacao['geoplugin_longitude']
            return coordenadas
        except:
            return None
            
def pegarCodigoLocal(lat, long):
    LocationAPIUrl = "http://dataservice.accuweather.com/locations/v1/"\
    +"cities/geoposition/search?apikey=" + accuweatherAPIKey\
    +"&q="+ lat +"%2C"+ long +"&language=pt-br"
    r = requests.get(LocationAPIUrl)
    if(r.status_code != 200):
        print("Não foi possível obter código do local")
        return None
    else:
        try:
            locationResponse = json.loads(r.text)
            infoLocal = {}
            infoLocal['nomeLocal'] = locationResponse["LocalizedName"] + ", "\
                        + locationResponse["AdministrativeArea"]["LocalizedName"] + ". "\
                        + locationResponse["Country"]["LocalizedName"]
            infoLocal['codigoLocal'] = locationResponse["Key"]
            return infoLocal
        except:
            return None

def pegarTempoAgora(codigoLocal, nomeLocal):
    CurrentConditionAPIUrl = "http://dataservice.accuweather.com/currentconditions/v1/"\
                            +codigoLocal+"?apikey="+accuweatherAPIKey+"&language=pt-br"
    r = requests.get(CurrentConditionAPIUrl)
    if(r.status_code != 200):
        print("Não foi possível obter clima atual")
        return None
    else:
        try:
            CurrentConditionsResponse = json.loads(r.text)
            infoClima = {}
            infoClima['textoClima'] = CurrentConditionsResponse[0]["WeatherText"]
            infoClima['temperatura'] = CurrentConditionsResponse[0]["Temperature"]["Metric"]["Value"]
            infoClima['nomeLocal'] = nomeLocal
            return infoClima
        except:
            return None
        
def pegarPrevisao5Dias(codigoLocal):
    DailyAPIUrl = "http://dataservice.accuweather.com/forecasts/v1/daily/5day/"\
                +codigoLocal+"?apikey="+accuweatherAPIKey+"&language=pt-br&metric=true"
    r = requests.get(DailyAPIUrl)
    if(r.status_code != 200):
        print("Não foi possível obter clima dos 5 dias")
        return None
    else:
        try:
            DailyResponseResponse = json.loads(r.text)
            infoClima5Dias = []
            for dia in DailyResponseResponse['DailyForecasts']:
                climaDia = {}
                climaDia['max'] = dia['Temperature']['Maximum']['Value']
                climaDia['min'] = dia['Temperature']['Minimum']['Value']
                climaDia['clima'] = dia['Day']['IconPhrase']
                diaSemana = int(date.fromtimestamp(dia['EpochDate']).strftime("%w"))
                climaDia['dia'] = dias_semanas[diaSemana]
                infoClima5Dias.append(climaDia)
            return infoClima5Dias
        except:
            return None

def mostarPrevisao(lat, long):
    try:
        local = pegarCodigoLocal(lat, long)
        climaAtual = pegarTempoAgora(local['codigoLocal'], local['nomeLocal'])
        print("Clima atual em: "+climaAtual['nomeLocal'])
        print(climaAtual['textoClima'])
        print("Temperatura: "+ str(climaAtual['temperatura'])+ "\xb0"+"C")
    except:
        print("Errro ao obter o clima atual")
        
    opcao = input("\nDeseja ver a previsão para os próximos dias? (s ou n): ").lower()

    if (opcao == "s"):
        print("\nClima para hoje e para os próximos dias: \n")

        try:
            previsao5Dias = pegarPrevisao5Dias(local['codigoLocal'])
            for dia in previsao5Dias:
                print(dia['dia'])
                print("Mínima: "+ str(dia['min']) + "\xb0"+"C")
                print("Máxima: "+ str(dia['max']) + "\xb0"+"C")
                print("Clima: " + dia['clima'])
                print('----------------------------')
        except:
            print("Erro ao obter a previsão para os próximos dias")

def pesquisarLocal(local):
    
    #usar símbolo, espaço ou acentuação
    _local = urllib.parse.quote(local)
    mapboxGeocodeUrl = "https://api.mapbox.com/geocoding/v5/mapbox.places/"\
                       +_local+".json?access_token="+mapboxToken

    r = requests.get(mapboxGeocodeUrl)
    if(r.status_code != 200):
        print("Não foi possível obter clima dos 5 dias.")
        return None
    else:
        try:
           MapboxResponse = json.loads(r.text)
           coordenadas = {}
           coordenadas['long'] = str(MapboxResponse['features'][0]['geometry']['coordinates'][0])
           coordenadas['lat'] = str(MapboxResponse['features'][0]['geometry']['coordinates'][1])
           return coordenadas
        except:
            print("Erro na pesquisa de local.")


































            
