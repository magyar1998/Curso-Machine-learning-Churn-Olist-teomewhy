-- Prever se o vendedor vai ficar sem vender nos proximos 3 meses

with tb_primeira_venda as (
    
        select  t2.seller_id,
        julianday('2017-04-01') - julianday(date(min(t1.order_approved_at))) as idade_base

        from tb_orders as t1

        left join tb_order_items as t2
        on t1.order_id = t2.order_id


        where t1.order_status = "delivered" and
        t1.order_approved_at >= "2016-10-01" and
        t1.order_approved_at < "2017-04-01" 


        group by t2.seller_id

)

select t2.seller_id,
       sum(t2.price) as receita_total,
       count(distinct t2.order_id) as quantidade_vendas,
       sum(t2.price) / count(DISTINCT t2.order_id) as ticket_medio,
       count(t2.product_id) as qtd_produto,
       count(distinct t2.product_id) as qtd_produto_diferentes,
       sum(t2.price) / count(t2.product_id) as media_vl_produto,
       count(t2.product_id) / count(distinct  t2.order_id) as qtd_avg_produto_venda,
       t3.idade_base,
       min (1 + cast (t3.idade_base / 30 as int), 6) as idade_mensal_base,
       sum(t2.price)  / min (1 + cast (t3.idade_base / 30 as int), 6) as receita_total_mensal_na_base,
       sum(t2.price) / 6 as receita_total_mensal,
       count(distinct strftime('%m', t1.order_approved_at)) as qtd_meses_ativado,
       sum(t2.price)  / count(distinct strftime('%m', t1.order_approved_at)) as receita_total_mensal_ativado,
       cast (count(distinct strftime('%m', t1.order_approved_at)) as float) / min (1 + cast (t3.idade_base / 30 as int), 6) as proporcao_ativado


from tb_orders as t1

left join tb_order_items as t2
on t1.order_id = t2.order_id

left join tb_primeira_venda as t3
on t2.seller_id = t3.seller_id


where t1.order_status = "delivered" and
t1.order_approved_at >= "2016-10-01" and
t1.order_approved_at < "2017-04-01" 


group by t2.seller_id


limit 10