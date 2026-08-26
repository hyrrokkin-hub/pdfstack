from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from pypdf import Pt, PdfWriter
import io
from typing import List

app = FastAPI(title="DamarPDF Engine", version="1.0.0")

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    """Halaman web sederhana untuk upload dan merge PDF"""
    html_content = """
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DamarPDF - Local Processing</title>
        <style>
            body { font-family: system-ui, sans-serif; background: #1a1a24; color: #e0e0e0; margin: 0; padding: 40px; display: flex; justify-content: center; }
            .container { background: #262636; padding: 30px; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.3); width: 100%; max-width: 500px; }
            h1 { font-size: 1.5rem; margin-top: 0; color: #4f46e5; text-align: center; }
            p { font-size: 0.9rem; color: #a0a0b0; text-align: center; }
            form { display: flex; flex-direction: column; gap: 15px; margin-top: 20px; }
            input[type="file"] { background: #1a1a24; padding: 10px; border-radius: 6px; border: 1px solid #3b3b54; color: #fff; }
            button { background: #4f46e5; color: white; border: none; padding: 12px; border-radius: 6px; font-weight: bold; cursor: pointer; transition: 0.2s; }
            button:hover { background: #4338ca; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📄 DamarPDF Stack</h1>
            <p>Gabungkan beberapa file PDF secara lokal & aman.</p>
            <form action="/merge" method="post" enctype="multipart/form-data">
                <input type="file" name="files" multiple accept=".pdf" required>
                <button type="submit">Gabungkan PDF</button>
            </form>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/health")
async def health_check():
    """Endpoint untuk pemantauan health status kontainer"""
    return {"status": "healthy", "service": "damarpdf-engine"}

@app.post("/merge")
async def merge_pdfs(files: List[UploadFile] = File(...)):
    """API endpoint untuk menggabungkan file PDF"""
    if len(files) < 2:
        raise HTTPException(status_code=400, detail="Minimal unggah 2 file PDF untuk digabungkan.")
    
    merger = PdfWriter()
    
    try:
        for file in files:
            if not file.filename.endswith('.pdf'):
                raise HTTPException(status_code=400, detail=f"File {file.filename} bukan PDF.")
            contents = await file.read()
            pdf_stream = io.BytesIO(contents)
            merger.append(pdf_stream)
        
        output_stream = io.BytesIO()
        merger.write(output_stream)
        merger.close()
        output_stream.seek(0)
        
        return StreamingResponse(
            output_stream,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=merged_output.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal memproses PDF: {str(e)}")
