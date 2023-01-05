import PDFDissector
def main():
    while True:
        pdf_filename = PDFDissector.input_file()
        choice = PDFDissector.select_option()

        if choice == 1:
            PDFDissector.store_metadata(pdf_filename=pdf_filename)
            print("Successful!")
        elif choice == 2:
            PDFDissector.extract_text(pdf_filename=pdf_filename)
            print("Successful!")
        elif choice == 3:
            PDFDissector.store_tables(pdf_filename=pdf_filename)
            print("Successful!")
        elif choice == 4:
            print(PDFDissector.perform_document_analysis(pdf_filename=pdf_filename)[0])
            print(PDFDissector.perform_document_analysis(pdf_filename=pdf_filename)[1])
            print("Successful!")
        elif choice == 5:
            PDFDissector.store_images(pdf_filename=pdf_filename)
            print("Successful!")
        elif choice == 6:
            PDFDissector.store_word_sentence_count(pdf_filename=pdf_filename)
            print("Successful!")
        elif choice == 7:
            PDFDissector.extract_pages(pdf_filename=pdf_filename)
            print("Successful!")
        elif choice == 8:
            PDFDissector.extract_headers_para(pdf_filename=pdf_filename)
            print("Successful!")
        elif choice == 9:
            page_number = int(input("Enter the page number that you want to analyze: "))
            print(PDFDissector.perform_page_analysis(pdf_filename=pdf_filename, page_number=page_number)[0])
            print(PDFDissector.perform_page_analysis(pdf_filename=pdf_filename, page_number=page_number)[1])
            print("Successful!")
        elif choice == 10:
            print(PDFDissector.extract_references(pdf_filename=pdf_filename))
        elif choice == 11:
            PDFDissector.store_image_table_count(pdf_filename=pdf_filename)
            print("Successful!")
        elif choice == 12:
            PDFDissector.dissector(pdf_filename=pdf_filename)
            print("Successful!")
        elif choice == 13:
            PDFDissector.reducesiz(pdf_filename=pdf_filename)
            print("Successful!")
        elif choice == 14:
            PDFDissector.store_word_sentence_count(pdf_filename=pdf_filename)
            print("Successful!")
        else:
            print("Invalid choice!")
            continue

        to_continue = PDFDissector.continue_or_quit().upper()
        if to_continue == "Y":
            continue
        elif to_continue == "N":
            break
        else:
            print("Invalid response!")
            continue


if __name__ == "__main__":
    main()