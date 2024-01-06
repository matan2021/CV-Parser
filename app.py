import tkinter as tk
from tkinter import ttk, filedialog
import pymongo
from bson import ObjectId
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pymongo import MongoClient
import re
import spacy
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from pytesseract import pytesseract
import shutil

nlp = spacy.load("en_core_web_sm")

#extract text from PDF file
def extract_text_from_pdf(pdf_path):
    text = ''
    if pdf_path.endswith('.pdf'):
        pdf = PdfReader(pdf_path)
        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            text += page.extract_text()
    else:
        images = convert_from_path(pdf_path)
        for image in images:
            text += pytesseract.image_to_string(image)
    return text

#extract full name from text
def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return None

#extract email from text
def extract_email(text):
    email_pattern = r'\S+@\S+'
    match = re.search(email_pattern, text)
    if match:
        return match.group()
    else:
        return None

#extract phone number from text
def extract_phone_number(text):
    phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    match = re.search(phone_pattern, text)
    if match:
        return match.group()
    else:
        return None

#extract ID from text
def extract_id(text):
    # Define a regular expression pattern to match a 9-digit numeric ID
    id_pattern = r'\b\d{9}\b'
    # Search for the ID pattern in the text
    match = re.search(id_pattern, text)
    if match:
        return match.group()  # Return the matched ID as a string
    else:
        return None  # Return None if no ID is found

#extract linkedin url from text
def extract_linkedln(text):
    # Define a regular expression pattern to match LinkedIn profile URLs
    linkedin_pattern = "https://www.linkedin.com/in/"+name.lower().replace(' ','')
    text = "https://www.linkedin.com/in/"+name.lower().replace(' ','')
    matches = re.findall(linkedin_pattern, text)
    if matches:
        return matches # Return a list of matched LinkedIn URLs
    else:
        return None  # Return None if no LinkedIn URLs are found


#   function to crate a copy of applicant's CV as a PDF
def download_fields():
    selected_item = tree.selection()
    if selected_item:
        applicant_id = tree.item(selected_item, "values")[0]
        obj=ObjectId(applicant_id)
        applicant = collection.find_one({"_id": obj})
        if applicant:
            name = applicant["Name"]
            id=applicant["Id"]
            email=applicant["Email"]
            phone=applicant["phone_number"]
            linkedin=applicant["linkedin"]
            pdf_filename = f"C:/Users/97254/Desktop/{name}_CV_new.pdf"
            c = canvas.Canvas(pdf_filename, pagesize=letter)
            c.setFont("Helvetica",20)
            c.drawString(250, 750,  f"CV of {(name)}")
            c.drawString(100, 730, "----------------------------------------------------------------------------")
            c.setFont("Helvetica",12)
            c.drawString(100, 710, f"ID: {id}")
            c.drawString(100, 670, f"Email: {email}")
            c.drawString(100, 630, f"Phone Number: {phone}")
            c.drawString(100, 590, f"Linkedin: {linkedin}")
            c.save()
            print(f"Summary of cv for {name} downloaded successfully as {pdf_filename}")

#  function to download a new pdf file with the selected applicant record
def download_cv():
    selected_item = tree.selection()
    if selected_item:
        applicant_id = tree.item(selected_item, "values")[0]
        obj=ObjectId(applicant_id)
        applicant = collection.find_one({"_id": obj})
        # pdf_path = cv_file_path
        if applicant:
                # Construct the output path on the desktop
                output_path = 'C:\\Users\\97254\\Desktop\\copy CV '+name+'.pdf'
                # Copy the PDF file to the desktop
                shutil.copy(pdf_path, output_path)
                print(f"CV for {name} downloaded successfully as {output_path}")

#  function to delete the selected applicant record
def delete_applicant():
    selected_item = tree.selection()
    if selected_item:
        applicant_id = tree.item(selected_item, "values")[0]
        obj2=ObjectId(applicant_id)
        result=collection.delete_one({"_id": obj2})
        tree.delete(selected_item)
        # Check if a document was deleted
        try:
            if result.deleted_count > 0:
                print("Document deleted successfully")

            else:
                print("No matching document found for deletion")
        except pymongo.errors.PyMongoError as e:
            print(f"An error occurred: {e}")

#function to upload CV
def upload_cv():
    global pdf_path
    cv_file_path = filedialog.askopenfilename(
        title="Select CV File",
        filetypes=[("PDF files", "*.pdf")]
    )
    if cv_file_path:
        print(f"Selected CV file: {cv_file_path}")
        window2.destroy()
        pdf_path= cv_file_path

    else:
        print("No file selected")

# The main application loop
if __name__ == '__main__':
    pdf_path=None
    window2 = tk.Tk()
    window2.title("Applicant Management System For Upload")
    # a button to upload CV
    upload_button = tk.Button(window2, text="Upload CV",command=upload_cv)
    upload_button.pack()
    window2.mainloop()
    if pdf_path:
        # The main window
        window = tk.Tk()
        window.title("Applicant Management System")
        # The treeview widget to display applicant records
        tree = ttk.Treeview(window, columns=("ObjectId", "ID", "Name", "Email", "Phone", "Linkedin"))
        tree.heading("ObjectId", text="ObjectId")
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Email", text="Email")
        tree.heading("Phone", text="Phone")
        tree.heading("Linkedin", text="Linkedin")
        tree.pack()
        # a button to download  selected fields of CV
        download_fields_button = tk.Button(window, text="Download PDF With The Selected Fields",command=download_fields)
        download_fields_button.pack()
        # a button to download original CV
        download_button = tk.Button(window, text="Download CV", command=download_cv)
        download_button.pack()
        # a button to delete the selected record
        delete_button = tk.Button(window, text="Delete Applicant", command=delete_applicant)
        delete_button.pack()
    resume_text = extract_text_from_pdf(pdf_path)
    #Fields from the CV
    id = extract_id(resume_text)
    name = extract_name(resume_text)
    email = extract_email(resume_text)
    phone_number = extract_phone_number(resume_text)
    linkedin = extract_linkedln(resume_text)
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["CVParser"]
    collection = db["extracted_data"]
    # a document to store the extracted data
    data = {
        "Id": id,
        "Name": name,
        "Email": email,
        "phone_number": phone_number,
        "linkedin": linkedin
    }
    # Insert the data into the collection
    collection.insert_one(data)
    print("Data stored in MongoDB.")
    obj3 =(data["_id"])
    for applicant in collection.find():
        tree.insert("", "end", values=(
        obj3,str(applicant["Id"]), applicant["Name"], applicant["Email"], applicant["phone_number"], applicant["linkedin"]))
    print("Object id:"+str(applicant["_id"]))
    window.mainloop()
