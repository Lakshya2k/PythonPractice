try:
    import mysql.connector as sql
    import csv

    db = sql.connect(host="localhost", user="root", passwd="root", use_pure=True)
    cr = db.cursor()
    DB_NAME = "carbon_nanotubes"
    CREATE_DB = f"CREATE DATABASE {DB_NAME}"
    cr.execute(CREATE_DB)
    with open("carbon_nanotubes.csv", "r") as f:
        csv_reader = csv.DictReader(f, delimiter=";")
        head = list(next(csv_reader).keys())
        head_final = [
            f"`{i}` int(5)" if i[:2] == "Ch" else f"`{i}` varchar(20)" for i in head
        ]
        table_head = f"({','.join(head_final)})"
        TABLE_NAME = "data"
        CREATE_TABLE = f"CREATE TABLE {DB_NAME}.{TABLE_NAME}{table_head}"
        cr.execute(CREATE_TABLE)
        for line in csv_reader:
            value = list(line.values())
            value_final = [
                f"'{value[x]}'" if x > 1 else value[x] for x in range(len(value))
            ]
            table_value = f"({','.join(value_final)})"
            INSERT_INTO_TABLE = (
                f"INSERT INTO {DB_NAME}.{TABLE_NAME} values{table_value}"
            )
            cr.execute(INSERT_INTO_TABLE)
        db.commit()


except Exception as e:
    db.close()
    print(e)
