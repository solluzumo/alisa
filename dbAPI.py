from typing import Dict,Tuple,List
import sqlite3

db = sqlite3.connect("db.sqlite3")
sql = db.cursor()
#сохранение книги в бд
def save_book(table: str, columns_values: Dict):
    columns = ', '.join(columns_values.keys())
    values = [tuple(columns_values.values())]
    placeholders = ", ".join("?"*len(columns_values.keys()))
    sql.executemany(f"INSERT INTO {table} "
                    f"({columns}) "
                    f"VALUES ({placeholders})",
                    values)

    db.commit()

#выбор книг из бд
def fetchall(table:str, request_info: str, columns: List[str]) -> List[Tuple]:
    columns_joined = ", ".join(columns)
    group_name = request_info.split(";")[0]
    requested_date = request_info.split(";")[1]

    sql.execute(f"SELECT {columns_joined} FROM {table} "
                f"where group_name = '{group_name}' and "
                f"date_lesson = '{requested_date}'")
    rows = sql.fetchall()

    result = []
    for row in rows:
        result.append(row)
    return result


#удаление книг
def delete(table: str, row_id: int) -> None:
    row_id = int(row_id)
    sql.execute(f"DELETE FROM {table} WHERE ID={row_id}")
    db.commit()