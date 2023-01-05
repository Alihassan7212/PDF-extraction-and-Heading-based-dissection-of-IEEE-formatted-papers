import PyPDF2, tabula, fitz, textblob, operator, builtins


def input_file():
    pdf_filename = input("Enter name of PDF File: ") + ".pdf"
    
    try:
        PyPDF2.PdfFileReader(pdf_filename)
    except FileNotFoundError:
        print("File not found! Try again")
        input_file()

    return pdf_filename


def continue_or_quit():
    will_continue = input("Do you wish to continue [Y/N]? ")

    return will_continue


def select_option():
    print("[1]  Store the metadata of the document in a text file")
    print("[2]  Extract all the raw text from the document")
    print("[3]  Store all tabular data in CSV files")
    print("[4]  Perform sentiment analysis on the entire document")
    print("[5]  Store all images in separate files")
    print("[6]  Store the word and sentence count in a text file, also creating a file containing all the text")
    print("[7]  Create a separate PDF of selected pages, and another of the remaining pages")
    print("[8]  Print all headers, paragraphs and subscripts with labels")
    print("[9]  Perform sentiment analysis on a specific page")
    print("[10] Words Frequecy from the document")
    print("[11] Store the image and table count in a separate text file")
    print("[12] heading based dissection")
    print("[13] Reduce Image size")
    print("[14] Area Covered by Pictures")
    selected_option = int(input("What would you like to do? "))

    return selected_option


def store_metadata(pdf_filename):
    metadata_filename = pdf_filename.replace(".pdf", "_metadata.txt")

    with open(metadata_filename, "w", encoding="UTF-16") as f:
        f.write(str(PyPDF2.PdfFileReader(pdf_filename).documentInfo))


def extract_text(pdf_filename):
    pdf_file_object = PyPDF2.PdfFileReader(pdf_filename)

    for page in range(len(pdf_file_object.pages)):
        print(pdf_file_object.pages[page].extract_text())


def store_tables(pdf_filename):
    pdf_tables = tabula.read_pdf(pdf_filename, pages="all")
    table_filename = pdf_filename.replace(".pdf", "")

    for table in range(len(pdf_tables)):
        pdf_tables[table].to_csv(f"{table_filename}_table{table+1}.csv")


def perform_document_analysis(pdf_filename):
    analysis_result = ""
    document_text = ""
    document_pages = PyPDF2.PdfFileReader(pdf_filename).pages

    for page in range(len(document_pages)):
        document_text += document_pages[page].extract_text()
    
    document_polarity = textblob.TextBlob(document_text).sentiment.polarity

    if -1 <= document_polarity <= -0.5:
        analysis_result = "The document is very negative"
    elif -0.5 < document_polarity <= -0.1:
        analysis_result = "The document is negative"
    elif -0.1 < document_polarity <= -0.01:
        analysis_result = "The document is slightly negative"
    elif -0.01 < document_polarity <= 0:
        analysis_result = "The document is almost neutral but very slightly negative"
    elif document_polarity == 0:
        analysis_result = "The document is neutral"
    elif 0 < document_polarity <= 0.01:
        analysis_result = "The document is almost neutral but slightly positive"
    elif 0.01 < document_polarity <= 0.1:
        analysis_result = "The document is slightly positive"
    elif 0.1 < document_polarity <= 0.5:
        analysis_result = "The document is positive"
    elif 0.5 < document_polarity <= 1:
        analysis_result = "The document is very positive"
    
    return document_polarity, analysis_result


def perform_page_analysis(pdf_filename, page_number):
    analysis_result = ""
    page_text = PyPDF2.PdfFileReader(pdf_filename).pages[page_number].extract_text() 
    
    page_polarity = textblob.TextBlob(page_text).sentiment.polarity

    if -1 <= page_polarity <= -0.5:
        analysis_result = "The page is very negative"
    elif -0.5 < page_polarity <= -0.1:
        analysis_result = "The page is negative"
    elif -0.1 < page_polarity <= -0.01:
        analysis_result = "The page is slightly negative"
    elif -0.01 < page_polarity <= 0:
        analysis_result = "The page is almost neutral but very slightly negative"
    elif page_polarity == 0:
        analysis_result = "The page is neutral"
    elif 0 < page_polarity <= 0.01:
        analysis_result = "The page is almost neutral but slightly positive"
    elif 0.01 < page_polarity <= 0.1:
        analysis_result = "The page is slightly positive"
    elif 0.1 < page_polarity <= 0.5:
        analysis_result = "The page is positive"
    elif 0.5 < page_polarity <= 1:
        analysis_result = "The page is very positive"
    
    return page_polarity, analysis_result

