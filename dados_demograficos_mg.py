import pandas as pd
import googlemaps
import time

# Sua chave da API do Google
API_KEY = 'SUA_API_AQUI'

# Inicializa o cliente da API do Google Maps
gmaps = googlemaps.Client(key=API_KEY)

# Função para obter informações de bairro, CEP, latitude e longitude
def get_location_details(address):
    try:
        # Geocoding API request
        geocode_result = gmaps.geocode(address)
        if geocode_result:
            location = geocode_result[0]
            lat = location['geometry']['location']['lat']
            lng = location['geometry']['location']['lng']
            components = location['address_components']
            bairro = ''
            cep = ''
            for component in components:
                if 'sublocality_level_1' in component['types']:
                    bairro = component['long_name']
                if 'postal_code' in component['types']:
                    cep = component['long_name']
            return bairro, cep, lat, lng
    except Exception as e:
        print(f"Erro ao obter detalhes para o endereço {address}: {e}")
    return None, None, None, None

# Carregar o arquivo CSV com município e rua
df = pd.read_csv(r'C:\Files\BASE LATITUDE LONGITUDE\MUNICIPIOS_LAT_LONG.csv', delimiter=';')

# Cria colunas para armazenar os novos dados
df['Bairro'] = ''
df['CEP'] = ''
df['Latitude'] = ''
df['Longitude'] = ''

# Itera sobre as linhas do DataFrame
for index, row in df.iterrows():
    municipio = row['Municipio']
    rua = row['Logradouro']
    address = f"{rua}, {municipio}, Minas Gerais, Brasil"
    bairro, cep, lat, lng = get_location_details(address)
    df.at[index, 'Bairro'] = bairro
    df.at[index, 'CEP'] = cep
    df.at[index, 'Latitude'] = lat
    df.at[index, 'Longitude'] = lng
    print(f"Recebendo {municipio}, {bairro}, {rua}, {cep}, {lat}, {lng}") 
    # Adiciona um tempo de espera para não exceder o limite da API
    time.sleep(0.1)
    
    # A cada 1000 linhas, salva o DataFrame atualizado em um arquivo CSV
    if index % 1000 == 0:
        df.to_csv(r'C:\Files\BASE LATITUDE LONGITUDE\enderecos_completos.csv', mode='a', header=False, index=False)
        print("Salvando arquivo intermediário")

print("Gerando Arquivo Final")
# Salva o DataFrame atualizado em um novo arquivo CSV
df.to_csv(r'C:\Files\BASE LATITUDE LONGITUDE\enderecos_completos.csv', index=False)
