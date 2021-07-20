# TechConf Registration Website

## Project Overview
The TechConf website allows attendees to register for an upcoming conference. Administrators can also view the list of attendees and notify all attendees via a personalized email message.

The application is currently working but the following pain points have triggered the need for migration to Azure:
 - The web application is not scalable to handle user load at peak
 - When the admin sends out notifications, it's currently taking a long time because it's looping through all attendees, resulting in some HTTP timeout exceptions
 - The current architecture is not cost-effective 

In this project, you are tasked to do the following:
- Migrate and deploy the pre-existing web app to an Azure App Service
- Migrate a PostgreSQL database backup to an Azure Postgres database instance
- Refactor the notification logic to an Azure Function via a service bus queue message

## Dependencies

You will need to install the following locally:
- [Postgres](https://www.postgresql.org/download/)
- [Visual Studio Code](https://code.visualstudio.com/download)
- [Azure Function tools V3](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Ccsharp%2Cbash#install-the-azure-functions-core-tools)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Azure Tools for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-node-azure-pack)

## Project Instructions

### Part 1: Create Azure Resources and Deploy Web App
1. Create a Resource group `techconf`
2. Create an Azure Postgres Database:
   - Use Azure Portal to create new single server `techconfdbserver`:
     ![alt text](./screenshots/01.%20Postgres%20Server.png)

   - Allow all IPs to connect to database server:
     ![alt text](./screenshots/02.%20Allow%20All%20IPss.png)

   - [Add a new database](https://docs.microsoft.com/en-us/azure/postgresql/quickstart-create-server-database-portal) `techconfdb` using `pgAdmin4`:
     ``` bash
     host: techconfdbserver.postgres.database.azure.com
     port: 5432
     database name: postgres
     username: dbadmin@techconfdbserver
     ```
     ![alt text](./screenshots/03.%20pgAdmin4%20-%20Connect%20to%20Azure%20DB.png)
     ![alt text](./screenshots/04.%20pgAdmin4%20-%20Create%20Database.png)

   - Restore the database with the backup located in the data folder using `pgAdmin4`:
     ![alt text](./screenshots/05.%20pgAdmin4%20-%20Restore.png)

3. Create a Service Bus resource `techconfservicebus` with a `notificationqueue` that will be used to communicate between the web and the function:
   ![alt text](./screenshots/06.%20Notification%20Service%20Bus%20&%20Queue.png)

4. Open the web folder and update the following in the `config.py` file
   - `POSTGRES_URL`
   - `POSTGRES_USER`
   - `POSTGRES_PW`
   - `POSTGRES_DB`
   - `SERVICE_BUS_CONNECTION_STRING`
  
5. Create App Service plan `techconfappservice`:
   ![alt text](./screenshots/07.%20App%20Service%20Plan.png)

6. Create Azure Web App `techconfwebapp` under the App Service Plan `techconfappservice`:
   ![alt text](./screenshots/08.%20Web%20App.png)

7. Create a storage account `techconfstorageaccount`:
   ![alt text](./screenshots/09.%20Storage.png)

8. Deploy the web app:
   - Open `web` subfolder in Visual Studio Code
   - Select `Deploy to Web App...` 
   - Pick `techconfwebapp` from the list
   ![alt text](./screenshots/10.%20Atttendees%20Registration%20List.png)
   ![alt text](./screenshots/11.%20Email%20Notification%20List.png)

### Part 2: Create and Publish Azure Function
1. Create an Azure Function `techconffuncapp` in the `function` folder
2. Add a new function `notificationQueueTrigger` in type of `serviceBusTrigger` 
3. Update __init__.py with required business logic
4. Publish the Azure Function
   ![alt text](./screenshots/12.%20Function%20App.png)
   ![alt text](./screenshots/13.%20Service%20Bus%20Trigger.png)
### Part 3: Refactor `routes.py`
1. Refactor the post logic in `web/app/routes.py -> notification()` using servicebus `queue_client`:
   - The notification method on POST should save the notification object and queue the notification id for the function to pick it up
2. Re-deploy the web app to publish changes

## Monthly Cost Analysis
Complete a month cost analysis of each Azure resource to give an estimate total cost using the table below:

| Azure Resource            | Service Tier                   | Monthly Cost |
| ------------------------- | ------------------------------ | ------------:|
| *Azure Postgres Database* | *Basic, Gen 5, 2 vCores, 5 GB* | *$65.08*     |
| *Azure Service Bus*       | *Basic, 1 million messages*    | *$0.05*      |
| *Azure App Service*       | *F1, 60 minutes/day compute*   | *$0.00*      |
| *Azure Storage*           | *Standard, 1 GB*               | *$0.14*      |
| *Azure Function*          | *Consumption*                  | *$0.00*      |
|                           | Total:                         | *$65.27*      |

## Architecture Explanation
The Techconf is a simple web application which needs less than 14 GB of RAM and 4 virtual CPU so Azure App Service/Web App fits perfectly in terms of performance and cost. The selection still reserve the capability to scale out if needed in the future.

Sending notifications to attendees is not required immediate process, it can be off-loaded to Azure Service Bus queue and use Service Bus Trigger of Azure Function to send emails later. This approach can help the web app perform better.

The web app only needs basic RDBMS, Azure Postgres Database is the less expensive option. With the same configuration, Azure SQL Database costs $391.10 and Azure MySQL Database costs $150.19 per month.

SendGrid API is the most robust I have been using for years when it comes to sending emails. It is widely integrated within Azure built-in and custom solutions.
