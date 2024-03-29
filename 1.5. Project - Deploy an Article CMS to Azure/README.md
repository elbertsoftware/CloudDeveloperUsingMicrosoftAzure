# Project - Deploy an Article CMS to Azure

This is a standard web application built with Flask and Python. It connects to backend database to store user information and post details. The app leverages Blob storage to keep post associated photos. So hosting the app can be straighforward:

1. A Python enabled environment
2. Ability to connect to SQL database and Blob storage on Azure platform
3. Authentication and authorization can be configured with Azure portal
4. Logging and monitoring can be done using Azure provided features

There are two hosting approaches can be considered:

1. Azure Virtual Machines (VM)
2. Azure App Services (AP)

Let see pros and cons from these approaches:

| Criteria |     VM     |     AP     | Choice |
|--------------|------------|------------|:-------------:|
| Python, Flask, remote debuging | Supported | Supported | VM, AP |
| Small footprint, less dependencies | Full control of server, can install any software packages and apply any hardware configuration | Easy to deploy, quickly replace new codebase and add new libraries | AP |
| Multi-tier web app, SSL endpoint access | Supported | Supported | VM, AP |
| Ability to connect to SQL Database, Blob Storage | Supported | Supported | VM, AP |
| Server security, OS patches/upgrades | Fully responsible | Fully managed by Azure | AP |
| Logging, monitoring | Fully responsible | Fully managed by Azure | AP |
| Scalability | Require configuring VM Scale Set or Load Balancer | Built-in service, integrated with Azure | AP |
| Availability | Single Instance Virtual Machine using Standard HDD Managed Disks for Operating System Disks and Data Disks: 95% | Apps running in a customer subscription: 99.95% | AP |
| Cost Effectiveness | Same configuration (1 Core, 1.75 GB RAM): $43.80/month | Same configuration (1 Core, 1.75 GB RAM): $13.14/month | AP |

![alt text](./screenshots/00.%20COST%20-%20VM%20vs.%20AP.png)

So AP gonna be the best choice for this type of web application

## Screenshots

### Create SQL server and Article CMS database

- User table:
![alt text](./screenshots/01.%20DB%20-%20Users%20Table.png)

- Post table:
![alt text](./screenshots/02.%20DB%20-%20Posts%20Table.png)

### Create BLOB storage and container to store images

- Storage endpoints:
![alt text](./screenshots/03.%20BLOB%20-%20Endpoints.png)

- Storage container "images":
![alt text](./screenshots/04.%20BLOB%20-%20Container.png)
 
### Deployment

- Use "az" command to deploy the web app to Azure:
  ```bash
  az webapp up --sku F1 -n articlecmsapp --resource-group test --location westus
  ```

- It can be accessed via the link: https://articlecmsapp.azurewebsites.net/
![alt text](./screenshots/05.%20APP%20-%20Login%20Screen.png)
![alt text](./screenshots/06.%20APP%20-%20Main%20Screen.png)
  
### Create new post

- Add a new post:
![alt text](./screenshots/07.%20APP%20-%20New%20Post.png)

- Verify image is uploaded and stored in the blob container:
![alt text](./screenshots/08.%20APP%20-%20Verify%20New%20Post.png)

### OAuth 2.0 - Signin with Microsoft
![alt text](./screenshots/09.%20APP%20-%20MSAL.png)

### Logging
![alt text](./screenshots/10.%20APP%20-%20Log%20Stream.png)

### Save logs to BLOB storage
![alt text](./screenshots/11.%20APP%20-%20Logs%20to%20Blob.png)

### Article CMS Resources
![alt text](./screenshots/00.%20RG%20-%20All%20Resources.png)

## Switching hosting solution

Since the web app not only works with independent resources, including database, blob storage, logging but also was deployed on an isolated Linux host machine on either App Service or Virtual Machine, so switching between them is very easy, just redeploy the app to any hosting service and reconfigure MSALL URIs to the new host:
![alt text](./screenshots/12.%20APP%20-%20Switching%20Host.png)