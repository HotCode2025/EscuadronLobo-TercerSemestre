# Importación de Base de Datos - Permite la conexión con PostgreSQL
import psycopg2 as bd

conexion = bd.connect(user='postgres', password='admin', host='127.0.0.1', port='5432', database='test_bd', client_encoding='utf8')

# Bloque try
try:
    conexion.autocommit = False #esto directamente no deberia estar.Inicia la transaccion
    cursor = conexion.cursor()
    sentencia = 'INSERT INTO persona(nombre, apellido, email) VALUES (%s, %s, %s)'
    valores = ('Jorge', 'Prol', 'jprol@gmail.com')
    cursor.execute(sentencia, valores)

    sentencia = 'UPDATE persona SET nombre=%s, apellido=%s, email=%s WHERE id_persona=%s'
    valores = ('Juan Carlos', 'Perez', 'jcperez@email.com', 1) #modifica el id_persona1
    cursor.execute(sentencia, valores) #incorpora sentencia y valores

    conexion.commit()  # Hacemos commit manualmente, se cierra la transaccion
    print('Termina la transaccion')
# Excepción
except Exception as e:
    conexion.rollback()
    print(f'Ocurrió un error, se hizo un rollback: {e}.')
# Bloque finally
finally:
    # Cierre de la conexión de la base de datos

    conexion.close()
    #Clase 6 Parte 6
    #en BD postgre, columnas, apellido cambiamos la longitud de caracteres
    #en el apellido. Si colocamos algun apellido >10 caracteres no se modifica nada