# Setup Notes

1. **Prerequisites**
   - Python 3.10+
   - Node.js 18+
   - Docker (optional, but a skeleton compose file has been provided)
   - `uv` (for the upstream python app packaging)

2. **Upstream Core**
   The project maintains the upstream behavior and requires `uv`:
   ```bash
   uv sync
   uv run prepare.py
   uv run train.py
   ```

3. **Backend Setup** (Pending Claude Implementation)
   Navigate to `app/backend`.
   Once dependencies are added by Claude, you will likely run it via a command like:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

4. **Frontend Setup** (Pending Claude Implementation)
   Navigate to `app/frontend`:
   ```bash
   npm install
   npm run dev
   ```
