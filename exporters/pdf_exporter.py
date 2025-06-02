from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from typing import Dict, Any, Optional
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class PDFExporter:
    """Export processed content to PDF format with formatting preservation"""
    
    def __init__(self, page_size=A4):
        self.page_size = page_size
        self.styles = getSampleStyleSheet()
        self.story = []
    
    def add_heading(self, text: str, level: int = 1):
        """Add a heading with specified level"""
        style_name = 'Heading1' if level == 1 else f'Heading{level}'
        style = self.styles[style_name] if style_name in self.styles else self.styles['Heading1']
        self.story.append(Paragraph(text, style))
        self.story.append(Spacer(1, 0.2 * inch))
    
    def add_paragraph(self, text: str):
        """Add a paragraph"""
        style = self.styles['Normal']
        self.story.append(Paragraph(text, style))
        self.story.append(Spacer(1, 0.1 * inch))
    
    def add_table(self, data: pd.DataFrame, include_header: bool = True):
        """Add a table from pandas DataFrame"""
        try:
            if include_header:
                data_list = [list(data.columns)] + data.values.tolist()
            else:
                data_list = data.values.tolist()
            
            table = Table(data_list)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            self.story.append(table)
            self.story.append(Spacer(1, 0.2 * inch))
        except Exception as e:
            logger.error(f"Failed to add table: {e}")
            self.add_paragraph("[Table conversion failed]")
    
    def add_image(self, image_path: str, width: Optional[float] = None):
        """Add an image with optional width specification"""
        try:
            img = Image(image_path)
            if width:
                img.drawWidth = width * inch
                img.drawHeight = img.drawHeight * (width * inch) / img.drawWidth
            self.story.append(img)
            self.story.append(Spacer(1, 0.2 * inch))
        except Exception as e:
            logger.error(f"Failed to add image {image_path}: {e}")
            self.add_paragraph(f"[Image insertion failed: {image_path}]")
    
    def export_content(self, content: Dict[str, Any], output_path: str):
        """Export processed content to PDF file"""
        try:
            doc = SimpleDocTemplate(output_path, pagesize=self.page_size)
            
            # Add title if available
            if 'title' in content:
                self.add_heading(content['title'])
            
            # Add main content
            if 'text' in content:
                # Handle text content that might be a string or dict
                text_content = content['text']
                if isinstance(text_content, dict):
                    text_content = str(text_content)
                self.add_paragraph(text_content)
            
            # Add tables if available
            if 'tables' in content and content['tables']:
                self.add_heading('Tables', level=2)
                for table in content['tables']:
                    if isinstance(table, pd.DataFrame):
                        self.add_table(table)
                    elif isinstance(table, dict) and 'dataframe' in table:
                        self.add_table(table['dataframe'])
            
            # Add translation if available
            if 'translation' in content:
                self.add_heading('Translation', level=2)
                if isinstance(content['translation'], dict):
                    translation_text = content['translation'].get('translated_text', '')
                else:
                    translation_text = str(content['translation'])
                self.add_paragraph(translation_text)
            
            doc.build(self.story)
            logger.info(f"Successfully exported PDF to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to export PDF: {e}")
            return False
    
    def export_translation_result(self, original_text: str, translated_text: str, 
                                metadata: Dict[str, Any], output_path: str):
        """Export translation result with original and translated text"""
        try:
            doc = SimpleDocTemplate(output_path, pagesize=self.page_size)
            
            self.add_heading('Translation Result')
            
            # Add metadata
            self.add_heading('Processing Information', level=2)
            metadata_text = (
                f"Source Language: {metadata.get('detected_lang', 'Unknown').upper()}<br/>"
                f"Target Language: {metadata.get('target_lang', 'Unknown')}<br/>"
                f"Processing Time: {metadata.get('processing_time', 0):.2f}s<br/>"
                f"Confidence Score: {metadata.get('confidence', 0)*100:.1f}%"
            )
            self.add_paragraph(metadata_text)
            
            # Add original text
            self.add_heading('Original Text', level=2)
            self.add_paragraph(original_text)
            
            # Add translated text
            self.add_heading('Translation', level=2)
            self.add_paragraph(translated_text)
            
            doc.build(self.story)
            logger.info(f"Successfully exported translation to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to export translation: {e}")
            return False
