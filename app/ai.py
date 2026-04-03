import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def analyze_meeting(text):
    """
    Analyzes meeting text using Gemini AI to extract a summary and structured tasks.
    Returns a dictionary containing 'summary' and 'tasks'.
    """
    if not GEMINI_API_KEY:
        return {
            "summary": "Gemini API Key is missing. Please set GEMINI_API_KEY in your .env file.",
            "tasks": [
                {
                    "task": "Configure API Key",
                    "assigned_to": "User",
                    "deadline": "Immediate",
                    "priority": "High"
                }
            ]
        }

    # Enhanced internal prompt for high-quality extraction
    prompt = f"""
    You are a professional Meeting Intelligence AI. Your task is to process the following meeting transcript and convert it into structured executive data.

    TRANSCRIPT:
    \"\"\"{text}\"\"\"

    REQUIREMENTS:
    1. SUMMARY: Provide a high-level, 3-sentence summary of the meeting.
    2. TASKS: Extract every actionable item discussed. For each task:
       - 'task': Scientific, concise description starting with an action verb.
       - 'assigned_to': Name of the person responsible. Use 'Team' if general, or 'Unassigned' if unknown.
       - 'deadline': Specific date or relative time (e.g., 'Next Friday'). Default to 'N/A'.
       - 'priority': Categorize as 'High', 'Medium', or 'Low' based on urgency/importance.

    Strictly return a JSON object ONLY. Do not include any conversational text or markdown wrappers.

    JSON SCHEMA:
    {{
      "summary": "string",
      "tasks": [
        {{
          "task": "string",
          "assigned_to": "string",
          "deadline": "string",
          "priority": "High/Medium/Low"
        }}
      ]
    }}
    """

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        
        # Parse the JSON response
        clean_json = response.text.strip()
        
        # Remove potential markdown formatting
        if clean_json.startswith("```json"):
            clean_json = clean_json[7:-3].strip()
        elif clean_json.startswith("```"):
            clean_json = clean_json[3:-3].strip()
            
        data = json.loads(clean_json)
        
        # Basic validation of the structure
        if "summary" not in data: data["summary"] = "No summary provided."
        if "tasks" not in data: data["tasks"] = []
        
        return data
    except Exception as e:
        return {
            "summary": f"Failed to analyze text: {str(e)}",
            "tasks": []
        }
