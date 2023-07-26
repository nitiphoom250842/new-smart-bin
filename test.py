from core.log import LogSystems


# log_instance = LogSystems(data=None, type_log='error')
# data = log_instance.read_csv_file()
# print(data)

push_log_instance = LogSystems(data=[[1,2,3],[4,5,6]], type_log='error')
data = push_log_instance.write_csv_file()
print(data)