import pandas as pd


def unify(data, columns):
    data["ADDRESS"] = data[columns].apply(lambda x: ', '.join(filter(None, x.map(str))), axis=1)

    return data
