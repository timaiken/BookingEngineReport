import mysql.connector, smtplib, ssl, sys, getopt
from datetime import datetime, date, timedelta
import time
from html_formatter import print_records_in_html
from send_email import send_email
from printwrapper import PrintWrapper

# attr should be (attr_type, attr_name+booking_type, attr_value)
def isNamedAttribute(name, booking_type, attr):
    if isinstance(attr, list) and len(attr) >= 3:
        # print("%s %s" % (name + str(booking_type), attr[1]))
        return (name + str(booking_type)) == attr[1]
    else:
        return False

def getFieldValue(form_attribute_list, name, booking_type):
    matches = [attr[2] for attr in form_attribute_list if isNamedAttribute(name, booking_type, attr)] 
    if len(matches) > 0:
        return matches[0]
    else:
        return ""
    
    
def getSQLData(booking_type, startdate, enddate, is_rsgc, pwd):
    mydb = mysql.connector.connect(
        host="localhost",
        user="rsgcmgmt_wrdp1",
        password=pwd,
        database="rsgcmgmt_wrdp1"
        )

    mycursor = mydb.cursor()
    # stmt = "SELECT booking_id, sort_date, form from wp_booking where substring(sort_date,1,10) >= %s and substring(sort_date,1,10) <= %s and booking_type = %s and trash <> '1' order by sort_date asc"
    stmt = "SELECT wp_booking.booking_id, sort_date, form, attr.amount, attr.items \
            FROM wp_booking \
            LEFT JOIN \
              (SELECT t3.booking_id AS booking_id, t1.meta_value AS amount, t2.meta_value AS items \
               FROM (SELECT post_id, meta_value \
                     FROM wp_postmeta \
                     WHERE meta_key='wpsc_total_amount') t1, \
                    (SELECT post_id, meta_value \
                     FROM wp_postmeta \
                     WHERE meta_key='wpspsc_items_ordered') t2, \
                    (SELECT post_id, cast(substring_index(substring_index(meta_value,'\"',2),'\"',-1) AS UNSIGNED) AS booking_id \
                     FROM wp_postmeta \
                     WHERE meta_key='custom_fields_data') t3 \
               WHERE t1.post_id = t2.post_id \
                 AND t1.post_id = t3.post_id) AS attr \
            ON wp_booking.booking_id = attr.booking_id \
            WHERE substring(wp_booking.sort_date,1,10) >= %s \
              AND substring(wp_booking.sort_date,1,10) <= %s \
              AND wp_booking.booking_type = %s \
              AND wp_booking.trash <> '1' \
              ORDER BY wp_booking.sort_date asc"
    parms = (startdate, enddate, booking_type)

    mycursor.execute(stmt, parms)
    myresults = mycursor.fetchall()

    records =[]
    for row in myresults:
        # print(row)
        booking_id = row[0]
        sort_date = row[1]
        formrow = row[2]
        amount = "" if row[3] == None else row[3]
        items = "" if row[4] == None else row[4]

        # print('----------- amount %s        items %s --------------' % (amount, items))

        data = formrow.split("~")
        # print("# attributes %s" % (data))

        lol = []
        for l in data:
            lol.append(l.split("^"))

        # print("list of lists %s" % (lol))

        bookingDate = sort_date.strftime("%A %Y-%m-%d")
        # print("Booking date: %s" % (bookingDate))

        bookingTime = getFieldValue(lol, "rangetime", booking_type)
        # bookingTime = getFieldValue(lol, "rangetime", booking_type)[0:5] + '-' +  getFieldValue(lol, "rangetime", booking_type)[8:5]
        # print("Booking time: %s" % (bookingTime))

        holes = getFieldValue(lol, "holes", booking_type)
        # print("Holes: %s" % (holes))

        cart = getFieldValue(lol, "cart", booking_type)
        # print("cart: %s" % (cart))

        visitors = getFieldValue(lol, "visitors", booking_type)
        # print("# Players: %s" % (visitors))

        name = getFieldValue(lol, "name", booking_type)
        secondname = getFieldValue(lol, "secondname", booking_type)
        fullname =name.strip() + " " + secondname.strip()
        # print("name: %s" % (fullname))

        email = getFieldValue(lol, "email", booking_type)
        # print("email: %s" % (email))

        phone = getFieldValue(lol, "phone", booking_type)
        # print("phone: %s" % (phone))

        fname2 = getFieldValue(lol, "fname2", booking_type)
        lname2 = getFieldValue(lol, "lname2", booking_type)
        fullname2 = fname2.strip() + " " + lname2.strip()
        # print("2nd Player: %s" % (fullname2))

        fname3 = getFieldValue(lol, "fname3", booking_type)
        lname3 = getFieldValue(lol, "lname3", booking_type)
        fullname3 = fname3.strip() + " " + lname3.strip()
        # print("3rd Player: %s" % (fullname3))

        fname4 = getFieldValue(lol, "fname4", booking_type)
        lname4 = getFieldValue(lol, "lname4", booking_type)
        fullname4 = fname4.strip() + " " + lname4.strip()
        # print("4th Player: %s" % (fullname4))

        requests = getFieldValue(lol, "requests", booking_type)
        # print("requests: %s" % (requests))

        # print("------------------------------------------------")
        records.append([ booking_id, bookingDate, bookingTime, holes, cart, visitors, fullname, fullname2, 
                         fullname3, fullname4, requests, email, phone, amount, items])

    return records

