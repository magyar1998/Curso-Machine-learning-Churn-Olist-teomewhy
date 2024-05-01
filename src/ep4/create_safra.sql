with tb_venda_target_sellers as (

    select distinct t2.seller_id

    from tb_orders as t1

    left join tb_order_items as t2
    on t1.order_id = t2.order_id

    where   t1.order_status = "delivered" and
            t1.order_approved_at >= "2017-04-01" and
            t1.order_approved_at < "2017-07-01" 
)

select  t1.*,
        case when t2.seller_id is not null then 1 else 0 end as target_seller 

from tb_book_sellers as t1

left join tb_venda_target_sellers as t2
on t1.seller_id = t2.seller_id

limit 10