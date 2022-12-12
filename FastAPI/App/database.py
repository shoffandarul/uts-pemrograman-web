import mysql.connector

def getMysqlConnection():
    return mysql.connector.connect(user='root', host='localhost', port='3306', password='', database='uts_shoffandarulmufti')

def getMethod(sqlstr):
    db = getMysqlConnection()
    print("Query:\n",sqlstr)
    try:
        cur = db.cursor()
        cur.execute(sqlstr)
        output_json = cur.fetchall()
        db.commit()
        cur.close()
    except Exception as e:
        print("Error in SQL:\n", e)
        return ([{"message": "error in SQL"}])
    finally:
        db.close()
    return output_json

def postMethod(sqlstr):
    db = getMysqlConnection()
    try:
        cur = db.cursor()
        cur.execute(sqlstr)
        db.commit()
        cur.close()
    except Exception as e:
        print("Error in SQL:\n", e)
        return ({"message": "error in SQL"})
    finally:
        db.close()
    return ({"message": "sukses"})