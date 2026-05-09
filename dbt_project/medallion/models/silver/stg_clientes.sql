-- models/silver/stg_clientes.sql

SELECT DISTINCT
	UPPER(cliente_id)				AS cliente_id,
	nome,
	INITCAP(provincia)				AS provincia,
	INITCAP(tipo_conta)				AS tipo_conta,
	data_abertura::DATE				AS data_abertura,
	saldo_inicial_kz,
	CASE
		WHEN conta_ativa = 'Sim'
		THEN TRUE
		ELSE FALSE
	END								AS conta_ativa
FROM {{ source( 'bronze', 'clientes_raw' ) }}