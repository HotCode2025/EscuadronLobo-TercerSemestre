# Importación de Base de Datos - Permite la conexión con PostgreSQL
import psycopg2 as bd

conexion = bd.connect(user='postgres', password='admin', host='127.0.0.1', port='5432', database='test_bd', client_encoding='utf8')

try:
    with conexion: #Agregamos el with para que todo suceda de manera automática
        with conexion.cursor() as cursor:
            sentencia = 'INSERT INTO persona(nombre, apellido, email) VALUES (%s, %s, %s)'
            valores = ('Alex', 'Rojas', 'arojas@gmail.com')
            cursor.execute(sentencia, valores)

            sentencia = 'UPDATE persona SET nombre=%s, apellido=%s, email=%s WHERE id_persona=%s'
            valores = ('Juan Carlos', 'Roldan', 'jcroldan@email.com', 1) #modifica el id_persona1
            cursor.execute(sentencia, valores) #incorpora sentencia y valores

except Exception as e:

    print(f'Ocurrió un error, se hizo un rollback: {e}.')

finally:
    # Cierre de la conexión de la base de datos
    conexion.close()
print('Termina la transaccion')