def store_images(pdf_filename):
    img_base_filename = pdf_filename.replace(".pdf", "")
    pdf_file_object = fitz.open(pdf_filename)

    for page_number, page in enumerate(pdf_file_object.pages(), start=1):
        for image_number, image in enumerate(page.get_images(), start=1):
            xref = image[0]
            pix = fitz.Pixmap(pdf_file_object, xref)

            if pix.n > 4:
                pix = fitz.Pixmap(fitz.csRGB, pix)
            
            pix._writeIMG(f"{img_base_filename}_page{page_number}_image{image_number}.png", format=1)


def store_word_sentence_count(pdf_filename):
    text_filename = pdf_filename.replace(".pdf", ".txt")
    count_filename = text_filename.replace(".txt", "_count.txt")
    pdf_file_pages = PyPDF2.PdfFileReader(pdf_filename).pages
    word_count = 0
    sentence_count = 0

    with open(text_filename, "w", encoding="UTF-16") as f:
        for page in range(len(pdf_file_pages)):
            f.write(pdf_file_pages[page].extract_text())
    
    with open(text_filename, "r") as f:
        for line in f:
            words = line.split(" ")
            word_count += len(words)
            sentences = line.split(".")
            sentence_count += len(sentences)
    p=word_count/len(pdf_file_pages)
    if p>800:
        print("100 percent area is covered by text only")
    else:
        p=(p/800)*100
        print(p,"% area is covered by text only\n")
        print(100-p,"% area is covered by text only\n")
    with open(count_filename, "w") as f:
        f.write(f"Number of words: {word_count}\nNumber of sentences: {sentence_count}")


def extract_pages(pdf_filename):
    first_page_index = int(input("Enter the first page to be extracted: ")) - 1
    last_page_index = int(input("Enter the last page to be extracted: "))
    split_filename = pdf_filename.replace(".pdf", "_split.pdf")
    rest_filename = pdf_filename.replace(".pdf", "_rest.pdf")
    pages_to_extract = list(range(first_page_index, last_page_index))

    with open(pdf_filename, "rb") as f:
        read_file = PyPDF2.PdfFileReader(f)
        write_file = PyPDF2.PdfFileWriter()
        rest_file = PyPDF2.PdfFileWriter()

        for page in range(len(read_file.pages)):
            if page in pages_to_extract:
                write_file.addPage(read_file.getPage(page))
            else:
                rest_file.addPage(read_file.getPage(page))

        with open(split_filename, "wb") as f2:
            write_file.write(f2)
        with open(rest_filename, "wb") as f2:
            rest_file.write(f2)


def extract_headers_para(pdf_filename):
    pdf_file_object = fitz.open(pdf_filename)
    font_styles = {}
    font_counts = {}

    #getting font counts and styles
    for page in pdf_file_object:
        blocks = page.get_text('dict')['blocks']
        for b in blocks:
            if b['type'] == 0:
                for l in b['lines']:
                    for s in l['spans']:
                        identifier = "{0}".format(s['size'])
                        font_styles[identifier] = {'size': s['size'], 'font': s['font']}
                        font_counts[identifier] = font_counts.get(identifier, 0) + 1
    
    font_counts = sorted(font_counts.items(), key=operator.itemgetter(1), reverse=True)
    
    if len(font_counts) < 1:
        raise ValueError("Zero discriminating fonts found!")

    #creating HTML style tags for font sizes
    p_style = font_styles[font_counts[0][0]]
    p_size = p_style['size']
    font_sizes = []
    for (font_size, count) in font_counts:
        font_sizes.append(float(font_size))
    font_sizes.sort(reverse=True)

    index = 0
    size_tag = {}
    for size in font_sizes:
        index += 1
        if size == p_size:
            index = 0
            size_tag[size] = '<p>'
        if size > p_size:
            size_tag[size] = '<h{0}>'.format(index)
        elif size < p_size:
            size_tag[size] = '<s{0}>'.format(index)
    
    #separating headers and paragraphs
    header_para = []
    first = True
    previous_s = {}

    for page in pdf_file_object:
        blocks = page.get_text('dict')['blocks']
        for b in blocks:
            if b['type'] == 0:
                block_string = ""
                for l in b['lines']:
                    for s in l['spans']:
                        if s['text'].strip():
                            if first:
                                previous_s = s
                                first = False
                                block_string = size_tag[s['size']] + s['text']
                            else:
                                if s['size'] == previous_s['size']:
                                    if block_string and all((c == '|') for c in block_string):
                                        block_string = size_tag[s['size']] + s['text']
                                    if block_string == "":
                                        block_string = size_tag[s['size']] + s['text']
                                    else:
                                        block_string += " " + s['text']
                                else:
                                    header_para.append(block_string)
                                    block_string = size_tag[s['size']] + s['text']

                                previous_s = s

                    block_string += "|"

                header_para.append(block_string)

    for heading in header_para:
        headings_paragraphs = heading.split("|")
        if headings_paragraphs == "' ', ' '" or headings_paragraphs == "' '":
            continue
        else:
            for word in headings_paragraphs:
                print(word)


