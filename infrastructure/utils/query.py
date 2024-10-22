from pydantic import BaseModel


def build_insert(model: BaseModel, key: str, table_name: str, omit_key: bool):
    params = model.dict()
    keys = [k for k in params.keys() if key != k]
    if not omit_key:
        keys.append(key)
    values = [params[k] for k in keys]
    columns = ", ".join(keys)
    query_values = ", ".join(["%s" for i in range(len(values))])
    query = f"insert into {table_name} ({columns}) values ({query_values}) returning {key}"
    return query, tuple(values)


def build_update(model: BaseModel, key: str, table_name: str):
    params = model.dict()
    keys = [k for k in params.keys() if key != k]
    values = [params[k] for k in keys]
    keys = [f"{k} = %s" for k in keys]
    values.append(params[key])
    columns = ", ".join(keys)
    query = f"update {table_name} set {columns} where {key} = {'%s'}"
    return query, tuple(values)
