import mysql.connector


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

        return conn, cursor

    except mysql.connector.Error as err:
        print(f"Error: {err}")


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


def mysql_exectute(sql: str):
    conn, cursor = mysql_init()
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return results


if __name__ == "__main__":
    mysql_insert("test", {"ttt": 2})
    mysql_update("test", {"ttt": 3}, {"ttt": 1})
    print(mysql_select("test", {"ttt": 1}))
    print(mysql_select("test", {}))
    print(mysql_select("test", None))
