# SmartTextChunkerEnhanced Documentation

## Overview

SmartTextChunkerEnhanced là một hệ thống chia nhỏ văn bản thông minh với các tính năng nâng cao như:
- Phát hiện ranh giới chunk thông minh
- Bảo toàn ngữ cảnh giữa các chunks
- Hỗ trợ xử lý bất đồng bộ cho văn bản lớn
- Cache patterns để tối ưu hiệu suất
- Xử lý lỗi nâng cao
- Metadata chi tiết cho mỗi chunk

## Cài đặt

```bash
pip install -r requirements-dev.txt  # Cho development
```

## Sử dụng cơ bản

```python
from chunking.text_chunker import SmartTextChunkerEnhanced

# Khởi tạo chunker
chunker = SmartTextChunkerEnhanced(
    max_chunk_size=2800,  # Kích thước tối đa của mỗi chunk
    overlap_size=150      # Kích thước overlap giữa các chunks
)

# Xử lý văn bản đồng bộ
text = "Your long text here..."
chunks = chunker.chunk_text(text)

# Xử lý văn bản bất đồng bộ
async def process_text():
    chunks = await chunker.chunk_text_async(text)
```

## Cấu trúc dữ liệu

### ChunkMetadata
```python
@dataclass
class ChunkMetadata:
    chunk_id: int          # ID của chunk
    start_pos: int         # Vị trí bắt đầu trong văn bản gốc
    end_pos: int           # Vị trí kết thúc trong văn bản gốc
    word_count: int        # Số từ trong chunk
    char_count: int        # Số ký tự trong chunk
    has_context: bool      # Có context hay không
    original_start: int    # Vị trí bắt đầu của nội dung chính
    original_end: int      # Vị trí kết thúc của nội dung chính
```

### ChunkResult
```python
@dataclass
class ChunkResult:
    chunk_id: int              # ID của chunk
    text: str                  # Văn bản đầy đủ (bao gồm context)
    main_content: str          # Nội dung chính của chunk
    metadata: ChunkMetadata    # Metadata của chunk
    context: Optional[str]     # Context (nếu có)
```

## Tính năng chi tiết

### 1. Phát hiện ranh giới thông minh
- Sử dụng nhiều patterns để tìm điểm cắt tối ưu
- Ưu tiên cắt tại các dấu câu và khoảng trắng
- Hỗ trợ nhiều loại dấu câu (tiếng Anh, tiếng Trung)

### 2. Context preservation
- Tự động thêm context từ chunk trước
- Đánh dấu rõ ràng phần context và nội dung chính
- Có thể tùy chỉnh kích thước overlap

### 3. Async support
- Xử lý bất đồng bộ cho văn bản lớn
- Tối ưu hiệu suất với parallel processing
- Tự động điều chỉnh số lượng chunks xử lý đồng thời

### 4. Pattern caching
- Cache các pattern matches
- Tối ưu hiệu suất cho văn bản lặp lại
- Tự động invalidate cache khi cần

### 5. Error handling
- Validation đầu vào chi tiết
- Exception handling rõ ràng
- Error messages có ý nghĩa

## Performance Optimization

### Caching
```python
@lru_cache(maxsize=1024)
def _find_pattern_match(self, text: str, start: int, end: int) -> Optional[int]:
    # Implementation
```

### Async Processing
```python
async def chunk_text_async(self, text: str) -> List[ChunkResult]:
    # Parallel processing for large texts
```

## Testing

Chạy tests:
```bash
pytest tests/ -v
```

Chạy tests với coverage:
```bash
pytest tests/ --cov=chunking --cov-report=html
```

## Best Practices

1. Kích thước chunks:
   - max_chunk_size: 2000-3000 ký tự là tối ưu cho nhiều use cases
   - overlap_size: 100-200 ký tự để bảo toàn ngữ cảnh

2. Xử lý văn bản lớn:
   - Sử dụng chunk_text_async() cho văn bản > 10000 ký tự
   - Theo dõi memory usage với văn bản rất lớn

3. Error handling:
   - Luôn wrap calls trong try-except
   - Kiểm tra input validation
   - Log errors để debug

## Examples

### Basic Usage
```python
chunker = SmartTextChunkerEnhanced()
chunks = chunker.chunk_text("Your text here")
for chunk in chunks:
    print(f"Chunk {chunk.chunk_id}:")
    print(f"Main content: {chunk.main_content}")
    if chunk.context:
        print(f"Context: {chunk.context}")
```

### Async Usage
```python
async def process_large_text():
    chunker = SmartTextChunkerEnhanced()
    chunks = await chunker.chunk_text_async("Very long text...")
    return chunks

# Run with asyncio
import asyncio
chunks = asyncio.run(process_large_text())
```

### Custom Configuration
```python
chunker = SmartTextChunkerEnhanced(
    max_chunk_size=2000,  # Smaller chunks
    overlap_size=200      # Larger overlap
)
```

## Contributing

1. Fork repository
2. Create feature branch
3. Run tests: `pytest tests/`
4. Submit pull request

## License

MIT License
