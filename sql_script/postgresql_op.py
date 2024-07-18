import psycopg2


# 连接 PostgreSQL 数据库的初始化函数
def postgresql_init():
    # 定义连接参数
    host = "rm-cn-8ex3tyk4a000675o.rwlb.rds.aliyuncs.com"
    port = 5432
    user = "mysql_admin"
    password = "mysql@admin123"
    database = "copy_check_sentence"  # 替换为实际的数据库名称

    try:
        conn = psycopg2.connect(
            host=host, port=port, user=user, password=password, dbname=database
        )

        cursor = conn.cursor()

        return conn, cursor

    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL:", e)


# PostgreSQL 插入操作函数
def postgresql_insert(table: str, columns_values: dict):
    conn, cursor = postgresql_init()

    columns = ", ".join(columns_values.keys())
    values = ", ".join(["%s"] * len(columns_values))

    try:
        sql = f"INSERT INTO {table} ({columns}) VALUES ({values})"
        cursor.execute(sql, list(columns_values.values()))
        conn.commit()

    except psycopg2.Error as e:
        print(f"Error inserting into PostgreSQL: {e}")

    finally:
        cursor.close()
        conn.close()


# PostgreSQL 更新操作函数
def postgresql_update(table: str, columns_values: dict, conditions: dict | None):
    conn, cursor = postgresql_init()

    cv_pairs = ", ".join([f"{k} = %s" for k in columns_values.keys()])
    condition_pairs = " AND ".join([f"{k} = %s" for k in conditions.keys()])

    try:
        sql = f"UPDATE {table} SET {cv_pairs}"
        if conditions:
            sql += f" WHERE {condition_pairs}"

        cursor.execute(sql, list(columns_values.values()) + list(conditions.values()))
        conn.commit()

    except psycopg2.Error as e:
        print(f"Error updating PostgreSQL: {e}")

    finally:
        cursor.close()
        conn.close()


def postgresql_select(table: str, conditions: dict | None) -> list:
    conn, cursor = postgresql_init()

    if not conn or not cursor:
        return []

    try:
        if conditions:
            condition_pairs = " AND ".join([f"{k} = %s" for k in conditions.keys()])
            sql = f"SELECT * FROM {table} WHERE {condition_pairs}"
            cursor.execute(sql, list(conditions.values()))
        else:
            sql = f"SELECT * FROM {table}"
            cursor.execute(sql)

        results = cursor.fetchall()
        return results

    except psycopg2.Error as e:
        print(f"Error selecting from PostgreSQL: {e}")
        return []

    finally:
        cursor.close()
        conn.close()


# PostgreSQL 执行自定义 SQL 操作函数
def postgresql_execute(sql: str):
    conn, cursor = postgresql_init()

    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        conn.commit()
        return results

    except psycopg2.Error as e:
        print(f"Error executing SQL in PostgreSQL: {e}")
        return []

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    # 定义测试表名和数据
    test_table = "test_table"
    insert_data = {"column1": "value1", "column2": "value2"}

    # 插入数据
    print("Inserting data into the table...")
    postgresql_insert(test_table, insert_data)

    # 查询数据
    print("Querying data from the table...")
    results = postgresql_select(test_table, None)

    # 打印查询结果
    print("Query results:")
    for row in results:
        print(row)
