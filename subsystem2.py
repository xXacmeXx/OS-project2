# subsystem1.py
import threading
from DS import Task, Queue
import copy

cpu_tasks = [None, None]
cpu_stall = [False, False]
def core_function(core_id, barrier, resources):
    
    
    while True:
        barrier.wait()
        if cpu_stall[core_id - 1]:
            if cpu_tasks[core_id - 1].required_R1 <= resources['R1'] and cpu_tasks[core_id - 1].required_R2 <= resources['R2']:
                cpu_stall[core_id - 1] = False
                cpu_tasks[core_id - 1].duration -= 1
                resources['R1'] -= cpu_tasks[core_id - 1].required_R1
                resources['R2'] -= cpu_tasks[core_id - 1].required_R2
        elif cpu_tasks[core_id - 1] == None:
            pass     
        else:
            cpu_tasks[core_id - 1].duration -= 1
        barrier.wait()
    

class Subsystem2(threading.Thread):
    def __init__(self, resources, tasks, main_barrier):
        """
        تعریف زیرسیستم اول به صورت یک نخ.
        
        پارامترها:
        - resources: دیکشنری شامل تعداد منابع R1 و R2 برای این زیرسیستم.
        - tasks: لیستی از شیء‌های Task که به این زیرسیستم تعلق دارند.
        """
        threading.Thread.__init__(self)
        self.resources = resources
        self.tasks = tasks
        self.ready_queue = Queue()
        self.time_count = 0
        self.barrier = threading.Barrier(3)  # ۳ هسته + ۱ حلقه اصلی
        self.main_barrier = main_barrier
        self.cpu_stall = [False, False]
        self.running_tasks = [] 

    def get_resources(self):
        """
        بازگرداندن وضعیت منابع.
        
        بازگشت:
        - دیکشنری شامل تعداد منابع R1 و R2.
        """
        return self.resources

    def get_ready_queue(self):
        """
        بازگرداندن وضعیت صف آماده‌به‌کار.
        
        بازگشت:
        - لیستی از تسک‌های داخل صف آماده‌به‌کار.
        """
        return self.ready_queue.tasks

    def get_cpu_tasks(self):
        """
        بازگرداندن وضعیت تسک‌های در حال اجرا روی پردازنده‌ها.
        
        بازگشت:
        - لیستی از تسک‌های در حال اجرا روی پردازنده‌ها.
        """
        return cpu_tasks
    
    def are_all_queues_empty(self):
        """
        بررسی می‌کند که آیا همه صف‌های Ready، صف Waiting و لیست تسک‌ها خالی هستند یا نه.
        
        بازگشت:
        - True اگر همه خالی باشند، در غیر این صورت False.
        """
        # بررسی صف‌های Ready
        is_ready_empty = self.ready_queue.is_empty()
        # بررسی صف Waiting
        # بررسی لیست تسک‌ها (اگر همه تسک‌ها وارد صف‌ها شده‌اند)
        all_tasks_added = all(task.arrival_time < self.time_count for task in self.tasks)
        is_cpu_empty = (not(cpu_tasks[0])) and (not(cpu_tasks[1]))
        
        return is_ready_empty and all_tasks_added and is_cpu_empty
    def send_test():
        return "slaaaaaaaam!"
    
    def remove_from_cpu(self, core_id):
        if cpu_stall[1] == False:
            self.resources['R1'] += cpu_tasks[core_id].required_R1
            self.resources['R2'] += cpu_tasks[core_id].required_R2
        self.ready_queue.enqueue(cpu_tasks[1])
        self.ready_queue.sort_by_remaining_time()
    def assign_to_cpu(self, core_id, task):
        if task.required_R1 <= self.resources['R1'] and task.required_R2 <= self.resources['R2']:
            self.resources['R1'] -= task.required_R1
            self.resources['R2'] -= task.required_R2
        else:
            cpu_stall[core_id] = True
        cpu_tasks[core_id] = task
    
    def run(self):
        """
        اجرای زیرسیستم اول.
        """
        print("subsystem2 started...")
        self.tasks.sort(key=lambda task: task.arrival_time)
        cores = []
        for i in range(2):
            core_thread = threading.Thread(target=core_function, args=(i + 1 ,self.barrier, self.resources))
            core_thread.start()
            cores.append(core_thread)
        
        while not self.are_all_queues_empty():
            self.main_barrier.wait()

            turn = []
            for i in range(len(cpu_tasks)):
                if cpu_tasks[i] != None:
                    if cpu_tasks[i].duration == 0:
                        if not(self.ready_queue.is_empty()):
                            turn.append(self.ready_queue.dequeue())
                        cpu_tasks[i] = None
            for task in self.tasks:
                if task.arrival_time == self.time_count:
                    turn.append(task)
                    self.tasks.remove(task)
                else:
                    break

            choose1 = None
            choose2 = None
            turn.sort(key=lambda task: task.duration)
            if(len(turn) == 1):
                choose1 = turn.pop(0)
            elif(len(turn) > 1):
                choose1 = turn.pop(0)
                choose2 = turn.pop(0)
            for task in turn:
                self.ready_queue.enqueue(task)
                self.ready_queue.sort_by_remaining_time()

            
            if cpu_tasks[0] == None and cpu_tasks[1] == None:
                if choose1 != None:
                    self.assign_to_cpu(0, choose1)
                    if choose2 != None:
                        self.assign_to_cpu(1, choose2)
            elif cpu_tasks[0] == None or cpu_tasks[1] == None:
                empty = None
                full = None
                if cpu_tasks[0] == None:
                    empty = 0
                    full = 1
                else:
                    empty = 1
                    full = 0
                if choose1 != None:
                    self.assign_to_cpu(empty, choose1)
                    if choose2 != None:
                        if choose2.duration < cpu_tasks[full].duration:
                            self.remove_from_cpu(full)
                            self.assign_to_cpu(full, choose2)
                        else:
                            self.ready_queue.enqueue(choose2)
                            self.ready_queue.sort_by_remaining_time()
            else:
                if choose1 != None:
                    if choose1.duration < min(cpu_tasks[0].duration, cpu_tasks[1].duration):
                        self.remove_from_cpu(0)
                        self.assign_to_cpu(0, choose1)
                        if choose2 != None:
                            if choose2.duration < cpu_tasks[1].duration:
                                self.remove_from_cpu(1)
                                self.assign_to_cpu(1, choose2)
                            else:
                                self.ready_queue.enqueue(choose2)
                                self.ready_queue.sort_by_remaining_time()
                    elif choose1.duration >= max(cpu_tasks[0].duration, cpu_tasks[1].duration):
                        self.ready_queue.enqueue(choose1)
                        if choose2 != None:
                            self.ready_queue.enqueue(choose2)
                        self.ready_queue.sort_by_remaining_time()
                    else:
                        bigger = None
                        if cpu_tasks[0].duration < cpu_tasks[1].duration:
                            bigger = 1
                        else:
                            bigger = 0
                        self.remove_from_cpu(bigger)
                        self.assign_to_cpu(bigger, choose1)
                        if choose2 != None:
                            self.ready_queue.enqueue(choose2)
                            self.ready_queue.sort_by_remaining_time()
        

            self.barrier.wait()
            self.time_count += 1
            self.barrier.wait()
            self.main_barrier.wait()

        

        
