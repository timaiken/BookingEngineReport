#!/bin/bash
#
# Note: Most of the command line options are processed by the the python script booking.py
#
usage() {
  echo ""
  echo "This command connects wrapper to Python scripts that connect the WP MySQL database "
  echo "and run SQL commands that retrieve bookings. Data is returned an HTML file and"
  echo "mailed to recipients."
  echo ""
  echo "Usage: $0 [options]"
  echo "where:"
  echo " -h [--help]    - print this help info"
  echo " -t [--test]    - test mode. Emails booking filess to testers (currently tim@timaiken.com)"
  echo " "
}

export PATH=/opt/rh/rh-python35/root/usr/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/opt/rh/rh-python35/root/usr/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
export MANPATH=/opt/rh/rh-python35/root/usr/share/man:$MANPATH
export PKG_CONFIG_PATH=/opt/rh/rh-python35/root/usr/lib64/pkgconfig${PKG_CONFIG_PATH:+:${PKG_CONFIG_PATH}}
export XDG_DATA_DIRS="/opt/rh/rh-python35/root/usr/share:${XDG_DATA_DIRS:-/usr/local/share:/usr/share}"

#
# change the following variables if you want to move the python files or the output files and log
#
PYTHON_DIR=/home3/rsgcmgmt/bin/python
# PYTHON_DIR/home3/rsgcmgmt/bemods/BookingEngineReportGen
HTML_PAGE_DIR=/home3/rsgcmgmt/booking_pages

testmode=""
while [ -n "$(echo $1 | grep '-')" ]; do
  case $1 in 
    -h | --help )           usage
                            exit 1
                            ;;
    -t | --test )           testmode="-t"
                            shift
                            ;;
    * )                     usage
                            exit 1
  esac
done

now=`date`
date=`date +%Y-%m-%d`
longdate=`date "+%A, %B %d, %Y"`
/opt/rh/rh-python35/root/usr/bin/python ${PYTHON_DIR}/booking.py  -d -p 3N95y7M7jWsQFWF ${testmode} -l 7 -m rsGc4fun -o ${HTML_PAGE_DIR}/dagc_${date}.html
echo "${now}: Desert Aire booking page for ${longdate} created and emailed." >> ${HTML_PAGE_DIR}/log

/opt/rh/rh-python35/root/usr/bin/python ${PYTHON_DIR}/booking.py  -r -p 3N95y7M7jWsQFWF ${testmode} -l 7 -m rsGc4fun -o ${HTML_PAGE_DIR}/rsgc_${date}.html
echo "${now}: Rancho Sierra booking page for ${longdate} created and emailed." >> ${HTML_PAGE_DIR}/log


