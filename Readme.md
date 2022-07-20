# Azure SSO

An example of SSO set up with Azure, using the OAuth Code Flow with an Azure App Registration to restrict access to users attached to that tenant.

## Setting up the App Registration in Azure
To set up the App Registration appropriately, first sign into the Azure portal, and from there:
* Create an App Registration; give it an appropriate name and set a "Web" redirect URI to: `http://localhost:5000/auth/redirect`
* Note the tenant & client ids, and set them in a `.env` file following the `.env.template` pattern
* Generate a client secret under the "Certificates & secrets" tab, and set it in the `.env` file
* From the "Expose an API" tab:
  * Click "set" to generate an Application ID URI
  * Add a scope for reading user details, give it a sensible name/description for reading the user's identity, and allow both Admins & Users to consent
* From the "API Permissions" tab, you should already have a permission added for "User.Read"
  * Grant consent for it using the "Grant admin consent for <Tenant>" option

## The code

### Handling the flow directly
See `src/app.py` for the code for handling the flow fairly manually, simialrly to how we handled OAuth in the project exercises.

### Using Flask Dance


### Using something else