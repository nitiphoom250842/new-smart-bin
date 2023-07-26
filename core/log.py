import csv

file_path_error = './log/error-log.csv'
file_path_log = './log/error-log.csv'

class LogSystems:
   
    def __init__(self,data,type_log):
        self.data = data
        self.type_log = type_log
    
    def read_csv_file(self):
        data = []
        if (self.type_log =='error'):
            with open(file_path_error, 'r', newline='') as csvfile:
                csv_reader = csv.reader(csvfile)
                for row in csv_reader:
                    data.append(row)
            return data
        else:
            with open(file_path_log, 'r', newline='') as csvfile:
                csv_reader = csv.reader(csvfile)
                for row in csv_reader:
                    data.append(row)
            return data
    
    def write_csv_file(self):
        if (self.type_log =='error'):
            with open(file_path_error, 'a', newline='') as csvfile:  
                csv_writer = csv.writer(csvfile)
                for row in self.data:
                    csv_writer.writerow(row)
        else:
            with open(file_path_log, 'a', newline='') as csvfile:  
                csv_writer = csv.writer(csvfile)
                for row in self.data:
                    csv_writer.writerow(row)
