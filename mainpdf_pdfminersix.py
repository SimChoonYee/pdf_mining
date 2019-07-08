import io
import re
import os
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage

from PyPDF2 import PdfFileReader, PdfFileWriter

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

    def search_regex_crewid(self, ptext):
        matchid = re.search(r'crew id:\w{6}', ptext)
        print('matchid', matchid)
        if matchid:
            return matchid
        else:
            return None

    def pdf_splitter(self, crewidnum="", pdf_path=None, start_page_pdf=None, end_page_pdf=None):
        '''
        Need to add this statement "from PyPDF2 import PdfFileReader, PdfFileWriter"
        :param crewidnum: add a name if you need
        :param pdf_path: the full pdf path that you need to split, i.e. r'C:\Users\etc.pdf'
        :param start_page_pdf: just provide a start page number
        :param end_page_pdf: and a end page number that you want to split
        :return:
        '''
        print('start_page_pdf:', start_page_pdf, 'end_page_pdf:', end_page_pdf, 'crewidnum:', crewidnum)
        pdf = PdfFileReader(pdf_path)
        pdf_writer = PdfFileWriter()
        for i in range(start_page_pdf, (end_page_pdf+1)):
            pdf_writer.addPage(pdf.getPage(i))
            print(i)

        output_filename = '{}_page_{}_{}.pdf'.format(crewidnum, start_page_pdf,  end_page_pdf)
        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)
            print('Created: {}'.format(output_filename))

    def pdf_getpagenumber(self, pdf_path):
        pdf_getpagenumberobj = PdfFileReader(pdf_path)
        return pdf_getpagenumberobj.getNumPages()


if __name__ == '__main__':
    pdfpath = r'C:\Users\Choon Yee Sim\Desktop\CY\Freelancer\pdfFilepages\toPost.pdf'
    writepath = r'C:\Users\Choon Yee Sim\Desktop\CY\Freelancer\pdfFilepages\toPost.txt'
    writepath_bypage0 = r'C:\Users\Choon Yee Sim\Desktop\CY\Freelancer\pdfFilepages\toPost_bypage0.txt'

    pdfobj = PDF_extractor()
    with open(writepath, 'w+') as filewrite:
        all_text = pdfobj.miner_extract_all_text_from_pdf(pdf_path=pdfpath)
        filewrite.write(all_text)

    with open(writepath_bypage0, 'w+') as filewrite:
        pdf_pagenum = pdfobj.pdf_getpagenumber(pdf_path = pdfpath)
        start_page = None
        end_page = None
        crewidnumber = str(-1)

        for i in range(0, pdf_pagenum):
            print('i', i, 'pdf_pagenum', pdf_pagenum)
            pagetext = pdfobj.miner_extract_text_by_page(pdf_path=pdfpath, pagenum=i)
            # filewrite.write(pagetext)
            crewid_regexobj = pdfobj.search_regex_crewid(pagetext)

            if crewid_regexobj and start_page is None:
                # Meaning it found a crewid page
                print('Found a crewid page')
                start_page = i
                crewidnumber = crewid_regexobj.group(0)[-6:]
            elif crewid_regexobj is None and start_page is not None and i != (pdf_pagenum-1):
                # Meaning, it start counting the subpages
                print('Found a subpage')
                end_page = i
            elif crewid_regexobj and start_page is not None:
                # Meaning it met another crewid
                # split
                print('SPLIT!')
                start_page = i
                end_page = i
                crewidnumber = crewid_regexobj.group(0)[-6:]
                pdfobj.pdf_splitter(crewidnum=crewidnumber, pdf_path=pdfpath,
                             start_page_pdf=start_page, end_page_pdf=end_page)
            elif i == (pdf_pagenum-1):
                # -1 as pagenum is startpage start at 0
                print('END of PDF')
                print('SPLIT!')
                end_page = i
                pdfobj.pdf_splitter(crewidnum=crewidnumber, pdf_path=pdfpath,
                             start_page_pdf=start_page, end_page_pdf=end_page)
            else:
                print('The page is not a start page nor a end page')










