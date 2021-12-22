import weather_app

try:
    coordenadas = weather_app.pegarCoordenadas()
    weather_app.mostarPrevisao(coordenadas['lat'],coordenadas['long'])

    continuar = "s"
    while(continuar == "s"):
        continuar = input("\nDeseja consultar a previsão de outro local? (s ou n): ").lower()
        if(continuar != "s"):
            break
        local = input("Digite a cidade e o estado: ")
        try:
            coordenadas = weather_app.pesquisarLocal(local)
            weather_app.mostarPrevisao(coordenadas['lat'],coordenadas['long'])
        except:
            print("Não foi possivel obter a previsão para este local.")
except:
    print("Erro ao processar a solicitação.")

