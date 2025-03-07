from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
import Autofill
import sys
from io import StringIO
import random
from datetime import datetime
import time

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

is_running = True

class ScriptInput(BaseModel):
    selected_date: str
    target_hours: float
    run_headless: bool
    min_wait: int
    max_wait: int
    test: bool

class StreamToWeb(StringIO):
    def __init__(self):
        super().__init__()
        self.buffer = []

    def write(self, text):
        self.buffer.append(text)
        return super().write(text)

    def flush(self):
        pass

def run_playwright(selected_date: str, target_hours: float, run_headless: bool, min_wait: int, max_wait: int, test: bool):
    global is_running
    Autofill.total_minutes = 0
    TARGET_TOTAL_MINUTES = int(target_hours * 60)
    run_counter = 0

    stream = StreamToWeb()
    original_stdout = sys.stdout
    sys.stdout = stream

    try:
        while Autofill.total_minutes < TARGET_TOTAL_MINUTES and is_running:
            run_counter += 1
            print(f"🚀 Starting Run {run_counter} with date {selected_date} (Current total: {Autofill.total_minutes} minutes)...")
            yield f"🚀 Starting Run {run_counter} with date {selected_date} (Current total: {Autofill.total_minutes} minutes)...\n"
            Autofill.fill_form(selected_date, run_headless, test)
            yield f"DEBUG: Total minutes after run {run_counter} = {Autofill.total_minutes}\n"

            if Autofill.total_minutes < TARGET_TOTAL_MINUTES and is_running:
                wait_time = random.randint(min_wait, max_wait)
                finished_time = datetime.now().strftime("%I:%M %p MST")
                total_hours = Autofill.total_minutes // 60
                remaining_minutes = Autofill.total_minutes % 60
                print(f"✅ Run {run_counter} finished at {finished_time}. ⏳ Waiting {wait_time // 60} minutes and {wait_time % 60} seconds before next run. 🕒 Current Total: {total_hours} hours and {remaining_minutes} minutes")
                yield f"✅ Run {run_counter} finished at {finished_time}. ⏳ Waiting {wait_time // 60} minutes and {wait_time % 60} seconds before next run. 🕒 Current Total: {total_hours} hours and {remaining_minutes} minutes\n"
                for _ in range(wait_time):
                    if not is_running:
                        break
                    time.sleep(1)

        if not is_running:
            print("❌ Automation canceled by user.")
            yield "❌ Automation canceled by user.\n"
            Autofill.cancel_automation()
        else:
            total_hours = Autofill.total_minutes // 60
            remaining_minutes = Autofill.total_minutes % 60
            print(f"✅ All runs completed successfully! Total runs: {run_counter}. Total time reached: {total_hours} hours and {remaining_minutes} minutes (Target was {target_hours} hours)")
            yield f"✅ All runs completed successfully! Total runs: {run_counter}. Total time reached: {total_hours} hours and {remaining_minutes} minutes (Target was {target_hours} hours)\n"
            Autofill.cancel_automation()  # Clean up only on successful completion
    except Exception as e:
        print(f"❌ Server error: {e}")
        yield f"❌ Server error: {e}\n"
        Autofill.cancel_automation()
    finally:
        sys.stdout = original_stdout

@app.post("/run-script")
async def run_script(data: ScriptInput):
    global is_running
    is_running = True
    def generate():
        for line in run_playwright(data.selected_date, data.target_hours, data.run_headless, data.min_wait, data.max_wait, data.test):
            yield line
    return StreamingResponse(generate(), media_type="text/plain")

@app.post("/cancel")
async def cancel_script():
    global is_running
    is_running = False
    Autofill.cancel_automation()
    return {"status": "success", "message": "Automation cancellation requested"}

@app.get("/")
async def serve_home():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)