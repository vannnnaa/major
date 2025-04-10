import pandas as pd


def quick_bag(active, extra_table):
    pass
def main(data, active_or_passive, index, active, passive, date, rate):
    if active_or_passive == 'active':
        extra_list = []
        for stroka in data.itertuples(index=False):
            next_active, next_passive, next_date, next_rate = stroka._0, stroka._1, stroka._2, stroka._4
            if abs(next_rate - rate) > 0.15 or abs((next_date - date)) > pd.Timedelta(days=30):
                break
            if next_passive > 0:
                extra_list.append(stroka)
        if len(extra_list) != 0:
            extra_table = pd.DataFrame(extra_list)
            extra_table.sort_values(by=extra_table.columns[1], ascending=[False], inplace=True)
            # for passive_row in extra_table.itertuples(index=False):
    else:
        extra_list = []
        for stroka in data.itertuples(index=False):
            next_active, next_passive, next_date, next_rate = stroka._0, stroka._1, stroka._2, stroka._4
            if abs(next_rate - rate) > 0.15 or abs((next_date - date)) > pd.Timedelta(days=30):
                break
            if next_active > 0:
                extra_list.append(stroka)
        if len(extra_list) != 0:
            extra_table = pd.DataFrame(extra_list)
            extra_table.sort_values(by=extra_table.columns[0], ascending=[False], inplace=True)
            # for passive_row in extra_table.itertuples(index=False):

data = pd.read_csv('Банк_3мес_данные.csv', sep=';', encoding='cp1251')
data['Вклад (пассив)'] = data['Вклад (пассив)'].str.replace(',', '.', regex=False).astype(float)
data['Дата погашения'] = pd.to_datetime(data['Дата погашения'], format='%d.%m.%Y')


data.info()
data.sort_values(by=['Ставка, %', 'Дата погашения'], ascending=[True, True], inplace=True) #сортировка
left_active = 0
left_passive = 0
used = set()
for row in data.itertuples(index=True):
    index, active, passive, date, rate = row.Index, row._1, row._2,row._3, row._5

    if active > 0:
        main(data, 'active', index, active, passive, date, rate)



    else:
        main(data, 'passive', index, active, passive, date, rate)












#data.to_csv('имя_файла.csv', index=False, encoding='cp1251')