# main.py
from DS import Task, Queue
from subsystem1 import Subsystem1
from subsystem2 import Subsystem2
import threading
def read_input():
    """
    خواندن ورودی‌های کاربر.
    
    بازگشت:
    - منابع: یک لیست از دیکشنری‌ها که شامل تعداد منابع R1 و R2 برای هر زیرسیستم است.
    - وظایف: یک لیست از لیست‌ها که هر لیست شامل وظایف یک زیرسیستم است.
    """
    # خواندن تعداد منابع برای هر زیرسیستم
    resources = []
    print("enter number of R1 & R2 for each subsystem: ")
    for i in range(4):  # 4 زیرسیستم داریم
        r1, r2 = map(int, input(f"subsystem {i+1}: ").split())
        resources.append({"R1": r1, "R2": r2})

    # خواندن وظایف هر زیرسیستم
    tasks = []
    print("enter each subsystem tasks seprated with $: ")
    for i in range(4):  # 4 زیرسیستم داریم
        subsystem_tasks = []
        print(f"subsystem {i+1} tasks :")
        while True:
            task_input = input().strip()
            if task_input == "$":
                break
            if task_input == "":
                continue
            subsystem_tasks.append(task_input)
        tasks.append(subsystem_tasks)

    return resources, tasks

def parse_tasks(subsystem_tasks, subsystem_type):
    """
    تجزیه و تحلیل وظایف هر زیرسیستم و تبدیل آن‌ها به شیء Task.
    
    پارامترها:
    - subsystem_tasks: لیستی از رشته‌های ورودی وظایف.
    - subsystem_type: نوع زیرسیستم (1, 2, 3, 4).
    
    بازگشت:
    - لیستی از شیء‌های Task.
    """
    tasks = []
    for task_input in subsystem_tasks:
        task_data = task_input.split()
        if subsystem_type == 1:
            task = Task(
                name=task_data[0],
                duration=int(task_data[1]),
                required_R1=int(task_data[2]),
                required_R2=int(task_data[3]),
                arrival_time=int(task_data[4]),
                destination_core=int(task_data[5])
            )
        elif subsystem_type == 2:
            task = Task(
                name=task_data[0],
                duration=int(task_data[1]),
                required_R1=int(task_data[2]),
                required_R2=int(task_data[3]),
                arrival_time=int(task_data[4])
            )
        elif subsystem_type == 3:
            task = Task(
                name=task_data[0],
                duration=int(task_data[1]),
                required_R1=int(task_data[2]),
                required_R2=int(task_data[3]),
                arrival_time=int(task_data[4]),
                period=int(task_data[5])
            )
        elif subsystem_type == 4:
            task = Task(
                name=task_data[0],
                duration=int(task_data[1]),
                required_R1=int(task_data[2]),
                required_R2=int(task_data[3]),
                arrival_time=int(task_data[4]),
                prerequisite_task=task_data[5] if task_data[5] != "-" else None
            )
        tasks.append(task)
    return tasks

# نمونه استفاده
if __name__ == "__main__":
    resources, tasks = read_input()
    print("resources for each subsystem: ")
    for i, resource in enumerate(resources):
        print(f"subsystem {i+1}: R1={resource['R1']}, R2={resource['R2']}")
    
    # ایجاد و اجرای زیرسیستم اول
    main_barrier = threading.Barrier(2)
    subsystem1_tasks = parse_tasks(tasks[0], 1)
    subsystem1 = Subsystem1(resources[0], subsystem1_tasks)
    subsystem2_tasks = parse_tasks(tasks[1], 2)
    subsystem2 = Subsystem2(resources[1], subsystem2_tasks, main_barrier)
    
    #subsystem1.start()  # شروع اجرای زیرسیستم اول به صورت یک نخ
    subsystem2.start()
    time_unit = 0
    while subsystem2.is_alive() and time_unit < 20:  # تا زمانی که subsystem2 در حال اجرا هست

        print(f"\nTime Unit: {time_unit}")
        
        resources_status = subsystem2.get_resources()
        print(f"Resources: R1={resources_status['R1']}, R2={resources_status['R2']}")

        # چاپ وضعیت صف آماده‌به‌کار
        ready_queue_status = subsystem2.get_ready_queue()
        print("Ready Queue:")
        for task in ready_queue_status:
            print(task)

        cpu_tasks_status = subsystem2.get_cpu_tasks()
        print("CPU Tasks:")
        for i, task in enumerate(cpu_tasks_status):
            if task is not None:
                print(f"Core {i+1}: {task}")
            else:
                print(f"Core {i+1}: idle")
        
        main_barrier.wait()
        # افزایش زمان
        time_unit += 1
        print("yoooooooo...")
        main_barrier.wait()
        print("yooooooooooo 2")
        print(subsystem2.is_alive())

    subsystem2.join()
    #subsystem1.join()   # منتظر ماندن تا زیرسیستم اول کارش را تمام کند
