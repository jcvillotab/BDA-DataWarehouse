Create database datawarehouse;
use datawarehouse;

Create table Dim_Empresa(
	idEmpresa int PRIMARY KEY auto_increment,
	empresaAltId 	bigint ,
    nombreEmpresa 	varchar(60),
    region 			varchar(60),
    idRegion 		int(4)
);

Create table Dim_Cliente(
    idCliente   int AUTO_INCREMENT primary key,
    nombre 		varchar(150),
    razonSocial varchar(150),
    documento 	varchar(15),
    ciudad      varchar(20),
    direccion 	varchar(90),
    idSegmento smallint,
    segmento   varchar(60)
);

Create table Dim_Producto(
	idProducto int auto_increment primary key,
    idAltProducto varchar(15),
	nombre varchar(70),
    und varchar(4),
    categoriaClubMcCain varchar(7),
    linea varchar(40),
    sublinea varchar(40),
    categoria varchar(40),
    subCategoria varchar(40)
);

CREATE TABLE Fact_Venta(
	idVenta int auto_increment primary key,
    idCliente int,
    idEmpresa int,
    idFecha int,
    idProducto int,
    cantidadPedida int,
    cantidadDevuelta int,
    precioNoIVA decimal(10,2),
    precioIVA decimal(10,2),
    KG decimal(20,2)
);

CREATE TABLE Dim_Fecha (
	id                    INTEGER PRIMARY KEY,
	db_date               DATE NOT NULL,
	año                   INTEGER NOT NULL,
	mes                   INTEGER NOT NULL, 
	nombre_del_mes        VARCHAR(9) NOT NULL, 
	dia                   INTEGER NOT NULL, 
	trimestre             INTEGER NOT NULL, 
	semana                INTEGER NOT NULL, 
	nombre_dia            VARCHAR(9) NOT NULL, 
	dia_semana            VARCHAR(9) NOT NULL,
	dia_año               VARCHAR(9) not NULL,
	UNIQUE td_ymd_idx (año,mes,dia),
	UNIQUE td_dbdate_idx (db_date)

) Engine=MyISAM;

DROP PROCEDURE IF EXISTS poblar_Dim_Fecha;
DELIMITER //
CREATE PROCEDURE poblar_Dim_Fecha(IN startdate DATE,IN stopdate DATE)
BEGIN
    DECLARE currentdate DATE;
    SET currentdate = startdate;
    WHILE currentdate <= stopdate DO
        INSERT INTO Dim_Fecha VALUES (
            date_format(currentdate, "%Y%m%d"),
            currentdate,
            YEAR(currentdate),
            MONTH(currentdate),
			monthname(currentdate),
            DAY(currentdate),
            QUARTER(currentdate),
            WEEKOFYEAR(currentdate),
            dayname(currentdate),
            DAYOFWEEK(currentdate),
            dayofyear(currentdate)
            );
        SET currentdate = ADDDATE(currentdate,INTERVAL 1 DAY);
    END WHILE;
END
//
DELIMITER ;

TRUNCATE TABLE Dim_Fecha;
CALL poblar_Dim_Fecha('2020-01-01','2020-12-31');
OPTIMIZE TABLE Dim_Fecha;

ALTER TABLE Fact_Venta
ADD FOREIGN KEY (idCliente) REFERENCES Dim_Cliente(idCliente);

ALTER TABLE Fact_Venta
ADD FOREIGN KEY (idEmpresa) REFERENCES Dim_Empresa(idEmpresa);

ALTER TABLE Fact_Venta
ADD FOREIGN KEY (idFecha) REFERENCES Dim_Fecha(id);

ALTER TABLE Fact_Venta
ADD FOREIGN KEY (idProducto) REFERENCES Dim_Producto(idProducto);


#select * from Dim_Fecha;

#select * from Dim_Cliente
#drop table Dim_Cliente
#truncate table Dim_Cliente

#select * from Dim_Producto
#drop table Dim_Producto
#truncate table Dim_Producto


#drop table Dim_Empresa
#select * from Dim_Empresa
#truncate table Dim_Empresa

#drop table Fact_Venta
#select * from Fact_Venta
#truncate table Fact_Venta
#select count(*) from fact_venta
#select count(*) from Dim_Empresa
#select count(*) from Dim_Producto
#select count(*) from Dim_Cliente
