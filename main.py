import pandas as pd
import time
import numpy as np


start = time.time()
counter = 1


def one_element_update(row):
    global counter
    GLOBAL_used.update([int(row[0])])
    answer_df.loc[row[0], '[ОТВЕТ] Номер группы'] = counter
    counter += 1
    if row[-1] > 0:
        return [row[-1], 0, 'index', row[0]]
    else:
        return [0, row[-1], 'index', row[0]]


def all_elements_update(row, all_indexes):
    global counter
    GLOBAL_used.update(all_indexes)
    for i in all_indexes:
        answer_df.loc[i, '[ОТВЕТ] Номер группы'] = counter
    counter += 1
    return


def some_elements_update(all_indexes, cur_not_used_index):
    global counter
    indexes = list(set(all_indexes) - set(cur_not_used_index))
    GLOBAL_used.update(indexes)
    for i in indexes:
        answer_df.loc[i, '[ОТВЕТ] Номер группы'] = counter
    counter += 1
    return


def test(table, row):
    if len(table) != 0:
        table.sort_values(by=['Сумма'],
                          ascending=[True],
                          inplace=True)  # сортировка

        local_sum = table['Сумма'].sum() + row[-1]
        all_indexes = table['Новый индекс'].tolist() + [row[0]]
        active_sum = table[table['Сумма'] > 0]['Сумма'].sum()
        passive_sum = abs(table[table['Сумма'] < 0]['Сумма'].sum())
        if row[-1] > 0:
            active_sum += row[-1]
        else:
            passive_sum += abs(row[-1])

        if local_sum == 0:
            all_elements_update(row, all_indexes)
            return 0
        cur_not_used_index = []
        new_active_sum = active_sum
        new_passive_sum = passive_sum
        if local_sum < 0:
            for i in range(len(table)):
                s = table.iloc[i, 3]
                s_index = table.iloc[i, 0]
                if s < 0:
                    if abs(local_sum - s) <= abs(local_sum):
                        local_sum -= s
                        new_passive_sum += s
                        cur_not_used_index.append(s_index)
                        continue
                else:
                    if local_sum > 0:
                        break
                    else:
                        if abs(local_sum + s) <= abs(local_sum):
                            local_sum += s
                            new_active_sum -= s
                            cur_not_used_index.append(s_index)
                            continue
            if new_passive_sum != 0:
                if 5 / 7 <= ((new_active_sum) / (new_passive_sum)) <= 7 / 5:
                    some_elements_update(all_indexes, cur_not_used_index)
                    return abs(new_active_sum - new_passive_sum)
        else:
            for i in range(len(table)-1, -1, -1):
                s = table.iloc[i, 3]
                s_index = table.iloc[i, 0]
                if s > 0:
                    if abs(local_sum - s) <= abs(local_sum):
                        local_sum -= s
                        new_active_sum -= s
                        cur_not_used_index.append(s_index)
                        continue
                else:
                    if local_sum < 0:
                        break
                    else:
                        if abs(local_sum + s) <= abs(local_sum):
                            local_sum += s
                            new_passive_sum += s
                            cur_not_used_index.append(s_index)
                            continue
            if new_passive_sum != 0:
                if 5 / 7 <= ((new_active_sum) / (new_passive_sum)) <= 7 / 5:
                    some_elements_update(all_indexes, cur_not_used_index)
                    return abs(new_active_sum - new_passive_sum)
    return one_element_update(row)


def main(df, date, rate, i):
    extra_table = []
    for j in range(i + 1, len(df)):
        cur_index = df.index[j]
        cur_date, cur_rate, cur_summa = df.iloc[j]
        if cur_rate - rate > 0.15:
            break
        if abs(cur_date - date) > 30 or cur_index in GLOBAL_used:
            continue
        extra_table.append([cur_index, cur_date, cur_rate, cur_summa])
    extra_table = extra_table
    table = pd.DataFrame(extra_table,
                         columns=['Новый индекс'] + list(df.columns))
    return table


data = pd.read_csv('Банк_3мес_данные.csv',
                   sep=';',
                   encoding='cp1251')
data['Вклад (пассив)'] = data['Вклад (пассив)'].str.replace(',', '.', regex=False).astype(float)
data['Дата погашения'] = pd.to_datetime(data['Дата погашения'],
                                        format='%d.%m.%Y')
answer_df = data.copy()
data['Вклад (пассив)'] = -data['Вклад (пассив)']


data.sort_values(by=['Ставка, %', 'Дата погашения'],
                 ascending=[True, True], inplace=True)
df = data[['Срок погашения, дней', 'Ставка, %']].copy()
df['Сумма'] = data['Вклад (пассив)'] + data['Кредит (актив)']

GLOBAL_used = set()

left_active = 0
left_passive = 0
RWA = 0
for i in range(len(df)):
    index = df.index[i]
    if index in GLOBAL_used:
        continue
    date, rate, summa = df.iloc[i]
    row = [index, date, rate, summa]
    table = main(df, date, rate, i)

    result = test(table, row)
    if isinstance(result, np.float64) or type(result) == int:
        RWA += result
    else:
        left_active += result[0]
        left_passive -= result[1]

RWA += (left_active + left_passive) * 0.1 + abs(left_active - left_passive) * 0.4
print('Answer RWA:', RWA)
print(answer_df['Кредит (актив)'].sum() - answer_df['Вклад (пассив)'].sum())
end = time.time()
print("Количество групп неттирования:", counter - 1)
print(f"Время выполнения: {end - start:.4f} секунд")

# answer_df.to_csv('ОТВЕТ.csv', index=False, encoding='cp1251')
