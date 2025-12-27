# API Contracts: Computer Parts Pricing Application

## Overview
This document defines the RESTful API endpoints for the computer parts pricing application. The API provides functionality for submitting part lists, processing price calculations, and retrieving results.

## Base URL
```
http://localhost:8000/api/v1
```

## Endpoints

### Submit Part List for Pricing Analysis
```
POST /parts/submit
```

**Description**: Submits a list of computer parts for price calculation analysis.

**Request Body**:
```json
{
  "parts": [
    "RTX5070",
    "64GB-DDR5-RAM"
  ],
  "geo_location": "GB",
  "parse_enabled": true
}
```

**Response Codes**:
- `202 Accepted`: Request accepted for processing
- `400 Bad Request`: Invalid request data

### Get Processing Status
```
GET /parts/{request_id}/status
```

**Description**: Gets the current status of a price calculation request.

**Path Parameters**:
- `request_id` (string, required): Unique identifier for the processing request

**Response Body**:
```json
{
  "request_id": "abc123",
  "status": "processing|completed|failed",
  "message": "Description of current status"
}
```

### Get Pricing Results
```
GET /parts/{request_id}/results
```

**Description**: Retrieves the complete pricing results for a processed request.

**Path Parameters**:
- `request_id` (string, required): Unique identifier for the processing request

**Response Body**:
```json
{
  "request_id": "abc123",
  "parts": [
    {
      "name": "RTX5070",
      "price": 899.99,
      "source": "amazon_search",
      "currency": "GBP"
    },
    {
      "name": "64GB-DDR5-RAM", 
      "price": 129.99,
      "source": "amazon_search",
      "currency": "GBP"
    }
  ],
  "total_price": 1029.98,
  "processing_time_seconds": 2.3
}
```

### Get Part Details
```
GET /parts/{part_name}/details
```

**Description**: Retrieves detailed information about a specific computer part.

**Path Parameters**:
- `part_name` (string, required): Name of the computer part

**Response Body**:
```json
{
  "name": "RTX5070",
  "category": "GPU",
  "specifications": {
    "memory": "12GB GDDR6X",
    "cuda_cores": 10240,
    "base_clock": 1410
  },
  "price_records": [
    {
      "source": "amazon_search",
      "price": 899.99,
      "timestamp": "2025-01-01T10:00:00Z"
    }
  ]
}
```

## Error Responses

All error responses follow this format:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": "Additional technical details (optional)"
  }
}
```

**Error Codes**:
- `INVALID_INPUT`: Request body contains invalid data
- `PART_NOT_FOUND`: Specified part could not be found 
- `PROCESSING_ERROR`: Error occurred during price calculation
- `REQUEST_TIMEOUT`: Processing took too long to complete

## Authentication and Security
All endpoints are currently unauthenticated. In a production environment, authentication should be implemented using API tokens or session management.

## Versioning
API version 1.0 is currently supported.