# Análisis de logs de un servidor web con DuckDB

## Descripción

Proyecto de análisis de logs de un servidor web desarrollado con Python, SQL y DuckDB. El análisis permite estudiar el tráfico, los endpoints más utilizados, los errores del servidor y el rendimiento de las peticiones.

## Tecnologías usadas

* Python
* DuckDB
* SQL
* JSON
* Pandas

## Dataset

Los datos contienen información sobre las peticiones realizadas al servidor web, incluyendo:

* `log_id`
* `timestamp`
* `service_id`
* `server_id`
* `method`
* `endpoint`
* `status_code`
* `response_time_ms`
* `request_size_bytes`
* `response_size_bytes`
* `user_agent`
* `client_ip`
* `user_id`

## Análisis realizado

* Exploración inicial del número de registros, periodo temporal y usuarios únicos.
* Identificación de los endpoints más utilizados.
* Análisis de errores HTTP 500 por endpoint.
* Análisis del tiempo medio de respuesta y percentiles P50 y P95.
* Identificación de las peticiones más lentas.
* Análisis del tráfico y errores por hora.
* Comparación del tráfico entre días consecutivos.

## Resultados

* 5.000 registros analizados.
* 2.822 usuarios únicos.
* `/api/auth/login` es el endpoint más utilizado.
* `/api/payments` presenta el mayor número de errores HTTP 500.
* Los errores HTTP 500 presentan tiempos de respuesta significativamente superiores a las peticiones correctas.
* Los tiempos medios de las peticiones correctas se sitúan aproximadamente entre 238 y 265 ms.

## Recomendaciones

* Investigar las causas de los errores HTTP 500, especialmente en `/api/payments`, `/api/products` y `/api/orders`.
* Monitorizar los tiempos de respuesta mediante percentiles como P95 para detectar peticiones lentas.
* Establecer alertas para detectar incrementos anómalos de errores y tiempos de respuesta.

## Instalación

```bash
pip install duckdb
```

## Ejecución

```bash
python analisis_logs.py
```

## Autor

Juan Poma
