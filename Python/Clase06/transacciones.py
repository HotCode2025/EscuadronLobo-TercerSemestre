# Clase 6: Corrección de mensajes de error en Postgres:
# para eso-> C:\Program Files\PostgreSQL\18\data postgresql.conf abrimos con sublime text
# y agregamos:
# lc_massages = 'en-US'
# lc_monetary = 'en-US'
# lc_numeric = 'en-US'
# lc_time = 'en-US'   hacemos esos cambios y reiniciamos el equipo


# MANEJO DE TRANSACCIONES:(Manualmente)
# Importación de Base de Datos - Permite la conexión con PostgreSQL
import psycopg2 as bd

# Variable de conexión
# Este código puede simplificarse en una sola línea:
# conexion = psycopg2.connect(user='postgres', password='admin', host='127.0.0.1', port='5432', database='Test_BD', client_encoding='utf8')
conexion = bd.connect(user='postgres', password='admin', host='127.0.0.1', port='5432', database='test_bd', client_encoding='utf8')

# Bloque try
try:
    conexion.autocommit = False #Asignamos FALSE para que no se guarde de manera automática,
    #usar TRUE no es una buena práctica)
    cursor = conexion.cursor()
    sentencia = 'INSERT INTO persona(nombre, apellido, email) VALUES (%s, %s, %s)'
    valores = ('Maria', 'Esparza', 'mesparza@gmail.com')
    cursor.execute(sentencia, valores)
    conexion.commit()  #Hacemos commit manualmente
    print('Termina la transaccion')
# Excepción
except Exception as e:
    conexion.rollback()
    print(f'Ocurrió un error, se hizo un rollback: {e}.')
# Bloque finally
finally:
    # Cierre de la conexión de la base de datos
      conexion.close()