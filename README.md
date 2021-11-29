# Acompanhamento_epidemiologico_covid_19

Criação de uma API para filtrar dados providos da base de dados COVID-19 disponível em: https://github.com/turicas/covid19-br/blob/master/api.md#caso_full

Programa gerado de modo avaliativo para o modulo 2 do curso Santander Coders disponibilizado pela lets code

### Modos de uso

- Para iniciar, execute o arquivo api_covid19.py, ele demora um pouco para carregar pois ela e grande. 

### Uso da API 

🔍 /raw_data: pega a base de dados padrão bruta

🔍  /raw_data/<column_id>/: Filtrar a base de dados pelas colunas 
    
🔍 /covid19_filter_data/<UF_id>/<city_id>: Passar o UF do estado e o nome da cidade

