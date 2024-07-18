import mysql.connector
from sqlalchemy import create_engine, text


def mysql_init():
    # 配置数据库连接参数
    config = {
        "user": "mysql_admin",
        "password": "mysql@admin123",
        "host": "rm-wz900944kd610ohzl4o.mysql.rds.aliyuncs.com",
        "database": "copy_check",
        "charset": "utf8mb4",
        "collation": "utf8mb4_unicode_ci",
        "raise_on_warnings": True,
    }

    try:
        conn = mysql.connector.connect(**config)

        cursor = conn.cursor()
        cursor.execute("SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;")
        return conn, cursor

    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL database: {err}")
        return None, None


def mysql_insert(table: str, columns_values: dict):
    conn, cursor = mysql_init()

    columns = ""
    values = ""
    for k, v in columns_values.items():
        columns += "{},".format(k)
        values += "'{}',".format(v)
    columns = columns[:-1]
    values = values[:-1]

    sql = (
        "insert into {} ({}) values({});".format(table, columns, values)
        .encode("utf-8")
        .decode("utf-8")
    )

    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


def mysql_update(table: str, columns_values: dict, conditions: dict | None):
    conn, cursor = mysql_init()

    cv = ""
    for k, v in columns_values.items():
        cv += "{} = {},".format(k, v)
    cv = cv[:-1]

    if conditions is None or len(conditions) == 0:
        sql = "update {} set {};".format(table, cv).encode("utf-8").decode("utf-8")
    else:
        cs = ""
        for k, v in conditions.items():
            cs += "{} = {} and".format(k, v)
        cs = cs[:-4]
        sql = (
            "update {} set {} where {};".format(table, cv, cs)
            .encode("utf-8")
            .decode("utf-8")
        )

    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


def mysql_select(table: str, conditions: dict | None) -> list:
    conn, cursor = mysql_init()

    if conditions is None or len(conditions) == 0:
        sql = "select * from {};".format(table)
    else:
        cs = ""
        for k, v in conditions.items():
            cs += "{} = {} and".format(k, v)
        cs = cs[:-4]
        sql = (
            "select * from {} where {};".format(table, cs)
            .encode("utf-8")
            .decode("utf-8")
        )

    results = []
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return results


def mysql_execute(sql: str):
    print(sql)
    conn, cursor = mysql_init()
    if not conn or not cursor:
        print("Failed to initialize database connection")
        return None
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        conn.commit()
        return results
    except mysql.connector.Error as err:
        print(f"Error executing SQL command on database: {err}")
        return None
    finally:
        cursor.close()
        conn.close()


def execute_query(query):
    engine = create_engine(
        f"mysql+mysqlconnector://mysql_admin:mysql%40admin123@rm-wz900944kd610ohzl4o.mysql.rds.aliyuncs.com:3306/copy_check?charset=utf8mb4"
    )

    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
            return result.fetchall()
    except Exception as e:
        print(f"Error executing query: {e}")
        return None


if __name__ == "__main__":
    print(
        execute_query(
            """
        SELECT id, `index`, content, title, author, `from`, shash, 
            hamming_distance(shash, CONVERT('0010010010011011010000010101011100100001010011111010000110100000' USING utf8mb4)) 
            FROM corpus 
            LIMIT 10;
            """
        )
    )
