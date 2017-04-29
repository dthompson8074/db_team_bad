/****** Script for SelectTopNRows command from SSMS  ******/
/*
SELECT TOP (1000) [Incident ID]
      ,[Dispatch Date   Time]
      ,[Class]
      ,[Class Description]
      ,[Police District Name]
      ,[Block Address]
      ,[City]
      ,[State]
      ,[Zip Code]
      ,[Agency]
      ,[Place]
      ,[Start Date   Time]
  FROM [dbo].[crime]
  */

/*Drop that view if it exists, son!*/
IF object_id('Percentage Table', 'v') is not null
	DROP VIEW [Percentage Table]

GO

/*Drop that view if it exists, daughter!*/
IF object_id('Count Table', 'v') is not null
	DROP VIEW [Count Table]

GO

/*Need those percentages? Well, I got you covered, bro!*/
CREATE VIEW [Percentage Table] AS
SELECT	[City]
		,[Class Description]
		,CONVERT(DECIMAL(15,5), 
			(CONVERT(DECIMAL(15,5), COUNT([Class])*100) / (
				SELECT CONVERT(DECIMAL(15,5), COUNT(*)) FROM [dbo].[crime]))) AS [Incident Percentage]
FROM [dbo].[crime]
GROUP BY [City], [Class Description]

GO

/*What do you mean "count the number of incidents!" Oh wait, I can do that in no time!*/
CREATE VIEW [Count Table] AS
SELECT	[City]
		,[Class Description]
		,COUNT([Class]) AS [Number of Incidents]
FROM [dbo].[crime]
GROUP BY [City], [Class Description]

GO

/*What?! You need to see both of those tables in action?! Well, I got you covered!*/
SELECT	[Count Table].[City]
		,[Count Table].[Class Description]
		,[Count Table].[Number of Incidents]
		,[Percentage Table].[Incident Percentage]
FROM [Count Table]
INNER JOIN [Percentage Table] ON [Count Table].[Class Description]=[Percentage Table].[Class Description] AND [Count Table].[City]=[Percentage Table].[City]
ORDER BY [Count Table].[City], [Count Table].[Number of Incidents] DESC

/*Show that View!*/
/*
SELECT SUM([Incident Percentage]) AS Total FROM [Percentage Table]
*/

/*Show Those Percentages!*/
/*
SELECT * FROM [Percentage Table]
ORDER BY [Incident Percentage] DESC
*/

/*Show That Count!*/
/*
SELECT * FROM [Count Table]
ORDER BY [Number of Incidents] DESC
*/
