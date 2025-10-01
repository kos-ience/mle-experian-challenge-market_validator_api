# Marketplace Validator API Documentation

## Overview

The Marketplace Validator API is a production-ready REST API that validates credit card listings against marketplace standards. It uses OpenAI API to analyze listings and provide structured feedback on compliance issues.

## Architecture

```
Frontend (Node.js/Express) → Backend (FastAPI) → LLM (OpenAI) → Structured Response
```

### Tech Stack
- **Backend**: FastAPI + Pydantic for type safety and validation
- **LLM Provider**: OpenAI API
- **Frontend**: Node.js + Express with vanilla JavaScript
- **Response Format**: Structured JSON with Pydantic models

## API Endpoints

### Base URL
```
http://localhost:8000
```

### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### 2. Validate Listing
```http
POST /validate
```

**Request Body:**
```json
{
  "listing": "Card Name: Example Card..."
}
```

**Response:**
```json
{
  "status": "compliant" | "non_compliant",
  "compliance_score": 7.5,
  "issues": [
    {
      "category": "Regulatory & Compliance",
      "rule_violated": "APR disclosure",
      "current_text": "Low rates available",
      "issue": "APR not clearly stated",
      "suggested_fix": "Include specific APR range like '17.49%–25.49% variable APR'",
      "severity": "high"
    }
  ],
  "suggestions": "Overall suggestions for improvement...",
  "word_count": 245,
  "reading_level": "Grade 8 or below"
}
```

### 3. API Documentation
```http
GET /docs
```
Interactive Swagger UI documentation

```http
GET /redoc
```
ReDoc documentation

## Validation Categories

The API validates against 6 main categories:

1. **Regulatory & Compliance**
   - APR disclosure requirements
   - Fee transparency
   - Credit requirements clarity

2. **Content Quality**
   - Language clarity and simplicity
   - Grammar and spelling
   - Completeness of information

3. **User Experience**
   - Appropriate content length (100-300 words)
   - Reading level (Grade 8 or below)
   - Consistent structure

4. **Brand & Tone Alignment**
   - Professional, informative tone
   - Factual vs. emotional appeals
   - Non-promotional language

5. **Prohibited Language**
   - No misleading claims
   - No exaggerated superlatives
   - No vague promotional terms

6. **Ethical Standards**
   - Inclusive language
   - Fair representation
   - No predatory targeting

## Response Model Details

### ValidationResponse
- `status`: Overall compliance status
- `compliance_score`: Score from 0-10
- `issues`: Array of specific violations found
- `suggestions`: Overall improvement recommendations
- `word_count`: Total words in the listing
- `reading_level`: Estimated reading difficulty

### ValidationIssue
- `category`: Which validation category was violated
- `rule_violated`: Specific rule name
- `current_text`: Exact problematic text from listing
- `issue`: Description of the problem
- `suggested_fix`: Specific recommendation
- `severity`: "low", "medium", or "high"

## Error Handling

### 422 Validation Error
Invalid request format or missing required fields

### 500 Internal Server Error
LLM processing errors or system failures

### 503 Service Unavailable
API key not configured or LLM service unavailable

## Rate Limiting

Currently no rate limiting implemented. In production, consider:
- Per-API-key rate limits
- Request throttling
- Queue management for high traffic

## Security Considerations

### Current Implementation
- CORS enabled for development
- Basic input validation with Pydantic
- Error message sanitization

### Production Recommendations
- API key authentication
- Request size limits
- Input sanitization for XSS prevention
- HTTPS only
- Specific CORS origins

## Performance

### Response Times
- Typical validation: 2-5 seconds
- Depends on LLM provider latency
- Consider caching for repeated validations

### Scalability
- Stateless API design
- Horizontal scaling ready
- Consider async processing for batch validations

## Monitoring & Logging

### Current Logging
- Basic FastAPI request/response logging
- Error tracking and stack traces

### Production Recommendations
- Structured logging (JSON format)
- Request/response metrics
- LLM usage tracking
- Performance monitoring
- Health check endpoints

## Configuration

### Environment Variables
```bash
OPENAI_API_KEY=your_api_key_here
```

### Optional Configuration
- `LOG_LEVEL`: Logging verbosity
- `API_HOST`: Host binding
- `API_PORT`: Port binding
- `CORS_ORIGINS`: Allowed origins for CORS

## Testing

### Sample Test Request
```bash
curl -X POST "http://localhost:8000/validate" \
  -H "Content-Type: application/json" \
  -d '{
    "listing": "Card Name: Example Card\nBrief Description: Low rates available\nFeatures: Great benefits"
  }'
```

### Test Data
Use the sample listings in `sample_listings/` directory for testing various scenarios.

## Deployment

### Local Development
1. Install dependencies: `pip install -r requirements.txt`
2. Set up environment: Copy `.env.example` to `.env` and add API key
3. Run server: `python run_server.py`
4. Access API: `http://localhost:8000`

### Production Deployment
- Use production WSGI server (Gunicorn, uWSGI)
- Set up reverse proxy (Nginx)
- Configure SSL/TLS
- Set up monitoring and logging
- Use environment-specific configuration

## Future Enhancements

### Planned Features
- Batch validation endpoint
- Custom validation rules
- Integration with more LLM providers
- Caching layer for improved performance
- Admin dashboard for monitoring

### API Versioning
Current version: v1.0.0
Future versions will maintain backward compatibility
