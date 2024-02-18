import nest_asyncio
import subprocess

nest_asyncio.apply()


def convert_pdf_to_html(pdf_name):
    command = f"pdf2htmlEX {pdf_name} --dest-dir result"
    subprocess.call(command, shell=True)
