# Domain Checker 🌐

A fast and efficient Python tool for checking domain availability with automatic TLD expansion and beautiful progress tracking.

## ✨ Features

- **Multi-domain checking**: Check multiple domains at once
- **Auto-expansion**: Automatically checks `.com`, `.io`, and `.ai` versions of each domain
- **Progress tracking**: Real-time progress bar with current domain display
- **Smart sorting**: Results sorted by availability, then price, then alphabetically
- **Cost display**: Shows minimum annual cost for available domains
- **Clean output**: Only displays available domains in results
- **Global command**: Use `dom` command from anywhere in your terminal

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/DTNR64/domainChecker.git
cd domainChecker
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional) Set up global command:
```bash
# Add alias to your shell profile (.zshrc, .bashrc, etc.)
echo 'alias dom="/path/to/domainChecker/dom"' >> ~/.zshrc
source ~/.zshrc
```

## 📋 Usage

### Basic Usage
```bash
python domainChecker.py example.com
```

### Multiple Domains
```bash
python domainChecker.py domain1.com domain2.com domain3.com
```

### Using Global Command (if set up)
```bash
dom myproject.com
```

## 📊 Example Output

```
Domain Availability Checker
================================================================================
Domain                                   | Status       | Minimum Cost
--------------------------------------------------------------------------------
myproject.com                           | ✅ AVAILABLE  | $10         
myproject.io                            | ✅ AVAILABLE  | $50         
myproject.ai                            | ✅ AVAILABLE  | $200        
--------------------------------------------------------------------------------
Summary: 1 domains provided, 3 checked, 3 available
```

## 💰 Pricing

- **.com domains**: $10/year minimum
- **.io domains**: $50/year minimum  
- **.ai domains**: $200/year minimum

*Note: Prices shown are minimum costs and may vary by registrar*

## 🔧 Requirements

- Python 3.6+
- python-whois library
- tqdm (for progress bars)

## 📁 Files

- `domainChecker.py` - Main domain checking script
- `requirements.txt` - Python dependencies
- `dom` - Global command wrapper script
- `README.md` - This file

## 🤝 Contributing

Feel free to open issues or submit pull requests to improve the tool!

## 📄 License

This project is open source and available under the MIT License.

---

*Happy domain hunting! 🎯*
