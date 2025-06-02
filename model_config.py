
# model_config.py

# ==== CẤU HÌNH MÔ HÌNH DỊCH ====

MODEL_CONFIG = {
    "thô": {
        "models": [
            {
                "model": "gpt-3.5-turbo",
                "provider": "openai",
                "endpoint": "https://api.openai.com/v1/chat/completions",
                "price_per_1k_token": 0.5,
                "max_tokens": 4096
            }
        ]
    },
    "chuẩn": {
        "models": [
            {
                "model": "gpt-4o",          # id hợp lệ
                "provider": "openai",
                "endpoint": "https://api.openai.com/v1/chat/completions",
                "max_tokens": 4096          # an toàn
            }
        ]
    },
    "cao cấp": {
        "models": [
            {
                "model": "gpt-4-turbo-preview",   # hoặc gpt-4-1106-preview
                "provider": "openai",
                "endpoint": "https://api.openai.com/v1/chat/completions",
                "max_tokens": 4096
            }
        ]
    }

}

# ==== CHUẨN HÓA CẤP ĐỘ ====

STYLE_LEVEL_MAP = {
    "thô": "thô",
    "chuẩn": "chuẩn",
    "chuẩn in ấn": "cao cấp",
    "cao cấp": "cao cấp",
    "basic": "thô",
    "standard": "chuẩn",
    "premium": "cao cấp"
}

# ==== HÀM TRỢ GIÚP ====

def get_model_info(style_level: str):
    level = style_level.strip().lower()
    mapped_level = STYLE_LEVEL_MAP.get(level)
    if not mapped_level:
        return None
    return MODEL_CONFIG.get(mapped_level, {}).get("models", [None])[0]

def get_all_models(style_level: str):
    level = style_level.strip().lower()
    mapped_level = STYLE_LEVEL_MAP.get(level)
    if not mapped_level:
        return []
    return MODEL_CONFIG.get(mapped_level, {}).get("models", [])
