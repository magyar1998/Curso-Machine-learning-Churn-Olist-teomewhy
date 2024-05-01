-- Prever se o vendedor vai ficar sem vender nos proximos 3 meses
drop table if exists tb_book_sellers;
create table tb_book_sellers as 

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

        ),

        tb_ultima_venda as (
        
                select  t2.seller_id,
                julianday('2017-04-01') - julianday(date(max(t1.order_approved_at))) as tempo_ultima_venda

                from tb_orders as t1

                left join tb_order_items as t2
                on t1.order_id = t2.order_id


                where t1.order_status = "delivered" and
                t1.order_approved_at >= "2016-10-01" and
                t1.order_approved_at < "2017-04-01" 


                group by t2.seller_id

        )

        select  t2.seller_id,     
                t5.seller_state,
                t5.seller_city,
                avg (t7.review_score) as avg_score,
                sum (case when t6.product_category_name =  'cama_mesa_banho' then 1 else 0 end ) as qtd_cama_mesa_banho,
                sum (case when t6.product_category_name =  'moveis_decoracao' then 1 else 0 end ) as qtd_moveis_decoracao,
                sum (case when t6.product_category_name =  'beleza_saude' then 1 else 0 end ) as qtd_beleza_saude,
                sum (case when t6.product_category_name =  'esporte_lazer' then 1 else 0 end ) as qtd_esporte_lazer,
                sum (case when t6.product_category_name =  'informatica_acessorios' then 1 else 0 end ) as qtd_informatica_acessorios,
                sum (case when t6.product_category_name =  'utilidades_domesticas' then 1 else 0 end ) as qtd_utilidades_domesticas,
                sum (case when t6.product_category_name =  'relogios_presentes' then 1 else 0 end ) as qtd_relogios_presentes,
                sum (case when t6.product_category_name =  'ferramentas_jardim' then 1 else 0 end ) as qtd_ferramentas_jardim,
                sum (case when t6.product_category_name =  'telefonia' then 1 else 0 end ) as qtd_telefonia,
                sum (case when t6.product_category_name =  'automotivo' then 1 else 0 end ) as qtd_automotivo,
                sum (case when t6.product_category_name =  'brinquedos' then 1 else 0 end ) as qtd_brinquedos,
                sum (case when t6.product_category_name =  'cool_stuff' then 1 else 0 end ) as qtd_cool_stuff,
                sum (case when t6.product_category_name =  'perfumaria' then 1 else 0 end ) as qtd_perfumaria,
                sum (case when t6.product_category_name =  'bebes' then 1 else 0 end ) as qtd_bebes,
                sum (case when t6.product_category_name =  'eletronicos' then 1 else 0 end ) as qtd_eletronicos,
                sum (case when t6.product_category_name =  'papelaria' then 1 else 0 end ) as qtd_papelaria,
                sum (case when t6.product_category_name =  'moveis_escritorio' then 1 else 0 end ) as qtd_moveis_escritorio,
                sum (case when t6.product_category_name =  'pet_shop' then 1 else 0 end ) as qtd_pet_shop,
                sum (case when t6.product_category_name =  'fashion_bolsas_e_acessorios' then 1 else 0 end ) as qtd_fashion_bolsas_e_acessorios,
                sum (case when t6.product_category_name =  'construcao_ferramentas_construcao' then 1 else 0 end ) as qtd_construcao_ferramentas_construcao,
                sum (case when t6.product_category_name =  'consoles_games' then 1 else 0 end ) as qtd_consoles_games,
                sum (case when t6.product_category_name =  'malas_acessorios' then 1 else 0 end ) as qtd_malas_acessorios,
                sum (case when t6.product_category_name =  'casa_construcao' then 1 else 0 end ) as qtd_casa_construcao,
                sum (case when t6.product_category_name =  'eletrodomesticos' then 1 else 0 end ) as qtd_eletrodomesticos,
                sum (case when t6.product_category_name =  'instrumentos_musicais' then 1 else 0 end ) as qtd_instrumentos_musicais,
                sum (case when t6.product_category_name =  'eletroportateis' then 1 else 0 end ) as qtd_eletroportateis,
                sum (case when t6.product_category_name =  'moveis_sala' then 1 else 0 end ) as qtd_moveis_sala,
                sum (case when t6.product_category_name =  'livros_interesse_geral' then 1 else 0 end ) as qtd_livros_interesse_geral,
                sum (case when t6.product_category_name =  'alimentos' then 1 else 0 end ) as qtd_alimentos,
                sum (case when t6.product_category_name =  'bebidas' then 1 else 0 end ) as qtd_bebidas,
                sum (case when t6.product_category_name =  'casa_conforto' then 1 else 0 end ) as qtd_casa_conforto,
                sum (case when t6.product_category_name =  'construcao_ferramentas_iluminacao' then 1 else 0 end ) as qtd_construcao_ferramentas_iluminacao,
                sum (case when t6.product_category_name =  'audio' then 1 else 0 end ) as qtd_audio,
                sum (case when t6.product_category_name =  'market_place' then 1 else 0 end ) as qtd_market_place,
                sum (case when t6.product_category_name =  'telefonia_fixa' then 1 else 0 end ) as qtd_telefonia_fixa,
                sum (case when t6.product_category_name =  'alimentos_bebidas' then 1 else 0 end ) as qtd_alimentos_bebidas,
                sum (case when t6.product_category_name =  'climatizacao' then 1 else 0 end ) as qtd_climatizacao,
                sum (case when t6.product_category_name =  'moveis_cozinha_area_de_servico_jantar_e_jardim' then 1 else 0 end ) as qtd_moveis_cozinha_area_de_servico_jantar_e_jardim,
                sum (case when t6.product_category_name =  'industria_comercio_e_negocios' then 1 else 0 end ) as qtd_industria_comercio_e_negocios,
                sum (case when t6.product_category_name =  'sinalizacao_e_seguranca' then 1 else 0 end ) as qtd_sinalizacao_e_seguranca,
                sum (case when t6.product_category_name =  'construcao_ferramentas_jardim' then 1 else 0 end ) as qtd_construcao_ferramentas_jardim,
                sum (case when t6.product_category_name =  'fashion_calcados' then 1 else 0 end ) as qtd_fashion_calcados,
                sum (case when t6.product_category_name =  'livros_tecnicos' then 1 else 0 end ) as qtd_livros_tecnicos,
                sum (case when t6.product_category_name =  'agro_industria_e_comercio' then 1 else 0 end ) as qtd_agro_industria_e_comercio,
                sum (case when t6.product_category_name =  'construcao_ferramentas_seguranca' then 1 else 0 end ) as qtd_construcao_ferramentas_seguranca,
                sum (case when t6.product_category_name =  'eletrodomesticos_2' then 1 else 0 end ) as qtd_eletrodomesticos_2,
                sum (case when t6.product_category_name =  'pcs' then 1 else 0 end ) as qtd_pcs,
                sum (case when t6.product_category_name =  'artes' then 1 else 0 end ) as qtd_artes,
                sum (case when t6.product_category_name =  'artigos_de_natal' then 1 else 0 end ) as qtd_artigos_de_natal,
                sum (case when t6.product_category_name =  'fashion_roupa_masculina' then 1 else 0 end ) as qtd_fashion_roupa_masculina,  
                sum(t2.price) as receita_total,
                count(distinct t2.order_id) as quantidade_vendas,
                sum(t2.price) / count(distinct t2.order_id) as ticket_medio,
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
                cast (count(distinct strftime('%m', t1.order_approved_at)) as float) / min (1 + cast (t3.idade_base / 30 as int), 6) as proporcao_ativado,
                sum(case when julianday (date(t1.order_estimated_delivery_date)) < julianday (date (t1.order_delivered_customer_date)) then 1 else 0 end) as qtd_atrasos,
                sum(case when julianday (date(t1.order_estimated_delivery_date)) < julianday (date (t1.order_delivered_customer_date)) then 1 else 0 end) / cast (count(distinct t2.order_id) as float) as prop_atrasos,
                cast (avg (julianday (t1.order_delivered_customer_date) - julianday(t1.order_purchase_timestamp)) as INt) as avg_entrega,
                t4.tempo_ultima_venda

        from tb_orders as t1

        left join tb_order_items as t2
        on t1.order_id = t2.order_id

        left join tb_primeira_venda as t3
        on t2.seller_id = t3.seller_id

        left join tb_ultima_venda as t4
        on t2.seller_id = t4.seller_id

        left join tb_sellers as t5
        on t2.seller_id = t5.seller_id

        left join tb_products as t6
        on t2.product_id = t6.product_id

        left join tb_order_reviews as t7
        on t1.order_id = t7.order_id


        where t1.order_status = "delivered" and
        t1.order_approved_at >= "2016-10-01" and
        t1.order_approved_at < "2017-04-01" 


        group by t2.seller_id
;



