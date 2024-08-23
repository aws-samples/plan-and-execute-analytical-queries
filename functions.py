from enum import Enum
from typing import Optional

import pandas as pd


def get_patients():
    df = pd.read_csv('dataset/patients.csv')
    df.columns = [c.lower() for c in df.columns]
    return df


def get_allergies():
    df = pd.read_csv('dataset/allergies.csv')
    df.columns = [c.lower() for c in df.columns]
    df = df.rename(columns={'patient': 'patient_id'})
    return df


def get_immunization():
    df = pd.read_csv('dataset/immunizations.csv')
    df.columns = [c.lower() for c in df.columns]
    df = df.rename(columns={'patient': 'patient_id'})
    return df


def filter(list, keys, values):
    for k, v in zip(keys, values):
        list = list[list[k] == v]
    return list


def count(list):
    return len(list)


def distinct(list, key: str):
    return list[key].drop_duplicates().tolist()


class JoinMode(Enum):
    INNER = 1
    LEFT = 2
    RIGHT = 3
    OUTER = 4


def join(a: pd.DataFrame, b: pd.DataFrame, left_key: str, right_key: str, how: JoinMode):
    return pd.merge(a, b, left_on=left_key, right_on=right_key, how=str(how).lower())


class SortOrder(Enum):
    ASCENDING = 1
    DESCENDING = 2


def order_by(list, key: str, value: SortOrder):
    return list.sort_values(by=key, ascending=True if value == 'ASCENDING' else False)


class GroupByAggregation(Enum):
    COUNT = 1
    MEAN = 2


def group_by(list, group_key: str, aggregation_key: Optional[str], aggregation: GroupByAggregation):
    df = list.groupby(by=group_key)
    if aggregation == 'COUNT':
        df = df.size()
        df = df.to_frame().rename(columns={0: 'count'})
        df = df.reset_index()
    else:
        raise Exception('not implemented')
    return df


def limit(list, k):
    return list.iloc[:k]


def select(list, keys):
    return list[keys]