def extract_references(pdf_filename):
    #Python code for Word frequency in pdf file
    from collections import Counter

    # Open the PDF file in read-binary mode
    with open(pdf_filename, 'rb') as file:
  # Create a PDF object
        pdf = PyPDF2.PdfFileReader(file)
    # Initialize an empty list to store the words
        words = []
  
    # Iterate through the pages and extract the words
        for page in range(pdf.getNumPages()):
            page_text = pdf.getPage(page).extractText()
            words += page_text.split()
    # Count the frequency of each word
        word_counts = Counter(words)
  # Print the word frequency counts
        for word, count in word_counts.items():
            print(f'{word}: {count}')
    


def store_image_table_count(pdf_filename):
    count_filename = pdf_filename.replace(".pdf", "_image_table_count.txt")
    pdf_tables = tabula.read_pdf(pdf_filename, pages="all")
    pdf_images = fitz.open(pdf_filename)
    image_count = 0
    table_count = 0

    for table in range(len(pdf_tables)):
        table_count += 1
    for i, page in enumerate(pdf_images.pages()):
        for image in enumerate(page.get_images()):
            image_count += 1
    
    with open(count_filename, "w") as f:
        f.write(f"Image count = {image_count}\nTable count = {table_count}")
    
def dissector(pdf_filename):
    from pdfminer.high_level import extract_text
    import re
    from fpdf import FPDF
    #filename = input("Enter filename of IEEE formatted research Paper with extension: ")
    text = extract_text(pdf_filename)

    #Encode the text to utf for slightly better formatting/easier detection of headers
    text2 = text.encode('utf-8')

    #regex pattern to detect headers. It looks for pattern e.g IV. This is a header
    pattern = r'(?<=\n)[IV]+\.\s*.*?(?=\n)'
    check_reference = r'References|REFERENCES'  #Regex pattern to detect word "References" in text
    reference = re.findall(check_reference, text, re.M) #Find the word References
    headers = []
    raw_headers = re.findall(pattern,text,re.M) #Find all the headers present in the text

    print(reference)
    for heading in raw_headers:
        heading = heading.replace("\n",' ') #Cleaning of header since it was in utf-8 format and to allow for it to be written as file name '''
        heading2 = heading.replace(","," ") #Same task as above
        headers.append(heading2)
    print(headers)

    heading_amount = len(headers)   #No of headings obtained
    count = 0
    i = 0
    while (count <= (heading_amount)):
        try:
            #Check if the heading list is completed then set index from references till end of text
            if (count == heading_amount):  
                start_index = text.find(reference[0])
                end_index = (len(text)-1)
            else:
                #set text extraction index between the first heading and the last heading and the last heading till references
                start_index = text.find(headers[count])
            if (count == heading_amount - 1):
                end_index = text.find(reference[0])
            else:    
                end_index = text.find(headers[count + 1])
        except:
            break

        # Extract the text between the delimiters
        extracted_text = text[start_index:end_index]
        extracted_text.encode('utf-8')
        #Add the text to a newly created PDF along with its heading name
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
        pdf.set_font('DejaVu', size=12)
        pdf.multi_cell(0, 5,extracted_text)
        if (count == heading_amount):
            pdf.output(pdf_filename + " REFERENCES" +".pdf")
        else:
            pdf.output(headers[i] +".pdf")
        count += 1
        i += 1

def reducesiz(pdf_filename):
    #Reduce the size of pdf
    from PyPDF2 import PdfReader, PdfWriter
    reader = PdfReader(pdf_filename)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    writer.add_metadata(reader.metadata)
    with open("Smallers-new-file.pdf", "wb") as fp:
        writer.write(fp)
        