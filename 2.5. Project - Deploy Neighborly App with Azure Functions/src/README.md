# Deploying the Neighborly App with Azure Functions

## Project Overview

For the final project, we are going to build an app called "Neighborly". Neighborly is a Python Flask-powered web application that allows neighbors to post advertisements for services and products they can offer.

The Neighborly project is comprised of a front-end application that is built with the Python Flask micro framework. The application allows the user to view, create, edit, and delete the community advertisements.

The application makes direct requests to the back-end API endpoints. These are endpoints that we will also build for the server-side of the application.

You can see an example of the deployed app below.

![Deployed App](../images/final-app.png)

## Dependencies

You will need to install the following locally:

- [Pipenv](https://pypi.org/project/pipenv/)
- [Visual Studio Code](https://code.visualstudio.com/download)
- [Azure Function tools V3](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Ccsharp%2Cbash#install-the-azure-functions-core-tools)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Azure Tools for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-node-azure-pack)

On Mac, you can do this with:

```bash
# install pipenv
brew install pipenv

# install azure-cli
brew update && brew install azure-cli

# install azure function core tools 
brew tap azure/functions
brew install azure-functions-core-tools@3

# get the mongodb library
brew tap mongodb/brew
brew install mongodb-community@4.4

brew link --overwrite mongodb-community
brew link --overwrite mongodb-database-tools

# check if mongoimport lib exists
mongod --version
mongoimport --version
```

## Project Instructions

In case you need to return to the project later on, it is suggested to store any commands you use so you can re-create your work. You should also take a look at the project rubric to be aware of any places you may need to take screenshots as proof of your work (or else keep your resource up and running until you have passed, which may incur costs).

### I. Creating Azure Function App

We need to set up the Azure resource group, region, storage account, and an app name before we can publish.

1. Create a resource group - `test`

2. Create a storage account (within the previously created resource group and region) - `neighborlystorage`

3. Create an Azure Function App within the resource group, region and storage account. 
   - Note that app names need to be unique across all of Azure.
   - Make sure it is a Linux app, with a Python runtime.

    Example of successful output, if creating the app `neighborlyapp`:

    ```bash
    Your Linux function app 'myneighborlyapi', that uses a consumption plan has been successfully created but is not active until content is published using Azure Portal or the Functions Core Tools.
    ```

4. Set up a Cosmos DB Account - `neighborlycosmos`. You will need to use the same resource group, region and storage account, but can name the Cosmos DB account as you prefer. **Note:** This step may take a little while to complete (15-20 minutes in some cases).

5. Create a MongoDB Database - `neighborlydb` - in CosmosDB Azure and two collections, one for `advertisements` and one for `posts`.

6. Print out your connection string or get it from the Azure Portal. Copy/paste the **primary connection** string.  You will use it later in your application.

    Example connection string output:
    
    ```bash
    bash-3.2$ Listing connection strings from COSMOS_ACCOUNT:
    + az cosmosdb keys list -n neighborlycosmos -g neighborlyapp --type connection-strings
    {
    "connectionStrings": [
        {
        "connectionString": "AccountEndpoint=https://neighborlycosmos.documents.azure.com:443/;AccountKey=xxxxxxxxxxxx;",
        "description": "Primary SQL Connection String"
        },
        {
        "connectionString": "AccountEndpoint=https://neighborlycosmos.documents.azure.com:443/;AccountKey=xxxxxxxxxxxxx;",
        "description": "Secondary SQL Connection String"
        } 
        
        ... [other code omitted]
    ]
    }
    ```

7. Sample Data Into MongoDB: Use Visual Studio Code Azure extension Database tab to import

8. Hook up your connection string into the NeighborlyAPI server folder. You will need to replace the *url* variable with your own connection string you copy-and-pasted in the last step, along with some additional information.
    - Tip: Check out [this post](https://docs.microsoft.com/en-us/azure/cosmos-db/connect-mongodb-account) if you need help with what information is needed.
    - Go to each of the `__init__.py` files in getPosts, getPost, getAdvertisements, getAdvertisement, deleteAdvertisement, updateAdvertisement, createAdvertisements and replace your connection string. You will also need to set the related `database` and `collection` appropriately.

    ```bash
    # inside getAdvertisements/__init__.py

    def main(req: func.HttpRequest) -> func.HttpResponse:
        logging.info('Python getAdvertisements trigger function processed a request.')

        try:
            # copy/paste your primary connection url here
            #-------------------------------------------
            url = ""
            #--------------------------------------------

            client=pymongo.MongoClient(url)

            database = None # Feed the correct key for the database name to the client
            collection = None # Feed the correct key for the collection name to the database

            ... [other code omitted]
            
    ```

    Make sure to do the same step for the other 6 HTTP Trigger functions.

9. Deploy your Azure Functions.

    1. Test it out locally first.

        ```bash
        # cd into NeighborlyAPI
        cd NeighborlyAPI

        # install dependencies (--skip-lock is needed when running on macOSSpip)
        pipenv install --skip-lock

        # go into the shell (use 'exit' to deactivate the environment)
        pipenv shell

        # cd into NeighborlyAPI again
        cd NeighborlyAPI
        
        # test func locally
        func start
        ```

        You may need to change `"IsEncrypted"` to `false` in `local.settings.json` if this fails.

        At this point, Azure functions are hosted in localhost:7071.  You can use the browser or Postman to see if the GET request works.  For example, go to the browser and type in: 

        ```bash
        # example endpoint for all advertisements
        http://localhost:7071/api/getadvertisements

        #example endpoint for all posts
        http://localhost:7071/api/getposts
        ```

    2. Now you can deploy functions to Azure by publishing your function app.

        The result may give you a live url in this format, or you can check in Azure portal for these as well:

        Expected output if deployed successfully:
        
        ```bash
        Functions in <APP_NAME>:
            createAdvertisement - [httpTrigger]
                Invoke url: https://<APP_NAME>.azurewebsites.net/api/createadvertisement

            deleteAdvertisement - [httpTrigger]
                Invoke url: https://<APP_NAME>.azurewebsites.net/api/deleteadvertisement

            getAdvertisement - [httpTrigger]
                Invoke url: https://<APP_NAME>.azurewebsites.net/api/getadvertisement

            getAdvertisements - [httpTrigger]
                Invoke url: https://<APP_NAME>.azurewebsites.net/api/getadvertisements

            getPost - [httpTrigger]
                Invoke url: https://<APP_NAME>.azurewebsites.net/api/getpost

            getPosts - [httpTrigger]
                Invoke url: https://<APP_NAME>.azurewebsites.net/api/getposts

            updateAdvertisement - [httpTrigger]
                Invoke url: https://<APP_NAME>.azurewebsites.net/api/updateadvertisement

        ```

        **Note:** It may take a minute or two for the endpoints to get up and running if you visit the URLs.

        Save the function app url **https://<APP_NAME>.azurewebsites.net/api/** since you will need to update that in the client-side of the application:

        ```bash
        createAdvertisement: https://neighborlyapp.azurewebsites.net/api/createadvertisement
        deleteAdvertisement: https://neighborlyapp.azurewebsites.net/api/deleteadvertisement
        getAdvertisement: https://neighborlyapp.azurewebsites.net/api/getadvertisement
        getAdvertisements: https://neighborlyapp.azurewebsites.net/api/getadvertisements
        getPost: https://neighborlyapp.azurewebsites.net/api/getpost
        getPosts: https://neighborlyapp.azurewebsites.net/api/getposts
        updateAdvertisement: https://neighborlyapp.azurewebsites.net/api/updateadvertisemen
        ```

### II. Deploying the client-side Flask web application

We are going to update the Client-side `settings.py` with published API endpoints. First navigate to the `settings.py` file in the NeighborlyFrontEnd/ directory.

Use a text editor to update the API_URL to your published url from the last step.

```bash
# Inside file settings.py

# ------- Local Testing -------
# for local host if Azure functions served locally
# API_URL = "http://localhost:7071/api"

# ------- Production -------
# for serverless function app deployment
# API_URL = "https://neighborlyapp.azurewebsites.net/api"

# for Azure Kubernetes Service deployment
API_URL = "http://137.135.15.55/api"
```

Start the client app locally

- Change to `NeighborlyFrontEnd` folder
- Install dependencies with `pipenv install`
- Go into the pip env shell with `pipenv shell`
- Execute `python app.py`
- Navigate to `http://localhost:5000/`

### III. CI/CD Deployment

1. Deploy your client app. **Note:** Use a **different** app name here to deploy the front-end, or else you will erase your API. From within the `NeighborlyFrontEnd` directory:
    
    - Deploy your application to the app service. **Note:** It may take a minute or two for the front-end to get up and running if you visit the related URL.

    Make sure to also provide any necessary information in `settings.py` to move from localhost to your deployment.

    ```bash
    az webapp up \
        --location westus \
        --resource-group test \
        --plan neighborlyclient \
        --name neighborlyclient \
        --os-type Linux \
        --sku FREE
    ```

    - Get the app URL and navigate to it `https://neighborlyclient.azurewebsites.net/`
  
2. Create an Azure `Container Registry` called `ebsrepo` in Azure Portal and dockerize your Azure Functions. Then, push the container to the Azure Container Registry:
   
   - Create Dockerfile:
    
     ```bash
     cd NeighborlyAPI
     func init --docker-only
     ```
   
   - Verify `docker` CLI installed:
  
     ```bash
     docker version
     ```

   - Build docker image for the NeighborlyAPI function app:

     ```bash
     docker image build --tag neighborlyapi .
     ```
   
   - Test the image locally:

     ```bash
     docker run -p 8080:80 -it neighborlyapi
     ```
     
   - Create new registry if not done via Azure portal:

     ```bash
     az acr create --resource-group test --name ebsrepo --sku Basic
     ```

   - Log into the registry and make sure the registry is available:
     
     ```bash
     az acr login --name ebsrepo
     az acr show --name ebsrepo --query loginServer --output table
     ```

   - Tag the container to the newly created registry:
     
     ```bash
     docker image tag neighborlyapi ebsrepo.azurecr.io/neighborlyapi
     ```

   - Push the image to the registry:
  
     ```bash
     docker push ebsrepo.azurecr.io/neighborlyapi
     ```

   - Check if the docker image is up in the cloud.:
  
     ```bash
     az acr repository list --name ebsrepo --output table
     ```

3. Create a Kubernetes cluster aka. `AKS - Azure Kubernates Service` called `neighborlycluster` in Azure Portal, and verify your connection to it with `kubectl get nodes`:
   
   - Verify `kubectl` CLI installed:
  
     ```bash
     kubectl version
     ```

   - Create a Kubernetes cluster on Azure if not done via Azure portal:

     ```bash
     az aks create \
        --resource-group test \
        --name ebsrepo \
        --node-count 1 \
        --enable-addons monitoring \
        --generate-ssh-keys
     ```
   
   - Get your credentials for AKS:

     ```bash
     az aks get-credentials --name neighborlycluster --resource-group test
     ```

   - Verify the connection to your cluster with the command:
     ```bash
     kubectl get nodes
     ```

4. Deploy app to Kubernetes, and check your deployment with `kubectl config get-contexts`.

   - KEDA is Google's opensource tool for Kubernetes event-driven Autoscaling. Let's set up the KEDA namespace for our Kubernetes cluster:

     ```bash
     func kubernetes install --namespace keda
     ```
     
   - Deploy the function app to container registry (optional):
     
     ```bash
     func deploy \
        --platform kubernetes \
        --name neighborlyapi \
        --registry ebsrepo
     ```

   - Dry-run the deployment of the function app in order to review deploy.yml:    
  
     ```bash
     func kubernetes deploy --name neighborlycluster --image-name ebsrepo.azurecr.io/neighborlyapi --dry-run > deploy.yml
     ```
   
   - Deploy the function app to Kubernetes cluster:
  
     ```bash
     func kubernetes deploy --name neighborlycluster --image-name ebsrepo.azurecr.io/neighborlyapi -—polling-interval 3 —-cooldown-period 5

     createAdvertisement - [httpTrigger]
        Invoke url: http://137.135.15.55/api/createadvertisement

     deleteAdvertisement - [httpTrigger]
        Invoke url: http://137.135.15.55/api/deleteadvertisement

     getAdvertisement - [httpTrigger]
        Invoke url: http://137.135.15.55/api/getadvertisement

     getAdvertisements - [httpTrigger]
        Invoke url: http://137.135.15.55/api/getadvertisements

     getPost - [httpTrigger]
        Invoke url: http://137.135.15.55/api/getpost

     getPosts - [httpTrigger]
        Invoke url: http://137.135.15.55/api/getposts

     updateAdvertisement - [httpTrigger]
        Invoke url: http://137.135.15.55/api/updateadvertisement

     Master key: kq/PBQNYmpO1gNGd4pieCdB44cX9WTXBHbUGO4EYNEGDO9D4UeVULg==
     ```

   - Verify the deployment:

     ```bash
     kubectl get service --watch

     kubectl config get-contexts
     ```

### IV. Event Hubs and Logic App

1. Create a Logic App that watches for an HTTP trigger. When the HTTP request is triggered, send yourself an email notification.
2. Create a namespace for event hub in the portal. You should be able to obtain the namespace URL.
3. Add the connection string of the event hub to the Azure Function.

### V.  Cleaning Up Your Services

Before completing this step, make sure to have taken all necessary screenshots for the project! Check the rubric in the classroom to confirm.

Clean up and remove all services, or else you will incur charges.

```bash
# replace with your resource group
RESOURCE_GROUP="<YOUR-RESOURCE-GROUP>"
# run this command
az group delete --name $RESOURCE_GROUP

kubectl delete deploy <name-of-function-deployment>
kubectl delete ScaledObject <name-of-function-deployment>
kubectl delete secret <name-of-function-deployment>
```