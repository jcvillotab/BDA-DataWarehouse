import mysql.connector, openpyxl as opx, os, sys,re

from mysql.connector import Error

#print (os.path.abspath(__file__))



def createConnection():
    try:
        connection = mysql.connector.connect(
            host='localhost', database='datawarehouse', user='root', password='juancamilovill9')
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


def executeInsertStatement(connection, statement, values, cursor):
    result = cursor.execute(statement, values)

def executeStatement(connection, statement, cursor):
    cursor.execute(statement)
    result = cursor.fetchone()
    return result

def insertEmpresas(listE, workbook):
    sheet = workbook.active
    myDB = createConnection()
    cursor = myDB.cursor()
    
    for i in range(2, 6000):
        cValue = sheet["D"+str(i)].value
        idEmpresa = re.search('([0-9]+)', cValue).group()
        if idEmpresa not in listE:
            nombreEmpresa = cValue[re.search('([0-9]+)', cValue).span()[1] + 3 :]
            bValue= sheet["C"+str(i)].value
            region = bValue.split(" - ")[1]
            idRegion = bValue.split(" - ")[0]

            statement = "INSERT INTO Dim_empresa (empresaAltId, nombreEmpresa, region, idRegion) values (%s,%s,%s, %s)"
            val = (idEmpresa, nombreEmpresa, region, idRegion)

            executeInsertStatement(myDB, statement,val, cursor)
            listE[idEmpresa] = len(listE)+1
    myDB.commit()
    myDB.close()

def insertCliente(diccClient, workbook):
    sheet = workbook.active
    myDB = createConnection()
    cursor = myDB.cursor()
    for i in range(2, 6000):
        nombre = sheet["G"+str(i)].value
        razonSocial = sheet["H"+str(i)].value
        if razonSocial not in diccClient:
            documento = sheet["I"+str(i)].value
            jValue = sheet["J"+str(i)].value
            idSegmento = sheet["M"+str(i)].value
            segmento = sheet["N"+str(i)].value
            #telefono = sheet["K"+str(i)].value
            #telefono = str(telefono)
            ciudad = sheet["AH"+str(i)].value
            

            if(sheet.cell(row=i, column=34).value is not None):
                if "-" in ciudad:
                    ciudad = ciudad.split("-")[1]
            
            
            if (sheet.cell(row=i, column=10).value is not None):
                if "CARRERA" in jValue:
                    jValue = jValue.replace("CARRERA", "CRA")
                elif "CALLE" in jValue:
                    jValue = jValue.replace("CALLE", "CLL")
                elif "AVENIDA" in jValue:
                    jValue = jValue.replace("AVENIDA", "AV")
                elif "DIAGONAL" in jValue:
                    jValue = jValue.replace("DIAGONAL", "DIAG")
                
            
            statement = "INSERT INTO Dim_Cliente (nombre, razonSocial, documento, direccion, idSegmento, segmento, ciudad) values (%s,%s, %s, %s, %s, %s, %s)"
            val = (nombre, razonSocial, documento, jValue, idSegmento, segmento, ciudad)
            executeInsertStatement(myDB, statement,val, cursor)


            diccClient[razonSocial] = len(diccClient)+1
    myDB.commit()
    myDB.close()

def insertarProducto(workbook, productDict):
    sheet = workbook.active
    myDB = createConnection()
    cursor = myDB.cursor()
    for i in range(2,6000):
        nombre = sheet["Q"+str(i)].value
        idProducto = sheet["P"+str(i)].value
        if idProducto not in productDict:
            und = sheet["R"+str(i)].value
            categoriaClubMcCain = sheet["AA"+str(i)].value.split("-")[1]
            linea = sheet["AB"+str(i)].value.split("-")[1]
            subLinea = sheet["AC"+str(i)].value.split("-")[1]
            categoria = sheet["AD"+str(i)].value.split("-")[1]
            subCategoria = sheet["AE"+str(i)].value.split("-")[1]

            statement = "INSERT INTO Dim_Producto (idAltProducto, nombre, und, categoriaClubMcCain, linea, subLinea, categoria, subCategoria) values (%s,%s, %s, %s, %s, %s, %s, %s)"
            val = (idProducto, nombre, und, categoriaClubMcCain, linea, subLinea, categoria, subCategoria)
            executeInsertStatement(myDB, statement,val,cursor)
            productDict[idProducto] = len(productDict)+1
            #print(idProducto+ " " + str(len(productDict)))
    myDB.commit()
    myDB.close()

def insertarVenta(diccEmpresas, diccClientes, diccProductos, workbook):
    sheet = workbook.active
    myDB = createConnection()
    cursor = myDB.cursor()
    for i in range(2,6000):
        idCliente = diccClientes.get(sheet["H"+str(i)].value)
        idEmpresa = diccEmpresas.get(sheet["D"+str(i)].value.split(" - ")[0])
        idFecha = (sheet["A"+str(i)].value).strftime("%Y%m%d")
        idProducto = diccProductos.get(sheet["P"+str(i)].value)
        cantidadPedida = sheet["S"+str(i)].value
        cantidadDevuelta = sheet["T"+str(i)].value
        precioNoIva = sheet["W"+str(i)].value
        precioIva = sheet["X"+str(i)].value
        KG = sheet["AQ"+str(i)].value
        statement = "INSERT INTO Fact_Venta (idCliente, idEmpresa, idFecha, idProducto, cantidadPedida, cantidadDevuelta, precioNoIVA, precioIVA, KG) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (idCliente, idEmpresa, idFecha, idProducto, cantidadPedida, cantidadDevuelta, precioNoIva, precioIva, KG)
        executeInsertStatement(myDB, statement,val,cursor)
    
    myDB.commit()
    myDB.close()

absPath = os.path.join(os.path.dirname(sys.argv[0]), "Datos.xlsx")
workbook = opx.load_workbook(absPath)

diccEmpresas = {}
diccClientes = {}
diccProductos = {}
insertEmpresas(diccEmpresas, workbook)
insertCliente(diccClientes, workbook)
insertarProducto(workbook, diccProductos)
insertarVenta(diccEmpresas, diccClientes, diccProductos, workbook)





