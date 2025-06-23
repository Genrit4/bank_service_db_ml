# .\env\Scripts\Activate.ps1

from database import init_db
@app.on_event("startup")
def on_startup():
    init_db()
