select InvoiceNo as 'Order', 
CustomerID as 'Customer',time1 as 'OrderDate',time2 AS 'FirstOrderDate',
datediff(time1,time2)gap from(
select
CustomerID,
InvoiceNo,
InvoiceDate as time1,
ROW_NUMBER() OVER(PARTITION BY CustomerID ORDER BY InvoiceDate) AS rank1,
FIRST_VALUE(InvoiceDate) OVER(PARTITION BY CustomerID ORDER BY InvoiceDate) AS time2
from OnlineRetail 
WHERE CustomerID is not NULL
GROUP BY InvoiceNo,CustomerID,InvoiceDate)a;


SELECT InvoiceNo,CustomerID,InvoiceDate 
FROM OnlineRetail WHERE CustomerID = '12352'
GROUP BY InvoiceNo,CustomerID,InvoiceDate; -- 15、30、35、7个月+




