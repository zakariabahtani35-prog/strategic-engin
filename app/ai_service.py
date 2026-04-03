import json
import logging
import time
from typing import Dict, Any
import google.generativeai as genai
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIIntelligenceEngine:
    """Production-ready wrapper for interacting with the Gemini Intelligence model."""
    
    def __init__(self):
        self.api_key = Config.GEMINI_API_KEY
        self.primary_model_name = Config.GEMINI_MODEL
        self.is_configured = False
        
        if self.api_key and "placeholder" not in self.api_key.lower():
            try:
                genai.configure(api_key=self.api_key)
                self.is_configured = True
            except Exception as e:
                logger.error(f"Failed to initialize Gemini library: {e}")

    def _get_working_model(self) -> str:
        """Dynamically finds a working model if the primary one is unavailable."""
        try:
            available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            
            # Check if primary exists
            primary_full = f"models/{self.primary_model_name}" if not self.primary_model_name.startswith("models/") else self.primary_model_name
            if self.primary_model_name in available_models or primary_full in available_models:
                return self.primary_model_name
                
            # Fallbacks
            for fallback in ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]:
                if fallback in available_models or f"models/{fallback}" in available_models:
                    logger.info(f"Primary model not found. Falling back to: {fallback}")
                    return fallback
                    
            if available_models:
                return available_models[0].replace("models/", "")
                
        except Exception as e:
            logger.warning(f"Could not list models: {e}")
            
        # Default back to primary if we can't fetch the list and hope for the best
        return self.primary_model_name

    def _structured_response(self, success: bool, error_type: str, error_message: str, raw_error: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Returns a stable, predictable dictionary for the frontend."""
        if data is None:
            data = {
                "short_summary": "Analysis failed or was bypassed.",
                "detailed_summary": f"System encountered an issue: {error_message}",
                "executive_summary": "No intelligence generated.",
                "main_topics": ["System Status"],
                "tasks": [],
                "risks": ["AI Pipeline Interruption"],
                "next_steps": ["Check API Configuration"]
            }
            
        return {
            "success": success,
            "error_type": error_type,
            "error_message": error_message,
            "raw_error": raw_error,
            "data": data
        }

    def analyze_meeting(self, transcript: str) -> Dict[str, Any]:
        """
        Sends transcript to Gemini for JSON extraction.
        Implements Retry Logic, Timeout Simulation, and robust Parsing.
        """
        if not self.is_configured:
            return self._structured_response(False, "AUTH_ERROR", "API Key not configured or invalid.", "Missing GEMINI_API_KEY")
            
        if not transcript or len(transcript.strip()) < 20:
            return self._structured_response(False, "VALIDATION_ERROR", "Transcript is too brief to analyze.", "Input < 20 chars")

        system_instruction = """
        You are a World-Class Executive Strategy Analyst and Decision Intelligence Engine. 
        Your goal is to transform meeting transcripts into actionable strategic intelligence.

        ROLE & OBJECTIVES:
        1. DECISION INTELLIGENCE: Identify every formal agreement or mandate. Assign a confidence score (0-100) based on how clearly it was stated. Detect ambiguity (e.g., lack of 'how' or 'when').
        2. PREDICTIVE RISK: For every task, predict the probability of failure (0-100) based on complexity and timeline. Flag potential bottlenecks.
        3. IMPACT ASSESSMENT: Rate the overall strategic impact of the session.

        OUTPUT FORMAT (CRITICAL):
        You MUST return ONLY a raw JSON dictionary without any markdown blocks (No ```json).
        
        SCHEMA:
        {
          "short_summary": "1 sentence brief.",
          "detailed_summary": "Contextual narrative (3-5 sentences).",
          "executive_summary": "Strategic impact and core takeaway.",
          "overall_sentiment": "Positive/Neutral/Negative/Contention",
          "strategic_score": 0-100,
          "main_topics": ["topic 1", "topic 2"],
          "decisions": [
            {
              "decision": "The formal agreement text",
              "owner": "Person responsible or 'Management'",
              "confidence_score": 0-100,
              "is_ambiguous": true/false,
              "ambiguity_reason": "Why it might fail due to lack of clarity",
              "impact_level": "Critical/High/Medium/Low"
            }
          ],
          "tasks": [
            {
              "task": "Action description",
              "assigned_to": "Name or 'Unassigned'",
              "deadline": "Date or 'Open'",
              "priority": "High/Medium/Low",
              "failure_probability": 0-100,
              "bottleneck_detected": true/false
            }
          ],
          "risks": [
            {
              "risk": "Risk description",
              "risk_level": "Critical/Moderate/Low",
              "prevention_strategy": "Mitigation steps"
            }
          ],
          "next_steps": ["logical next step 1"]
        }
        """
        
        model_name = self._get_working_model()
        logger.info(f"Targeting model: {model_name}")
        
        try:
            model = genai.GenerativeModel(model_name)
        except Exception as e:
            return self._structured_response(False, "MODEL_INIT_ERROR", "Failed to initialize generative model.", str(e))

        max_retries = 3
        last_error = ""

        # Retry Loop for Transient Errors / Timeouts
        for attempt in range(max_retries):
            try:
                logger.info(f"Execution attempt {attempt + 1}/{max_retries}...")
                
                # We enforce timeout at the application/library level if possible, 
                # but with google-generativeai wrapping requests natively handles reasonable limits.
                response = model.generate_content([system_instruction, f"TRANSCRIPT:\n{transcript}"])
                
                # Defensive clean up
                raw_text = response.text.strip()
                if raw_text.startswith("```json"):
                    raw_text = raw_text[7:-3].strip()
                elif raw_text.startswith("```"):
                    raw_text = raw_text[3:-3].strip()
                    
                parsed_data = json.loads(raw_text)
                
                # Defensive defaults mapping
                parsed_data.setdefault("short_summary", "Not provided")
                parsed_data.setdefault("detailed_summary", "Not provided")
                parsed_data.setdefault("executive_summary", "Not provided")
                parsed_data.setdefault("main_topics", [])
                parsed_data.setdefault("tasks", [])
                parsed_data.setdefault("risks", [])
                parsed_data.setdefault("next_steps", [])
                
                return self._structured_response(True, "NONE", "Intelligence successfully synthesized.", "", parsed_data)
                
            except json.JSONDecodeError as jde:
                logger.error(f"JSON Parsing failed: {jde}. Output: {raw_text}")
                last_error = f"JSONDecodeError: {str(jde)}"
                # If it's a parsing error, retrying might yield a better format
                
            except Exception as e:
                err_str = str(e)
                logger.error(f"Gemini API Exception: {err_str}")
                
                # Break immediately on critical auth/quota issues, do not retry
                if "403" in err_str or "API key" in err_str:
                    return self._structured_response(False, "AUTH_ERROR", "Access denied. Check your Gemini API Key.", err_str)
                if "429" in err_str or "quota" in err_str.lower():
                    return self._structured_response(False, "QUOTA_ERROR", "API Quota exceeded or rate limited.", err_str)
                if "404" in err_str or "not found" in err_str.lower():
                    return self._structured_response(False, "MODEL_ERROR", f"Requested model ({model_name}) is unavailable or deprecated.", err_str)
                    
                last_error = err_str
            
            # Wait before next attempt
            if attempt < max_retries - 1:
                time.sleep(2 * (attempt + 1))
                
        # If loop exhausts
        return self._structured_response(
            False, 
            "EXECUTION_FAILED", 
            "AI Service failed to respond properly after multiple attempts.", 
            last_error
        )

# Global singleton
ai_engine = AIIntelligenceEngine()
