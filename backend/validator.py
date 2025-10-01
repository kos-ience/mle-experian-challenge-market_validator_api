from openai import OpenAI
import json
import os
import logging
from typing import Dict, Any
from .models import ValidationResponse, ValidationIssue, ValidationCategory
import re

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketplaceValidator:
    def __init__(self, api_key: str = None):
        logger.info("🔧 Initializing MarketplaceValidator...")
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            logger.error("❌ OpenAI API key not found in environment")
            raise ValueError("OpenAI API key is required")
        
        logger.info("✅ OpenAI API key found, creating client...")
        self.client = OpenAI(api_key=self.api_key)
        
        # Load the validation prompt
        logger.info("📋 Loading validation prompt...")
        self.validation_prompt = self._load_validation_prompt()
        logger.info("✅ MarketplaceValidator initialized successfully")
    
    def _load_validation_prompt(self) -> str:
        """Load the validation prompt from the marketplace_validator_prompt.txt file"""
        try:
            with open('/Users/sachinkosepaul/Desktop/Mine/mle-genai-marketplace-validator-1/marketplace_validator_prompt.txt', 'r') as f:
                base_prompt = f.read()
            
            # Add structured output instructions
            structured_output_instruction = """

IMPORTANT: You must respond with a valid JSON object in the following format:

{
    "status": "compliant" or "non_compliant",
    "compliance_score": <float between 0-10>,
    "issues": [
        {
            "category": "<one of: Regulatory & Compliance, Content Quality, User Experience, Brand & Tone Alignment, Prohibited Language, Ethical Standards>",
            "rule_violated": "<specific rule name>",
            "current_text": "<exact text from listing that violates the rule>",
            "issue": "<description of the issue>",
            "suggested_fix": "<specific suggested replacement>",
            "severity": "<low, medium, or high>"
        }
    ],
    "suggestions": "<overall suggestions for improvement>",
    "word_count": <number of words in the listing>,
    "reading_level": "<estimated reading level>"
}

Only return the JSON object, no other text.
"""
            
            return base_prompt + structured_output_instruction
        except FileNotFoundError:
            # Fallback prompt if file not found
            return self._get_fallback_prompt()
    
    def _get_fallback_prompt(self) -> str:
        """Fallback validation prompt"""
        return """You are an AI validator for credit card marketplace listings. Validate the listing against these standards:

1. Regulatory & Compliance: APR disclosure, fee transparency, credit requirements
2. Content Quality: Clear language, proper grammar, completeness
3. User Experience: Appropriate length (100-300 words), readability
4. Brand & Tone: Professional, factual, not overly promotional
5. Prohibited Language: No misleading claims, exaggerated superlatives, vague terms
6. Ethical Standards: Inclusive language, fair representation

Return a JSON object with validation results in the specified format."""

    def _calculate_word_count(self, text: str) -> int:
        """Calculate word count of the listing"""
        return len(text.split())
    
    def _estimate_reading_level(self, text: str) -> str:
        """Simple reading level estimation based on sentence and word length"""
        sentences = text.split('.')
        words = text.split()
        
        if not sentences or not words:
            return "Unknown"
        
        avg_sentence_length = len(words) / len([s for s in sentences if s.strip()])
        avg_word_length = sum(len(word) for word in words) / len(words)
        
        # Simple heuristic
        if avg_sentence_length > 20 or avg_word_length > 6:
            return "Grade 12+"
        elif avg_sentence_length > 15 or avg_word_length > 5:
            return "Grade 10-12"
        else:
            return "Grade 8 or below"

    def validate_listing(self, listing: str) -> ValidationResponse:
        """Validate a credit card listing against marketplace standards"""
        logger.info("🔍 Starting validation for listing...")
        logger.info(f"📝 Listing preview: {listing[:100]}{'...' if len(listing) > 100 else ''}")
        
        try:
            # Prepare the prompt with the listing
            logger.info("🔄 Preparing prompt with listing content...")
            full_prompt = self.validation_prompt.replace("{{ listing }}", listing)
            logger.info(f"📊 Full prompt length: {len(full_prompt)} characters")
            
            # Get response from OpenAI
            logger.info("🤖 Calling OpenAI API...")
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a marketplace validator that analyzes credit card listings for compliance. Always respond with valid JSON only."},
                    {"role": "user", "content": full_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.1,
                max_tokens=2000
            )
            response_text = response.choices[0].message.content.strip()
            
            logger.info("✅ Received response from OpenAI")
            logger.info(f"📄 LLM Response length: {len(response_text)} characters")
            logger.info("🔍 Raw LLM Response:")
            logger.info("-" * 50)
            logger.info(response_text)
            logger.info("-" * 50)
            
            # Try to parse JSON response
            try:
                logger.info("🧹 Cleaning up response text...")
                original_length = len(response_text)
                
                # Clean up response text - remove markdown code blocks if present
                if response_text.startswith('```json'):
                    logger.info("📝 Removing '```json' markdown formatting...")
                    response_text = response_text.replace('```json', '').replace('```', '').strip()
                elif response_text.startswith('```'):
                    logger.info("📝 Removing '```' markdown formatting...")
                    response_text = response_text.replace('```', '').strip()
                
                if len(response_text) != original_length:
                    logger.info(f"✂️ Cleaned response: {original_length} → {len(response_text)} characters")
                
                logger.info("🔄 Parsing JSON response...")
                validation_data = json.loads(response_text)
                logger.info("✅ JSON parsing successful!")
                logger.info(f"📊 Parsed data keys: {list(validation_data.keys())}")
                
                # Add calculated fields
                logger.info("🔢 Adding calculated metadata...")
                validation_data['word_count'] = self._calculate_word_count(listing)
                if 'reading_level' not in validation_data or not validation_data['reading_level']:
                    validation_data['reading_level'] = self._estimate_reading_level(listing)
                    logger.info(f"📖 Calculated reading level: {validation_data['reading_level']}")
                
                logger.info("✅ Creating ValidationResponse object...")
                result = ValidationResponse(**validation_data)
                logger.info(f"🎯 Final validation score: {result.compliance_score}/10")
                logger.info(f"📝 Status: {result.status}")
                logger.info(f"🔍 Issues found: {len(result.issues)}")
                return result
                
            except json.JSONDecodeError as e:
                logger.error(f"❌ JSON parsing failed: {str(e)}")
                logger.error(f"🔍 Problematic response: {response_text[:200]}...")
                logger.info("🔄 Using fallback response...")
                return self._create_fallback_response(listing, response_text)
                
        except Exception as e:
            logger.error(f"💥 System error during validation: {str(e)}")
            logger.error(f"🔍 Error type: {type(e).__name__}")
            logger.info("🛡️ Creating emergency fallback response...")
            # Error handling
            return ValidationResponse(
                status="non_compliant",
                compliance_score=0.0,
                issues=[
                    ValidationIssue(
                        category=ValidationCategory.CONTENT_QUALITY,
                        rule_violated="System Error",
                        current_text="N/A",
                        issue=f"Validation failed: {str(e)}",
                        suggested_fix="Please try again or contact support",
                        severity="high"
                    )
                ],
                suggestions="System error occurred during validation. Please try again.",
                word_count=self._calculate_word_count(listing),
                reading_level=self._estimate_reading_level(listing)
            )
    
    def _create_fallback_response(self, listing: str, llm_response: str) -> ValidationResponse:
        """Create a fallback response when JSON parsing fails"""
        return ValidationResponse(
            status="non_compliant",
            compliance_score=5.0,
            issues=[
                ValidationIssue(
                    category=ValidationCategory.CONTENT_QUALITY,
                    rule_violated="Response Format",
                    current_text="N/A",
                    issue="Unable to parse validation response",
                    suggested_fix="Please review the listing manually",
                    severity="medium"
                )
            ],
            suggestions=f"Validation completed but response format was unexpected: {llm_response[:200]}...",
            word_count=self._calculate_word_count(listing),
            reading_level=self._estimate_reading_level(listing)
        )
