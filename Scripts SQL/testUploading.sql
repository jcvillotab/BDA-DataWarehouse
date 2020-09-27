Create database testPython;
use testPython;

Create table Dim_Empresa(
	empresaId 		int PRIMARY KEY ,
    nombreEmpresa 	varchar(60),
    region 			varchar(60),
    idRegion 		int(4)
);

Create table Dim_Cliente(
    idCliente   int AUTO_INCREMENT primary key,
    nombre 		varchar(60),
    razonSocial varchar(60),
    documento 	varchar(15),
    direccion 	varchar(60),
    telefono 	varchar(15)
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
#select * from Dim_Fecha;

#select * from Dim_Cliente;
#drop table Dim_Cliente


#drop table Dim_Empresa
#select * from Dim_Empresa
#truncate table Dim_Empresa
