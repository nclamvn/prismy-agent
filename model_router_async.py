
import os
import httpx
import asyncio
import time
from api_keys import API_KEYS
from model_config import get_all_models
from logger_utils import log_model_error, log_model_benchmark

os.makedirs("logs", exist_ok=True)
MOCK_MODE = os.getenv("MOCK_MODE", "False") == "True"

async def _call_openai_async(model_info, messages):
    if MOCK_MODE:
        await asyncio.sleep(0.1)
        mock_response = f"[MOCK OPENAI] {messages[0]['content'][:80]}..."
        log_model_benchmark(model_info, duration=0.1, tokens=100)
        return mock_response

    keys = API_KEYS.get("openai", [])
    for key in keys:
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model_info["model"],
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": model_info.get("max_tokens", 2048)
        }
        try:
            start = time.perf_counter()
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(model_info["endpoint"], headers=headers, json=payload)
                response.raise_for_status()
                end = time.perf_counter()
                data = response.json()
                log_model_benchmark(model_info, end - start,
                                    tokens=data.get("usage", {}).get("total_tokens", None))
                if data and "choices" in data and data["choices"]:
                    return data["choices"][0]["message"]["content"]
                else:
                    log_model_error(model_info, f"[OPENAI][{key[-6:]}] ❌ Thiếu 'choices': {response.text}", tag="PARSE")
        except Exception as e:
            log_model_error(model_info, f"[OPENAI][{key[-6:]}] {str(e)}", tag="KEY")

    raise RuntimeError("Tất cả OpenAI API key đều thất bại.")

async def _call_anthropic_async(model_info, messages):
    if MOCK_MODE:
        await asyncio.sleep(0.1)
        mock_response = f"[MOCK ANTHROPIC] {messages[0]['content'][:80]}..."
        log_model_benchmark(model_info, duration=0.1, tokens=100)
        return mock_response

    keys = API_KEYS.get("anthropic", [])
    for key in keys:
        headers = {
            "x-api-key": key,
            "Content-Type": "application/json"
        }
        payload = {
            "model": model_info["model"],
            "max_tokens": model_info.get("max_tokens", 2048),
            "temperature": 0.3,
            "messages": messages
        }
        try:
            start = time.perf_counter()
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(model_info["endpoint"], headers=headers, json=payload)
                response.raise_for_status()
                end = time.perf_counter()
                data = response.json()
                log_model_benchmark(model_info, end - start)
                if data and "content" in data:
                    return data["content"]
                else:
                    log_model_error(model_info, f"[ANTHROPIC][{key[-6:]}] ❌ Thiếu 'content': {response.text}", tag="PARSE")
        except Exception as e:
            log_model_error(model_info, f"[ANTHROPIC][{key[-6:]}] {str(e)}", tag="KEY")

    raise RuntimeError("Tất cả Anthropic API key đều thất bại.")

async def _call_google_async(model_info, messages):
    if MOCK_MODE:
        await asyncio.sleep(0.1)
        mock_response = f"[MOCK GOOGLE] {messages[0]['content'][:80]}..."
        log_model_benchmark(model_info, duration=0.1, tokens=100)
        return mock_response

    keys = API_KEYS.get("google", [])
    for key in keys:
        headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": model_info["model"],
            "contents": messages,
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": model_info.get("max_tokens", 2048)
            }
        }
        try:
            start = time.perf_counter()
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(model_info["endpoint"], headers=headers, json=payload)
                response.raise_for_status()
                end = time.perf_counter()
                data = response.json()
                log_model_benchmark(model_info, end - start)
                if data and "candidates" in data and data["candidates"]:
                    return data["candidates"][0]["content"]
                else:
                    log_model_error(model_info, f"[GOOGLE][{key[-6:]}] ❌ Thiếu 'candidates': {response.text}", tag="PARSE")
        except Exception as e:
            log_model_error(model_info, f"[GOOGLE][{key[-6:]}] {str(e)}", tag="KEY")

    raise RuntimeError("Tất cả Google API key đều thất bại.")

async def call_model_async(style_level, messages):
    model_list = get_all_models(style_level)
    if not model_list:
        raise ValueError(f"Không tìm thấy mô hình cho cấp độ: {style_level}")

    for model_info in model_list:
        try:
            provider = model_info["provider"]
            if provider == "openai":
                return await _call_openai_async(model_info, messages)
            elif provider == "anthropic":
                return await _call_anthropic_async(model_info, messages)
            elif provider == "google":
                return await _call_google_async(model_info, messages)
            else:
                raise ValueError(f"Nhà cung cấp không hỗ trợ: {provider}")
        except Exception as e:
            log_model_error(model_info, f"[FALLBACK] {str(e)}", tag="FALLBACK")

    raise RuntimeError(f"Tất cả mô hình đều thất bại cho cấp độ: {style_level}")
