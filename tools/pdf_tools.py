from langchain.tools import tool
from pydantic import BaseModel, Field
import PyPDF2
import os


class PDFReadInput(BaseModel):
    """Input schema for the PDF reading tool."""
    file_path: str = Field(description="Full file path of the PDF to read from your system")
    extract_conclusion: bool = Field(
        default=False, 
        description="If True, attempts to extract the conclusion section text."
    )


@tool("read_pdf_file", args_schema=PDFReadInput, description="Read and extract text content from a PDF file on the system.")
def read_pdf_file(file_path: str, extract_conclusion: bool = False) -> str:
    """
    Reads the contents of a given PDF file and optionally extracts the conclusion section.
    
    Args:
        file_path: The full path to the PDF file.
        extract_conclusion: If True, only extracts the 'Conclusion' section.
    Returns:
        A string containing the extracted text or relevant section.
    """
    if not os.path.exists(file_path):
        return f"❌ File not found at: {file_path}"

    title, conclusion, text_output = None, None, ""

    try:
        with open(file_path, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)

            # Read all pages
            for page_num in range(pdf_reader.numPages):
                page_text = pdf_reader.getPage(page_num).extractText()
                text_output += page_text + "\n"

                # Capture title and conclusion heuristically
                if page_num == 0 and not title:
                    title = page_text.split('\n')[0].strip()
                if extract_conclusion and "Conclusion" in page_text:
                    conclusion_index = page_text.find("Conclusion")
                    conclusion = page_text[conclusion_index:].strip()
                    break

        if extract_conclusion:
            if conclusion:
                return f"📘 **Title:** {title or 'Unknown'}\n\n🧩 **Conclusion Section:**\n{conclusion}"
            else:
                return "⚠️ 'Conclusion' section not found in the PDF."

        return f"📘 **Title:** {title or 'Unknown'}\n\n📄 **Full Text Extracted:**\n{text_output.strip()}"

    except Exception as e:
        return f"❌ Error while reading {file_path}: {str(e)}"
