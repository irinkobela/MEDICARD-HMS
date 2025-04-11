# load_terms.py

import os
from run import app, db # Import your Flask app and db instance
from models.models import MedicalTerm # Import your MedicalTerm model

# --- Embedded Terms Data (Converted from JSON) ---
terms_data = {
  "Patient Management & Registration": [
    {
      "term": "Patient",
      "translation": "პაციენტი",
      "transliteration": "Patsienti",
      "note": ""
    },
    {
      "term": "Admission",
      "translation": "მიღება",
      "transliteration": "Migheba",
      "note": "Use 'Hospitalizatsia' for actual hospitalization"
    },
    {
      "term": "Discharge",
      "translation": "გაწერა",
      "transliteration": "Gatsera",
      "note": ""
    },
    {
      "term": "Transfer",
      "translation": "გადაყვანა",
      "transliteration": "Gadayvana",
      "note": "Between units/facilities"
    },
    {
      "term": "Inpatient",
      "translation": "სტაციონარული პაციენტი",
      "transliteration": "Statsionaruli Patsienti",
      "note": ""
    },
    {
      "term": "Outpatient",
      "translation": "ამბულატორიული პაციენტი",
      "transliteration": "Ambulatoriuli Patsienti",
      "note": ""
    },
    {
      "term": "Patient ID",
      "translation": "პაციენტის ნომერი",
      "transliteration": "Patsientis Nomeri",
      "note": ""
    },
    {
      "term": "Medical Record Number (MRN)",
      "translation": "სამედიცინო ბარათის ნომერი",
      "transliteration": "Sameditsino Baratis Nomeri",
      "note": ""
    },
    {
      "term": "Visit",
      "translation": "ვიზიტის ნომერი",
      "transliteration": "Vizitis Nomeri",
      "note": ""
    },
    {
      "term": "Demographics",
      "translation": "დემოგრაფიული მონაცემები",
      "transliteration": "Demograpiuli Monatsmemebi",
      "note": "Name, DOB, Address, Gender, Contact"
    },
    {
      "term": "Gender",
      "translation": "სქესი",
      "transliteration": "Sqesi",
      "note": ""
    },
    {
      "term": "Date of Birth (DOB)",
      "translation": "დაბადების თარიღი",
      "transliteration": "Dadebis Tarighi",
      "note": ""
    },
    {
      "term": "Address",
      "translation": "მისამართი",
      "transliteration": "Misamarti",
      "note": ""
    },
    {
      "term": "Contact Number",
      "translation": "საკონტაქტო ნომერი",
      "transliteration": "Sakontakto Nomeri",
      "note": ""
    },
    {
      "term": "Emergency Contact",
      "translation": "საგანგებო საკონტაქტო პირი",
      "transliteration": "Sagangebo Sakontakto Piri",
      "note": ""
    },
    {
      "term": "Insurance Information",
      "translation": "სადაზღვევო ინფორმაცია",
      "transliteration": "Sadazghveo Informatsia",
      "note": ""
    },
    {
      "term": "Insurance Verification",
      "translation": "დაზღვევის ვერიფიკაცია",
      "transliteration": "Dazghvevis Veripikatsia",
      "note": ""
    },
    {
      "term": "Consent Form",
      "translation": "თანხმობის ფორმა",
      "transliteration": "Tankhmobis Porma",
      "note": ""
    },
    {
      "term": "Primary Care Physician (PCP)",
      "translation": "პირველადი ჯანდაცვის ექიმი",
      "transliteration": "Pirveladi Jandatsvis Eqimi",
      "note": "'Ojakhi Eqimi' is commonly used"
    },
    {
      "term": "Bed Management",
      "translation": "საწოლფონდის მართვა",
      "transliteration": "Satsolfondis Martva",
      "note": ""
    },
    {
      "term": "Ward Assignment",
      "translation": "პალატაში განაწილება",
      "transliteration": "Palatashi Ganatsileba",
      "note": ""
    },
    {
      "term": "Patient Status",
      "translation": "პაციენტის სტატუსი",
      "transliteration": "Patsientis Statusi",
      "note": "e.g., Admitted, Discharged, Pending" 
    },
  ],
  "Clinical Documentation & Terms": [
    {
      "term": "Diagnosis",
      "translation": "დიაგნოზი",
      "transliteration": "Diagnozi",
      "note": ""
    },
    {
      "term": "Chief Complaint",
      "translation": "მთავარი ჩივილი",
      "transliteration": "Mtavari Chivili",
      "note": ""
    },
    {
      "term": "History of Present Illness (HPI)",
      "translation": "მიმდინარე ავადმყოფობის ისტორია",
      "transliteration": "Mimdinare Avadmyopobis Istoria",
      "note": ""
    },
    {
      "term": "Past Medical History (PMH)",
      "translation": "გადატანილი დაავადებების ისტორია",
      "transliteration": "Gadatanili Daavadebebis Istoria",
      "note": ""
    },
    {
      "term": "Family History",
      "translation": "ოჯახური ანამნეზი",
      "transliteration": "Ojakhuri Anamnezi",
      "note": ""
    },
    {
      "term": "Social History",
      "translation": "სოციალური ანამნეზი",
      "transliteration": "Sotsialuri Anamnezi",
      "note": ""
    },
    {
      "term": "Review of Systems (ROS)",
      "translation": "სისტემების მიმოხილვა",
      "transliteration": "Systemebis Mimokhilva",
      "note": ""
    },
    {
      "term": "Physical Examination",
      "translation": "ფიზიკალური გასინჯვა",
      "transliteration": "Pizikaluri Gasinjva",
      "note": ""
    },
    {
      "term": "Assessment",
      "translation": "შეფასება",
      "transliteration": "Shepaseba",
      "note": "Clinical assessment"
    },
    {
      "term": "Plan",
      "translation": "გეგმა",
      "transliteration": "Gegma",
      "note": "Treatment plan"
    },
    {
      "term": "Order",
      "translation": "დანიშნულება",
      "transliteration": "Danishnuleba",
      "note": "For meds, labs, imaging"
    },
    {
      "term": "Result",
      "translation": "შედეგი",
      "transliteration": "Shedegi",
      "note": "Lab/imaging result"
    },
    {
      "term": "Critical Value",
      "translation": "კრიტიკული მაჩვენებელი",
      "transliteration": "Kritikuli Machvenebeli",
      "note": ""
    },
    {
      "term": "Observation",
      "translation": "დაკვირვება",
      "transliteration": "Dakvirveba",
      "note": ""
    },
    {
      "term": "Progress Note",
      "translation": "მიმდინარეობის ჩანაწერი",
      "transliteration": "Mimdinareobis Chanatseri",
      "note": ""
    },
    {
      "term": "Consultation Request",
      "translation": "კონსულტაციის მოთხოვნა",
      "transliteration": "Konsultatsiis Motkhovna",
      "note": ""
    },
    {
      "term": "Consultation Report",
      "translation": "საკონსულტაციო დასკვნა",
      "transliteration": "Sakonsultatsio Daskvna",
      "note": ""
    },
    {
      "term": "Discharge Summary",
      "translation": "გაწერის ეპიკრიზი",
      "transliteration": "Gatseris Epikrizi",
      "note": "'Epikrizi' is common for summaries"
    },
    {
      "term": "Procedure Note",
      "translation": "პროცედურის ოქმი",
      "transliteration": "Protseduris Oqmi",
      "note": ""
    },
    {
      "term": "Operative Report",
      "translation": "ოპერაციის ოქმი",
      "transliteration": "Operatsiis Oqmi",
      "note": ""
    },
    {
      "term": "Allergy",
      "translation": "ალერგია",
      "transliteration": "Alergia",
      "note": ""
    },
    {
      "term": "Allergy Severity",
      "translation": "ალერგიის სიმძიმე",
      "transliteration": "Alergiis Simdzime",
      "note": ""
    },
    {
      "term": "Contraindication",
      "translation": "უკუჩვენება",
      "transliteration": "Ukuchveneba",
      "note": ""
    },
    {
      "term": "Side Effect",
      "translation": "გვერდითი ეფექტი",
      "transliteration": "Gverdit'i Epekti",
      "note": ""
    },
    {
      "term": "Symptom",
      "translation": "სიმპტომი",
      "transliteration": "Simptomi",
      "note": ""
    },
    {
      "term": "Treatment",
      "translation": "მკურნალობა",
      "transliteration": "Mkurnaloba",
      "note": ""
    },
    {
      "term": "Vital Signs",
      "translation": "სასიცოცხლო ნიშნები",
      "transliteration": "Sasitsotskhlo Nishnebi",
      "note": ""
    },
    {
      "term": "Blood Pressure",
      "translation": "სისხლის წნევა",
      "transliteration": "Siskhlis Tsneva",
      "note": ""
    },
    {
      "term": "Temperature",
      "translation": "ტემპერატურა",
      "transliteration": "Temperatura",
      "note": ""
    },
    {
      "term": "Pulse",
      "translation": "პულსი",
      "transliteration": "Pulsi",
      "note": ""
    },
    {
      "term": "Respiratory Rate",
      "translation": "სუნთქვის სიხშირე",
      "transliteration": "Suntkvis Sikshkhire",
      "note": ""
    },
    {
      "term": "Oxygen Saturation",
      "translation": "ჟანგბადის სატურაცია",
      "transliteration": "Jangbadis Saturatsia",
      "note": ""
    },
    {
      "term": "Pain Scale",
      "translation": "ტკივილის შკალა",
      "transliteration": "Tkivilis Shkala",
      "note": ""
    }
  ],
  "Orders & Results (Lab, Radiology, Meds)": [
    {
      "term": "Laboratory Order",
      "translation": "ლაბორატორიული დანიშნულება",
      "transliteration": "Laboratoriuli Danishnuleba",
      "note": ""
    },
    {
      "term": "Specimen",
      "translation": "ნიმუში",
      "transliteration": "Nimushi",
      "note": ""
    },
    {
      "term": "Sample Collection",
      "translation": "ნიმუშის აღება",
      "transliteration": "Nimushis Agheba",
      "note": ""
    },
    {
      "term": "Lab Test",
      "translation": "ლაბორატორიული ტესტი",
      "transliteration": "Laboratoriuli Testi / Analizi",
      "note": ""
    },
    {
      "term": "Lab Result",
      "translation": "ლაბორატორიული შედეგი",
      "transliteration": "Laboratoriuli Shedegi / Pasukhi",
      "note": ""
    },
    {
      "term": "Reference Range",
      "translation": "რეფერენტული ნორმები",
      "transliteration": "Referentuli Normebi",
      "note": ""
    },
    {
      "term": "Microbiology",
      "translation": "მიკრობიოლოგია",
      "transliteration": "Mikrobiologia",
      "note": ""
    },
    {
      "term": "Hematology",
      "translation": "ჰემატოლოგია",
      "transliteration": "Hematologia",
      "note": ""
    },
    {
      "term": "Chemistry Panel",
      "translation": "ბიოქიმიური ანალიზი",
      "transliteration": "Bioqimiuri Analizi",
      "note": ""
    },
    {
      "term": "Urinalysis",
      "translation": "შარდის ანალიზი",
      "transliteration": "Shardis Analizi",
      "note": ""
    },
    {
      "term": "Radiology Order",
      "translation": "რადიოლოგიური კვლევის დანიშნულება",
      "transliteration": "Radiologiuri Kvlevis Danishnuleba",
      "note": ""
    },
    {
      "term": "Modality",
      "translation": "მოდალობა",
      "transliteration": "Modaloba",
      "note": "e.g., X-ray, CT, MRI, Ultrasound"
    },
    {
      "term": "X-ray",
      "translation": "რენტგენი",
      "transliteration": "Rentgeni",
      "note": ""
    },
    {
      "term": "CT Scan",
      "translation": "კომპიუტერული ტომოგრაფია",
      "transliteration": "Komp'iuteruli Tomograpia",
      "note": "Often abbreviated KT - კტ"
    },
    {
      "term": "MRI",
      "translation": "მაგნიტურ-რეზონანსული ტომოგრაფია",
      "transliteration": "Magnitur-Rezonansuli Tomograpia",
      "note": "Often abbreviated MRT - მრტ"
    },
    {
      "term": "Ultrasound",
      "translation": "ულტრაბგერითი კვლევა",
      "transliteration": "Ultrabgeriti Kvleva",
      "note": "'Eqoskopia' is very common"
    },
    {
      "term": "Radiologist",
      "translation": "ექიმი-რადიოლოგი",
      "transliteration": "Eqimi-Radiologi",
      "note": ""
    },
    {
      "term": "Radiology Report",
      "translation": "რადიოლოგიური დასკვნა",
      "transliteration": "Radiologiuri Daskvna",
      "note": ""
    },
    {
      "term": "Report Status",
      "translation": "დასკვნის სტატუსი",
      "transliteration": "Daskvnis Statusi",
      "note": "e.g., Preliminary - წინასწარი (Tsinastsari), Final - საბოლოო (Saboolo)"
    },
    {
      "term": "Medication Order",
      "translation": "მედიკამენტის დანიშნულება",
      "transliteration": "Medikamentis Danishnuleba",
      "note": ""
    },
    {
      "term": "Prescription",
      "translation": "რეცეპტი",
      "transliteration": "Retsepti",
      "note": ""
    },
    {
      "term": "Dosage",
      "translation": "დოზა",
      "transliteration": "Doza",
      "note": ""
    },
    {
      "term": "Frequency",
      "translation": "მიღების სიხშირე",
      "transliteration": "Mighebis Sikshkhire",
      "note": ""
    },
    {
      "term": "Route of Administration",
      "translation": "მიღების გზა",
      "transliteration": "Mighebis Gza",
      "note": "e.g., Oral - პერორალური (Peroraluri), IV - ინტრავენური (Intravenuri)"
    }
  ],
  "Appointments & Scheduling": [
    {
      "term": "Appointment",
      "translation": "ვიზიტი",
      "transliteration": "Viziti",
      "note": ""
    },
    {
      "term": "Schedule",
      "translation": "განრიგი",
      "transliteration": "Ganrigi",
      "note": ""
    },
    {
      "term": "To Schedule",
      "translation": "დაჯავშნა",
      "transliteration": "Dajavshna",
      "note": ""
    },
    {
      "term": "Availability",
      "translation": "ხელმისაწვდომობა",
      "transliteration": "Khelmisatsvdomoba",
      "note": ""
    },
    {
      "term": "Resource Scheduling",
      "translation": "რესურსების დაგეგმვა",
      "transliteration": "Resursebis Dagegmva",
      "note": "Rooms, equipment"
    },
    {
      "term": "Block Scheduling",
      "translation": "დროის ბლოკირება",
      "transliteration": "Drois Blokireba",
      "note": ""
    },
    {
      "term": "Reschedule",
      "translation": "ვიზიტის გადადება",
      "transliteration": "Vizitis Gadadeba",
      "note": ""
    },
    {
      "term": "Cancel Appointment",
      "translation": "ვიზიტის გაუქმება",
      "transliteration": "Vizitis Gauqmeba",
      "note": ""
    },
    {
      "term": "No-show",
      "translation": "გამოუცხადებლობა",
      "transliteration": "Gamoutskhadebloba",
      "note": ""
    },
    {
      "term": "Check-in",
      "translation": "რეგისტრაცია",
      "transliteration": "Registratsia",
      "note": ""
    },
    {
      "term": "Check-out",
      "translation": "ვიზიტის დასრულება",
      "transliteration": "Vizitis Dasruleba",
      "note": ""
    },
    {
      "term": "Waiting List",
      "translation": "მომლოდინეთა სია",
      "transliteration": "Momlodineta Sia",
      "note": ""
    }
  ],
  "Surgery & Operating Room (OR)": [
    {
      "term": "Operating Room (OR)",
      "translation": "საოპერაციო",
      "transliteration": "Saoperatsio",
      "note": ""
    },
    {
      "term": "Surgery",
      "translation": "ოპერაცია",
      "transliteration": "Operatsia",
      "note": ""
    },
    {
      "term": "Pre-operative Assessment",
      "translation": "პრეოპერაციული შეფასება",
      "transliteration": "Preoperatsiuli Shepaseba",
      "note": ""
    },
    {
      "term": "Surgical Consent",
      "translation": "თანხმობა ოპერაციაზე",
      "transliteration": "Tankhmoba Operatsiaze",
      "note": ""
    },
    {
      "term": "Anesthesia",
      "translation": "ანესთეზია",
      "transliteration": "Anestezia",
      "note": ""
    },
    {
      "term": "Anesthesiologist",
      "translation": "ანესთეზიოლოგი",
      "transliteration": "Anesteziologi",
      "note": ""
    },
    {
      "term": "Surgeon",
      "translation": "ქირურგი",
      "transliteration": "Qirurgi",
      "note": ""
    },
    {
      "term": "OR Schedule",
      "translation": "საოპერაციო განრიგი",
      "transliteration": "Saoperatsio Ganrigi",
      "note": ""
    },
    {
      "term": "Post-operative Care",
      "translation": "პოსტოპერაციული მოვლა",
      "transliteration": "Postoperatsiuli Movla",
      "note": ""
    },
    {
      "term": "Recovery Room",
      "translation": "პოსტოპერაციული პალატა",
      "transliteration": "Postoperatsiuli Palata",
      "note": ""
    }
  ],
  "Billing, Finance & Administration": [
    {
      "term": "Bill",
      "translation": "ანგარიში",
      "transliteration": "Angarishi",
      "note": ""
    },
    {
      "term": "Payment",
      "translation": "გადახდა",
      "transliteration": "Gadakhda",
      "note": ""
    },
    {
      "term": "Insurance",
      "translation": "დაზღვევა",
      "transliteration": "Dazghveva",
      "note": ""
    },
    {
      "term": "Insurance Policy Number",
      "translation": "სადაზღვევო პოლისის ნომერი",
      "transliteration": "Sadazghveo Polisis Nomeri",
      "note": ""
    },
    {
      "term": "Insurance Claim",
      "translation": "სადაზღვევო მოთხოვნა",
      "transliteration": "Sadazghveo Motkhovna",
      "note": ""
    },
    {
      "term": "Claim Submission",
      "translation": "სადაზღვევო მოთხოვნის გაგზავნა",
      "transliteration": "Sadazghveo Motkhovnis Gagzavna",
      "note": ""
    },
    {
      "term": "Remittance Advice",
      "translation": "ანაზღაურების შეტყობინება",
      "transliteration": "Anazghaurebis Shetyobineba",
      "note": ""
    },
    {
      "term": "Co-pay",
      "translation": "თანაგადახდა",
      "transliteration": "Tanagadakhda",
      "note": ""
    },
    {
      "term": "Deductible",
      "translation": "გამოქვითვადი თანხა",
      "transliteration": "Gamokvitvadi Tankha",
      "note": ""
    },
    {
      "term": "Pre-authorization",
      "translation": "წინასწარი ავტორიზაცია",
      "transliteration": "Tsinastsari Avtorizatsia",
      "note": ""
    },
    {
      "term": "Charge",
      "translation": "საფასური",
      "transliteration": "Sapasuri",
      "note": ""
    },
    {
      "term": "Service Code",
      "translation": "მომსახურების კოდი",
      "transliteration": "Momsakhurebis Kodi",
      "note": "Verify local standard used, e.g., CPT or Georgian codes"
    },
    {
      "term": "Diagnosis Code",
      "translation": "დიაგნოზის კოდი",
      "transliteration": "Diagnozis Kodi",
      "note": "Verify local standard used, e.g., ICD or Georgian codes"
    },
    {
      "term": "Financial Report",
      "translation": "ფინანსური ანგარიში",
      "transliteration": "Pinansuri Angarishi",
      "note": ""
    },
    {
      "term": "Audit Trail",
      "translation": "აუდიტის კვალი",
      "transliteration": "Auditis Kvali / Jurnali",
      "note": ""
    },
    {
      "term": "Administration",
      "translation": "ადმინისტრაცია",
      "transliteration": "Administratsia",
      "note": ""
    },
    {
      "term": "Management",
      "translation": "მართვა",
      "transliteration": "Martva",
      "note": ""
    },
    {
      "term": "Statistics",
      "translation": "სტატისტიკა",
      "transliteration": "Statistika",
      "note": ""
    },
    {
      "term": "Regulation",
      "translation": "რეგულაცია",
      "transliteration": "Regulatsia",
      "note": ""
    },
    {
      "term": "Quality Management",
      "translation": "ხარისხის მართვა",
      "transliteration": "Khariskhis Martva",
      "note": ""
    },
    {
      "term": "Infection Control",
      "translation": "ინფექციის კონტროლი",
      "transliteration": "Inpektsiis Kontroli",
      "note": ""
    },
    {
      "term": "Waste Management",
      "translation": "ნარჩენების მართვა",
      "transliteration": "Narchenebis Martva",
      "note": ""
    },
    {
      "term": "Patient Rights",
      "translation": "პაციენტის უფლებები",
      "transliteration": "Patsientis Uplebebi",
      "note": ""
    }
  ],
  "Pharmacy & Inventory / Materials Management": [
    {
      "term": "Pharmacy",
      "translation": "აფთიაქი",
      "transliteration": "Aptiaqi",
      "note": ""
    },
    {
      "term": "Medication",
      "translation": "მედიკამენტი",
      "transliteration": "Medikamenti",
      "note": ""
    },
    {
      "term": "Formulary",
      "translation": "ფორმულარი",
      "transliteration": "Formulari",
      "note": "List of approved medications"
    },
    {
      "term": "Dispense",
      "translation": "გაცემა",
      "transliteration": "Gatsema",
      "note": ""
    },
    {
      "term": "Dispensing Unit",
      "translation": "გაცემის ერთეული",
      "transliteration": "Gatsemis Erteuli",
      "note": "e.g., tablet, vial"
    },
    {
      "term": "Inventory",
      "translation": "მარაგი",
      "transliteration": "Maragi",
      "note": ""
    },
    {
      "term": "Stock Count",
      "translation": "მარაგის აღრიცხვა",
      "transliteration": "Maragis Aghritskhva",
      "note": ""
    },
    {
      "term": "Reorder Level",
      "translation": "მარაგის შევსების დონე",
      "transliteration": "Maragis Shevsebis Done",
      "note": ""
    },
    {
      "term": "Lot Number",
      "translation": "პარტიის ნომერი",
      "transliteration": "Partiis Nomeri",
      "note": ""
    },
    {
      "term": "Batch Number",
      "translation": "სერიის ნომერი",
      "transliteration": "Seriis Nomeri",
      "note": ""
    },
    {
      "term": "Expiration Date",
      "translation": "ვარგისიანობის ვადა",
      "transliteration": "Vargisianobis Vada",
      "note": ""
    },
    {
      "term": "Supply",
      "translation": "მარაგი",
      "transliteration": "Maragi",
      "note": "Medical supplies"
    },
    {
      "term": "Purchase Order",
      "translation": "შესყიდვის ორდერი",
      "transliteration": "Shesyidvis Orderi",
      "note": ""
    },
    {
      "term": "Vendor",
      "translation": "მომწოდებელი",
      "transliteration": "Momtsodebeli",
      "note": ""
    }
  ],
  "Staff, Roles & Departments": [
    {
      "term": "Doctor",
      "translation": "ექიმი",
      "transliteration": "Eqimi",
      "note": ""
    },
    {
      "term": "Nurse",
      "translation": "ექთანი",
      "transliteration": "Eqtani",
      "note": ""
    },
    {
      "term": "Surgeon",
      "translation": "ქირურგი",
      "transliteration": "Qirurgi",
      "note": ""
    },
    {
      "term": "Specialist",
      "translation": "სპეციალისტი",
      "transliteration": "Spetsialisti",
      "note": ""
    },
    {
      "term": "Technician",
      "translation": "ტექნიკოსი",
      "transliteration": "Teknikosi",
      "note": "Lab, Radiology, etc."
    },
    {
      "term": "Pharmacist",
      "translation": "ფარმაცევტი",
      "transliteration": "Parmatsevti",
      "note": ""
    },
    {
      "term": "Administrator",
      "translation": "ადმინისტრატორი",
      "transliteration": "Administratori",
      "note": ""
    },
    {
      "term": "Staff",
      "translation": "პერსონალი",
      "transliteration": "Personali",
      "note": ""
    },
    {
      "term": "User Role",
      "translation": "მომხმარებლის როლი",
      "transliteration": "Momkhmareblis Roli",
      "note": ""
    },
    {
      "term": "Credentials",
      "translation": "კვალიფიკაცია",
      "transliteration": "Kvalipikatsia",
      "note": ""
    },
    {
      "term": "Shift",
      "translation": "ცვლა",
      "transliteration": "Tsvla",
      "note": ""
    },
    {
      "term": "On-call Schedule",
      "translation": "მორიგეობის განრიგი",
      "transliteration": "Morigeobis Ganrigi",
      "note": ""
    },
    {
      "term": "Directory",
      "translation": "ცნობარი",
      "transliteration": "Tsnobari",
      "note": "Staff directory"
    },
    {
      "term": "Department",
      "translation": "დეპარტამენტი",
      "transliteration": "Departamenti",
      "note": "'Ganyopileba' is common"
    },
    {
      "term": "Ward",
      "translation": "პალატა",
      "transliteration": "Palata",
      "note": ""
    },
    {
      "term": "Emergency Room (ER)",
      "translation": "გადაუდებელი დახმარების განყოფილება",
      "transliteration": "Gadaudebeli Dakhmarebis Ganyopileba",
      "note": ""
    },
    {
      "term": "Intensive Care Unit (ICU)",
      "translation": "ინტენსიური თერაპიის განყოფილება",
      "transliteration": "Intensiuri Terapiis Ganyopileba",
      "note": "'Reanimatsia' is common"
    },
    {
      "term": "Laboratory",
      "translation": "ლაბორატორია",
      "transliteration": "Laboratoria",
      "note": ""
    },
    {
      "term": "Radiology Department",
      "translation": "რადიოლოგიის განყოფილება",
      "transliteration": "Radiologiis Ganyopileba",
      "note": ""
    }
  ],
  "System Interface, Actions & Security": [
    {
      "term": "Save",
      "translation": "შენახვა",
      "transliteration": "Shenakhva",
      "note": ""
    },
    {
      "term": "Edit",
      "translation": "რედაქტირება",
      "transliteration": "Redaktireba",
      "note": ""
    },
    {
      "term": "Cancel",
      "translation": "გაუქმება",
      "transliteration": "Gauqmeba",
      "note": ""
    },
    {
      "term": "Delete",
      "translation": "წაშლა",
      "transliteration": "Tsashla",
      "note": ""
    },
    {
      "term": "Search",
      "translation": "ძებნა",
      "transliteration": "Dzebna",
      "note": ""
    },
    {
      "term": "Filter",
      "translation": "ფილტრი",
      "transliteration": "Piltri",
      "note": ""
    },
    {
      "term": "Sort",
      "translation": "დალაგება",
      "transliteration": "Dalageba",
      "note": ""
    },
    {
      "term": "Add",
      "translation": "დამატება",
      "transliteration": "Damateba",
      "note": ""
    },
    {
      "term": "Confirm",
      "translation": "დადასტურება",
      "transliteration": "Dadastureba",
      "note": ""
    },
    {
      "term": "Submit",
      "translation": "გაგზავნა",
      "transliteration": "Gagzavna",
      "note": ""
    },
    {
      "term": "Print",
      "translation": "ბეჭდვა",
      "transliteration": "Bechdva",
      "note": ""
    },
    {
      "term": "Export",
      "translation": "ექსპორტი",
      "transliteration": "Exporti",
      "note": ""
    },
    {
      "term": "Import",
      "translation": "იმპორტი",
      "transliteration": "Importi",
      "note": ""
    },
    {
      "term": "Refresh",
      "translation": "განახლება",
      "transliteration": "Ganakleba",
      "note": ""
    },
    {
      "term": "User",
      "translation": "მომხმარებელი",
      "transliteration": "Momkhmarebeli",
      "note": ""
    },
    {
      "term": "Username",
      "translation": "მომხმარებლის სახელი",
      "transliteration": "Momkhmareblis Sakheli",
      "note": ""
    },
    {
      "term": "Password",
      "translation": "პაროლი",
      "transliteration": "Paroli",
      "note": ""
    },
    {
      "term": "Login",
      "translation": "ავტორიზაცია",
      "transliteration": "Avtorizatsia",
      "note": ""
    },
    {
      "term": "Logout",
      "translation": "სისტემიდან გამოსვლა",
      "transliteration": "Sistemidan Gamosvla",
      "note": ""
    },
    {
      "term": "Settings",
      "translation": "პარამეტრები",
      "transliteration": "Parametrebi",
      "note": ""
    },
    {
      "term": "Configuration",
      "translation": "კონფიგურაცია",
      "transliteration": "Konpiguratsia",
      "note": ""
    },
    {
      "term": "Permissions",
      "translation": "უფლებები",
      "transliteration": "Uplebebi",
      "note": ""
    },
    {
      "term": "User Role",
      "translation": "მომხმარებლის როლი",
      "transliteration": "Momkhmareblis Roli",
      "note": ""
    },
    {
      "term": "Access Control",
      "translation": "წვდომის კონტროლი",
      "transliteration": "Tsvdomis Kontroli",
      "note": ""
    },
    {
      "term": "Audit Log",
      "translation": "აუდიტის ჟურნალი",
      "transliteration": "Auditis Jurnali",
      "note": ""
    },
    {
      "term": "Password Reset",
      "translation": "პაროლის აღდგენა",
      "transliteration": "Parolis Aghdgena",
      "note": ""
    },
    {
      "term": "Authentication",
      "translation": "ავთენტიფიკაცია",
      "transliteration": "Avtentipikatsia",
      "note": ""
    },
    {
      "term": "Notification",
      "translation": "შეტყობინება",
      "transliteration": "Shetyobineba",
      "note": ""
    },
    {
      "term": "Alert",
      "translation": "განგაში",
      "transliteration": "Gangashi",
      "note": ""
    },
    {
      "term": "Error Message",
      "translation": "შეცდომის შეტყობინება",
      "transliteration": "Shetsdomis Shetyobineba",
      "note": ""
    },
    {
      "term": "Status",
      "translation": "სტატუსი",
      "transliteration": "Statusi",
      "note": "e.g., Pending - მომლოდინე (Momlodine), Completed - დასრულებული (Dasrulebuli), In Progress - მიმდინარე (Mimdinare), Canceled - გაუქმებული (Gauqmebuli)"
    },
    {
      "term": "Dashboard",
      "translation": "სამუშაო დაფა",
      "transliteration": "Samushao Dapa",
      "note": ""
    },
    {
      "term": "Report",
      "translation": "ანგარიში",
      "transliteration": "Angarishi",
      "note": ""
    },
    {
      "term": "Help",
      "translation": "დახმარება",
      "transliteration": "Dakhmareba",
      "note": ""
    }
  ],
  "Patient Information & Clinical Details": [
    {
      "term": "Marital Status",
      "translation": "ოჯახური მდგომარეობა",
      "transliteration": "Ojakhuri Mdgomareoba",
      "note": ""
    },
    {
      "term": "Occupation",
      "translation": "პროფესია",
      "transliteration": "Profesia",
      "note": ""
    },
    {
      "term": "Nationality",
      "translation": "მოქალაქეობა",
      "transliteration": "Mokalakeoba",
      "note": ""
    },
    {
      "term": "Preferred Language",
      "translation": "სასურველი ენა",
      "transliteration": "Sasurveli Ena",
      "note": ""
    },
    {
      "term": "Guardian",
      "translation": "მეურვე",
      "transliteration": "Meurve",
      "note": ""
    },
    {
      "term": "Next of Kin",
      "translation": "უახლოესი ნათესავი",
      "transliteration": "Uakhloesi Natesavi",
      "note": ""
    },
    {
      "term": "Relationship (to patient)",
      "translation": "დამოკიდებულება",
      "transliteration": "პაციენტთან",
      "note": "Damokidebuleba (Patsienttan)) (e.g., Parent, Spouse"
    },
    {
      "term": "Advance Directive",
      "translation": "წინასწარი განკარგულება",
      "transliteration": "Tsinastsari Gankarguleba",
      "note": "Regarding medical care"
    },
    {
      "term": "Do Not Resuscitate (DNR)",
      "translation": "რეანიმაციაზე უარის თქმა",
      "transliteration": "Reanimatsiaze Uaris Tkma",
      "note": "Verify specific legal/medical term used in Georgia"
    },
    {
      "term": "Immunization",
      "translation": "იმუნიზაცია",
      "transliteration": "Imunizatsia",
      "note": "'Atsra' is common"
    },
    {
      "term": "Immunization Record",
      "translation": "აცრების ბარათი",
      "transliteration": "Atsrebis Barati",
      "note": ""
    },
    {
      "term": "Growth Chart",
      "translation": "ზრდის გრაფიკი",
      "transliteration": "Zrdis Grapiki",
      "note": "Pediatrics"
    },
    {
      "term": "Problem List",
      "translation": "პრობლემების სია",
      "transliteration": "Problemebis Sia",
      "note": "Ongoing patient issues"
    },
    {
      "term": "Medication Reconciliation",
      "translation": "მედიკამენტების შეჯერება",
      "transliteration": "Medikamentebis Shejereba",
      "note": ""
    },
    {
      "term": "Clinical Pathway",
      "translation": "კლინიკური გზამკვლევი",
      "transliteration": "Klinikuri Gzamkvlevi",
      "note": ""
    },
    {
      "term": "Care Plan",
      "translation": "მოვლის გეგმა",
      "transliteration": "Movlis Gegma",
      "note": ""
    },
    {
      "term": "Discharge Instructions",
      "translation": "გაწერის რეკომენდაციები",
      "transliteration": "Gatseris Rekomendatsiebi",
      "note": ""
    },
    {
      "term": "Follow-up (appointment)",
      "translation": "შემდგომი ვიზიტი",
      "transliteration": "Shemdgomi Viziti",
      "note": ""
    },
    {
      "term": "Referral Source",
      "translation": "მომმართველი წყარო",
      "transliteration": "Mommartveli Tskaro",
      "note": "Who referred the patient"
    },
    {
      "term": "Referral Reason",
      "translation": "მიმართვის მიზეზი",
      "transliteration": "Mimartvis Mizezi",
      "note": ""
    },
    {
      "term": "Secondary Diagnosis",
      "translation": "თანმხლები დიაგნოზი",
      "transliteration": "Tanmkhlebi Diagnozi",
      "note": ""
    },
    {
      "term": "Comorbidity",
      "translation": "კომორბიდობა",
      "transliteration": "Komorbidoba",
      "note": ""
    },
    {
      "term": "Complication",
      "translation": "გართულება",
      "transliteration": "Gartuleba",
      "note": ""
    },
    {
      "term": "Allergen",
      "translation": "ალერგენი",
      "transliteration": "Alergeni",
      "note": "e.g., Food - საკვები (Sakvebi), Drug - მედიკამენტური (Medikamenturi)"
    },
    {
      "term": "Reaction (to allergen)",
      "translation": "რეაქცია",
      "transliteration": "Reaktsia",
      "note": "e.g., Rash - გამონაყარი (Gamonayari), Anaphylaxis - ანაფილაქსია (Anapilaksia)"
    },
    {
      "term": "Measurement Time",
      "translation": "გაზომვის დრო",
      "transliteration": "Gazomvis Dro",
      "note": "For vital signs, etc."
    },
    {
      "term": "Units",
      "translation": "ერთეულები",
      "transliteration": "Erteulebi",
      "note": "e.g., mg, ml, kg, cm"
    }
  ],
  "Scheduling & Resources": [
    {
      "term": "Duration",
      "translation": "ხანგრძლივობა",
      "transliteration": "Khangrdzlivoba",
      "note": "Appointment length"
    },
    {
      "term": "Priority",
      "translation": "პრიორიტეტი",
      "transliteration": "Prioriteti",
      "note": "Appointment urgency, order priority - Stat, Routine"
    },
    {
      "term": "Recurrence",
      "translation": "განმეორებადობა",
      "transliteration": "Ganmeorebadoba",
      "note": "Appointments"
    },
    {
      "term": "Room Number",
      "translation": "ოთახის ნომერი",
      "transliteration": "Otakhis Nomeri",
      "note": ""
    },
    {
      "term": "Equipment ID",
      "translation": "აპარატურის იდენტიფიკატორი",
      "transliteration": "Aparaturis Identipikatori",
      "note": ""
    },
    {
      "term": "Resource Conflict",
      "translation": "რესურსების კონფლიქტი",
      "transliteration": "Resursebis Konflikti",
      "note": "Scheduling clash"
    },
    {
      "term": "Availability Slot",
      "translation": "თავისუფალი დრო",
      "transliteration": "Tavisupali Dro",
      "note": "Scheduling"
    },
    {
      "term": "Overbooking",
      "translation": "ჭარბი ჯავშანი",
      "transliteration": "Ch'arbi Javshani",
      "note": ""
    }
  ],
  "Billing, Insurance & Administration": [
    {
      "term": "Guarantor",
      "translation": "გარანტორი",
      "transliteration": "Garantori",
      "note": "Person responsible for the bill"
    },
    {
      "term": "Payer",
      "translation": "გადამხდელი",
      "transliteration": "Gadamkhdeli",
      "note": ""
    },
    {
      "term": "Policy Holder",
      "translation": "პოლისის მფლობელი",
      "transliteration": "Polisis Mplobeli",
      "note": ""
    },
    {
      "term": "Group Number",
      "translation": "ჯგუფის ნომერი",
      "transliteration": "Jgupis Nomeri",
      "note": "Insurance"
    },
    {
      "term": "Subscriber ID",
      "translation": "აბონენტის ID",
      "transliteration": "Abonentis ID",
      "note": "Insurance"
    },
    {
      "term": "Coverage Details",
      "translation": "დაფარვის დეტალები",
      "transliteration": "Daparvis Detalebi",
      "note": ""
    },
    {
      "term": "Claim Status",
      "translation": "მოთხოვნის სტატუსი",
      "transliteration": "Motkhovnis Statusi",
      "note": "Billing claim"
    },
    {
      "term": "Adjustment",
      "translation": "კორექტირება",
      "transliteration": "Korektireba",
      "note": "Billing adjustment"
    },
    {
      "term": "Denial",
      "translation": "უარყოფა",
      "transliteration": "Uaryopa",
      "note": "Claim denial"
    },
    {
      "term": "Denial Code",
      "translation": "უარყოფის კოდი",
      "transliteration": "Uaryopis Kodi / Mizezi",
      "note": ""
    },
    {
      "term": "Appeal",
      "translation": "აპელაცია",
      "transliteration": "Apelatsia",
      "note": "Claim appeal"
    },
    {
      "term": "Statement",
      "translation": "ამონაწერი",
      "transliteration": "Amonatseri",
      "note": "Patient bill/statement"
    },
    {
      "term": "Aging Report",
      "translation": "დავალიანების ხანდაზმულობის ანგარიში",
      "transliteration": "Davalianebis Khandazmulobis Angarishi",
      "note": ""
    },
    {
      "term": "Revenue Cycle",
      "translation": "შემოსავლების ციკლი",
      "transliteration": "Shemosavlebis Tsikli",
      "note": ""
    },
    {
      "term": "Fiscal Year",
      "translation": "ფისკალური წელი",
      "transliteration": "Piskaluri Tseli",
      "note": ""
    },
    {
      "term": "Budget Code",
      "translation": "ბიუჯეტის კოდი",
      "transliteration": "Biujetis Kodi",
      "note": ""
    },
    {
      "term": "Cost Center",
      "translation": "ხარჯების ცენტრი",
      "transliteration": "Kharjebis Tsentri",
      "note": ""
    }
  ],
  "Orders & Results (Deeper Dive)": [
    {
      "term": "Order Status",
      "translation": "დანიშნულების სტატუსი",
      "transliteration": "Danishnulebis Statusi",
      "note": "e.g., Ordered, Collected, Pending, Completed, Canceled"
    },
    {
      "term": "Order Priority",
      "translation": "დანიშნულების პრიორიტეტი",
      "transliteration": "Danishnulebis Prioriteti",
      "note": "e.g., Stat - სასწრაფო (Sastsrapo), Routine - გეგმიური (Gegmiuri)"
    },
    {
      "term": "Specimen Condition",
      "translation": "ნიმუშის მდგომარეობა",
      "transliteration": "Nimushis Mdgomareoba",
      "note": "e.g., Hemolyzed - ჰემოლიზირებული (Hemolizirebuli), Insufficient - არასაკმარისი (Arasakmarisi)"
    },
    {
      "term": "Abnormal Flag",
      "translation": "პათოლოგიური მაჩვენებელი",
      "transliteration": "Patologiuri Machvenebeli",
      "note": "On results"
    },
    {
      "term": "Interpretation Status",
      "translation": "ინტერპრეტაციის სტატუსი",
      "transliteration": "Interpretatsiis Statusi",
      "note": "Radiology reports: Dictated, Preliminary, Final, Amended - შეცვლილი (Shetsvlili)"
    }
  ],
  "Pharmacy & Inventory (Materials Management)": [
    {
      "term": "Unit of Measure (UOM)",
      "translation": "ზომის ერთეული",
      "transliteration": "Zomis Erteuli",
      "note": "e.g., Box, Vial, Each"
    },
    {
      "term": "Minimum Stock Level",
      "translation": "მინიმალური მარაგი",
      "transliteration": "Minimaluri Maragi",
      "note": ""
    },
    {
      "term": "Maximum Stock Level",
      "translation": "მაქსიმალური მარაგი",
      "transliteration": "Maksimaluri Maragi",
      "note": ""
    },
    {
      "term": "Requisition",
      "translation": "მოთხოვნა",
      "transliteration": "Motkhovna",
      "note": "Request for supplies/meds"
    },
    {
      "term": "Order Fulfillment",
      "translation": "მოთხოვნის შესრულება",
      "transliteration": "Motkhovnis Shesruleba",
      "note": ""
    },
    {
      "term": "Stock Adjustment",
      "translation": "მარაგის კორექცია",
      "transliteration": "Maragis Korektsia",
      "note": ""
    },
    {
      "term": "Wastage",
      "translation": "დანაკარგი",
      "transliteration": "Danakargi",
      "note": "Due to expiry or damage"
    },
    {
      "term": "Controlled Substance",
      "translation": "კონტროლს დაქვემდებარებული ნივთიერება",
      "transliteration": "Kontrols Dakvemdebarebuli Nivtiereba",
      "note": ""
    },
    {
      "term": "Narcotic Count",
      "translation": "ნარკოტიკული საშუალებების აღრიცხვა",
      "transliteration": "Narkotikuli Sashualebebis Aghritskhva",
      "note": ""
    }
  ],
  "System, UI & Technical Terms": [
    {
      "term": "Identifier",
      "translation": "იდენტიფიკატორი",
      "transliteration": "Identipikatori",
      "note": "Generic ID"
    },
    {
      "term": "Code",
      "translation": "კოდი",
      "transliteration": "Kodi",
      "note": "Generic system code"
    },
    {
      "term": "Description",
      "translation": "აღწერა",
      "transliteration": "Aghtsera",
      "note": ""
    },
    {
      "term": "Notes",
      "translation": "შენიშვნები",
      "transliteration": "Shenishvnebi",
      "note": ""
    },
    {
      "term": "Is Active",
      "translation": "აქტიური",
      "transliteration": "Aktiuri",
      "note": "Boolean flag, often for records like users, services"
    },
    {
      "term": "Created Date",
      "translation": "შექმნის თარიღი",
      "transliteration": "Shekmnis Tarighi/Dro",
      "note": ""
    },
    {
      "term": "Created By",
      "translation": "შემქმნელი",
      "transliteration": "Shemkhmneli",
      "note": "User who created the record"
    },
    {
      "term": "Last Updated Date",
      "translation": "ბოლო განახლების თარიღი",
      "transliteration": "Bolo Ganaklebis Tarighi/Dro",
      "note": ""
    },
    {
      "term": "Updated By",
      "translation": "განმაახლებელი",
      "transliteration": "Ganmaakhlebeli",
      "note": "User who last updated"
    },
    {
      "term": "Status Code",
      "translation": "სტატუსის კოდი",
      "transliteration": "Statusis Kodi",
      "note": ""
    },
    {
      "term": "Priority Level",
      "translation": "პრიორიტეტის დონე",
      "transliteration": "Prioritetis Done",
      "note": ""
    },
    {
      "term": "Required Field",
      "translation": "სავალდებულო ველი",
      "transliteration": "Savaldebulo Veli",
      "note": ""
    },
    {
      "term": "Optional Field",
      "translation": "არასავალდებულო ველი",
      "transliteration": "Arasavaldebulo Veli",
      "note": ""
    },
    {
      "term": "Validation Error",
      "translation": "ვალიდაციის შეცდომა",
      "transliteration": "Validatsiis Shetsdoma",
      "note": ""
    },
    {
      "term": "Confirmation Message",
      "translation": "დადასტურების შეტყობინება",
      "transliteration": "Dadasturebis Shetyobineba",
      "note": ""
    },
    {
      "term": "Success Message",
      "translation": "წარმატების შეტყობინება",
      "transliteration": "Tsarmatebis Shetyobineba",
      "note": ""
    },
    {
      "term": "Failure Message",
      "translation": "წარუმატებლობის შეტყობინება",
      "transliteration": "Tsarumateblobis Shetyobineba",
      "note": ""
    },
    {
      "term": "Loading...",
      "translation": "იტვირთება...",
      "transliteration": "Itvirteba...",
      "note": ""
    },
    {
      "term": "Pagination",
      "translation": "პაგინაცია",
      "transliteration": "Paginatsia",
      "note": ""
    },
    {
      "term": "Next (Page)",
      "translation": "შემდეგი",
      "transliteration": "Shemdegi",
      "note": ""
    },
    {
      "term": "Previous (Page)",
      "translation": "წინა",
      "transliteration": "Tsina",
      "note": ""
    },
    {
      "term": "Page Number",
      "translation": "გვერდის ნომერი",
      "transliteration": "Gverdis Nomeri",
      "note": ""
    },
    {
      "term": "Search Criteria",
      "translation": "ძებნის კრიტერიუმები",
      "transliteration": "Dzebnis Kriteriumebi",
      "note": ""
    },
    {
      "term": "Results Found",
      "translation": "ნაპოვნია შედეგები",
      "transliteration": "Napovnia Shedegebi",
      "note": ""
    },
    {
      "term": "No Results Found",
      "translation": "შედეგები ვერ მოიძებნა",
      "transliteration": "Shedegebi Ver Moidzebna",
      "note": ""
    },
    {
      "term": "Default Value",
      "translation": "ნაგულისხმევი მნიშვნელობა",
      "transliteration": "Naguliskhmevi Mnishvneloba",
      "note": ""
    },
    {
      "term": "Timezone",
      "translation": "დროის ზონა",
      "transliteration": "Drois Zona",
      "note": ""
    },
    {
      "term": "Currency",
      "translation": "ვალუტა",
      "transliteration": "Valuta",
      "note": ""
    },
    {
      "term": "Language Setting",
      "translation": "ენის პარამეტრი",
      "transliteration": "Enis Parametri",
      "note": ""
    },
    {
      "term": "Integration",
      "translation": "ინტეგრაცია",
      "transliteration": "Integratsia",
      "note": ""
    },
    {
      "term": "Interface",
      "translation": "ინტერფეისი",
      "transliteration": "Interpeisi",
      "note": "System interface"
    },
    {
      "term": "Log Level",
      "translation": "ლოგირების დონე",
      "transliteration": "Logirebis Done",
      "note": "e.g., Info, Warn, Error"
    },
    {
      "term": "Timestamp",
      "translation": "დროის ნიშნული",
      "transliteration": "Drois Nishnuli",
      "note": ""
    },
    {
      "term": "Event Type",
      "translation": "მოვლენის ტიპი",
      "transliteration": "Movlenis Tipi",
      "note": "In logs"
    },
    {
      "term": "Module Name",
      "translation": "მოდულის სახელი",
      "transliteration": "Modulis Sakheli",
      "note": ""
    },
    {
      "term": "Queue",
      "translation": "რიგი",
      "transliteration": "Rigi",
      "note": "For background tasks"
    },
    {
      "term": "Job Status",
      "translation": "დავალების სტატუსი",
      "transliteration": "Davalebis Statusi",
      "note": "Queued, Running, Completed, Failed"
    }
  ],
  "Staff & Security": [
    {
      "term": "User Group",
      "translation": "მომხმარებელთა ჯგუფი",
      "transliteration": "Momkhmarebelta Jgupi",
      "note": ""
    },
    {
      "term": "Role Description",
      "translation": "როლის აღწერა",
      "transliteration": "Rolis Aghtsera",
      "note": ""
    },
    {
      "term": "Access Level",
      "translation": "წვდომის დონე",
      "transliteration": "Tsvdomis Done",
      "note": "e.g., Read - წაკითხვა (Tsakitkhva), Write - ჩაწერა (Ch'atsera), Admin - ადმინი (Admini)"
    },
    {
      "term": "Authentication Method",
      "translation": "ავთენტიფიკაციის მეთოდი",
      "transliteration": "Avtentipikatsiis Metodi",
      "note": ""
    },
    {
      "term": "Session Timeout",
      "translation": "სესიის დრო ამოიწურა",
      "transliteration": "Sesiis Dro Amoიtsura",
        "note": ""
    },
  ],
  "Staff & Security": [
    {
        "term": "Audit Trail",
        "translation": "აუდიტის კვალი",
        "transliteration": "Auditis Kvali",
        "note": ""
    },
    {
        "term": "Incident Report",
        "translation": "შემთხვევის ანგარიში",
        "transliteration": "Shemtkhvevis Angarishi",
        "note": ""
    },
    {
        "term": "Security Breach",
        "translation": "უსაფრთხოების დარღვევა",
        "transliteration": "Usafrtkhoebis Darghveva",
        "note": ""
    },
    {
        "term": "Password Policy",
        "translation": "პაროლის პოლიტიკა",
        "transliteration": "Parolis Politika",
        "note": ""
    },
    {
        "term": "Two-Factor Authentication (2FA)",
        "translation": "ორ ფაქტორული ავთენტიფიკაცია (2FA)",
        "transliteration": "",
        "note": ""
    }
  ]
} 