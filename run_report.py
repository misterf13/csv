from calendar import monthrange
from optparse import OptionParser
import csv
import os

def run_report(directory, filename, month, year, low_date, high_date):
    call_dict = {}
    for name in os.listdir():
        if name.endswith(".csv"):
            nice_name = name.split('.')[0]
            call_dict[nice_name] = {}
            with open(directory + name, 'r') as csvfile:
                report_reader = csv.reader(csvfile)
                next(report_reader)
                for row in report_reader:
                    call_dict[nice_name][int(row[0].split(':')[0])] = int(row[1])

    #print(call_dict)
    output = 'hours,'
    for day in range(1, high_date+1):
        date_data = f'{month}-{day}-{year}'
        output += date_data + ','
    output += '\n'

    for hour in range(24):
        output += f'{hour},'
        for day in range(1, high_date+1):
            date_data = f'{month}-{day}-{year}'
            if date_data in call_dict:
                if hour in call_dict[date_data]:
                    output += f'{call_dict[date_data][hour]},'
                else:
                    output += ','
            else:
                 output += ','
        output += '\n'

    print(output)
    with open(filename, 'w') as output_file:
        output_file.write(output)


def main(output_file, directory, month, year):
    low_date, high_date = monthrange(year, month)
    print(low_date, high_date)
    run_report(directory, output_file, month, year, low_date, high_date)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
                      help="write report to FILE", metavar="FILE")
    parser.add_option("-d", "--directory", dest="dir_name",
                      help="read report from DIR")
    parser.add_option("-m", "--month", dest="month",
                      help="month of report", type=int)
    parser.add_option("-y", "--year", dest="year",
                      help="year of report", type=int)
    (options, args) = parser.parse_args()
    print(options)

    main(options.filename, options.dir_name, options.month, options.year)