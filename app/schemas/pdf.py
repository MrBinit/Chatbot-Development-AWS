from pydantic import BaseModel
from typing import List

class PdfSyncResult(BaseModel):
    uploaded_files: List[str]