column_styles = [
"bookingid-style", # booking id
"bookingdate-style", # booking date
"bookingtime-style", # booking time
"holes-style", # holes
"cart-style", # cart
"numgolfers-style", # num golfers
"golfer1-style", # golfer1
"golfer1-style", # golfer2
"golfer1-style", # golfer3
"golfer1-style", # golfer4
"requests-style", # requests
"email-style", # email
"phone-style", # phone
"amount-style", # amount
"items-style" # items
]

column_titles = [
    "Booking Id",     # 0
    "Booking Date",   # 1
    "Booking Time",   # 2
    "Holes",          # 3
    "Cart?",          # 4
    "# Golfers",      # 5
    "Golfer 1",       # 6
    "Golfer 2",       # 7
    "Golfer 3",       # 8
    "Golfer 4",       # 9
    "Requests",       # 10
    "Email",          # 11
    "Phone",          # 12
    "Amount Paid",    # 13
    "Items Purchased" #14
]

def usage():
    print ('usage: ', sys.argv[0],'[Options]')
    print("Options:")
    print("  -c cc_email        Cc recipient of email")
    print("  -d                 Generate Desert Aire Bookings")
    print("  -e enddate         End date for bookings (yyyy-mm-dd)")
    print("  -h                 Print this help message")
    print("  -l num_days        Number of days for bookings")
    print("  -m pwd             Email results (password must be supplied)")
    print("  -o output_file     Target file for bookings")
    print("  -p pwd             SQL password (required to get bookings)")
    print("  -r                 Generate Rancho Sierra Bookings")
    print("  -s startdate       Start date for bookings (yyyy-mm-dd)")
    print("  -t to_email        to recipient of email")
    print("  -v                 verbose - primarily debugging - output printed")
    print(" ")
    print("One of -r or -d is required. If no start date is given, the current date is used. ")
    print("Also, -l takes precedence over -e. ")

def main(argv):
    passwd = None
    wp_passwd = None
    rsgc = False
    dagc = False
    sendemail = False
    startdate_str = None
    enddate_str = None
    ndays = None
    recipientEmail = None
    prod = True
    testmode = False
    filename = None
    verbose = False
    to = None
    cc = None
    try:
        opts, args = getopt.getopt(argv,"c:de:hl:m:o:p:rs:t:v")
    except getopt.GetoptError:
        print ("Error in options")
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt in ("-c", "--cc"):
            cc = arg
        elif opt in ("-d", "--dagc"):
            dagc = True
        elif opt in ("-e", "--enddate"):
            enddate_str = arg
        elif opt in ("-l", "--timelength"):
            ndays = arg
        elif opt in ("-m", "--mail"):
            sendemail = True
            wp_passwd = arg
        elif opt in ("-p", "--pwd"):
            passwd = arg
        elif opt in ("-o", "--output"):
            filename = arg
        elif opt in ("-r", "--rsgc"):
            rsgc = True
        elif opt in ("-s", "--startdate"):
            startdate_str = arg
        elif opt in ("-t", "--to"):
            to = arg
        elif opt in ("-v", "--verbose"):
            verbose = True
        else:
            print("Bad option:", opt)

    if passwd == None:
        print ('Password required. Exiting.')
        print ('usage: ',sys.argv[0],'[-dhr] [-p <passwd>]')
        sys.exit(-1);

    if startdate_str == None:
        startdate = date.today()
    else:
        startdate = (datetime.strptime(startdate_str, "%Y-%m-%d")).date()  # convert string to date obj

    if enddate_str == None and ndays == None:      # no end date - use start date for end date
        enddate = startdate
    if ndays != None:
        enddate = startdate + timedelta(days = int(ndays))
    else:
        enddate = datetime.strptime(enddate_str, "%Y-%m-%d").date()

    if verbose:
        print("Testing ... ")
        print("Start date: ", startdate)
        print("End date: ", enddate)

    if enddate < startdate:
        print("End date is less than start date.  Bookings will be empty. Exiting.")
        exit(1)

    if not rsgc and not dagc:
        print('Must specify one of -r and -d')
        print ('usage: ',sys.argv[0],'[-dhr] [-p <passwd>]')
        sys.exit(-1);

    if rsgc and dagc:
        print('Must specify only one of -r and -d')
        print ('usage: ',sys.argv[0],'[-dhr] [-p <passwd>]')
        sys.exit(-1);

    if (rsgc):
        booking_type = 36
        golf_course_name = "Rancho Sierra Golf Course"
        gc_code = "rsgc"
    else:
        booking_type = 37
        golf_course_name = "Desert Aire Golf Course"
        gc_code = "dagc"

    if to == None and cc == None:
        print("Warning: no email recipients specified. Defaulting.")

    startdate_str = startdate.strftime("%Y-%m-%d")
    enddate_str = enddate.strftime("%Y-%m-%d")

    if filename == None and sendemail:
        filename = '/tmp/temp_' + datetime.now().strftime("%Y%m%d%H%S%f")
        if verbose:
            print("temporary filename is", filename)

    records = getSQLData(booking_type, startdate_str, enddate_str, rsgc, passwd)
    print_records_in_html(filename, gc_code, golf_course_name, column_styles, column_titles, records)

    if verbose:
        print("to:", to)
        print("cc:", cc)
    if sendemail and to == None and cc == None:
        send_email(wp_passwd, filename, rsgc, prod, "ranchosierragc@gmail.com", "desertairegc@gmail.com")
        time.sleep(2)
        send_email(wp_passwd, filename, rsgc, prod, "desertairegc@gmail.com", "ranchosierragc@gmail.com")
    else:
        send_email(wp_passwd, filename, rsgc, prod, to, cc, verbose)

if __name__ == "__main__":
   main(sys.argv[1:])
