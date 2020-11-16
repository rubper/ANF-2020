from django.apps import AppConfig
import logging
from django.db import connection

class EstadosConfig(AppConfig):
    name = 'Estados'
    #proceso al inicio de la aplicación
    def ready(self):
        #prepara variable de log para debug
        logger = logging.getLogger(__name__ + '.logPersonalizado')
        with connection.cursor() as cursorVerificacion:
            #Verificar si la tabla existe
            ###Usar
            #SELECT * FROM information_schema.tables WHERE table_schema = 'nombreesquema' AND table_name = 'nombretabla' LIMIT 1;
            ###Para MySQL
            cursorVerificacion.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Empresa_sobrenombre';")
            existeSobrenombre=cursorVerificacion.fetchone()
            cursorVerificacion.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Usuarios_user';")
            existeUsuarios=cursorVerificacion.fetchone()
            cursorVerificacion.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Usuarios_opcionform';")
            existeOpcionForm=cursorVerificacion.fetchone()
            cursorVerificacion.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Usuarios_accesousuario';")
            existeAccesoUsuarios=cursorVerificacion.fetchone()
            cursorVerificacion.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Giro_ratios';")
            existeRatios=cursorVerificacion.fetchone()
        with connection.cursor() as cursor:
            if(existeSobrenombre!=None):
                cursor.execute("SELECT Count(*) FROM Empresa_sobrenombre;")
                cantidad=cursor.fetchone()
                if(cantidad[0]==0):
                    sobrenombres=[
                        'Activo de corto plazo',
                        'Cuenta por cobrar',
                        'Cuenta por pagar',
                        'Inventario',
                        'Activo Fijo',
                        'Ventas netas',
                        'Costo de servicio o ventas',
                        'Costo de operación o administración',
                        'Gastos financieros',
                        'Otros gastos',
                        'Otros ingresos',
                        'Impuestos',
                    ]
                    cadenaEjecucion = ""
                    for sobren in sobrenombres:
                        cadenaEjecucion = ""
                        cadenaEjecucion += "INSERT INTO Empresa_sobrenombre (sobreNombre) VALUES ('"
                        cadenaEjecucion += sobren
                        cadenaEjecucion += "'); "
                        cursor.execute(cadenaEjecucion)
                        logger.error("[Debug] Cadena de ejecución generada: " + cadenaEjecucion)
                    logger.error("[Debug] Se ejecutaron con éxito las sentencias sql.")
                else:
                    logger.error("[Debug] No se ejecutó ninguna sentencia.")
            if(existeUsuarios!=None):
                    cursor.execute("SELECT Count(*) FROM Usuarios_user;")
                    cantidad=cursor.fetchone()
                    if(cantidad[0]==0):
                        cursor.execute("INSERT INTO Usuarios_user (password, last_login, id, nomUsuario, activo, rol, is_administrador, is_analista, is_gerente) VALUES(\"pbkdf2_sha256$216000$QHPDlSYDbxRY$6JU7Jfs9HdP5PAMHCsQhJxy+9OifUMzwju5C6HHd5c0=\", NULL, \"01\", \"rubper\", 1,1,1,0,0);")
            if(existeUsuarios!=None):
                    cursor.execute("SELECT Count(*) FROM Usuarios_opcionform;")
                    cantidad=cursor.fetchone()
                    if(cantidad[0]==0):
                        cursor.execute("INSERT INTO Usuarios_opcionform (idOpcion, descOpcion, numForm) VALUES (\"000\", \"Lista de usuarios\", 0);")
                        cursor.execute("INSERT INTO Usuarios_opcionform (idOpcion, descOpcion, numForm) VALUES (\"001\", \"Lista de pantallas\", 1);")
                        cursor.execute("INSERT INTO Usuarios_opcionform (idOpcion, descOpcion, numForm) VALUES (\"002\", \"Lista de accesos de usuario\", 2);")
                        cursor.execute("INSERT INTO Usuarios_opcionform (idOpcion, descOpcion, numForm) VALUES (\"003\", \"Lista de giros\", 3);")
                        cursor.execute("INSERT INTO Usuarios_opcionform (idOpcion, descOpcion, numForm) VALUES (\"004\", \"Lista de empresas\", 4);")
                        cursor.execute("INSERT INTO Usuarios_opcionform (idOpcion, descOpcion, numForm) VALUES (\"005\", \"Lista de estados financieros\", 5);")
            if(existeAccesoUsuarios!=None and existeUsuarios!=None and existeOpcionForm!=None):
                    cursor.execute("SELECT Count(*) FROM Usuarios_accesousuario;")
                    cantidad=cursor.fetchone()
                    if(cantidad[0]==0):
                        cursor.execute("INSERT INTO Usuarios_accesousuario (id, idOpcion_id, idUsuario_id) VALUES (1, \"000\", \"01\");")     
                        cursor.execute("INSERT INTO Usuarios_accesousuario (id, idOpcion_id, idUsuario_id) VALUES (2, \"001\", \"01\");")  
                        cursor.execute("INSERT INTO Usuarios_accesousuario (id, idOpcion_id, idUsuario_id) VALUES (3, \"002\", \"01\");")
            if(existeRatios!=None):
                    cursor.execute("SELECT Count(*) FROM Giro_ratios;")
                    cantidad=cursor.fetchone()
                    if(cantidad[0]==0):
                        cursor.execute("INSERT INTO Giro_ratios (idRatio, categoria, nomRatio) VALUES (1,'Liquidez','Razón circulante');")
                        cursor.execute("INSERT INTO Giro_ratios (idRatio, categoria, nomRatio) VALUES (2,'Liquidez','Prueba ácida');")
                        cursor.execute("INSERT INTO Giro_ratios (idRatio, categoria, nomRatio) VALUES (3,'Liquidez','Razón de capital de trabajo');")
                        cursor.execute("INSERT INTO Giro_ratios (idRatio, categoria, nomRatio) VALUES (4,'Liquidez','Razón de efectivo');")
                        cursor.execute("INSERT INTO Giro_ratios (idRatio, categoria, nomRatio) VALUES (5,'Actividad','Razón de rotación de inventario');")
                        cursor.execute("INSERT INTO Giro_ratios (idRatio, categoria, nomRatio) VALUES (6,'Actividad','Razón de días de inventario');")
                        cursor.execute("INSERT INTO Giro_ratios (idRatio, categoria, nomRatio) VALUES (7,'Actividad','Razón de rotación de cuentas por cobrar');")
                        cursor.execute("INSERT INTO Giro_ratios (idRatio, categoria, nomRatio) VALUES (8,'Actividad','Razón de periodo medio de cobranza');")
                        cursor.execute("INSERT INTO Giro_ratios (idRatio, categoria, nomRatio) VALUES (9,'Actividad','Razón de rotación de cuentas por pagar');")
                        cursor.execute("INSERT INTO Giro_ratios (idRatio, categoria, nomRatio) VALUES (10,'Actividad','Razón de periodo medio de pago');")
                        cursor.execute("INSERT INTO Giro_ratios (idRatio, categoria, nomRatio) VALUES (11,'Actividad','Índice de rotación de activos totales');")
                        cursor.execute("INSERT INTO Giro_ratios (idRatio, categoria, nomRatio) VALUES (12,'Actividad','Índice de rotación de activos fijos');")
                        cursor.execute("INSERT INTO Giro_ratios (idRatio, categoria, nomRatio) VALUES (13,'Actividad','Índice de margen bruto');")
                        cursor.execute("INSERT INTO Giro_ratios (idRatio, categoria, nomRatio) VALUES (14,'Actividad','Índice de margen operativo');")
                        cursor.execute("INSERT INTO Giro_ratios (idRatio, categoria, nomRatio) VALUES (15,'Apalancamiento','Grado de endeudamiento');")
                        cursor.execute("INSERT INTO Giro_ratios (idRatio, categoria, nomRatio) VALUES (16,'Apalancamiento','Grado de propiedad');")
                        cursor.execute("INSERT INTO Giro_ratios (idRatio, categoria, nomRatio) VALUES (17,'Apalancamiento','Razón de endeudamiento patrimonial');")
                        cursor.execute("INSERT INTO Giro_ratios (idRatio, categoria, nomRatio) VALUES (18,'Apalancamiento','Razón de cobertura de gastos financieros');")
                        cursor.execute("INSERT INTO Giro_ratios (idRatio, categoria, nomRatio) VALUES (19,'Rentabilidad','Rentabilidad neta del patrimonio');")
                        cursor.execute("INSERT INTO Giro_ratios (idRatio, categoria, nomRatio) VALUES (20,'Rentabilidad','Rentabilidad por acción');")
                        cursor.execute("INSERT INTO Giro_ratios (idRatio, categoria, nomRatio) VALUES (21,'Rentabilidad','Rentabilidad del activo');")
                        cursor.execute("INSERT INTO Giro_ratios (idRatio, categoria, nomRatio) VALUES (22,'Rentabilidad','Rentabilidad sobre ventas');")
                        cursor.execute("INSERT INTO Giro_ratios (idRatio, categoria, nomRatio) VALUES (23,'Rentabilidad','Rentabilidad sobre inversión');")