-- Gets these information from Project database: 
-- order ID, the customer's first and last name, the customer city, state, the order date, 
-- quantity, revenue, product name, category name, brand name, store name, staff name

-- Gets staff_id, staff_name, store_name
select E.staff_id, concat(E.first_name, ' ', E.last_name) as staff_name, F.store_name
into #TempStaffStore
from sales.staffs E
join sales.stores F
on E.store_id = F.store_id

select * from #TempStaffStore

-- Gets order_id, customer_id, order_date, staff_name, store_name 
select order_id, customer_id, order_date, staff_name, store_name
into #Temp2
from sales.orders 
join #TempStaffStore
on sales.orders.staff_id = #TempStaffStore.staff_id

select * from #Temp2

-- Gets order_id, customer_id, order_date, staff_name, store_name, product_id, quantity, revenue
select T.order_id, customer_id, order_date, staff_name, store_name,
product_id, quantity, quantity*list_price*(1-discount) as revenue
into #Temp3
from #Temp2 T
join sales.order_items O
on T.order_id = O.order_id

select * from #Temp3

-- Gets order_id, customer_id, order_date, staff_name, store_name, product_id, quantity, revenue
-- customer's first_name and last_name, city, state

with cte as
(select customer_id, concat(first_name, ' ', last_name) as customer_name, city, state from sales.customers)

select order_id, cte.customer_id, order_date, staff_name, store_name, product_id, quantity, revenue, customer_name, city, state
into #Temp4
from cte
join #Temp3
on cte.customer_id = #Temp3.customer_id

select * from #Temp4
drop table #Temp4

-- gets product name, category name, brand name
select P.product_id, P.product_name, B.brand_name, C.category_name
into #Temp5
from production.products P
join production.categories C
on P.category_id = C.category_id
join production.brands B
on P.brand_id = B.brand_id

select * from #Temp5

-- gets all information we need 


select * from #Temp5
select * from #Temp4

select order_id, customer_name, city, state, order_date, quantity, revenue, product_name, category_name, brand_name, store_name,
staff_name
from #Temp4
join #Temp5
on #Temp4.product_id = #Temp5.product_id
order by order_id









