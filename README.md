# crc-website-server
The backend server for the CRC website.

## Setup Instructions
After cloning the repository and moving into the directory:
1. Create a virtual environment.
```bash
virtualenv --python=python3 venv
```
NOTE: Make sure virtualenv is installed on your machine first.

2. Activate the virtual environment
Windows: `.\venv\Scripts\activate`
macOS or Linux: `. venv/bin/activate`

3. Install the required Python packages
```bash
pip install -r requirements.txt
```

4. Install pipreqs (for automatically updating requirements.txt when new packages are imported)
```bash
pip install pipreqs
```

5. Fire up the server!
```bash
python api.py
```

+ To udpate requirements.txt, run `pipreqs --force .`
