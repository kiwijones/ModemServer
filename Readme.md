Required install modules
pip install colorama
pip install serial
pip install pyserial
pip install pyodbc
pip install pandas
pip install sqlalchemy
pip install requests




begin transaction qq
	declare @requestId int
	insert into [dbo].[tbl_GATEWAY_FlexyRequests]([AccountId],[SupplierId],[ModemID],[PhoneNumber],[Amount],[RefNumber],[Status])
	values(13000,3,0,'0560195955',100,'',0)
	set @requestId = @@IDENTITY

	update [dbo].[tbl_GATEWAY_FlexyTransactions]
	set [RequestId] = @requestId
	where [TransactionID] = 5676

	select * from [dbo].[tbl_GATEWAY_FlexyRequests]
	select * from [dbo].[tbl_GATEWAY_FlexyTransactions]
	where [TransactionID] = 5676


--ROLLBACK transaction qq
commit transaction qq
