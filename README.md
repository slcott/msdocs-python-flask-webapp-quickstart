# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react/README.md) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type aware lint rules:

- Configure the top-level `parserOptions` property like this:

```js
export default tseslint.config({
  languageOptions: {
    // other options...
    parserOptions: {
      project: ['./tsconfig.node.json', './tsconfig.app.json'],
      tsconfigRootDir: import.meta.dirname,
    },
  },
})
```

- Replace `tseslint.configs.recommended` to `tseslint.configs.recommendedTypeChecked` or `tseslint.configs.strictTypeChecked`
- Optionally add `...tseslint.configs.stylisticTypeChecked`
- Install [eslint-plugin-react](https://github.com/jsx-eslint/eslint-plugin-react) and update the config:

```js
// eslint.config.js
import react from 'eslint-plugin-react'

export default tseslint.config({
  // Set the react version
  settings: { react: { version: '18.3' } },
  plugins: {
    // Add the react plugin
    react,
  },
  rules: {
    // other rules...
    // Enable its recommended rules
    ...react.configs.recommended.rules,
    ...react.configs['jsx-runtime'].rules,
  },
})
```


## Notes


https://learn.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=flask%2Cmac-linux%2Cvscode-aztools%2Clocal-git-deploy%2Cdeploy-instructions-azportal%2Cterminal-bash%2Cdeploy-instructions-zip-azcli


## Setup 
Setup API
```shell
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  
deactivate
```

Test API
```shell
 .venv/bin/python3.12 -m pytest testing

 .venv/bin/python3.12 -m pytest -rP testing
```

Run backend API 
```shell
npm run start:api
```


Run frontend
```shell
npm run dev
```


## Links
https://blog.miguelgrinberg.com/post/how-to-create-a-react--flask-project
https://vite.dev/guide/
https://vite.dev/config/server-options#server-proxy


https://designsystem.digital.gov/


# Design

## Process data
The design doc that Vamshi created is called `P9 Mail Maximize System Design.pdf`.
It shows two components for processing data files, policy docs and emails.
The process for both of them is similar. To process the policy docs, it is necessary to call https://www.ecfr.gov/api/ to fetch data and then store in blob storage. To process the emails it is necessary to use Azure Graph API to read emails and then store in blob storage. 

### Create database
Create a database in Azure AI Search.
Use the following tables.


Emails
------
pk id
fk EmailThreads
fk EmailPolicies
blob url
send date
embedding vectors

Policies
--------
pk id
web url
policy blob url
embedding vectors

EmailThreads
-----------
pk id

Keywords
-------------
pk keyword

EmailKeywords
-------------
pk emailId, keyword

PolicyKeywords
-------------
pk policyId, keyword


### Populate the database with email data
Included below are steps with documentation or sample code.

Use an Azure Function to periodically fetch emails and store their metadata.
https://learn.microsoft.com/en-us/azure/azure-functions/

Trigger function using an Azure Function Timer
https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-timer

Fetch emails using Azure Graph
https://learn.microsoft.com/en-us/graph/overview

Use a custom vectorizer to calculate embeddings for email content
https://github.com/Azure/azure-search-vector-samples/blob/main/demo-python/code/custom-vectorizer/azure-search-custom-vectorization-sample.ipynb
https://github.com/Azure-Samples/azure-search-power-skills/blob/main/Vector/EmbeddingGenerator/README.md

It might be worth exploring other models to improved embedding performance.
https://www.bentoml.com/blog/a-guide-to-open-source-embedding-models

Calculate other metadata about the email
* Keywords
* Subject, date, recipients

Then store all of the data in the db and blob storage.

### Search database for email data
Create API endpoint using either flask full stack app or Azure functions.
API should allow user to search for emails with keywords, phrases, date ranges.
https://learn.microsoft.com/en-us/python/api/overview/azure/search-documents-readme?view=azure-python

The phrases should be vectorized and a similarity search can be performed using Azure AI Search SDK.

## Full stack app
Use Azure App Service to create a python web app.
Use the flask API because it is simple and easier to use than Django or FastAPI.
APIs can either call Azure SDKs directly to call Azure functions.
React frontend can query backend.

### Deployment
This is an example for heroku but something similar can be done in Azure.
https://freedium.cfd/https://towardsdatascience.com/build-deploy-a-react-flask-app-47a89a5d17d9


