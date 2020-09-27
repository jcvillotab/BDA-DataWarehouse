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


def insertEmpresas(listE, workbook):
    sheet = workbook.active
    myDB = createConnection()

    
    for i in range(2, 100):
        cValue = sheet["D"+str(i)].value
        idEmpresa = re.search('([0-9]+)', cValue).group()
        if idEmpresa not in listE:
            nombreEmpresa = cValue[re.search('([0-9]+)', cValue).span()[1] + 3 :]
            bValue= sheet["C"+str(i)].value
            region = bValue.split(" - ")[1]
            idRegion = bValue.split(" - ")[0]

            statement = "INSERT INTO Dim_empresa values (%s,%s, %s, %s)"
            val = (idEmpresa, nombreEmpresa, region, idRegion)

            executeInsertStatement(myDB, statement,val)
            listE.append(idEmpresa)
        

    myDB.close()

def insertCliente(listClient, workbook):
    sheet = workbook.active
    myDB = createConnection()
    for i in range(2, 100):
        nombre = sheet["G"+str(i)].value
        razonSocial = sheet["H"+str(i)].value
        documento = sheet["I"+str(i)].value
        telefono = sheet["K"+str(i)].value
        jValue = sheet["J"+str(i)].value

        if "CARRERA" in jValue:
            jValue = jValue.replace("CARRERA", "CRA")
        elif "CALLE" in jValue:
            jValue = jValue.replace("CALLE", "CLL")
        elif "AVENIDA" in jValue:
            jValue = jValue.replace("AVENIDA", "AV")
        elif "DIAGONAL" in jValue:
            jValue = jValue.replace("DIAGONAL", "DIAG")

        if ")" in telefono:
            telefono = telefono.split(")")[1]
        if "-" in telefono:
            telefono = telefono.split("-")[0]
        if "/" in telefono:
            telefono = telefono.split("/")[0]
        
        statement = "INSERT INTO Dim_Cliente (nombre, razonSocial, documento, direccion, telefono) values (%s,%s, %s, %s, %s)"
        val = (nombre, razonSocial, documento, jValue, telefono)
        executeInsertStatement(myDB, statement,val)
    myDB.close()



absPath = os.path.join(os.path.dirname(sys.argv[0]), "Datos.xlsx")
workbook = opx.load_workbook(absPath)
listaEmpresas = []
diccClientes = {}
insertEmpresas(listaEmpresas, workbook)
insertCliente(diccClientes, workbook)





