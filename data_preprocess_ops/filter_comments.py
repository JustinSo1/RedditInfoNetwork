def filter_comments(df, column, drop_values):
    filtered_comments = df[~df[column].str.contains('|'.join(drop_values))]
    return filtered_comments