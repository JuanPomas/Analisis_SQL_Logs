#Importamos Duckdb
import duckdb

# Conectar a Duckdb
con = duckdb.connect()

#Cargamos de datos
con.execute('''
CREATE TABLE logs AS
SELECT * FROM read_json_auto('Datos segundo proyecto/data/logs_access_logs.json');
''')

#Comprobación de carga de los datos, estructura de estos y observación
print("=" * 60)
print('Carga de datos')
print("=" * 60)
print(
    con.execute('''
    SELECT COUNT(*) AS numero_registros
    FROM logs;
    ''').fetchdf()
)

print("=" * 60)
print('Estructura de los datos')
print("=" * 60)
print(
    con.execute('''
    DESCRIBE logs;
    ''').fetchdf())

print("=" * 60)
print('Observación de los datos')
print("=" * 60)
print(
    con.execute('''
    SELECT *
    FROM logs
    LIMIT 3;
    ''').fetchdf()
)

#Exploración inicial: ¿Cuántos datos hay? ¿Qué periodo abarca? ¿Cuantos usuarios únicos hay?
print("=" * 60)
print('Exploración de datos')
print("=" * 60)
print(
    con.execute('''
    SELECT
        COUNT(*) AS numero_registros,
        MIN(timestamp) AS fecha_inicial,
        MAX(timestamp) AS fecha_final,
        COUNT(DISTINCT user_id) AS usuarios_unicos
    FROM logs;
    ''').fetchdf()
)

#¿Cuáles son los endpoints más usados?
print("=" * 60)
print('Endpoint más usados y porcentaje')
print("=" * 60)
print(
    con.execute('''
    SELECT
        endpoint,
        COUNT(*) AS cantidad,
        ROUND(COUNT(*) * 100 / (SELECT COUNT(*) FROM logs),2) AS porcentaje
    FROM logs
    GROUP BY endpoint
    ORDER BY cantidad DESC;
    ''').fetchdf()
)

#Si el status_code es igual a 500, esto significa que hay errores crítcos.
#¿Cuáles son los endpoint que presentan estos errores, su tiempo medio de respuesta y los usuarios afectados?
print("=" * 60)
print('Endpoint afectados por errores')
print("=" * 60)
print(
    con.execute('''
    SELECT
        endpoint,
        COUNT(*) AS cantidad,
        COUNT(DISTINCT user_id) AS numero_usuarios,
        ROUND(AVG(response_time_ms),2) AS tiempo_medio_respuesta
    FROM logs
    WHERE status_code = '500'
    GROUP BY endpoint
    ORDER BY cantidad DESC;
    ''').fetchdf()
)

#¿Cómo es el rendimiento de los endpoints?
print("=" * 60)
print('Rendimiento de los endpoints sin errores')
print("=" * 60)
print(
    con.execute('''
    SELECT
        endpoint,
        COUNT(*) AS cantidad,
        ROUND(AVG(response_time_ms),2) AS tiempo_medio,
        PERCENTILE_CONT(0.5) WITHIN GROUP(ORDER BY response_time_ms) AS percentil_50,
        PERCENTILE_CONT(0.95) WITHIN GROUP(ORDER BY response_time_ms) AS percentil_95,
        MAX(response_time_ms) AS tiempo_maximo
    FROM logs
    WHERE status_code < 500
    GROUP BY endpoint
    ORDER BY cantidad DESC;
    ''').fetchdf()
)

#¿Cuál es el tráfico medio existente por horas?
print("=" * 60)
print('Tráfico existente por horas')
print("=" * 60)
print(
    con.execute('''
    SELECT
        EXTRACT(HOUR FROM timestamp) AS horas,
        COUNT(*) AS cantidad,
        ROUND(AVG(response_time_ms),2) AS tiempo_medio_respuesta,
        SUM(CASE WHEN status_code = 500 THEN 1 ELSE 0 END) AS numero_errores
    FROM logs
    GROUP BY EXTRACT(HOUR FROM timestamp)
    ORDER BY horas;
    ''').fetchdf()
)

#¿Cuáles son los endpoints más lentos, sin tener en cuenta los errores?
print("=" * 60)
print('Endpoints más lentos por fecha')
print("=" * 60)
print(
    con.execute('''
    WITH ranking AS (
    SELECT
        endpoint,
        timestamp,
        response_time_ms,
        user_id,
        ROW_NUMBER() OVER(PARTITION BY endpoint ORDER BY response_time_ms DESC) AS rango
    FROM logs
    WHERE status_code < 500
    )
    SELECT *
    FROM ranking
    WHERE rango <= 3
    ORDER BY endpoint,rango
    ''').fetchdf()
)

#Comparación de trafico con día anterior y tiempo medio
print("=" * 60)
print('Comparación día anterior')
print("=" * 60)
print(
    con.execute('''
    WITH comparacion AS (
    SELECT
        DATE(timestamp) AS fecha,
        COUNT(*) AS cantidad,
        ROUND(AVG(response_time_ms),2) AS tiempo_medio
    FROM logs
    GROUP BY DATE(timestamp)
    )
    SELECT
        fecha,
        cantidad,
        LAG(cantidad) OVER(ORDER BY fecha) AS cantidad_anterior,
        cantidad - LAG(cantidad) OVER(ORDER BY fecha) AS diferencia,
        ROUND((cantidad - LAG(cantidad) OVER(ORDER BY fecha)) * 100 / LAG(cantidad) OVER(ORDER BY fecha),2) AS cambio_porcentual
    FROM comparacion
    ORDER BY fecha;
    ''').fetchdf()
)