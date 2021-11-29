import json
import numpy as np
import pandas as pd
import requests
import seaborn as sns
from brasil_io import BrasilIO
import os

class COVID19:
    
    """
    Codigo utilizado para o donwload do dataset de casos sobre a covid-19 disponível no site Brasil IO.
    """
     
    _dias_da_semana = ['Segunda-Feira',
                            'Terça-Feira',
                            'Quarta-Feira',
                            'Quinta-Feira',
                            'Sexta-Feira',
                            'Sábado',
                            'Domingo']
    
    _raw_data_selected = ['place_type',
                          'state',
                          'city',
                          'date',
                          'day_of_week',
                          'epidemiological_week',
                          'new_confirmed',
                          'new_deaths']

    def __init__(self) -> None:
        
        self._dataset_slug = 'covid19'
        self._table_name = 'caso_full'
        self._key = 'f052cad482a37a956728c14796ce20bb25258f73'
        
        exist_file = os.path.isfile(f'{self._dataset_slug}_{self._table_name}.csv')
        exist_zip = os.path.isfile(f'{self._dataset_slug}_{self._table_name}.csv.gz')
         
        if not (exist_file or exist_zip):
            
            print('base de dados nao carregada')
            api = BrasilIO(self._key)
            response = api.download(self._dataset_slug, self._table_name)
            with open(f"{self._dataset_slug}_{self._table_name}.csv.gz", mode="wb") as fobj:
                fobj.write(response.read())
        
        if exist_file:
        
            self.database = pd.read_csv(f'{self._dataset_slug}_{self._table_name}.csv')
        
        else:
            
            self.database = pd.read_csv(f'{self._dataset_slug}_{self._table_name}.csv.gz')
        
        self._cria_dia_da_semana()
        print("Database Covid19 its ready!")
           
        
    def _get_database(self) -> pd.DataFrame:
         return self.database[self._raw_data_selected]
        
    def _get_city(self, UF: str = 'PE', city: str = 'Recife', dateInicial: str = '2021-01-24' , dateFinal: str = '2021-11-01' ) -> pd.DataFrame:
        
        self.UF = UF
        self.city = city
       
        dates = self.database['date'].between(dateInicial,dateFinal)
        
        this_state = self.database['state'] == self.UF
        only_cities = self.database['place_type'] == 'city'
        this_city = self.database['city'] == self.city
        
        df_this_city = self.database[dates & this_city & only_cities & this_state]
        
        return df_this_city
    
    def data_analysis(self, UF: str = "PE", city: str = "Recife", dateInicial: str = '2021-01-24' , dateFinal: str = '2021-11-01', modal_median: int = 14) -> pd.DataFrame:
        
        df = self._filter_data(UF, city, dataInicial, dateFinal, modal_median)
            
        # salvando dados 
        self._save(df)
        
        # plot dados
        self._plot_graph(df, dateInicial, dateFinal)
        
        return df
    
    def _filter_data(self, UF: str = "PE", city: str = "Recife", dateInicial: str = '2021-01-24' , dateFinal: str = '2021-11-01', modal_median: int = 14) -> pd.DataFrame:
        
        df_covid_city = self._get_city(UF, city, dateInicial, dateFinal) # recupera a cidade solicitada 
        
        # cria uma média modal para casos confirmados
        df1 = df_covid_city['new_confirmed'].rolling(window=modal_median).mean() 
        df_covid_city.assign(Mm_new_confirmed = df1) 
        df2 = df_covid_city['new_deaths'].rolling(window=modal_median).mean()
        df_covid_city.assign(Mm_new_deaths = df2) 
        
        # agrupando os dados por semana
        df = df_covid_city.fillna(10)
        df = df.groupby('epidemiological_week').sum()
        
        return df
        
        
        
    def _save(self, df: pd.DataFrame) -> None:
        nomeArquivo = f"filtered_data_covid19_{self.UF}_{self.city}"
        df.to_csv(nomeArquivo + ".csv")
        json = df.to_json(orient = 'split')
        
        with open(nomeArquivo + ".json", 'w') as arquivo:
            arquivo.write(json)
    
    def _plot_graph(self, df: pd.DataFrame, dateInicial: str = '2021-01-24' , dateFinal: str = '2021-11-01') -> None: 
        
        df = df.reset_index()
        fig , axis = plt.subplots(figsize = (7, 5))
        g = sns.barplot(x=df['epidemiological_week'], y=df['new_confirmed'], palette="rocket", ax=axis)
        axis.axhline(0, color="k", clip_on=False)
        axis.set_ylabel("cases confirmed")
        axis.set_xlabel("epidemiological week")
        axis.set_title(f"confirmed cases by covid 19 from {dateInicial} to {dateFinal}")
        g.savefig("Figure.png")
    
    def _cria_dia_da_semana(self) -> None:
        self.database['day_of_week'] = self.database['date'].apply(lambda x: pd.Timestamp(x)).apply(lambda x: x.day_name())
    
    def get_raw_data(self) -> pd.DataFrame:
        return self._get_database()
