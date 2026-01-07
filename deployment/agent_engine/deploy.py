# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import vertexai
import logging
from vertexai import agent_engines
from dotenv import load_dotenv, set_key, find_dotenv, unset_key
from adk_simple_drive.agent import root_agent
from vertexai.preview.reasoning_engines import AdkApp


load_dotenv()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

REQUIREMENTS_PATH = "requirements.txt"

def read_requirements(path):
    """Reads a requirements.txt file and returns a list of packages."""
    if not os.path.exists(path):
        print(f"🚨 Error: Requirements file not found at '{path}'")
        print("Please create the file and add your agent's dependencies.")
        return []
    with open(path) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]


vertexai.init(
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location=os.getenv("GOOGLE_CLOUD_LOCATION"),
    staging_bucket="gs://" + os.getenv("GOOGLE_CLOUD_PROJECT")+"-"+os.getenv("AGENT_ENGINE_NAME")+"",
)


requirements = read_requirements(REQUIREMENTS_PATH)
if not requirements:
    print("Deployment aborted due to missing requirements.")
else:
    print(f"Found {len(requirements)} packages in '{REQUIREMENTS_PATH}'.")

    logger.info("deploying app...")
    app = AdkApp(
        agent=root_agent,
        enable_tracing=True
    )

    logging.debug("deploying agent to agent engine:")

    remote_app = agent_engines.create(
        display_name=os.getenv("AGENT_ENGINE_NAME")+"-"+os.getenv("AGENT_VERSION"),
        description=os.getenv("GEMINI_ENT_AGENT_DESCRIPTION"),
        agent_engine=app,
        requirements=requirements,
        extra_packages = [
            "./adk_simple_drive",
        ],
    )

    env_file_path = ".env" 
    key_to_set = "AGENT_ENGINE_RESOURCE_NAME"
    # clean previous values
    unset_key(env_file_path, key_to_set)

    # set new agent resource name
    value_to_set = remote_app.resource_name
    set_key(env_file_path, key_to_set, value_to_set)

    logging.info(f"Deployed agent to Vertex AI Agent Engine successfully, resource name: {remote_app.resource_name}")
