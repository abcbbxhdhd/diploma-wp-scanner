import pdfkit
import json
from utils import llm_util
import pdfkit


def generate_report_from_json(jsonData, scanId):
    path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

    html_content = llm_util.ask_generate_report(jsonData)
    return pdfkit.from_string(html_content, output_path=False, configuration=config)
