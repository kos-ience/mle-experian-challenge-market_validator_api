# Assumptions and Design Decisions

## Project Overview

This document outlines the key assumptions made and design decisions taken while building the Marketplace Validator API for the GenAI Machine Learning Engineer interview challenge.

## 🎯 Core Assumptions

### 1. Problem Scope
- **Real-time validation**: Assumed lenders need immediate feedback on their listings
- **Single listing validation**: Focused on validating one listing at a time (not batch processing)
- **English language only**: Assumed all listings are in English
- **Credit cards only**: Focused specifically on credit card listings (not other financial products)

### 2. User Interaction Model
- **Self-service validation**: Lenders validate their own listings before marketplace submission
- **Iterative improvement**: Lenders can modify and re-validate listings multiple times
- **No persistent storage**: API doesn't store listings or validation history (stateless design)

### 3. Technical Requirements
- **Production-ready but not production-scale**: Built for demonstration with production patterns
- **Local deployment**: Designed to run locally for the interview challenge
- **LLM dependency**: Acceptable to have external dependency on OPENAI API

## 🏗️ Design Decisions

### 1. Architecture Choices

#### **FastAPI + Pydantic Backend**
**Decision**: Use FastAPI with Pydantic models for structured responses

**Rationale**:
- **Type Safety**: Pydantic ensures structured, validated responses from LLM
- **Auto Documentation**: FastAPI generates interactive API docs automatically
- **Modern Python**: Async support and modern Python features
- **Developer Experience**: Excellent tooling and error messages


#### **OPENAI as LLM Provider**
**Decision**: Use OPENAI API for validation logic

**Rationale**:
- **Good instruction following**: OPENAI API handles structured output requests well
- **Reasonable latency**: Acceptable response times for real-time validation
- **Easy integration**: Simple API with good Python SDK


#### **Node.js Frontend**
**Decision**: Simple Node.js/Express frontend with vanilla JavaScript

**Rationale**:
- **Quick development**: Fast to build and demonstrate
- **No framework overhead**: Vanilla JS keeps it simple and lightweight
- **Easy deployment**: Simple static files with minimal server
- **Cross-platform**: Works on any system with Node.js


### 2. API Design Choices

#### **Single Validation Endpoint**
**Decision**: One POST `/validate` endpoint for all validation

**Rationale**:
- **Simplicity**: Clear, focused API surface
- **Stateless**: Each request is independent
- **Easy testing**: Single endpoint to test and document


#### **Structured Error Responses**
**Decision**: Detailed error categorization with specific suggestions

**Rationale**:
- **Actionable feedback**: Lenders get specific, implementable suggestions
- **Categorization**: Issues grouped by validation category for organized review
- **Severity levels**: Helps prioritize which issues to fix first

#### **Compliance Scoring**
**Decision**: 0-10 compliance score which is decided internally by llm

**Rationale**:
- **Granular feedback**: More nuanced than binary pass/fail
- **Progress tracking**: Lenders can see improvement over iterations
- **Prioritization**: Helps focus on most impactful improvements

### 3. Implementation Decisions

#### **Prompt Engineering Approach**
**Decision**: Enhance existing prompt with structured output instructions

**Rationale**:
- **Leverage provided prompt**: Builds on the challenge's provided validation logic
- **JSON Schema enforcement**: Forces consistent, parseable responses
- **Fallback handling**: Graceful degradation when LLM doesn't follow format

#### **No Database**
**Decision**: Stateless API with no persistent storage

**Rationale**:
- **Simplicity**: Reduces infrastructure requirements for demo
- **Scalability**: Stateless design scales horizontally
- **Privacy**: No storage means no data retention concerns

**Trade-off**: Can't track usage patterns or provide historical analysis

#### **CORS Policy**
**Decision**: Allow all origins in development

**Rationale**:
- **Development ease**: Simplifies local testing and demo
- **Explicit configuration**: Clear comment about production requirements

**Production Note**: Would restrict to specific origins in production

## 🤔 Open Questions and Limitations

### 1. Validation Accuracy
**Question**: How accurate should the validation be?

