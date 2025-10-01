# Marketplace Validator API 

> **Implementation Status**: Option 1 (Marketplace Validator API) has been fully implemented with a production-ready FastAPI backend and Node.js frontend.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- OPENAI API Key 

### 1. Automatic Setup (Recommended)
```bash
# Run the setup script
python setup.py
```

### 2. Manual Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
cd frontend && npm install && cd ..

# Configure environment
cp .env.example .env
# Edit .env and add your Gemini API key
```

### 3. Run the Application
```bash
# Terminal 1: Start the backend API
python run_server.py

# Terminal 2: Start the frontend
cd frontend && npm start
```

### 4. Access the Application
- **Frontend UI**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health

## 🏗️ Architecture

```
Frontend (Node.js/Express) → Backend (FastAPI) → LLM (OpenAI) → Structured Response
```

### Tech Stack
- **Backend**: FastAPI + Pydantic for type-safe API responses
- **LLM**: OpenAI API for intelligent validation
- **Frontend**: Node.js + Express with vanilla JavaScript
- **Validation**: Structured JSON responses with detailed feedback

## 📋 Features Implemented

### ✅ Core Requirements Met
- [x] **Working API running locally** - FastAPI backend on port 8000
- [x] **Production-ready patterns** - Error handling, validation, documentation
- [x] **Marketplace standards validation** - Against all 6 categories
- [x] **Structured suggestions** - Specific, actionable feedback
- [x] **Documentation** - Comprehensive API docs and assumptions

### ✅ Additional Features
- [x] **Beautiful UI** - Modern, responsive frontend interface
- [x] **Real-time validation** - Immediate feedback on listing submission
- [x] **Compliance scoring** - 0-10 score with detailed breakdown
- [x] **Interactive documentation** - Auto-generated Swagger UI
- [x] **Health monitoring** - API health checks and error handling
- [x] **Type safety** - Full Pydantic validation for requests/responses

## 🎯 Validation Categories

The API validates against 6 main standards:

1. **Regulatory & Compliance** - APR disclosure, fee transparency, credit requirements
2. **Content Quality** - Clear language, proper grammar, completeness  
3. **User Experience** - Appropriate length, readability, structure
4. **Brand & Tone** - Professional, factual, non-promotional
5. **Prohibited Language** - No misleading claims or exaggerated terms
6. **Ethical Standards** - Inclusive language, fair representation

## 📊 API Response Example

```json
{
  "status": "non_compliant",
  "compliance_score": 7.2,
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
  "suggestions": "Focus on regulatory compliance and clearer language",
  "word_count": 245,
  "reading_level": "Grade 8 or below"
}
```

## 🧪 Testing

Test with provided sample listings:
```bash
# Test API directly
curl -X POST "http://localhost:8000/validate" \
  -H "Content-Type: application/json" \
  -d '{"listing": "Your listing text here..."}'

# Or use the sample listings
cat sample_listings/listing_01.txt
```

## 📚 Documentation

- **[API Documentation](./API_DOCUMENTATION.md)** - Complete API reference
- **[Assumptions & Design Decisions](./ASSUMPTIONS_AND_DESIGN_DECISIONS.md)** - Detailed rationale
- **[Marketplace Standards](./marketplace-standards.md)** - Validation criteria

## 🔧 Project Structure

```
├── backend/                 # FastAPI backend
│   ├── main.py             # API routes and app setup
│   ├── models.py           # Pydantic data models
│   ├── validator.py        # LLM integration logic
│   └── __init__.py
├── frontend/               # Node.js frontend
│   ├── server.js           # Express server
│   ├── package.json        # Dependencies
│   └── public/
│       └── index.html      # UI interface
├── sample_listings/        # Test data
├── requirements.txt        # Python dependencies
├── run_server.py          # Backend startup script
├── setup.py               # Automated setup
└── .env.example           # Environment template
```

## 🎯 Challenge Completion Status

### Original Challenge Requirements
- [x] **Option 1: Marketplace Validator API** ← **COMPLETED**
  - [x] Production-ready API ✅
  - [x] Validates against marketplace standards ✅
  - [x] Provides suggested changes ✅
  - [x] Works with provided prompt ✅
  - [x] Uses OpenAI LLM ✅

### Deliverables Completed
- [x] **Working API running locally** - Full FastAPI implementation
- [x] **Document assumptions/open questions** - Comprehensive documentation

### Features Added
- [x] **Frontend interface** - Beautiful, responsive UI
- [x] **Structured responses** - Type-safe Pydantic models
- [x] **Error handling** - Graceful error management
- [x] **Auto documentation** - Interactive API docs
- [x] **Health monitoring** - System status endpoints

## 🚨 Important Notes

### Environment Setup
1. **Get OpenAI API Key**: Get the keys from OpenAI API Platform
2. **Configure .env**: Add your API key to the `.env` file
3. **Check ports**: Ensure ports 3000 and 8000 are available

### Production Considerations
- Add authentication for production use
- Implement rate limiting for API protection
- Configure proper CORS origins
- Add monitoring and logging
- Consider caching for performance

## 🤝 Usage

1. **Start both servers** (backend on 8000, frontend on 3000)
2. **Open the frontend** at http://localhost:3000
3. **Paste a credit card listing** in the text area
4. **Click "Validate Listing"** to get instant feedback
5. **Review the results** with specific suggestions for improvement

The system provides immediate, actionable feedback to help lenders create compliant listings that meet all marketplace standards.

---

## Original Challenge Description

### Overview

Consider a marketplace that you are developing for consumers to compare credit cards, loans, etc. 

As part of setting up the marketplace third-party lenders provide offers to list to consumers. Each lender can create their listing and description as they wish, for example,

> **Card Name:** ClearPath Platinum by TrustBank
> 
> **Brief Description:**
> Simplify your finances with the ClearPath Platinum credit card from TrustBank. Earn generous rewards on everyday purchases, including 3% cashback on dining, 2% cashback on gas and groceries, and 1% cashback everywhere else. With no annual fees, clear terms, and straightforward rewards, managing your credit has never been easier.
> 
> **Features:**
> 
> - **Cashback:** 3% on dining, 2% on gas and groceries, 1% on other purchases
> 
> - **Annual Fee:** £0
> 
> - **APR:** 17.49%–25.49% variable APR
> 
> - **Introductory Offer:** 0% APR on purchases and balance transfers for the first 15 months
> 
> - **Credit Requirement:** Good to Excellent (680+ credit score)
> 
> **Ideal For:**
> Consumers who prefer transparent rewards, straightforward terms, and consistent savings on everyday spending.

which will then appear on the marketplace. 

As the marketplace administrator, you want to have control over the way that credit cards are listed to ensure the  [Marketplace Standards](./marketplace-standards.md) are met for all listings from all lenders. 

You are tasked with building a _Marketplace Validator_ that will validate a listing from a lender and suggest changes if required.

### 2. Improved Marketplace Validator

Take the existing Marketplace Validator (just the [prompt provided](marketplace_validator_prompt.txt)) and find possible improvements.

One approach might be to follow these steps:
- Evaluate current baseline performance
- Attempt to improve
- Consider tradeoffs to making the improvements

Your deliverables:
- [ ] Notebook / scripts / any code produced. 
- [ ] Document any assumptions you have made / open questions.# mle-experian-challenge-market_validator_api
