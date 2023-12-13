import PyPDF2
pdf_file_path = r"C:\Users\sriva\Downloads\notes1.pdf"
pdf_file = open(pdf_file_path, "rb")
pdf_reader = PyPDF2.PdfReader(pdf_file)
text = []
for page_num in range(len(pdf_reader.pages)):
    page = pdf_reader.pages[page_num]
    text.append(page.extract_text())
pdf_file.close()
full_text = "\n".join(text)
print(full_text)
