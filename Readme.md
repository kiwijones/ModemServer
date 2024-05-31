Required install modules
pip install colorama
pip install serial
pip install pyserial
pip install pyodbc
pip install pandas
pip install sqlalchemy
pip install requests
pip install pika

use [etl]

--declare @amount int = 10000
--declare @phoneNo varchar(12) = '0560195955'  -- for b2b
--declare @simTypeId int = 1

declare @amount int = 100
declare @phoneNo varchar(12) = '0558135017 '  -- for b2c
declare @simTypeId int = 2

begin transaction qq
	declare @requestId int
	insert into [dbo].[tbl_GATEWAY_FlexyRequests]([AccountId],[SupplierId],[ModemID],[PhoneNumber],[Amount],[RefNumber],[Status])
	values(13000,3,0,@phoneNo,@amount,'',0)
	set @requestId = @@IDENTITY

INSERT INTO [dbo].[tbl_GATEWAY_FlexyTransactions]
           ([RequestId]
           ,[SessionId]
           ,[SupplierId]
           ,[ModemID]
           ,[PhoneNumber]
           ,[Amount]
           ,[RefNumber]
           ,[Inserted]
           ,[FlexyResponseId]
           ,[FlexyResponseMessage]
           ,[ProductId]
           ,[StockTransactionId]
           ,[DeviceId]
           ,[BalanceBefore]
           ,[BalanceAfter]
           ,[Retry]
           ,[SimTypeId])
     VALUES
           (@requestId
           ,123456
           ,3
           ,0
           ,@phoneNo
           ,@amount
           ,'reff 001'
           ,getdate()
           ,1
           ,''
           ,24
           ,0
           ,0
           ,0
           ,0
           ,0
           ,@simTypeId
		   )
GO



	select * from [dbo].[tbl_GATEWAY_FlexyRequests]
	select top 1 * from [dbo].[tbl_GATEWAY_FlexyTransactions]
	order by [TransactionID] desc
	


--ROLLBACK transaction qq
commit transaction qq
