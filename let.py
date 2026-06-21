from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
import httpx  # Async alternative to requests

app = FastAPI()

# Mount the static directory for CSS, JS, and Images assets
app.mount("/static", StaticFiles(directory="static"), name="static")

def build_page(result_html: str):
    # Reads the template structure safely
    with open("static/index.html", "r", encoding="utf-8") as file:
        html_content = file.read()
    
    placeholder = '<p class="placeholder-text">Your awesome questions will appear here...</p>'
    return html_content.replace("<!-- Your awesome questions will appear here... -->", result_html)

@app.get("/", response_class=FileResponse)
async def home():
    # Native FastAPI way to serve static file structures efficiently
    return FileResponse("static/index.html")

@app.post("/generate", response_class=HTMLResponse)
async def generate_questions(
    subject: str = Form(...), 
    topic: str = Form(...), 
    count: int = Form(...)
):
    startocode_url = "https://startocode-ai-api-v1.fly.dev/ask"
    
    question = (
        f"Generate exactly {count} kid-friendly questions about the topic "
        f'"{topic}" in the subject "{subject}". '
        f"Return ONLY a JSON array of strings, no other text."
    )
    
    payload = {
        "question": question
    }

    try:
        # Using HTTPX async client to keep your application highly scalable
        async with httpx.AsyncClient() as client:
            response = await client.post(startocode_url, json=payload, timeout=15.0)
            response.raise_for_status() 
            data = response.json()
        
        # Fallback safety network parameters
        if isinstance(data, dict):
            if "answer" in data:
                questions_data = data["answer"]
            elif "response" in data:
                questions_data = data["response"]
            elif "questions" in data:
                questions_data = data["questions"]
            else:
                questions_data = data
        else:
            questions_data = data

        formatted_results = f"<h3 style='color: #ea580c; text-align: left;'>✨ Questions for {topic.capitalize()}:</h3>"
        formatted_results += "<ul style='text-align: left; padding-left: 20px; list-style-type: none;'>"
        
        if isinstance(questions_data, list):
            for q in questions_data:
                formatted_results += f"<li style='margin-bottom: 10px; font-size: 1.1rem;'>{q}</li>"
        else:
            formatted_results += f"<li style='margin-bottom: 10px; font-size: 1.1rem;'>{questions_data}</li>"
            
        formatted_results += "</ul>"

    except Exception as e:
        formatted_results = f"""
        <div style="text-align: center; color: red;">
            <h3>⚠️ Oops! The connection had a tiny hiccup.</h3>
            <p>We couldn't reach the super-brain right now. Error details: {e}</p>
        </div>
        """
    
    final_html = build_page(formatted_results)
    return HTMLResponse(content=final_html)
