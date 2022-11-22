import PyPDF2
from ioc_finder import find_iocs
import fire
from datetime import datetime

def scan(pdf_path):
    '''
    Extract IOC's from pdf pages
    '''
    empty = find_iocs("")
    report_path = f"{pdf_path}-ioc_report_{datetime.today().strftime('%Y%m%d')}.txt"
    with open(pdf_path,"rb") as pdf_file, open(report_path,"w") as report:
        read_pdf = PyPDF2.PdfFileReader(pdf_file,strict=False)
        number_of_pages = read_pdf.getNumPages()
        for page_number in range(number_of_pages):
            page = read_pdf.getPage(page_number)
            iocs = find_iocs(page.extractText())
            if not bool(empty==iocs):
                print(f'\nIOC found in page {page_number}/{number_of_pages}')
                print(iocs)
                report.write(f'Possible IOC found in page {page_number}/{number_of_pages}\n')
                for key, value in iocs.items():
                    if value and value != iocs['attack_tactics'] and value != iocs['attack_mitigations'] and value != iocs["attack_techniques"]:
                        report.write(f'\n{key} : {value}')
                report.write(f'\n-----------------------------------\n')

    print(f"[+] check your report results in {report_path}")

if __name__ == "__main__":
    fire.Fire()