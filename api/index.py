# api/index.py
from fastapi import FastAPI, HTTPException
from pykap.bist import BISTCompany
from pykap.get_bist_companies import get_bist_companies
from pykap.bist_company_list import bist_company_list
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "PyKAP API is running"}

@app.get("/companies")
def get_companies():
    try:
        companies = get_bist_companies(output_format='dict')
        return {"success": True, "companies": companies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/company/{ticker}")
def get_company_info(ticker: str):
    try:
        tickers = bist_company_list()
        if ticker not in tickers:
            raise HTTPException(status_code=404, detail=f"Company with ticker {ticker} not found")
        
        company = BISTCompany(ticker=ticker)
        return {
            "success": True,
            "ticker": company.ticker,
            "name": company.name,
            "city": company.city,
            "auditor": company.auditor,
            "company_id": company.company_id
        }
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/company/{ticker}/financial-reports")
def get_financial_reports(ticker: str):
    try:
        tickers = bist_company_list()
        if ticker not in tickers:
            raise HTTPException(status_code=404, detail=f"Company with ticker {ticker} not found")
        
        company = BISTCompany(ticker=ticker)
        reports = company.get_financial_reports()
        return {"success": True, "ticker": ticker, "reports": reports}
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/company/{ticker}/historical-disclosures")
def get_historical_disclosures(ticker: str, subject: str = "financial report"):
    try:
        tickers = bist_company_list()
        if ticker not in tickers:
            raise HTTPException(status_code=404, detail=f"Company with ticker {ticker} not found")
        
        company = BISTCompany(ticker=ticker)
        disclosures = company.get_historical_disclosure_list(subject=subject)
        return {"success": True, "ticker": ticker, "disclosures": disclosures}
    except Exception as e:
        if "not found" in str(e).lower():
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))