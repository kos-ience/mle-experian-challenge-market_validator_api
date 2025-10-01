from pydantic import BaseModel, Field
from typing import List, Literal, Optional
from enum import Enum

class ValidationCategory(str, Enum):
    REGULATORY_COMPLIANCE = "Regulatory & Compliance"
    CONTENT_QUALITY = "Content Quality"
    USER_EXPERIENCE = "User Experience"
    BRAND_TONE = "Brand & Tone Alignment"
    PROHIBITED_LANGUAGE = "Prohibited Language"
    ETHICAL_STANDARDS = "Ethical Standards"

class ValidationRequest(BaseModel):
    listing: str = Field(..., min_length=10, max_length=5000, description="Credit card listing text to validate")

class ValidationIssue(BaseModel):
    category: ValidationCategory = Field(..., description="Category of the validation issue")
    rule_violated: str = Field(..., description="Specific rule that was violated")
    current_text: str = Field(..., description="The problematic text from the listing")
    issue: str = Field(..., description="Description of the issue")
    suggested_fix: str = Field(..., description="Suggested replacement or fix")
    severity: Literal["low", "medium", "high"] = Field(..., description="Severity of the issue")

class ValidationResponse(BaseModel):
    status: Literal["compliant", "non_compliant"] = Field(..., description="Overall compliance status")
    compliance_score: float = Field(..., ge=0, le=10, description="Compliance score from 0-10")
    issues: List[ValidationIssue] = Field(default=[], description="List of validation issues found")
    suggestions: str = Field(..., description="Overall suggestions for improvement")
    word_count: int = Field(..., description="Word count of the listing")
    reading_level: Optional[str] = Field(None, description="Estimated reading level")

class HealthResponse(BaseModel):
    status: str = Field(..., description="Health status")
    version: str = Field(..., description="API version")
