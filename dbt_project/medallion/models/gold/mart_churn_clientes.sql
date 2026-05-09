-- models/gold/mart_churn_clientes.sql

SELECT
    cli.cliente_id,
    cli.nome,
    cli.provincia,
    cli.tipo_conta,
    cli.conta_ativa,
    COUNT(tra.transacao_id)  AS total_transacoes,
    SUM(tra.valor_kz)        AS valor_total_kz
FROM {{ ref('stg_clientes') }} AS cli
LEFT JOIN {{ ref('stg_transacoes') }} AS tra
ON cli.cliente_id = tra.cliente_id
WHERE cli.conta_ativa = false
GROUP BY
    cli.cliente_id,
    cli.nome,
    cli.provincia,
    cli.tipo_conta,
    cli.conta_ativa
ORDER BY cli.cliente_id
