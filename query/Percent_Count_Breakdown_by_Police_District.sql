/****** Script for SelectTopNRows command from SSMS  ******/

IF object_id('District Percentage Table', 'v') is not null
	DROP VIEW [District Percentage Table]

IF object_id('District Count Table', 'v') is not null
	DROP VIEW [District Count Table]

GO

CREATE VIEW [District Percentage Table] AS
SELECT	[Police District Number]
		,CONVERT(DECIMAL(15,5), 
			(CONVERT(DECIMAL(15,5), COUNT(*)*100) / (
				SELECT CONVERT(DECIMAL(15,5), COUNT(*)) FROM [dbo].[crime]))) AS [Incident Percentage]
FROM [dbo].[crime]
GROUP BY [Police District Number]

GO

CREATE VIEW [District Count Table] AS
SELECT	[Police District Number]
		,COUNT(*) AS [Number of Incidents]
FROM [dbo].[crime]
GROUP BY [Police District Number]

GO

SELECT	[District Count Table].[Police District Number]
		,[District Count Table].[Number of Incidents]
		,[District Percentage Table].[Incident Percentage]
FROM [District Count Table]
INNER JOIN [District Percentage Table] ON [District Count Table].[Police District Number]=[District Percentage Table].[Police District Number]
ORDER BY [District Count Table].[Police District Number]