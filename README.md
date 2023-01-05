# Diabetes Registers

*find the project on the next url*

The main objective for this project is to generate a CRUD which I can use to register my Glucose and Anxiety Levels in order to see if those variables are related. To achieve that I had to take the spreadsheet where I usually record the data, then transform that data and load it into a Postgres Database (ETL), create a CRUD where I can add more registers and finally, make an exploratory data analysis to find some relevant information.

## CRUD Directory

You will find the python code which allowed me to generate a program where I can Create, Read, Update and Delete registers. The CRUD is connected to a Database based in Postgresql named "aigda"; feel free to change the name. 

*Note; You will need the credential to connect to the Database.*

## EDA directory

Here you'll find all the Data Analysis starting with the data extraction from a Postgresql Database. The EDA is divided by Data Extraction, Data Validation, Diagnostic, Descriptive, Distributive, Probability and Predictive Analisys.

## ETL Directory

Here you'll find the load and transform process where I charged the data from an initial spreadsheet and the transformation of that data to normaliza the information.

Thanks for visiting this project.