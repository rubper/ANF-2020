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
        with connection.cursor() as cursor:
            if(len(existeSobrenombre)==1):
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
            if(len(existeUsuarios)==1):
                    cursor.execute("SELECT Count(*) FROM Usuarios_user;")
                    cantidad=cursor.fetchone()
                    if(cantidad[0]==0):
                        cursor.execute("INSERT INTO Usuarios_user VALUES(\"pbkdf2_sha256$216000$QHPDlSYDbxRY$6JU7Jfs9HdP5PAMHCsQhJxy+9OifUMzwju5C6HHd5c0=\", NULL, \"01\", \"rubper\", 1,1,1,0,0);")
            if(len(existeUsuarios)==1):
                    cursor.execute("SELECT Count(*) FROM Usuarios_opcionform;")
                    cantidad=cursor.fetchone()
                    if(cantidad[0]==0):
                        cursor.execute("INSERT INTO Usuarios_opcionform VALUES (\"000\", \"Lista de usuarios\", 0);")
                        cursor.execute("INSERT INTO Usuarios_opcionform VALUES (\"001\", \"Lista de pantallas\", 1);")
                        cursor.execute("INSERT INTO Usuarios_opcionform VALUES (\"002\", \"Lista de accesos de usuario\", 2);")
                        cursor.execute("INSERT INTO Usuarios_opcionform VALUES (\"003\", \"Lista de giros\", 3);")
                        cursor.execute("INSERT INTO Usuarios_opcionform VALUES (\"004\", \"Lista de empresas\", 4);")
            if(len(existeUsuarios)==1):
                    cursor.execute("SELECT Count(*) FROM Usuarios_accesousuario;")
                    cantidad=cursor.fetchone()
                    if(cantidad[0]==0):
                        cursor.execute("INSERT INTO Usuarios_accesousuario VALUES (1, \"000\", \"01\");")     
                        cursor.execute("INSERT INTO Usuarios_accesousuario VALUES (2, \"001\", \"01\");")  
                        cursor.execute("INSERT INTO Usuarios_accesousuario VALUES (3, \"002\", \"01\");")     