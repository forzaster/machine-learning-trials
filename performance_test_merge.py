import pandas as pd
import numpy as np
import time

ROW_N = 10000


def create_df():
    df = pd.DataFrame({'A': np.random.randint(0, 1000, ROW_N), 'B':np.random.randint(0, 1000, ROW_N),
                       'C': np.random.randint(0, 1000, ROW_N), 'value':np.random.randint(0, 1000, ROW_N)})
    df['A'] = df['A'].astype('str')
    df['B'] = df['B'].astype('str')
    df['C'] = df['C'].astype('str')
    return df


def method1(df1, df2):
    group = df1.groupby(['A', 'B', 'C'])

    df_tmp = pd.DataFrame()
    a = []
    b = []
    c = []
    va = []
    for name, df in group:
        v = 0
        for row in df.itertuples():
            v += row[4]
        if v > 0:
            a.append(name[0])
            b.append(name[1])
            c.append(name[2])
            va.append(v)
    df1 = pd.DataFrame({'A': a, 'B': b, 'C': c, 'value': va})

    df2 = df2.groupby(['A', 'B', 'C'])['value'].sum().reset_index()

    df1 = pd.merge(df1, df2, on=['A', 'B', 'C'], how='inner').set_index(['A', 'B', 'C'])
    df1_tmp = df1[['value_x', 'value_y']]
    df1 = df1.drop(columns=['value_x', 'value_y'])
    df1['value'] = df1_tmp.sum(axis=1)
    df1 = df1.reset_index()
    print(df1.sort_values(['A', 'B', 'C']))


def method2(df1, df2):
    df2 = df2.groupby(['A', 'B', 'C'])['value'].sum().reset_index()

    group = df1.groupby(['A', 'B', 'C'])

    df_tmp = pd.DataFrame()
    a = []
    b = []
    c = []
    va = []
    for name, df in group:
        v = 0
        for row in df.itertuples():
            v += row[4]
        if v > 0:
            a.append(name[0])
            b.append(name[1])
            c.append(name[2])
            df_tmp = df2[(df2['A'] == name[0]) & (df2['B'] == name[1]) & (df2['C'] == name[2])]
            if len(df_tmp) > 0:
                v += df_tmp.iat[0,3]
            va.append(v)

    df1 = pd.DataFrame({'A': a, 'B': b, 'C': c, 'value': va})
    print(df1)


def method3(df1, df2):
    df1 = df1.groupby(['A', 'B', 'C'])['value'].sum().reset_index()
    df2 = df2.groupby(['A', 'B', 'C'])['value'].sum().reset_index()

    df1 = pd.merge(df1, df2, on=['A', 'B', 'C'], how='inner').set_index(['A', 'B', 'C'])
    df1_tmp = df1[['value_x', 'value_y']]
    df1 = df1.drop(columns=['value_x', 'value_y'])
    df1['value'] = df1_tmp.sum(axis=1)
    df1 = df1.reset_index()
    print(df1.sort_values(['A', 'B', 'C']))


def method4(df1, df2):
    df1 = pd.concat([df1, df2])
    df1 = df1.groupby(['A', 'B', 'C'])['value'].sum().reset_index()
    print(df1.sort_values(['A', 'B', 'C']))


def main():
    print('main')
    df1 = create_df()
    df2 = df1.copy()
    df2['value'] = np.random.randint(0, 1000, len(df1))

    # Performance test of df1's value + df2's value

    print('--- method1 ---')
    s = time.time()
    method1(df1, df2)
    t = time.time() - s
    print(t)

    print('--- method2 ---')
    s = time.time()
    method2(df1, df2)
    t = time.time() - s
    print(t)

    print('--- method3 ---')
    s = time.time()
    method3(df1, df2)
    t = time.time() - s
    print(t)

    print('--- method4 ---')
    s = time.time()
    method4(df1, df2)
    t = time.time() - s
    print(t)



if __name__ == '__main__':
    main()


