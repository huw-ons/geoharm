def unify(data, columns):
    data["ADDRESS"] = data[columns].apply(lambda x: ', '.join(x.dropna().map(str)), axis=1)

    return data
