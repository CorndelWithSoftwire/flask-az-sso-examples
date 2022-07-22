# Azure SSO

An example of SSO set up with Azure, using the OAuth Code Flow with an Azure App Registration to restrict access to users attached to that tenant.

## Setting up the App Registration in Azure
To set up the App Registration appropriately, first sign into the Azure portal, and from there:
* Create an App Registration; give it an appropriate name and set a "Web" redirect URI to: `http://localhost:5000/login/azure/authorized`
* Note the tenant & client ids, and set them in a `.env` file following the `.env.template` pattern
* Generate a client secret under the "Certificates & secrets" tab, and set it in the `.env` file
* From the "API Permissions" tab, you should already have a permission added for "User.Read"
  * We will use this permission for now (through the `AZ_API_SCOPE` environment variable). If you need others, you can adjust them here

## The code
Two separate approaches are demonstrated below; we generally recommend using a library over writing the code yourself to take advantage of others learnings and avoid tripping points, but a more manual approach is also included for comparison.

### Handling the flow with MSAL (Microsoft Authentication Library)
See `src/app_msal.py` for the code for handling the flow with MSAL; this is [the documented recommended approach](https://github.com/Azure-Samples/ms-identity-python-webapp/), and there is a good (though more complex) example [available here for the authorization code flow](https://github.com/Azure-Samples/ms-identity-python-webapp/), or [other examples are available here for other flows](https://github.com/AzureAD/microsoft-authentication-library-for-python). 

### Handling the flow directly
See `src/app_manual.py` for the code for handling the flow fairly manually, similarly to how we handled OAuth in the project exercises. You should consider this carefully if you intend to use this for sensitive production instances, and should certainly look at extending it (e.g. [implementing state checking](https://medium.com/@alysachan830/the-basics-of-oauth-2-0-authorization-code-implicit-flow-state-and-pkce-ed95d3478e1c))

### Using Flask Dance
See `src/app_flask_dance` for the code handling the flow through Flask Dance - [for which more details can be found here](https://flask-dance.readthedocs.io/en/v1.0.0/quickstarts/azure.html).

### Running the code
To run the examples, the easiest approach is using Docker; simply set up the `.env` file and then run `docker compose up --build`: you should find the three apps are running locally on:
* Port 5001 - Manually handled approach
* Port 5002 - MSAL approach
* Port 5003 - Flask Dance approach