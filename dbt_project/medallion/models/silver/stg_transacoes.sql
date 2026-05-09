-- models/siver/transacoes.sql

SELECT DISTINCT
	UPPER(transacao_id)                          AS transacao_id,
	UPPER(cliente_id)                            AS cliente_id,
	INITCAP(tipo_transacao)                      AS tipo_transacao,
	valor_kz,
	CASE
        WHEN data_transacao LIKE '__/__/____%'
        THEN TO_TIMESTAMP(data_transacao, 'DD/MM//YYYY HH24:MI')
        ELSE TO_TIMESTAMP(data_transacao, 'YYYY-MM-DD HH24:MI:SS')
    END                                         AS data_transacao,
	canal,
	INITCAP(status)                             AS status,
	INITCAP(provincia)                          AS provincia,
	INITCAP(tipo_conta)                         AS tipo_conta
FROM {{ source( 'bronze', 'transacoes_raw' ) }}
WHERE valor_kz > 0