
import os
import hashlib
from pdf2image import convert_from_bytes
import pytesseract
import openai

def is_flowchart_like(file_name):
    """Nhận diện sơ đồ dựa vào tên file (có thể mở rộng thêm sau)"""
    keywords = ["flow", "logic", "tool", "checklist", "diagram", "plagiarism"]
    return any(k in file_name.lower() for k in keywords)

def extract_text_from_flowchart_pdf(file_bytes):
    """Chuyển PDF sơ đồ sang ảnh rồi trích xuất text bằng OCR"""
    images = convert_from_bytes(file_bytes)
    texts = [pytesseract.image_to_string(img) for img in images]
    return "\n\n".join(texts)

def restructure_flowchart_logic(text, openai_api_key, model="gpt-4"):
    """Dùng GPT tái cấu trúc nội dung flowchart thành checklist logic"""
    openai.api_key = openai_api_key
    system_prompt = (
        "Bạn là trợ lý học thuật. Hãy chuyển văn bản dưới đây thành một bảng checklist hoặc các bước logic tuần tự, "
        "dễ hiểu như người đang đọc một sơ đồ flowchart kiểm tra đạo văn. Dùng tiêu đề phụ, gạch đầu dòng, giữ cấu trúc điều kiện rõ ràng."
    )
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        temperature=0.3
    )
    return response["choices"][0]["message"]["content"]

def process_flowchart_file(file_bytes, file_name, openai_api_key):
    """Xử lý đầy đủ: OCR + tái cấu trúc logic + cache"""
    file_hash = hashlib.sha256(file_bytes).hexdigest()
    cache_logic_path = f"cache/{file_hash}_logic.txt"

    if os.path.exists(cache_logic_path):
        with open(cache_logic_path, "r") as f:
            return f.read(), "cache"

    raw_text = extract_text_from_flowchart_pdf(file_bytes)
    if len(raw_text.strip()) < 30:
        return None, "ocr_failed"

    logic_text = restructure_flowchart_logic(raw_text, openai_api_key)
    os.makedirs("cache", exist_ok=True)
    with open(cache_logic_path, "w") as f:
        f.write(logic_text)

    return logic_text, "gpt_success"
