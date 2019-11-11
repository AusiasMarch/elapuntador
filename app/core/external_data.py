"""
Data from WHO:
    - https://www.who.int/childgrowth/standards/height_for_age/en/
    - https://www.who.int/childgrowth/standards/weight_for_age/en/
    - ...

"""
import pandas as pd


import crud
from models.altura_who import AlturaWho
from models.peso_who import PesoWho
from db.session import db_session


def download_who_data():
    altura_13weeks_girls = pd.read_csv('https://www.who.int/childgrowth/standards/tab_lhfa_girls_p_0_13.txt', sep='\t')
    altura_13weeks_girls['Days'] = altura_13weeks_girls.Week * 7
    altura_2years_girls = pd.read_csv('https://www.who.int/childgrowth/standards/tab_lhfa_girls_p_0_2.txt', sep='\t')
    altura_2years_girls['Days'] = altura_2years_girls.Month * 30.4375
    altura_5years_girls = pd.read_csv('https://www.who.int/childgrowth/standards/tab_lhfa_girls_p_2_5.txt', sep='\t')
    altura_5years_girls['Days'] = altura_5years_girls.Month * 30.4375
    altura_girls = pd.concat([altura_13weeks_girls, altura_2years_girls, altura_5years_girls], sort=True)
    altura_girls = altura_girls.drop(columns=['Month', 'Week'])

    for i_row, row in altura_girls.drop_duplicates(subset='Days', keep='first').sort_values('Days').iterrows():
        altura_in = AlturaWho(
            day = row.Days,
            L = row.L,
            M = row.M,
            S = row.S,
            SD = row.SD,
            P01 = row.P01,
            P1 = row.P1,
            P3 = row.P3,
            P5 = row.P5,
            P10 = row.P10,
            P15 = row.P15,
            P25 = row.P25,
            P50 = row.P50,
            P75 = row.P75,
            P85 = row.P85,
            P90 = row.P90,
            P95 = row.P95,
            P97 = row.P97,
            P99 = row.P99,
            P999 = row.P999,
        )
        altura_who = crud.altura_who.create_girls(db_session, altura_in=altura_in)
    

    altura_13weeks_boys = pd.read_csv('https://www.who.int/childgrowth/standards/tab_lhfa_boys_p_0_13.txt', sep='\t')
    altura_13weeks_boys['Days'] = altura_13weeks_boys.Week * 7
    altura_2years_boys = pd.read_csv('https://www.who.int/childgrowth/standards/tab_lhfa_boys_p_0_2.txt', sep='\t')
    altura_2years_boys['Days'] = altura_2years_boys.Month * 30.4375
    altura_5years_boys = pd.read_csv('https://www.who.int/childgrowth/standards/tab_lhfa_boys_p_2_5.txt', sep='\t')
    altura_5years_boys['Days'] = altura_5years_boys.Month * 30.4375
    altura_boys = pd.concat([altura_13weeks_boys, altura_2years_boys, altura_5years_boys], sort=True)

    for i_row, row in altura_boys.drop_duplicates(subset='Days', keep='first').sort_values('Days').iterrows():
        altura_in = AlturaWho(
            day = row.Days,
            L = row.L,
            M = row.M,
            S = row.S,
            SD = row.SD,
            P01 = row.P01,
            P1 = row.P1,
            P3 = row.P3,
            P5 = row.P5,
            P10 = row.P10,
            P15 = row.P15,
            P25 = row.P25,
            P50 = row.P50,
            P75 = row.P75,
            P85 = row.P85,
            P90 = row.P90,
            P95 = row.P95,
            P97 = row.P97,
            P99 = row.P99,
            P999 = row.P999,
        )
        altura_who = crud.altura_who.create_boys(db_session, altura_in=altura_in)

    peso_13weeks_girls = pd.read_csv(
        'https://www.who.int/childgrowth/standards/tab_wfa_girls_p_0_13.txt', sep='\t')
    peso_13weeks_girls['Days'] = peso_13weeks_girls.Week * 7
    peso_5years_girls = pd.read_csv(
        'https://www.who.int/childgrowth/standards/tab_wfa_girls_p_0_5.txt', sep='\t')
    peso_5years_girls['Days'] = peso_5years_girls.Month * 30.4375
    peso_girls = pd.concat(
        [peso_13weeks_girls, peso_5years_girls], sort=True)
    peso_girls = peso_girls.drop(columns=['Month', 'Week'])

    for i_row, row in peso_girls.drop_duplicates(subset='Days',
                                                   keep='first').sort_values(
            'Days').iterrows():
        peso_in = PesoWho(
            day=row.Days,
            L=row.L,
            M=row.M,
            S=row.S,
            P01=row.P01,
            P1=row.P1,
            P3=row.P3,
            P5=row.P5,
            P10=row.P10,
            P15=row.P15,
            P25=row.P25,
            P50=row.P50,
            P75=row.P75,
            P85=row.P85,
            P90=row.P90,
            P95=row.P95,
            P97=row.P97,
            P99=row.P99,
            P999=row.P999,
        )
        peso_who = crud.peso_who.create_girls(db_session, peso_in=peso_in)

    peso_13weeks_boys = pd.read_csv(
        'https://www.who.int/childgrowth/standards/tab_wfa_boys_p_0_13.txt', sep='\t')
    peso_13weeks_boys['Days'] = peso_13weeks_boys.Week * 7
    peso_5years_boys = pd.read_csv(
        'https://www.who.int/childgrowth/standards/tab_wfa_boys_p_0_5.txt', sep='\t')
    peso_5years_boys['Days'] = peso_5years_boys.Month * 30.4375
    peso_boys = pd.concat(
        [peso_13weeks_boys, peso_5years_boys], sort=True)

    for i_row, row in peso_boys.drop_duplicates(subset='Days',
                                                  keep='first').sort_values(
            'Days').iterrows():
        peso_in = PesoWho(
            day=row.Days,
            L=row.L,
            M=row.M,
            S=row.S,
            P01=row.P01,
            P1=row.P1,
            P3=row.P3,
            P5=row.P5,
            P10=row.P10,
            P15=row.P15,
            P25=row.P25,
            P50=row.P50,
            P75=row.P75,
            P85=row.P85,
            P90=row.P90,
            P95=row.P95,
            P97=row.P97,
            P99=row.P99,
            P999=row.P999,
        )
        peso_who = crud.peso_who.create_boys(db_session, peso_in=peso_in)
