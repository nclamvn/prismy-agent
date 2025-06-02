# src/infrastructure/export/export_system.py
import io
import json
import csv
from datetime import datetime
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, asdict
import logging

# Simple path setup
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, '..', '..', '..')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

try:
    from docx import Document
    PYTHON_DOCX_AVAILABLE = True
except ImportError:
    PYTHON_DOCX_AVAILABLE = False

logger = logging.getLogger(__name__)

@dataclass
class ExportResult:
    """Result of export operation"""
    success: bool
    file_data: Optional[bytes] = None
    filename: str = ""
    file_type: str = ""
    error_message: Optional[str] = None
    metadata: Dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

@dataclass
class TranslationRecord:
    """Record of a translation for export"""
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    timestamp: datetime
    processing_time: float
    chunk_info: Optional[Dict] = None
    formulas_detected: int = 0
    confidence_score: Optional[float] = None

class JSONExporter:
    """Export translations to JSON format"""
    
    def export(self, data: Union[TranslationRecord, List[TranslationRecord]], 
               options: Dict = None) -> ExportResult:
        """Export to JSON format"""
        try:
            records = data if isinstance(data, list) else [data]
            
            export_data = {
                'export_info': {
                    'timestamp': datetime.now().isoformat(),
                    'version': '1.0',
                    'record_count': len(records)
                },
                'translations': []
            }
            
            for record in records:
                record_dict = asdict(record)
                if isinstance(record_dict.get('timestamp'), datetime):
                    record_dict['timestamp'] = record.timestamp.isoformat()
                export_data['translations'].append(record_dict)
            
            json_str = json.dumps(export_data, indent=2, ensure_ascii=False)
            json_bytes = json_str.encode('utf-8')
            
            filename = f"translations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            return ExportResult(
                success=True,
                file_data=json_bytes,
                filename=filename,
                file_type="json",
                metadata={'record_count': len(records)}
            )
            
        except Exception as e:
            return ExportResult(
                success=False,
                error_message=f"JSON export failed: {str(e)}"
            )

class CSVExporter:
    """Export translations to CSV format"""
    
    def export(self, data: Union[TranslationRecord, List[TranslationRecord]], 
               options: Dict = None) -> ExportResult:
        """Export to CSV format"""
        try:
            records = data if isinstance(data, list) else [data]
            
            output = io.StringIO()
            fieldnames = [
                'timestamp', 'original_text', 'translated_text', 
                'source_language', 'target_language', 'processing_time',
                'formulas_detected', 'confidence_score'
            ]
            
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            
            for record in records:
                row = {
                    'timestamp': record.timestamp.isoformat(),
                    'original_text': record.original_text,
                    'translated_text': record.translated_text,
                    'source_language': record.source_language,
                    'target_language': record.target_language,
                    'processing_time': record.processing_time,
                    'formulas_detected': record.formulas_detected,
                    'confidence_score': record.confidence_score or ""
                }
                writer.writerow(row)
            
            csv_content = output.getvalue()
            csv_bytes = csv_content.encode('utf-8-sig')
            
            filename = f"translations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            return ExportResult(
                success=True,
                file_data=csv_bytes,
                filename=filename,
                file_type="csv",
                metadata={'record_count': len(records)}
            )
            
        except Exception as e:
            return ExportResult(
                success=False,
                error_message=f"CSV export failed: {str(e)}"
            )

class ExportManager:
    """Manager for handling multiple export formats"""
    
    def __init__(self):
        """Initialize export manager"""
        self.exporters = {
            'json': JSONExporter(),
            'csv': CSVExporter(),
        }
    
    def export(self, data: Union[TranslationRecord, List[TranslationRecord]], 
               format_type: str, options: Dict = None) -> ExportResult:
        """Export data in specified format"""
        format_type = format_type.lower()
        
        if format_type not in self.exporters:
            return ExportResult(
                success=False,
                error_message=f"Unsupported export format: {format_type}"
            )
        
        exporter = self.exporters[format_type]
        return exporter.export(data, options)
    
    def get_available_formats(self) -> List[str]:
        """Get list of available export formats"""
        return list(self.exporters.keys())
    
    def create_translation_record(self, original_text: str, translated_text: str,
                                source_lang: str, target_lang: str,
                                processing_time: float, **kwargs) -> TranslationRecord:
        """Create a translation record for export"""
        return TranslationRecord(
            original_text=original_text,
            translated_text=translated_text,
            source_language=source_lang,
            target_language=target_lang,
            timestamp=datetime.now(),
            processing_time=processing_time,
            chunk_info=kwargs.get('chunk_info'),
            formulas_detected=kwargs.get('formulas_detected', 0),
            confidence_score=kwargs.get('confidence_score')
        )
