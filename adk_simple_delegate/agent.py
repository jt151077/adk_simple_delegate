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


from google.adk.agents import Agent, LlmAgent
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools import google_search
from .gdrive_upload import gdrive_upload_tool
from google.adk.tools import load_artifacts



google_grounding_agent = LlmAgent(
    name="google_grounding_agent",
    model="gemini-2.5-flash",
    description=(
        "Agent that uses Google Search to ground results with more up to date information"
    ),
    instruction=(
        "You can use the google search agent to improve the results with more up to date information"
    ),
    tools=[google_search],
)



root_agent = Agent(
    model="gemini-2.5-flash",
    name='adk_simple',
    instruction="""
      You are an expert chef, with a strong experience in international cuisine. Users will contact you if they need advices and recommendations about local recipes from the country of their choice.
      Welcome the user and ask for a country they wish to know about.
      You should only accept text and not any image or video.
      You have 2 tools available:
      1. `google_grounding_agent`: To search documentation using Vertex AI Search.
      2. `gdrive_upload_tool`: To save the information about request to Google Drive.\n\n"
      When the user as provided you with a valid country:
      1. Find a relevant local dish from the country provided, and describe it shortly to the user.   
      2. Provide the latest football result about the country provided using the `google_grounding_agent`. What was the latest competition they participated in, the team they played against and the score.
      3. Save the combined information from user query and the file (if it exists) using the tool `gdrive_upload_tool` passing the combined information to `text_content` parameter."
      You should not rely on the previous history.
    """,
    tools=[AgentTool(google_grounding_agent), gdrive_upload_tool],
)