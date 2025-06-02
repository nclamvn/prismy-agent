"""
Character Extraction Optimizer
Improve character name detection accuracy
"""

import re
from typing import List, Set

class CharacterOptimizer:
    """Optimize character name extraction"""
    
    def __init__(self):
        # Proper Vietnamese name patterns
        self.name_patterns = [
            r'\b([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]{2,15})\b',  # Capitalized names
            r'\b(?:anh|em|chị|ông|bà|cô|chú)\s+([A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐ][a-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]{2,15})\b',  # Vietnamese titles + names
        ]
        
        # Words to exclude (not character names)
        self.exclude_words = {
            'fade', 'cut', 'ext', 'int', 'continuous', 'sáng', 'chiều', 'tối', 'đêm',
            'nhà', 'đường', 'ruộng', 'cánh', 'đồng', 'nông', 'thôn', 'chợ',
            'bước', 'đi', 'nhìn', 'thấy', 'nói', 'hỏi', 'trả', 'lời',
            'mặc', 'đeo', 'cầm', 'ăn', 'uống', 'ngồi', 'đứng', 'nằm',
            'tuổi', 'gầy', 'béo', 'cao', 'thấp', 'đẹp', 'xấu',
            'trắng', 'đen', 'nâu', 'vàng', 'xanh', 'đỏ',
            'sớm', 'muộn', 'sáng', 'tối', 'nhanh', 'chậm'
        }
    
    def extract_characters(self, content: str) -> List[str]:
        """Extract real character names from content"""
        characters = set()
        
        # Apply patterns
        for pattern in self.name_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                name = match.strip().title()
                if len(name) >= 3 and name.lower() not in self.exclude_words:
                    characters.add(name)
        
        # Additional filtering
        filtered_characters = []
        for char in characters:
            if self._is_valid_character_name(char):
                filtered_characters.append(char)
        
        return filtered_characters
    
    def _is_valid_character_name(self, name: str) -> bool:
        """Validate if string is likely a character name"""
        # Basic validation rules
        if len(name) < 3 or len(name) > 15:
            return False
        
        if name.lower() in self.exclude_words:
            return False
        
        # Check if contains only letters
        if not re.match(r'^[A-ZÀÁẠẢÃÂẦẤẬẨẪĂẰẮẶẲẴÈÉẸẺẼÊỀẾỆỂỄÌÍỊỈĨÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠÙÚỤỦŨƯỪỨỰỬỮỲÝỴỶỸĐa-zàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]+$', name):
            return False
        
        return True

# Test the optimizer
if __name__ == "__main__":
    optimizer = CharacterOptimizer()
    
    test_content = """
    Anh MINH (40 tuổi, gầy, da ngăm đen, mặt khắc khổ) bước ra khỏi nhà tranh nhỏ.
    Anh dừng lại khi thấy em LAN (25 tuổi, xinh đẹp, mặc áo bà ba trắng).
    """
    
    characters = optimizer.extract_characters(test_content)
    print(f"Optimized Characters: {characters}")
