-- models/gold/mart_transacoes_por_provincia.sql

SELECT
    provincia,
    COUNT(*)                    AS total_transacoes,
    SUM(valor_kz)               AS valor_total_kz,
    AVG(valor_kz)               AS valor_medio_kz,
    COUNT(DISTINCT cliente_id)  AS total_clientes
FROM {{ ref('stg_transacoes') }}
GROUP BY provincia
ORDER BY total_transacoes DESC