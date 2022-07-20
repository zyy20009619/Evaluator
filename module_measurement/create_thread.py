# import threading
# import time
#
#
# class myThread(threading.Thread):
#     def __init__(self, threadID, name, delay):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.delay = delay
#
#     def run(self):
#         print("开启线程： " + self.name)
#         # 获取锁，用于线程同步
#         threadLock.acquire()
#         print_time(self.name, self.delay)
#         # 释放锁，开启下一个线程
#         threadLock.release()
#
#
# def print_time(threadName, delay, counter):
#     time.sleep(delay)
#     print("%s: %s" % (threadName, time.ctime(time.time())))
#     # measure structure dep
#     for package in package_info:
#         if type == 'module':
#             package_name = package
#         else:
#             package_name = variables[package]['qualifiedName']
#         package_dic[package_name] = dict()
#         scoh, scop, odd, idd, idcc_list, edcc_list, fan_in, fan_out, iodd, iidd = com_struct_metric(package,
#                                                                                                     package_info,
#                                                                                                     struct_dep)
#         package_dic[package_name]['scoh'] = float(format(scoh, '.4f'))
#         package_dic[package_name]['scop'] = float(format(scop, '.4f'))
#         package_dic[package_name]['odd'] = float(format(odd, '.4f'))
#         package_dic[package_name]['idd'] = float(format(idd, '.4f'))
#         package_dic[package_name]['spread'] = spread_dic[package_name]
#         package_dic[package_name]['focus'] = focus_dic[package_name]
#         package_dic[package_name]['icf'] = icf_dic[package_name]
#         package_dic[package_name]['ecf'] = ecf_dic[package_name]
#         package_dic[package_name]['rei'] = rei_dic[package_name]
#         package_dic[package_name]['DSM'] = len(package_info[package])
#         class_dic = class_and_method_metric_compete(variables, package_info[package], inherit, descendent, parameter,
#                                                     method_define_var, method_use_field, method_class, call, called,
#                                                     idcc_list, edcc_list, override, overrided, import_val, imported_val,
#                                                     fan_in, fan_out, iodd, iidd)
#         package_dic[package_name]['classes'] = class_dic
#
#
#
# threadLock = threading.Lock()
#
#
# def create_thread(modules_len):
#     threads = []
#     len = int(modules_len / 50)
#
#     for i in range(0, len + 1):
#         thread = myThread(i + 1, "Thread-" + str(i + 1), i + 1)
#         thread.start()
#         threads.append(thread)
#
#     # 等待所有线程完成
#     for t in threads:
#         t.join()
#     print("退出主线程")
#
#
# if __name__ == '__main__':
#     create_thread(260)