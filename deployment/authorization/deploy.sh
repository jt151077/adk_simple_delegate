#!/bin/bash

# ... (Variable assignments are fine)
GOOGLE_CLOUD_PROJECT=$(grep '^GOOGLE_CLOUD_PROJECT=' .env | cut -d '=' -f 2-)
GOOGLE_CLOUD_PROJECT_NUMBER=$(grep '^GOOGLE_CLOUD_PROJECT_NUMBER=' .env | cut -d '=' -f 2-)
GEMINI_ENT_REGION=$(grep '^GEMINI_ENT_REGION=' .env | cut -d '=' -f 2-)
CLIENT_ID=$(grep '^CLIENT_ID=' .env | cut -d '=' -f 2-)
CLIENT_SECRET=$(grep '^CLIENT_SECRET=' .env | cut -d '=' -f 2-)
AUTH_ID=$(grep '^AUTH_ID=' .env | cut -d '=' -f 2-)


echo "$GOOGLE_CLOUD_PROJECT"
echo "$GOOGLE_CLOUD_PROJECT_NUMBER"
echo "$GEMINI_ENT_REGION"
echo "$AUTH_ID"


http_response=$(curl -X POST \
-H "Authorization: Bearer $(gcloud auth print-access-token)" \
-H "Content-Type: application/json" \
-H "X-Goog-User-Project: ${GOOGLE_CLOUD_PROJECT}" \
"https://discoveryengine.googleapis.com/v1alpha/projects/${GOOGLE_CLOUD_PROJECT}/locations/${GEMINI_ENT_REGION}/authorizations?authorizationId=${AUTH_ID}" \
-d @- <<EOF
{
  "name": "projects/${GOOGLE_CLOUD_PROJECT}/locations/${GEMINI_ENT_REGION}/authorizations/${AUTH_ID}",
    "serverSideOauth2": {
      "clientId": "${CLIENT_ID}", 
      "clientSecret": "${CLIENT_SECRET}",
      "authorizationUri": "https://accounts.google.com/o/oauth2/v2/auth?client_id=${CLIENT_ID}&redirect_uri=https%3A%2F%2Fvertexaisearch.cloud.google.com%2Fstatic%2Foauth%2Foauth.html&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fdrive%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcloud-platform&include_granted_scopes=true&response_type=code&access_type=offline&prompt=consent",
      "tokenUri": "https://oauth2.googleapis.com/token"
    }
}
EOF
)


# ⚠️ The line below still attempts to execute the HTTP response as a command. 
# It should be replaced with 'echo "$http_response"' to just print it.
echo "$http_response"