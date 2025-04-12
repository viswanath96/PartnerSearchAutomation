# Partner Search Automation

An automation tool for managing partner search profiles on matrimonial websites.

## Setup

1. **Configure sensitive files**:
   - Copy `reminder.template.txt` to `reminder.txt`
   - Copy `data.template.json` to `data.json`
   - Customize both files with your data

2. **Environment Variables**:
   Create a `.env` file with:
   ```
   SH_USERNAME=your_username
   SH_PASSWORD=your_password
   ```

3. **Installation**:
   ```bash
   pip install -r requirements.txt
   ```

## Files Not Tracked in Git
- `reminder.txt` - Contains your custom messages
- `data.json` - Stores your activity data
- `.env` - Contains your credentials

These files are excluded for security reasons.
