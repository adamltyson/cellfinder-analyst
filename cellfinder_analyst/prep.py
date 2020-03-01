import pandas as pd


def read_csv_separate(csv, label="cell_count"):
    df = pd.read_csv(csv)
    df.set_index("structure_name", inplace=True)

    df_left = df["left_" + label]
    df_right = df["right_" + label]

    df_left.index = "Left " + df_left.index
    df_right.index = "Right " + df_right.index

    df = df_left.append(df_right)
    return df


def load_group_df(group_list, label="cell_count"):
    df = pd.DataFrame()
    for idx, key in enumerate(group_list.keys()):
        df[key] = read_csv_separate(group_list[key], label=label)
    return df


def select_min_number_single_df(df, min_number):
    df_selector = df > min_number
    return df[df_selector.any(axis=1)]


def combine_min_number(df1, df2, min_number):
    indexes1 = select_min_number_single_df(df1, min_number).index
    indexes2 = select_min_number_single_df(df2, min_number).index
    combined_indexes = list(set(indexes1) | set(indexes2))

    return df1.loc[combined_indexes], df2.loc[combined_indexes]
