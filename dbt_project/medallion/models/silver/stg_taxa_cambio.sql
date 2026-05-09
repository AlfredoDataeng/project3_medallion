-- models/silver/stg_taxa_cambio.sql

SELECT DISTINCT
	moeda_base 					AS moeda_base,
	moeda_destino 				AS moeda_destino,
	taxa 						AS taxa,
	data::TIMESTAMP 			AS data
FROM {{ source( 'bronze', 'taxas_cambio_raw' ) }}
WHERE moeda_destino IN ('AOA', 'EUR')
