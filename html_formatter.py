import sys

fp = None

def printf(*a):
    if fp == None:
        print(*a)
    else:
        print(*a, file=fp)

def print_html_style_section():
    printf("    <style>")
    printf(" \
.styled-table {\n \
    border-collapse: collapse;\n \
    margin: 25px 0;\n \
    font-size: 0.9em;\n \
    font-family: sans-serif;\n \
    min-width: 400px;\n \
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);\n \
}\n \
.styled-table thead tr {\n \
    background-color: #009879;\n \
    color: #ffffff;\n \
    text-align: left;\n \
}\n \
.styled-table th {\n \
    padding: 12px 15px;\n \
    background-color: #25d5da;\n \
}\n \
.styled-table td {\n \
    padding: 12px 15px;\n \
}\n \
.styled-table tbody tr {\n \
    border-bottom: 1px solid #dddddd;\n \
}\n \
\n \
.styled-table tbody tr:nth-of-type(even) {\n \
    background-color: #f3f3f3;\n \
}\n \
\n \
.styled-table tbody tr:last-of-type {\n \
    border-bottom: 2px solid #009879;\n \
}\n \
.styled-table tbody tr.active-row {\n \
    font-weight: bold;\n\n \
    color: #009879;\n \
}\n \
.bottom-border { border-bottom: 3px double darkgreen; } \n \
.bookingid-style {\n \
    \n \
}\n \
 caption {\n \
   font-size: 30px;\n \
 }\n \
.bookingdate-style {\n \
    min-width: 85px; \n \
    max-width: 90px; \n \
}\n \
.bookingtime-style {\n \
    \n \
}\n \
.holes-style {\n \
    \n \
}\n \
.cart-style {\n \
    \n \
}\n \
.numgolfers-style {\n \
    \n \
}\n \
.golfer1-style {\n \
    \n \
}\n \
.golfer1-style {\n \
    \n \
}\n \
.golfer1-style {\n \
    \n \
}\n \
.golfer1-style {\n \
    \n \
}\n \
.requests-style {\n \
    max-width: 250px;\n \
}\n \
.email-style {\n \
    \n \
}\n \
.phone-style {\n \
    \n \
}\n \
.paid-style {\n \
    \n \
}\n \
.paid-style::before {\n \
    content: \"PAID \";\n \
    color: red; \n \
    font-style: italic;\n \
    font-weight: bold;\n \
}\n \
.amount-style {\n \
    \n \
}\n \
.items-style {\n \
    white-space: pre-wrap;\n \
    \n \
}\n \
    ")
    printf("    </style>\n")


def print_html_head_section():
    printf("  <head>")
    print_html_style_section()
    printf("  </head>")

def print_html_body_message(golf_course_name):
    printf(" \n \
  <p>Hi Starter,</p> \n \
  <p>How are you today? I hope you are ready to <strong>Sell! Sell! Sell!</strong></p> \n \
  <p>In the table below you will find reservations for %s for the next seven days.</p> \n \
  <p><em>Enjoy!</em></p> \n \
  <p>The Boss</p><br /><br /> \n" % (golf_course_name))
    
def print_html_table_header(titles, styles):
    printf("  <tr> ")
    for title, style in zip(titles, styles):
        printf('   <th class="%s">%s</th>' % (title, style))
    printf("</tr>")

def print_html_table_row(column_styles, record, last_of_date):
    printf("<tr>")
    for style, value in zip(column_styles, record):
        if style=='amount-style' and value != "":
            style='paid-style'
        if not last_of_date:
            printf('<td class="%s">%s</td>' % (style, value))
        else:
            printf('<td class="%s bottom-border">%s</td>' % (style, value))
    printf("</tr>")

def print_html_table_rows(column_styles, records):
    head, *records_tail = records
    records_tail.append(records[-1])
    for (record, t) in zip(records, records_tail):
        # 3rd param in the call below determines if this record is the last for this date
        print_html_table_row(column_styles, record, record[1] != t[1])

def print_html_body_table(golf_course_name, column_styles, column_titles, records):
    printf('<table class="styled-table">')
    printf('<caption>%s</caption>' % (golf_course_name))
    print_html_table_header(column_styles, column_titles)
    print_html_table_rows(column_styles, records)
    printf('</table>')

def print_html_body_section(golf_course_name, column_styles, column_titles, records):
    printf("  <body>")
    # print_html_body_message(golf_course_name)
    print_html_body_table(golf_course_name, column_styles, column_titles, records)
    printf("  </body>")
 
def print_records_in_html(filename, golf_course_name, column_styles, column_titles, records):
    global fp
    if filename == None:
        fp = None
    else:
        fp = open(filename, "w")
    printf("<html>")
    print_html_head_section()
    print_html_body_section(golf_course_name, column_styles, column_titles, records)
    printf("</html>")
    if filename != None:
        fp.close()

