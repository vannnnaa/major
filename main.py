import pandas as pd
import time
start = time.time()
counter = 1
def test(table):
    global counter


def dublicates(table):
    global counter
    for i in range(len(table)):
        active = table.iloc[i]['Кредит (актив)']
        index_active = table.iloc[i]['Новый индекс']
        if index_active not in GLOBAL_used:
            for j in range(i+1, len(table)):
                passive = table.iloc[j]['Вклад (пассив)']
                index_passive = table.iloc[j]['Новый индекс']
                if index_passive not in GLOBAL_used and active != 0:
                    if active + passive == 0:

                        GLOBAL_used.append(index_passive)
                        GLOBAL_used.append(index_active)
                        data.at[index_passive, '[ОТВЕТ] Номер группы'] = counter
                        data.at[index_active, '[ОТВЕТ] Номер группы'] = counter
                        counter += 1

                    break

    return table


def main(data, days, rate, i):
    extra_table = []
    for j in range(i + 1, len(data)):
        cur_index = data.index[j]
        cur_active, cur_passive, cur_date, cur_days, cur_rate, cur_ans, cur_x = data.iloc[j]
        if cur_rate - rate > 0.15:
            break
        if abs(cur_days - days) > 30 or cur_index in GLOBAL_used:
            continue
        extra_table.append([cur_index, cur_active, -cur_passive, cur_date, cur_days, cur_rate, cur_ans, cur_x])
    extra_table = [row] + extra_table
    table = pd.DataFrame(extra_table, columns=['Новый индекс'] + list(data.columns))
    return table


data = pd.read_csv('Банк_3мес_данные.csv', sep=';', encoding='cp1251')
data['Вклад (пассив)'] = data['Вклад (пассив)'].str.replace(',', '.', regex=False).astype(float)
data['Дата погашения'] = pd.to_datetime(data['Дата погашения'], format='%d.%m.%Y')


k = 1
data.sort_values(by=['Ставка, %', 'Дата погашения'], ascending=[True, True], inplace=True) #сортировка


left_active = 0
left_passive = 0
GLOBAL_used = []
RWA = 0

for i in range(20):
    index = data.index[i]
    active, passive, date, days, rate, ans, x  = data.iloc[i]
    passive = -passive
    row = [index, active, passive, date, days, rate, ans, x]
    table = main(data, days, rate, i)



print(GLOBAL_used)
#RWA += (left_active + left_passive) * 0.1 + abs(left_active - left_passive) * 0.4

end = time.time()

print(f"Время выполнения: {end - start:.4f} секунд")

print(data['[ОТВЕТ] Номер группы'].head(20))




data.to_csv('имя_файла2.csv', index=True, encoding='cp1251')