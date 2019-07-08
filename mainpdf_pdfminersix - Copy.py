import io

from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

class PDFMiner:
    def extract_text_by_page(self, pdf_path, pagenum):
            with open(pdf_path, 'rb') as fh:
                for page in PDFPage.get_pages(fh,
                                              caching=True,
                                              check_extractable=True):
                    resource_manager = PDFResourceManager()
                    fake_file_handle = io.StringIO()
                    converter = TextConverter(resource_manager, fake_file_handle)
                    page_interpreter = PDFPageInterpreter(resource_manager, converter)
                    page_interpreter.process_page(page)

                    text = fake_file_handle.getvalue()
                    return text

                    # close open handles
                    converter.close()
                    fake_file_handle.close()


    # def extract_text(pdf_path):
    #     for page in extract_text_by_page(pdf_path):
    #         print(page)
    #         print()

    def extract_all_text_from_pdf(self, pdf_path):
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


if __name__ == '__main__':
    pdfpath = r'C:\Users\Choon Yee Sim\Desktop\CY\Freelancer\pdfFilepages\toPost.pdf'
    writepath = r'C:\Users\Choon Yee Sim\Desktop\CY\Freelancer\pdfFilepages\toPost.txt'
    writepath_bypage = r'C:\Users\Choon Yee Sim\Desktop\CY\Freelancer\pdfFilepages\toPost_bypage.txt'


    with open(writepath, 'w+') as filewrite:
        all_text = extract_all_text_from_pdf(pdfpath)
        filewrite.write(all_text)

    with open(writepath_bypage, 'w+') as filewrite:
        for page in extract_text_by_page(pdfpath):
            filewrite.write(page)
            filewrite.write('\n\n\n\n\n\n\n\n\n\n')