# Port Scanner

A simple **Python port scanner** that lets you scan individual ports or ranges of ports on a target host.  
The scanner detects which ports are **open** and which are **closed/filtered**, shows common services, and optionally saves results to a file.

---
## Requirements

- Python 3.x (tested on 3.8+)
- No additional libraries are needed; uses only standard Python modules:
  - `socket`
  - `concurrent.futures`
---

## ⚙️ Features

- Scan **individual ports** (e.g., 22, 80, 443)  
- Scan **port ranges** (e.g., 20-1000)  
- Detects common services (e.g., SSH, HTTP, HTTPS)  
- **Concurrent scanning** with `ThreadPoolExecutor` for faster results  
- Save scan results to a `.txt` file  
- Results printed in **ascending port order**

---

## 💻 Usage

1. **Run the scanner:**

```bash
python port_scanner.py