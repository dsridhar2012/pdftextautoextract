import io
import os
import re
from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams

FINAL_CSV = 'C:/Users/sridhar/Desktop/Upwork/out/Master_data.csv'



def extract_HCFA(pdf_path,outputDirectory):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    codec = 'utf-8'  # 'utf16','utf-8'
    laparams = LAParams()
    converter = TextConverter(resource_manager, fake_file_handle,codec=codec,laparams=laparams)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,caching=True,check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
    converter.close()
    fake_file_handle.close()

    with open(outputDirectory, 'w') as file_object:
        file_object.write(text)


    with open(outputDirectory, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(outputDirectory, 'w') as fout:
        fout.writelines(data[1:])
    #---------------END Final file line adjustments-----------------------#
    #---------------------Extracting Attributes --------------------------#
    # 1. Client Last Name|Text data[20].split(',')[0]
    # 1.1 Client First Name | Text data[20].split(',')[1][:-1]
    # 2. Client Street Address | Text
    # 3. Client City | Text
    # 4. Client State | Text
    # 5. Client Zip Code | Number
    # 6. Client Phone Number (if available) | Special Number
    # 7. Client Date of Birth | Date
    # 8. Client Gender | Text
    # 9. Date of Service (Encounter) | Date
    # 10. Provider Name | Text
    # 11. Provider Zip Code | Number
    # 12. Total Charges | Number
    # 13. Physician NPI | Number
    # 14. Date of Injury | Date
    lf = []
    count = 0
    for x in data:
        if ("," in x):
            if (len(x.strip()) > 7 ):
                lf.append(x)
                break

    fp = open(outputDirectory)
    for i, line in enumerate(fp):
        if ("," in line):
            if(len(x.strip())> 7):
                line_number = i+1
                break
    fp.close()
    lastnamefirstname = lf[0][:-1]
    print("name : "+ lastnamefirstname)
    street = data[26][:-1]

    j=1
    while( data[(line_number+(2*j))][:-1]):
        st = data[(line_number+(2*j))][:-1]
        if (j <= 15):
            if(len(st.strip()) == 2):
                if (st.strip() in ('AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY','AS','DC','FM','GU','MH','MP','PW','PR','VI')):
                    state = st.strip()
                    #--------CITY calculation -----------#
                    city_line = line_number + (2 * j)
                    if((data[(city_line - 6)][:-1].strip().isalpha()) & (len(data[(city_line - 6)][:-1].strip()) > 4)):
                        city = data[(city_line - 6)][:-1].strip()
                    elif((data[(city_line - 4)][:-1].strip().isalpha()) & (len(data[(city_line - 4)][:-1].strip()) > 4)):
                        city = data[(city_line - 4)][:-1].strip()
                    elif((data[(city_line - 2)][:-1].strip().isalpha()) & (len(data[(city_line - 2)][:-1].strip()) > 4)):
                        city = data[(city_line - 2)][:-1].strip()
                    elif((data[(city_line + 2)][:-1].strip().isalpha()) & (len(data[(city_line + 2)][:-1].strip()) > 4)):
                        city = data[(city_line + 2)][:-1].strip()
                    elif((data[(city_line + 4)][:-1].strip().isalpha()) & (len(data[(city_line + 4)][:-1].strip()) > 4)):
                        city = data[(city_line + 4)][:-1].strip()
                    elif((data[(city_line + 6)][:-1].strip().isalpha()) & (len(data[(city_line + 6)][:-1].strip()) > 4)):
                        city = data[(city_line + 6)][:-1].strip()
                    else:
                        city = 'XXXX'
                    #-----ZIP code Calculation ----------------#
                    zip_line = line_number + (2 * j)
                    if ((data[(zip_line - 6)][:-1].strip().isnumeric()) & (len(data[(zip_line - 6)][:-1].strip()) == 5)):
                        zip = data[(zip_line - 6)][:-1].strip()
                    elif ((data[(zip_line - 4)][:-1].strip().isnumeric()) & (len(data[(zip_line - 4)][:-1].strip())== 5)):
                        zip = data[(zip_line - 4)][:-1].strip()
                    elif ((data[(zip_line - 2)][:-1].strip().isnumeric()) & (len(data[(zip_line - 2)][:-1].strip())== 5)):
                        zip = data[(zip_line - 2)][:-1].strip()
                    elif ((data[(zip_line + 2)][:-1].strip().isnumeric()) & (len(data[(zip_line + 2)][:-1].strip())== 5)):
                        zip = data[(zip_line + 2)][:-1].strip()
                    elif ((data[(zip_line + 4)][:-1].strip().isnumeric()) & (len(data[(zip_line + 4)][:-1].strip())== 5)):
                        zip = data[(zip_line + 4)][:-1].strip()
                    elif ((data[(zip_line + 6)][:-1].strip().isnumeric()) & (len(data[(zip_line + 6)][:-1].strip())== 5)):
                        zip = data[(zip_line + 6)][:-1].strip()
                    else:
                        zip = 'XXXX'

                    street_line = line_number + (2 * j)
                    if ((data[(street_line - 6)][:-1].strip().replace(' ','').isalnum()) & (len(data[(street_line - 6)][:-1].strip()) > 10)):
                        street = data[(street_line - 6)][:-1]
                    elif ((data[(street_line - 4)][:-1].strip().replace(' ','').isalnum()) & (len(data[(street_line - 4)][:-1].strip()) > 10)):
                        street = data[(street_line - 4)][:-1]
                    elif ((data[(street_line - 2)][:-1].strip().replace(' ','').isalnum()) & (len(data[(street_line - 2)][:-1].strip()) > 10)):
                        street = data[(street_line - 2)][:-1]
                    elif ((data[(street_line + 2)][:-1].strip().replace(' ','').isalnum()) & (len(data[(street_line + 2)][:-1].strip()) > 10)):
                        street = data[(street_line + 2)][:-1]
                    elif ((data[(street_line + 4)][:-1].strip().replace(' ','').isalnum()) & (len(data[(street_line + 4)][:-1].strip()) > 10)):
                        street = data[(street_line + 4)][:-1]
                    elif ((data[(street_line + 6)][:-1].strip().replace(' ','').isalnum()) & (len(data[(street_line + 6)][:-1].strip()) > 10)):
                        street = data[(street_line + 6)][:-1]
                    else:
                        street = 'XXXX'


                    break
                else:
                    j += 1
                    continue
            else:
                j += 1
                continue
        else :
            state = 'XX'

            break

    #---doc calculation --#
    for k in range(0,10):
        dob = ''
        if(len(data[line_number+2+2*k][:-1].strip()) == 2 & len(data[line_number+4+2*k][:-1].strip()) == 2 ):#& len(data[line_number+6+2*k][:-1].split(' ')[0].strip()) == 4):
            dob = data[line_number+2+2*k][:-1]+'/'+data[line_number+4+2*k][:-1]+'/'+data[line_number+6+2*k][:-1].split(' ')[0]
            break
        else:
            continue
    phone = 'Phone#'
    if (data[line_number+6][:-1].strip().isnumeric()):
        gender = "F"
    else:
        gender = "M"

    fp1 = open(outputDirectory)
    for i, line in enumerate(fp1):
        if ("ABC" in line):
            abc_number = i + 1
            break
    fp1.close()
    #--------------npi calculation ----------#
    for m in range(0,12):
        npi = "XXX"

        if((len(data[abc_number + m][:-1].strip()) == 10) & (data[abc_number + m][:-1].strip().isnumeric())):
            npi = data[abc_number + m][:-1].strip()

            break
        else:
            continue
    #----------Total calculation------------------#
    total = data[abc_number + 2][:-1].split(' ')[0] + '.' + data[abc_number + 2][:-1].split(' ')[1]

    dos = data[abc_number - 16][:-1].strip() + '/' +data[abc_number - 18][:-1].strip()+'/20' + data[abc_number - 14][:-1].strip()
    doi = dos
    fp2 = open(outputDirectory)
    for i, line in enumerate(fp2):
        if ("PO BOX" in line):
            po_number = i + 1
            break
    fp2.close()
    provider_name = data[po_number -1][:-1]
    provider_zip = data[po_number][:-1].split(' ')[2]

    with open(FINAL_CSV, 'a') as final_file_append:
       final_file_append.write(lastnamefirstname+','+street+','+city+','+state+','+zip+','+phone+','+dob+','+gender+','+dos+','+ provider_name +','+provider_zip+','+ total+','+npi+','+doi+'\n')


#-----------------------END OF HCFA Function------------------------------------------------------------#


def extract_UB(pdf_path,outputDirectory):

    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    codec = 'utf-8'  # 'utf16','utf-8'
    laparams = LAParams()
    converter = TextConverter(resource_manager, fake_file_handle,codec=codec,laparams=laparams)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,caching=True,check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
    converter.close()
    fake_file_handle.close()

    with open(outputDirectory, 'w') as file_object:
        file_object.write(text)

    #--------------------Initial file line adjustments--------------------------#
    data_1 = []
    for x in text.split('\n'):
        data_1.append(x)
    data_zip = data_1[5].split(" ")[1]
    #-----------------Attributes Extraction Logic ------------------------------#

    #-----------------------Diminishing File -----------------------------------#
    with open(outputDirectory) as fi:
        for name in fi:
            tname = []
            for name in fi:
                if("," in name):
                    tname.append(name)

    count = 0
    tfile = []
    with open(outputDirectory) as infile:
        for line in infile:
            if(tname[0] in line):
                tfile.append(line)
                count += 1
                if(count == 2):
                    break
            elif(count == 1 ):
                tfile.append(line)
            elif(count == 2):
                tfile.append(line)
                break
    #----------------Final file line adjustments--------------------------#
    for tf in tfile:
        with open(outputDirectory, 'w') as outfile:
            outfile.write(tf)
    for tf in tfile:
        with open(outputDirectory, 'a') as outfile:
            if(tf !='\n'):
                outfile.write(tf)
    with open(outputDirectory, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(outputDirectory, 'w') as fout:
        fout.writelines(data[1:])
    print("name :"+data[1][:-1])
    #---------------END Final file line adjustments-----------------------#
    #---------------------Extracting Attributes --------------------------#
    with open(FINAL_CSV, 'a') as final_file_append:
       final_file_append.write(data[1][:-1]+','+data[6][:-1]+','+data[2][:-1]+','+data[3][:-1]+','+data[4][:-1]+',Phone#,'+data[7][:-1]+','+data[8][:-1]+','+data[13][:-1]+','+data_1[0]+','+data_zip+','+data[36][:-1]+'.'+data[37][:-1]+','+'Physician NPI'+','+data[13][:-1]+'\n')


#-----------------------END OF UB Function------------------------------------------------------------#




def extract_ERB(pdf_path,outputDirectory):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    codec = 'utf-8'  # 'utf16','utf-8'
    laparams = LAParams()
    converter = TextConverter(resource_manager, fake_file_handle,codec=codec,laparams=laparams)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,caching=True,check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
    converter.close()
    fake_file_handle.close()

    with open(outputDirectory, 'w') as file_object:
        file_object.write(text)


    with open(outputDirectory, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(outputDirectory, 'w') as fout:
        fout.writelines(data[1:])
    fp3 = open(outputDirectory)
    for i, line in enumerate(fp3):
        if ("PATIENT INFORMATION" in line):
            patient_number = i + 1
            break
    fp3.close()
    lastname = data[patient_number +1 ][:-1].split('D.O.B.')[0].strip().split(' ')[0]
    firstname = data[patient_number +1 ][:-1].split('D.O.B.')[0].replace('  ',' ').split(' ')[1].strip().replace('-','')

    print("lastname :"+lastname)
    street = data[patient_number +2 ][:-1].strip()
    city = data[patient_number +3 ][:-1].split(',')[0]
    state = data[patient_number +3 ][:-1].split(' ')[1].strip()
    zip = data[patient_number +3 ][:-1].split(' ')[2].strip()
    phone = "NA"
    dob = data[patient_number +1 ][:-1].split('D.O.B.')[1].strip()
    gender = "NA"
    fp4 = open(outputDirectory)
    for i, line in enumerate(fp4):
        if ("DATE OF SERVICE" in line):
            dos_number = i + 1
            break
    fp4.close()
    for k in range(0,10):
        if(data[dos_number + k][:-1].__contains__(',')):
            dateofservice = data[dos_number + k][:-1].replace(',','').strip().replace('DATE OF SERVICE: ','')
            break
    fp4 = open(outputDirectory)
    for i, line in enumerate(fp4):
        if ("ATTENDING PROVIDER" in line):
            provider_number = i + 1
            break
    fp4.close()

    providername=data[provider_number][:-1].split(':')[1].replace(',','').strip()
    fp5 = open(outputDirectory)
    for i, line in enumerate(fp5):
        if ("Fax" in line):
            fax_number = i + 1
            break
    fp5.close()
    for k in range(0,7):
        providerzip = data[fax_number - 1][:-1].split(' ')[2]
        break
    fp6 = open(outputDirectory)
    for i, line in enumerate(fp6):
        if ("TOTAL" in line):
            total_number = i + 1
            break
        elif("TOAL" in line):
            total_number = i + 1
            break
    fp6.close()

    total = data[total_number + 4][:-1].replace(',','').strip()
    npi = "NA"
    doi = dateofservice
    #---------------END Final file line adjustments-----------------------#
    #---------------------Extracting Attributes --------------------------#
    # 1. Client Last Name|Text
    # 1.1 Client First Name | Text
    # 2. Client Street Address | Text
    # 3. Client City | Text
    # 4. Client State | Text
    # 5. Client Zip Code | Number
    # 6. Client Phone Number (if available) | Special Number
    # 7. Client Date of Birth | Date
    # 8. Client Gender | Text
    # 9. Date of Service (Encounter) | Date
    # 10. Provider Name | Text
    # 11. Provider Zip Code | Number
    # 12. Total Charges | Number
    # 13. Physician NPI | Number
    # 14. Date of Injury | Date

    with open(FINAL_CSV, 'a') as final_file_append:

        final_file_append.write(lastname+','+firstname+','+street+','+city+','+state+','+zip+','+phone+','+dob+','+gender+','+dateofservice+','+providername+','+providerzip+','+total+','+npi+','+doi+'\n')


#-----------------------END OF ERBILL Type 3Function------------------------------------------------------------#




def extract_ERF(pdf_path,outputDirectory):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    codec = 'utf-8'  # 'utf16','utf-8'
    laparams = LAParams()
    converter = TextConverter(resource_manager, fake_file_handle,codec=codec,laparams=laparams)
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,caching=True,check_extractable=True):
            page_interpreter.process_page(page)
        text = fake_file_handle.getvalue()
    converter.close()
    fake_file_handle.close()

    with open(outputDirectory, 'w') as file_object:
        file_object.write(text)


    with open(outputDirectory, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(outputDirectory, 'w') as fout:
        fout.writelines(data[1:])
    fp6 = open(outputDirectory)
    for i, line in enumerate(fp6):
        if ("Bill To" in line):
            patient_number = i + 1
            break
    fp6.close()
    lastname = data[patient_number +2 ][:-1].strip().split(' ')[0]
    firstname = data[patient_number +2 ][:-1].strip().split(' ')[1]
    print("lastname : "+lastname)
    street = data[patient_number +4 ][:-1].strip()
    city = data[patient_number +6 ][:-1].split(',')[0]

    state = data[patient_number +6 ][:-1].split(' ')[1].strip()
    zip = data[patient_number +6 ][:-1].split(' ')[2].strip()
    phone = "NA"
    dob = "NA"
    gender = "NA"
    fp7 = open(outputDirectory)
    for i, line in enumerate(fp7):
        if ("Date:" in line):
            dos_number = i + 1
            break
    fp7.close()
    for k in range(0,7):
        if(data[dos_number + k][:-1].__contains__(',')):
            dateofservice = data[dos_number + k][:-1].replace(',','').strip().replace('Date: ','')
            break
    fp8 = open(outputDirectory)
    for i, line in enumerate(fp8):
        if ("," in line):
            provider_number = i + 1
            break
    fp8.close()

    providername=data[provider_number][:-1].split(',')[0].strip()

    providerzip = "NA"

    fp10 = open(outputDirectory)
    for i, line in enumerate(fp10):
        if ("Account Current Balance" in line):
            total_number = i + 1
            break
        elif("TOAL" in line):
            total_number = i + 1
            break
    fp10.close()

    total = data[total_number + 4][:-1].replace(',','').strip()
    npi = "NA"
    doi = dateofservice
    #---------------END Final file line adjustments-----------------------#
    #---------------------Extracting Attributes --------------------------#
    # 1. Client Last Name|Text
    # 1.1 Client First Name | Text
    # 2. Client Street Address | Text
    # 3. Client City | Text
    # 4. Client State | Text
    # 5. Client Zip Code | Number
    # 6. Client Phone Number (if available) | Special Number
    # 7. Client Date of Birth | Date
    # 8. Client Gender | Text
    # 9. Date of Service (Encounter) | Date
    # 10. Provider Name | Text
    # 11. Provider Zip Code | Number
    # 12. Total Charges | Number
    # 13. Physician NPI | Number
    # 14. Date of Injury | Date

    with open(FINAL_CSV, 'a') as final_file_append:

        final_file_append.write(lastname+','+firstname+','+street+','+city+','+state+','+zip+','+phone+','+dob+','+gender+','+dateofservice+','+providername+','+providerzip+','+total+','+npi+','+doi+'\n')


#---------------END OF ER FACILITY AND PHYSICIAN Type4 --------------------------------------------#



#----------------------------------MAIN Function------------------------------------------------------#
if __name__ == '__main__':

    INPUT_DIRECTORY = 'C:/Users/sridhar/Desktop/Upwork/in/'
    OUTPUT_DIRECTORY = 'C:/Users/sridhar/Desktop/Upwork/out/'

    #----------------reading the directory for any new PDF files-------------------------------------#
    arr = os.listdir(INPUT_DIRECTORY)
    INPUT_FILE = ""
    OUTPUT_FILE = ""
    for tfile in arr:
        if (tfile.startswith("UB")):
            INPUT_FILE = INPUT_DIRECTORY+tfile
            OUTPUT_FILE = OUTPUT_DIRECTORY+tfile[:-3]+"txt"
            extract_UB(INPUT_FILE,OUTPUT_FILE)

        elif (tfile.startswith("HCFA")):
            INPUT_FILE = INPUT_DIRECTORY+tfile
            OUTPUT_FILE= OUTPUT_DIRECTORY+tfile[:-3]+"txt"
            extract_HCFA(INPUT_FILE,OUTPUT_FILE)

        elif (tfile.startswith("ER Bill") | tfile.startswith("ER Inv") ):
            INPUT_FILE = INPUT_DIRECTORY+tfile
            OUTPUT_FILE= OUTPUT_DIRECTORY+tfile[:-3]+"txt"
            extract_ERB(INPUT_FILE,OUTPUT_FILE)

        elif (tfile.startswith("ER Facility") | tfile.startswith("ER Phy")):
            INPUT_FILE = INPUT_DIRECTORY+tfile
            OUTPUT_FILE= OUTPUT_DIRECTORY+tfile[:-3]+"txt"
            extract_ERF(INPUT_FILE,OUTPUT_FILE)

        else:
            print("Invalid/Undefined file format...")


    #pdfText = extract_text_from_pdf('C:/Users/sridhar/Desktop/ERF.pdf')

