# PJIP

![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![License](https://img.shields.io/badge/license-GPLv3-pink)
![Stars](https://img.shields.io/github/stars/Eystudio/PJIP?style=social)
![Last Update](https://img.shields.io/github/last-commit/Eystudio/PJIP)

[English Documentation](README.md) | [中文文档](README-ZH.md)

A classroom management assistant tool for Studentmain (极域) built with `Python`.

---

## Project Overview

`PJIP` is a Python-based assistant tool for managing the Studentmain classroom control software.  
It provides features such as killing processes, suspending/resuming Studentmain, password extraction, and includes a clean and intuitive graphical interface.

## Features

- **Kill Studentmain**: Instantly terminate the running Studentmain process  
- **Suspend Studentmain**: Suspend the process with the ability to resume later  
- **Retrieve Studentmain Password**: Attempt to extract the password  
- **User‑friendly UI**: Built with `PySide6`, simple and easy to use  

## Installation

This project runs on `Python 3.x`.

Before getting started, prepare your Python environment and clone the repository:

```bash
git clone https://github.com/Eystudio/PJIP.git
cd PJIP
```

If you prefer using a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Then install the dependencies according to the project configuration:

```bash
pip install .
```

If you prefer using requirements.txt, you can also run:

```bash
pip install -r requirements.txt
```

## Developer Notice

> A message from the developer:
> 
> Due to limited personal time, this project will temporarily enter maintenance mode, and future updates will be released irregularly.
> 
> Additionally, various limitations encountered with Python and PySide6 during development have significantly slowed progress. As a result, no major updates are expected in the near future.
> 
> Please look forward to the next-generation Studentmain management tool, built with a new language and a new UI framework.

## Contributing

Suggestions and code improvements are always welcome!
Feel free to open an Issue or submit a Pull Request.
If you have ideas or questions, you can contact the author or leave a message on GitHub.

Copyright (C) 2025 Errorsia & Yusulif