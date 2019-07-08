import io
import re
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage


class PDF_extractor:
    def miner_extract_text_by_page(self, pdf_path=None, pagenum=0):
        with open(pdf_path, 'rb') as fh:
            for pageNumber, page in enumerate(PDFPage.get_pages(fh,
                                          caching=True,
                                          check_extractable=True)):

                if pageNumber == pagenum:
                    resource_manager = PDFResourceManager()
                    fake_file_handle = io.StringIO()
                    converter = TextConverter(resource_manager, fake_file_handle)
                    page_interpreter = PDFPageInterpreter(resource_manager, converter)
                    page_interpreter.process_page(page)

                    text = fake_file_handle.getvalue()


                    # close open handles
                    converter.close()
                    fake_file_handle.close()

                    return text

    def miner_extract_all_text_from_pdf(self, pdf_path=None):
        resource_manager = PDFResourceManager()
        fake_file_handle = io.StringIO()
        converter = TextConverter(resource_manager, fake_file_handle)
        page_interpreter = PDFPageInterpreter(resource_manager, converter)

        with open(pdf_path, 'rb') as fh:
            for page in PDFPage.get_pages(fh,
                                          caching=True,
                                          check_extractable=True):
                page_interpreter.process_page(page)

            text = fake_file_handle.getvalue()

        # close open handles
        converter.close()
        fake_file_handle.close()

        if text:
            return text

    

class
if __name__ == '__main__':
    pdfpath = r'C:\Users\Choon Yee Sim\Desktop\CY\Freelancer\pdfFilepages\toPost.pdf'
    writepath = r'C:\Users\Choon Yee Sim\Desktop\CY\Freelancer\pdfFilepages\toPost.txt'
    writepath_bypage1 = r'C:\Users\Choon Yee Sim\Desktop\CY\Freelancer\pdfFilepages\toPost_bypage1.txt'

    pdfobj = PDF_extractor()
    with open(writepath, 'w+') as filewrite:
        all_text = pdfobj.miner_extract_all_text_from_pdf(pdf_path=pdfpath)
        filewrite.write(all_text)

    with open(writepath_bypage1, 'w+') as filewrite:
        pagetext = pdfobj.miner_extract_text_by_page(pdf_path=pdfpath, pagenum=1)
        filewrite.write(pagetext)
        filewrite.write('\n\n\n\n\n\n\n\n\n\n')