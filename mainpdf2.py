from PyPDF2 import PdfFileReader, PdfFileWriter


def pdf_main(pfilepath, pfilepath2):
    with open(pfilepath2, 'wb+') as fwritefile:
        with open(pfilepath, 'rb') as f:
            pdf = PdfFileReader(f)
            page = pdf.getPage(0)
            text = page.extractText()
            contents = page.getContents()
            print('page:', page)
            print('text:', text)
            print('contents:', contents)
            fwritefile.write(text.encode('utf-8'))



if __name__ == "__main__":
    path = r'C:\Users\Choon Yee Sim\Desktop\CY\Freelancer\pdfFilepages\toPost.pdf'
    writepath = r'C:\Users\Choon Yee Sim\Desktop\CY\Freelancer\pdfFilepages\toPost.txt'
    pdf_main(path, writepath)
