-- models/gold/mart_resumo_cambio.sql

SELECT
	moeda_destino AS moeda,
	taxa 		  AS taxa,
	data 		  AS data
FROM {{ ref('stg_taxa_cambio') }}