-- scripts/processar_dados.sql

-- A revisão do Copilot deve apontar que essa subquery pode ser transformada em CTE para otimização
SELECT
    t1.id_transacao,
    t1.valor,
    t1.data_processamento,
    t2.nome_cliente
FROM
    dados.transacoes t
INNER JOIN
    (
        SELECT id_cliente, nome_cliente
        FROM dados.clientes
        WHERE is_ativo = true
    ) t2 ON t1.id_cliente = t2.id_cliente
WHERE
    t1.data_processamento = date('${data_processamento}')
    AND t1.valor > 100.00;