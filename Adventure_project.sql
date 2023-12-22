--DATABASE: Adventure
-- sau khi nhập dữ liệu từ file CSV, nhiều cột có kiểu dữ liệu không hợp lý, có thể thay đổi bằng cách dùng lệnh:
ALTER TABLE table_name 
ALTER COLUMN column_name data_type


--Lấy 2 bảng thông tin: 
--Bảng Sales_info (gồm Order Date, Product Name, Category, Subcategory, Quantity, Profit, Customer Name, Customer Gender, Country) của 3 năm
--Bảng Returns_info ( Product Name, TotalOrder, TotalReturn, Return ratio)
--Dữ liệu thu được sẽ được lưu vào 2 sheets trong 1 file Excel

-- BẢNG Sales_info 

-- Gộp 3 bảng Sales_2015, Sales_2016, Sales_2017

with cte1 as
(select * from Sales_2015
union select * from Sales_2016
union select * from Sales_2017)

--join cte1 với bảng Products để lấy các thông tin OrderDate, ProductName, ProductSubcategoryKey, OrderQuantity, Profit

select OrderDate, ProductName, ProductSubcategoryKey, OrderQuantity, (ProductPrice-ProductCost)*OrderQuantity as Profit,
CustomerKey, TerritoryKey into #Temp1
from cte1
join Products
on cte1.ProductKey = Products.ProductKey

select * from #Temp1

-- Tạo cte2 lấy các thông tin ProductSubcategoryKey, SubcategoryName, CategoryName
with cte2 as 
(select ProductSubcategoryKey, SubcategoryName, CategoryName 
from Subcategories S
join Categories C
on S.ProductCategoryKey = C.ProductCategoryKey)

--Bảng Sales_info (gồm Order Date, Product Name, Category, Subcategory, Quantity, Profit, Customer Name, Customer Gender, Country) của 3 năm

select OrderDate, ProductName, SubcategoryName, CategoryName, OrderQuantity, Profit,
concat(FirstName, ' ', LastName) as CustomerName, Gender, Country into #Temp2
from cte2
join #Temp1 on cte2.ProductSubcategoryKey = #Temp1.ProductSubcategoryKey
join Territories on Territories.SalesTerritoryKey = #Temp1.TerritoryKey
join Customers on Customers.CustomerKey = #Temp1.CustomerKey

select * from #Temp2

--BẢNG Returns_info (gồm Product Name, TotalOrder, TotalReturn, Return ratio)

----Tạo cte để gộp 3 bảng Sales_2015, Sales_2016, Sales_2017
with cte1 as
(select * from Sales_2015
union select * from Sales_2017
union select * from Sales_2016)

----tạo bảng tạm #Temp4 chứa ProductName, TotalOrder
select ProductName, Sum(OrderQuantity) as TotalOrder into #Temp4
from cte1 
join Products
on cte1.ProductKey = Products.ProductKey
group by ProductName

select * from #Temp4

----Tạo bảng tạm #Temp5 chứa ProductName, TotalReturn
select ProductName, Sum(ReturnQuantity) as TotalReturn into #Temp5
from Returns 
join Products 
on Returns.ProductKey = Products.ProductKey
group by ProductName

select * from #Temp5

---- join 2 bảng tạm #Tem4 và #Temp5 để lấy đầy đủ các cột cần thiết. 
---- Khi tính ReturnRatio cần chuyển TotalOrder và TotalReturn về kiểu dữ liệu Float, kết quả làm tròn đến 2 chữ số thập phân
select #Temp4.ProductName, TotalOrder, TotalReturn, round((cast(TotalReturn as float)/(cast (TotalOrder as float))), 2) as ReturnRatio
from #Temp4
join #Temp5
on #Temp4.ProductName = #Temp5.ProductName
