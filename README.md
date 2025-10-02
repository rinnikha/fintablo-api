# Fintablo API Python Client

A Python client library for interacting with the Fintablo API, providing a clean and intuitive interface for financial data operations.

## Installation

```bash
pip install fintablo-api
```

## Quick Start

```python
from fintablo_api import Fintablo

# Initialize the client
client = Fintablo(
    api_key="your_api_key",
    base_url="https://my.fintablo.ru/api",  # Optional, uses default
    debug=True  # Optional, enables debug logging
)

# Example usage (endpoints to be added based on actual API)
# accounts = client.accounts.query().limit(10).execute()
# print(f"Found {len(accounts)} accounts")
```

## Features

- **Pythonic Interface**: Clean, object-oriented design following Python best practices
- **Query Builder**: Fluent interface for constructing complex queries
- **Error Handling**: Comprehensive exception hierarchy for different error scenarios
- **Authentication**: Built-in support for API key authentication
- **Rate Limiting**: Automatic handling of rate limits and retries
- **Debug Mode**: Optional detailed logging for development and troubleshooting

## Authentication

The client supports API key authentication:

```python
client = Fintablo(api_key="your_api_key")
```

## Query Building

Build complex queries using the fluent interface:

```python
# Example query structure (to be implemented based on actual API)
query = client.accounts.query()
query.filter().eq("status", "active")
query.order_by().add("name")
query.limit(50)
results = query.execute()
```

## Error Handling

The library provides specific exceptions for different error scenarios:

- `FinTabloException`: Base exception for all library errors
- `AuthenticationException`: Authentication-related errors
- `NotFoundException`: Resource not found errors
- `ValidationException`: Request validation errors
- `RateLimitException`: Rate limiting errors
- `ServerException`: Server-side errors

## Development

Clone the repository:

```bash
git clone https://github.com/rinnikha/fintablo-api.git
cd fintablo-api
```

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

Run tests:

```bash
pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.