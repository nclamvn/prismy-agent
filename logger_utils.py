# logger_utils.py
import os
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# ==== LOG LỖI MÔ HÌNH ====
def log_model_error(model_info, error_msg, tag="ERROR"):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    model_name = model_info.get("model", "unknown")
    provider = model_info.get("provider", "unknown")
    log_line = f"[{now}] ❌ [{tag}] {provider.upper()} - {model_name}: {error_msg}\n"

    with open(os.path.join(LOG_DIR, "failed_model.log"), "a", encoding="utf-8") as f:
        f.write(log_line)

# ==== LOG BENCHMARK ====
def log_model_benchmark(model_info, duration, tokens=None):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    model_name = model_info.get("model", "unknown")
    provider = model_info.get("provider", "unknown")
    log_line = f"[{now}] ✅ BENCHMARK {provider.upper()} - {model_name}: {duration:.2f}s"
    if tokens is not None:
        log_line += f", {tokens} tokens, ~{tokens/1000:.2f}K tokens"

    with open(os.path.join(LOG_DIR, "benchmark.log"), "a", encoding="utf-8") as f:
        f.write(log_line + "\n")
