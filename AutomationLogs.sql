CREATE DATABASE RPADatabase;
GO

USE RPADatabase;
GO

CREATE TABLE AutomationLogs (
    TaskID INT IDENTITY(1,1) PRIMARY KEY,
    TargetURL NVARCHAR(255),
    ExecutionStatus NVARCHAR(50),
    ItemsProcessed INT,
    ExecutionDate DATETIME DEFAULT GETDATE(),
    DurationSeconds FLOAT
);
GO

Select * From AutomationLogs;