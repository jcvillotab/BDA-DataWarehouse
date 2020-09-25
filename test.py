import mysql.connector, openpyxl as opx, os, sys,re

from mysql.connector import Error

#print (os.path.abspath(__file__))



def createConnection():
    try:
        connection = mysql.connector.connect(
            host='localhost', database='testpython', user='root', password='juancamilovill9')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return 0


def executeInsertStatement(connection, statement, values):
    cursor = connection.cursor()
    result = cursor.execute(statement, values)
    connection.commit()
    cursor.close()


def insertEmpresas(listE):
    absPath = os.path.join(os.path.dirname(sys.argv[0]), "Datos.xlsx")
    workbook = opx.load_workbook(absPath)
    sheet = workbook.active
    myDB = createConnection()

    for i in range(2, 15):
        cValue = sheet["C"+str(i)].value
        idEmpresa = re.search('([0-9]+)', cValue).group()
        nombreEmpresa = cValue[re.search('([0-9]+)', cValue).span()[1] + 3 :]
        #print(idEmpresa)
        #print(nombreEmpresa)
        bValue= sheet["B"+str(i)].value
        region = bValue.split(" - ")[1]
        idRegion = bValue.split(" - ")[0]

        statement = "INSERT INTO empresa values (%s,%s, %s)"
        val = (idEmpresa, nombreEmpresa, region)

        
        executeInsertStatement(myDB, statement,val)
    myDB.close()
    
insertEmpresas({})




