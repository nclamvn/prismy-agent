
#!/bin/bash

echo "🔍 Đang kiểm tra Python 3.9..."

if ! command -v python3.9 &> /dev/null
then
    echo "❌ Bạn chưa cài Python 3.9. Hãy chạy: brew install python@3.9"
    exit 1
fi

echo "✅ Đã tìm thấy Python 3.9 tại: $(which python3.9)"

# Xoá nếu môi trường đã tồn tại
if [ -d "agent_env" ]; then
  echo "🧹 Đã tồn tại agent_env – xoá để tạo lại..."
  rm -rf agent_env
fi

echo "🛠️ Đang tạo môi trường ảo mới: agent_env"
python3.9 -m venv agent_env
source agent_env/bin/activate

echo "⬆️ Đang nâng cấp pip, setuptools, wheel..."
pip install --upgrade pip setuptools wheel

echo "📦 Đang cài pillow bản ổn định..."
pip install "pillow==9.4.0"

echo "📦 Đang cài các gói còn lại từ requirements.txt (không đụng đến pillow)..."
pip install --no-deps -r requirements.txt

echo "✅ Hoàn tất! Bạn có thể chạy: source agent_env/bin/activate && streamlit run app.py"
