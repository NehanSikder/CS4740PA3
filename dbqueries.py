import pymysql.cursors

def connect_to_db():
    connection = pymysql.connect(host='uvaclasses.martyhumphrey.info',
                             user='UVAClasses',
                             password='TalkingHeads12',
                             db='uvaclasses',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    return connection

def get_class_info(classnum):
    connection = connect_to_db()
    output = "unable to retrieve information"
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = 'Select Description from CS1188Data WHERE Number= %d' % int(classnum)
            cursor.execute(sql)
            result = cursor.fetchone()
            output = result['Description']
    finally:
        connection.close()
    return output

def get_class_instructor(classnum):
    connection = connect_to_db()
    output = "unable to retrieve information"
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = 'Select Instructor from CS1188Data WHERE Number= %d' % int(classnum)
            cursor.execute(sql)
            result = cursor.fetchone()
            output = result['Instructor']
    finally:
        connection.close()
    return output

def get_available_seats(classnum):
    connection = connect_to_db()
    output = "unable to retrieve information"
    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = 'Select Enrollment, EnrollmentLimit from CS1188Data WHERE Number= %d' % int(classnum)
            cursor.execute(sql)
            result = cursor.fetchone()
            output = int(result['EnrollmentLimit']) - (result['Enrollment'])
    finally:
        connection.close()
    return output



if __name__ == "__main__":
    print(get_class_info("1010"))
    print(get_class_instructor("1010"))
    print(get_available_seats("1010"))


