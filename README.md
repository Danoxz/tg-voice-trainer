# TG Voice Trainer

Script deletes voices less than 15 seconds long from private messages, with auto-reply

### Get started

1. **Preparig:**
    ```bash
    python -m venv myenv
    source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
    pip install -r requirements.txt
    ```

2. **.env file:**
    ```ini
    API_ID=123456
    API_HASH=abcdef1234567890abcdef1234567890
    WHITELIST=123456789,987654321
    ```

    Get `API_ID` and `API_HASH` on [my.telegram.org](my.telegram.org)

3. **Run:**
   ```bash
   python main.py
   ```