**Current Approach**: Rely on LLM's judgment with structured prompting

**Limitations**: 
- No ground truth dataset to measure accuracy against
- LLM responses can be inconsistent
- Some edge cases may not be handled properly

**Future Improvement**: Could build evaluation dataset and fine-tune validation

### 2. Performance Requirements
**Question**: What are acceptable response times?

**Current Approach**: Synchronous processing, 2-5 second response times

**Limitations**:
- Dependent on LLM provider latency
- No caching or optimization
- Could be slow for high-traffic scenarios

**Future Improvement**: Add caching, async processing, or batch endpoints

### 3. Scalability Needs
**Question**: How many concurrent validations should the system handle?

**Current Approach**: Basic FastAPI setup without optimization

**Limitations**:
- No rate limiting
- No request queuing
- No load balancing

**Future Improvement**: Add rate limiting, caching, and horizontal scaling

### 4. Validation Completeness
**Question**: Should the API catch all possible compliance issues?

**Current Approach**: Rely on marketplace standards document and LLM analysis

**Limitations**:
- May miss subtle regulatory issues
- No integration with actual FCA guidance updates
- Human review still needed for final approval

**Future Improvement**: Add rule-based validation for critical compliance items

## 🔧 Technical Trade-offs

### 1. LLM vs Rule-Based Validation
**Chosen**: LLM-based validation with structured output

**Pros**:
- Flexible and adaptable to new requirements
- Can understand context and nuance
- Handles natural language well

**Cons**:
- Less predictable than rule-based systems
- Requires external API dependency
- Can be more expensive at scale

**Alternative**: Hybrid approach with rules for critical items and LLM for subjective analysis

### 2. Synchronous vs Asynchronous Processing
**Chosen**: Synchronous validation with immediate response

**Pros**:
- Simple implementation
- Immediate feedback for users
- Easy to test and debug

**Cons**:
- Blocks during LLM processing
- Limited scalability
- No ability to queue requests

**Alternative**: Async processing with job IDs and polling/webhooks

### 3. Frontend Complexity
**Chosen**: Simple vanilla JavaScript interface

**Pros**:
- Quick to build and modify
- No build process or dependencies
- Easy to understand and extend

**Cons**:
- Limited UI sophistication
- No state management
- Manual DOM manipulation

**Alternative**: React/Vue for richer UI but longer development time

## 🚀 Production Readiness Assessment

### What's Production-Ready
- ✅ **API Structure**: RESTful design with proper status codes
- ✅ **Input Validation**: Pydantic models ensure data integrity
- ✅ **Error Handling**: Graceful error responses and logging
- ✅ **Documentation**: Auto-generated API docs and comprehensive README
- ✅ **Type Safety**: Full type hints and validation

### What Needs Production Work
- ⚠️ **Authentication**: No API key or user authentication
- ⚠️ **Rate Limiting**: No protection against abuse
- ⚠️ **Monitoring**: Basic logging but no metrics or alerting
- ⚠️ **Caching**: No response caching for performance
- ⚠️ **Security**: CORS open, no input sanitisation beyond validation
- ⚠️ **Deployment**: No containerisation or deployment automation

## 💡 Future Enhancement Opportunities

### Short-term (< 1 month)
1. **Authentication system** with API keys
2. **Rate limiting** to prevent abuse
3. **Response caching** for identical listings
4. **Batch validation** endpoint for multiple listings
5. **Health monitoring** and metrics collection

### Medium-term (1-3 months)
1. **Custom validation rules** configuration
2. **Multiple LLM provider** support with fallbacks
3. **Validation history** and analytics
4. **Integration testing** suite with sample data
5. **Performance optimization** and caching layers

### Long-term (3+ months)
1. **Machine learning** for validation accuracy improvement
2. **Real-time collaboration** features for teams
3. **Integration APIs** for marketplace platforms
4. **Advanced analytics** and reporting dashboard
5. **Multi-language support** for international markets

This document represents the current state of assumptions and decisions. These should be revisited as requirements evolve and production usage patterns emerge.
