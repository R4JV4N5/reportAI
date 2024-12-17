# db_columns_info = '''
# Table:university_data

# Price units are in 'INR',

# 1. University (VARCHAR):
#    - Description: Represents the name of the university offering the course. This is used to identify the institution within the data.
#    - Unique Values: ['JAIN (DEEMED-TO-BE UNIVERSITY)']

# 2. UniversityCode (VARCHAR):
#    - Description: The code representing the university.

# 3. Batch (VARCHAR):
#    - Description: Indicates the batch or cohort in which a student is enrolled, with details like start date and course duration.
#    - Unique Values: ['July 2020 - 3 Years', 'July 2020 - 2 Years', 'July 2019 - 2 Years', 'July 2019 - 3 Years', 'WorkX - 2020', 
#                       'July 2020 - 1 Year', 'Jan 2020 - 2 Years', 'Jan 2019 - 2 Years', 'Jan 2021 -3 Years', 'Jan 2021 - 2 Year', 
#                       'Jan 2020 - 3 Years', 'July 2021 - 2 Years', 'July 2019 - 1 Year', 'July 2021 - 3 Years', 'Jan 2019 - 3 Years', 
#                       'Jan 2022 - 2 Years', 'Jan 2022 - 3 Years']

# 4. Course (VARCHAR):
#    - Description: Indicates the name of the course a student is enrolled in.
#    - Unique Values: ['Bachelor of Science', 'Bachelor of Business Administration', 'Master of Science Psychology', 
#                      'Master of Commerce', 'Bachelor of Arts', 'Bachelor of Commerce', 'Bachelors in Computer Application', 
#                      'WorkX Diploma Program', 'Post Graduate Diploma Program in Banking & Finance Management', 
#                      'MA in Economics', 'Bachelor of Business Administration with Apprenticeship', 
#                      'Master of Science (Psychology) with Apprenticeship', 'Bachelor of Arts with Apprenticeship', 
#                      'Post Graduate Diploma Program in Human Resource Management', 'Post Graduate Diploma Program in Finance Management',
#                      'Master of Commerce with Apprenticeship', 'Bachelor of Commerce with Apprenticeship', 
#                      'MA in Economics with Apprenticeship', 'Post Graduate Diploma Program in Information Technology', 
#                      'M.A. (English)']

# 5. Semester (VARCHAR):
#    - Description: Denotes the semester within the academic year.
#    - Unique Values: ['Semester 1', 'Semester 3', 'Registration', 'Semester 5']

# 6. InstallmentNo (INTEGER):
#    - Description: Represents the installment number for payment.

# 7. EnrollmentNo (VARCHAR):
#    - Description: The unique identifier for each student’s enrollment.

# 8. Name (VARCHAR):
#    - Description: The name of the student.

# 9. PaymentId (INTEGER):
#    - Description: The unique identifier for each payment made.

# 10. Amount (FLOAT):
#     - Description: The total payment amount made by the student.

# 11. Mode (VARCHAR):
#     - Description: The mode of payment used by the student, such as online payment or demand draft.
#     - Unique Values: ['Net Banking', 'DD']

# 12. Provider (VARCHAR):
#     - Description: The payment service provider used to process the payment.
#     - Unique Values: ['ATOM TECHNOLOGIES LTD.', 'CITRUS PAYMENT SOLUTIONS PVT. LTD.', 'AGGREPAY', 'CCAvenue']

# 13. Status (VARCHAR):
#     - Description: The status of the payment.
#     - Unique Values: ['C']

# 14. PaidOn (VARCHAR):
#     - Description: The date when the payment was made.

# '''
db_columns_info = '''
Table:university_data

Price units are in 'INR',

1. University (VARCHAR):
   - Description: Represents the name of the university offering the course. This is used to identify the institution within the data.

2. UniversityCode (VARCHAR):
   - Description: The code representing the university.

3. Batch (VARCHAR):
   - Description: Indicates the batch or cohort in which a student is enrolled, with details like start date and course duration.

4. Course (VARCHAR):
   - Description: Indicates the name of the course a student is enrolled in.

5. Semester (VARCHAR):
   - Description: Denotes the semester within the academic year.


6. InstallmentNo (INTEGER):
   - Description: Represents the installment number for payment.

7. EnrollmentNo (VARCHAR):
   - Description: The unique identifier for each student’s enrollment.

8. Name (VARCHAR):
   - Description: The name of the student.

9. PaymentId (INTEGER):
   - Description: The unique identifier for each payment made.

10. Amount (FLOAT):
    - Description: The total payment amount made by the student.

11. Mode (VARCHAR):
    - Description: The mode of payment used by the student, such as online payment or demand draft.
  
12. Provider (VARCHAR):
    - Description: The payment service provider used to process the payment.
    
13. Status (VARCHAR):
    - Description: The status of the payment.
   

14. PaidOn (VARCHAR):
    - Description: The date when the payment was made.

'''







