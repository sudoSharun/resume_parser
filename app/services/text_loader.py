from langchain_community.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader
import os
import ocrmypdf

class ExtractText:
    def __init__(self, filepath: str):
        self.file_path = filepath
        self.text_content = self.extract()

    def extract_pdf(self):
        ocrmypdf.ocr(self.file_path, self.file_path, redo_ocr = True)
        document = PyPDFLoader(self.file_path)
        pages = document.load()
        text = "\n".join([page.page_content for page in pages])
        return text

    def extract_docx(self):
        doc = UnstructuredWordDocumentLoader(self.file_path).load()
        text = "\n".join(page.page_content for page in doc)
        return text

    def extract(self):
        ext = os.path.splitext(self.file_path)[-1].lower()
        match ext:
            case ".pdf": return self.extract_pdf()
            case ".docx" | ".doc": return self.extract_docx()
            case "": return ""
        return ""