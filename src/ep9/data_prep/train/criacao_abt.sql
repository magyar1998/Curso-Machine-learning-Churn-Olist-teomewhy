
drop table if exists tb_abt_churn;
create table tb_abt_churn as 

with tb_venda_sellers as (

    select 
        strftime('%Y-%m', t1.order_approved_at) || '-01' as dt_venda,
        t2.seller_id,
        max(0) as venda
        
    from tb_orders as t1

    left join tb_order_items as t2
    on t1.order_id = t2.order_id

    where order_approved_at is not null 
    and seller_id is not null 
    and order_status = 'delivered'


    group by  t1.order_approved_at , t2.seller_id
), 



tb_venda_range as (

select
    t1.dt_ref,
    t1.seller_id,
    t2.dt_venda,
    t2.venda
from tb_book_sellers as t1


left join tb_venda_sellers as t2
on t1.seller_id = t2.seller_id and t2.dt_venda between t1.dt_ref and date(t1.dt_ref, '+2 months') 

group by t2.dt_venda, t1.seller_id

order by t1.dt_ref


),

tb_target as (

select 

t1.dt_ref,
t1.seller_id,
min(coalesce(t1.venda, 1)) as flag_compra

from tb_venda_range as t1

group by t1.seller_id, t1.dt_ref 

)


select 

    t1.*,
    t2.*

from tb_target as t1

left join tb_book_sellers as t2
on t1.seller_id = t2.seller_id and
t1.dt_ref = t2.dt_ref
;
