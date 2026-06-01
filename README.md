# mini_safe

A small, simple Python project for securely storing and managing sensitive data using password-based encryption. Built with industry-standard cryptography libraries to provide confidentiality for your data at rest.

## Overview

`mini_safe` is a lightweight utility designed to help you encrypt and store sensitive information (passwords, API keys, personal data, etc.) securely. It uses password-based key derivation and modern encryption algorithms to protect your data.

## Features

✨ **Password-Based Encryption** - Encrypt sensitive data using only a password  
🔐 **Industry-Standard Cryptography** - Built on proven libraries (cryptography, bcrypt)  
🎯 **Lightweight** - Minimal dependencies and simple API  
📦 **Easy Integration** - Use it as a library or standalone tool  
🛡️ **Secure by Default** - Uses best practices for data protection  

## Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`:
  - `bcrypt==5.0.0` - Password hashing
  - `cryptography==48.0.0` - Encryption primitives
  - `cffi==2.0.0` - C Foreign Function Interface
  - `pycparser==2.23` - C parser
  - `typing_extensions==4.15.0` - Type hints

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nadav26740/mini_safe.git
   cd mini_safe
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

_Usage examples and API documentation coming soon._

## Project Structure

```
mini_safe/
├── src/              # Source code
├── requirements.txt  # Python dependencies
├── LICENSE          # Apache 2.0 License
├── .gitignore       # Git ignore rules
└── README.md        # This file
```

## License

This project is licensed under the [Apache License 2.0](LICENSE).

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## Author

Created by [nadav26740](https://github.com/nadav26740)

---

**Note:** This project is designed for sensitive data management. Ensure you understand the security implications before using it with critical information.
