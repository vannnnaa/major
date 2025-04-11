import pandas as pd


def quick_bag(index, target, extra_table):
    extra_table = pd.DataFrame(extra_table)
    extra_table.sort_values(by=extra_table.columns[1], ascending=[False], inplace=True)

    current_sum = 0
    used = [index]
    best_diff = 10**20

    for row in extra_table.itertuples(index=False):
        if abs((current_sum + row[2]) - target) < best_diff:
            used.append(row[0])
            #print(used)
            current_sum += row[2]
            best_diff = abs(current_sum - target)

        if best_diff == 0:
            break
    if target < (target - best_diff) * 1.4:
        return used, best_diff
    return [index], target


def main(data, active_or_passive, index, active, passive,  date, rate):
    extra_list = []
    for stroka in data.itertuples(index=True):
        next_index, next_active, next_passive, next_date, next_rate = stroka.Index, stroka._1, stroka._2, stroka._3, stroka._5

        if abs(next_rate - rate) > 0.15:
            break
        if abs((next_date - date)) > pd.Timedelta(days=30) or next_index in GLOBAL_used:
            continue
        if active_or_passive == 'active':
            if next_passive > 0:
                extra_list.append(stroka)
        else:
            if next_active > 0 :
                extra_list.append(stroka)
    if len(extra_list) == 0:
        return [index], active + passive
    else:
        if active_or_passive == 'active':
            return quick_bag(index, active, extra_table=extra_list)
        else:
            return quick_bag(index, passive, extra_table=extra_list)



data = pd.read_csv('Банк_3мес_данные.csv', sep=';', encoding='cp1251')
data['Вклад (пассив)'] = data['Вклад (пассив)'].str.replace(',', '.', regex=False).astype(float)
data['Дата погашения'] = pd.to_datetime(data['Дата погашения'], format='%d.%m.%Y')


#data.info()
data.sort_values(by=['Ставка, %', 'Дата погашения'], ascending=[True, True], inplace=True) #сортировка

left_active = 0
left_passive = 0
GLOBAL_used = set()
RWA = 0
for row in data.itertuples(index=True):

    index, active, passive, date, rate = row.Index, row._1, row._2,row._3, row._5
    if index not in GLOBAL_used:
        if active > 0:
            current_used, rwa = main(data, 'active', index, active, passive, date, rate)
            if len(current_used) == 1:
                left_active += rwa
            else:
                RWA += rwa




        else:
            current_used, rwa = main(data, 'passive', index, active, passive, date, rate)
            if len(current_used) == 1:
                left_passive += rwa
            else:
                RWA += rwa
        GLOBAL_used.update(current_used)


RWA += (left_active + left_passive) * 0.1 + abs(left_active - left_passive) * 0.4

print(RWA)






#data.to_csv('имя_файла111.csv', index=True, encoding='cp1251')