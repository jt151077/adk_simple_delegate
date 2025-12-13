#!/bin/bash

# ... (Variable assignments are fine)
GOOGLE_CLOUD_PROJECT=$(grep '^GOOGLE_CLOUD_PROJECT=' .env | cut -d '=' -f 2-)
GOOGLE_CLOUD_PROJECT_NUMBER=$(grep '^GOOGLE_CLOUD_PROJECT_NUMBER=' .env | cut -d '=' -f 2-)
AUTH_ID=$(grep '^AUTH_ID=' .env | cut -d '=' -f 2-)


http_response=$(curl -X GET \
   -H "Authorization: Bearer $(gcloud auth print-access-token)" \
   -H "Content-Type: application/json" \
   -H "X-Goog-User-Project: ${GOOGLE_CLOUD_PROJECT}" \
   "https://discoveryengine.googleapis.com/v1alpha/projects/${GOOGLE_CLOUD_PROJECT_NUMBER}/locations/global/authorizations"
)


# ⚠️ The line below still attempts to execute the HTTP response as a command. 
# It should be replaced with 'echo "$http_response"' to just print it.
echo "$http_response"