
Applicant Management System
This is a Python program that serves as an Applicant Management System. It allows you to upload and manage applicant information, including their CVs.
 The program is built using the Tkinter graphical user interface library for the front-end and MongoDB for data storage.
 It also utilizes various Python libraries for text extraction, PDF processing, and image recognition.

Features
Upload applicant CVs in PDF format.
Extract information from CVs, including name, email, phone number, and LinkedIn profile.
Display applicant records in a table.
Download original CVs or a summary of selected fields as PDF files.
Delete applicant records from the system.

Prerequisites
Before running the program, ensure you have the following installed on your system:
Python 3
Tkinter
MongoDB
Required Python libraries (PyMongo, spacy, PyPDF2, pdf2image, pytesseract, reportlab)

Getting Started
1.Clone the repository to your local machine:
2.Install the required Python libraries using pip:
3.Start your MongoDB server. Make sure it's running on mongodb://localhost:27017.
4.Run the program


Usage
1.Launch the program. A window will open with an "Upload CV" button.
2.Click the "Upload CV" button to select an applicant's CV in PDF format. The program will extract information from the CV and store it in the MongoDB database.
3.Once the CV is uploaded, you can see the applicant's information displayed in a table.
4.You can select an applicant's record and use the following buttons:
	-Download PDF With The Selected Fields": This button will generate a PDF file with the selected fields from the applicant's record.
	-Download CV": This button allows you to download the original CV in PDF format.
	-Delete Applicant": Use this button to delete the selected applicant's record from the system.

Note
If the program throws a "keyError: Arial" error, make sure you have a font that is available on your system and recognized by the reportlab library.
You can check available fonts using the provided code and update the font name accordingly
The program will only work if the MongoDB server is running on mongodb://localhost:27017. Ensure that MongoDB is properly set up and configured.
The program uses various Python libraries for text extraction and processing. Make sure to install all required libraries as mentioned in the "Prerequisites" section.
The program's main window opens after uploading an applicant's CV. The window2 is destroyed automatically after a file is selected.

Author
Matan Ben Ishay
Contact: matan12333445@email.com