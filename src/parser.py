from dataclasses import dataclass
import re
from enum import Enum

class RecordType(str, Enum):
    PARAGRAPH = "paragraph"
    ANNEX = "annex"
    APPENDIX = "appendix"
    FIGURE = "figure"
    FOOTNOTE = "footnote"
    NORMAL = "normal"

class DocumentParser:

    def clean_text(self, text: str) -> str:
        if not text:
            text = ""
        
        text = text.strip()
        text = re.sub(r"\s+", " ", text)

        return text

    def detect_record_type(self, text: str) -> RecordType:

        if not text:
            return RecordType.NORMAL

        # specific to more general one
        flag = re.match(r"^Annex\s+\d+\s*[-–]\s*Appendix\s+\d+\b", text)
        if flag:
             return RecordType.APPENDIX
        
        flag = re.match(r"^Annex\s+\d+\b", text)
        if flag:
            return RecordType.ANNEX
        
        flag = re.match(r"^Appendix\s+\d+\b", text)
        if flag:
            return RecordType.APPENDIX
        
        flag = re.match(r"^Figure\s+\d+\b", text)
        if flag:
            return RecordType.FIGURE
        
        flag = re.match(r"^\d+[A-Za-z(\"']", text)
        if flag:
            return RecordType.FOOTNOTE 
            
        flag = re.match(r"^\d+(?:\.\d+)*\.?(?:\s|$)", text)
        if flag:
            return RecordType.PARAGRAPH   
        
        return RecordType.NORMAL
    
    def extract_label(self, text: str, record_type: RecordType):

        if record_type == RecordType.PARAGRAPH:
            match = re.match(r"^(\d+(?:\.\d+)*)\.?", text)
            if match:
                return match.group(1)
            return None
        
        if record_type == RecordType.ANNEX:
            match = re.match(r"^(Annex\s+\d+)", text)
            if match:
                return match.group(1)
            return None

        if record_type == RecordType.APPENDIX:
            match = re.match(r"^(Annex\s+\d+\s*[-–]\s*Appendix\s+\d+)", text)
            if match:
                return match.group(1)
            
            match = re.match(r"^(Appendix\s+\d+)", text)
            if match:
                return match.group(1)
            
            return None

        if record_type == RecordType.FIGURE:
            match = re.match(r"^(Figure\s+\d+)", text)
            if match:
                return match.group(1)
            return None
    
        return None
    
    def extract_body_text(self, text: str, record_type: RecordType, label: str | None) -> str:
        
        if not text:
            return ""

        if label and text.startswith(label):
            if record_type.value == "paragraph":
                return text[len(label):].lstrip(" .:-–")

            if record_type.value == "annex":
                return text[len(label):].lstrip(" .:-–")

            if record_type.value == "appendix":
                return text[len(label):].lstrip(" .:-–")

            if record_type.value == "figure":
                return text[len(label):].lstrip(" .:-–")

        return text

    def run(self, text:str) -> dict:

        text = self.clean_text(text)
        record_type = self.detect_record_type(text)
        label = self.extract_label(text, record_type)
        body_text = self.extract_body_text(text, record_type, label)

        return {"text": text, "type": record_type.value, "label": label, "body_text": body_text}

