


class Task:
    def __init__(self, name, duration, required_R1, required_R2, arrival_time, 
                 destination_core=None, period=None, repetitions=None, prerequisite_task=None):
        
        self.name = name
        self.duration = duration
        self.required_R1 = required_R1
        self.required_R2 = required_R2
        self.arrival_time = arrival_time
        self.destination_core = destination_core  # فقط برای زیرسیستم اول
        self.quantum_num = None
        self.period = period  # فقط برای زیرسیستم سوم
        self.repetitions = repetitions  # فقط برای زیرسیستم سوم
        self.prerequisite_task = prerequisite_task  # فقط برای زیرسیستم چهارم
        self.state = 'R'  # وضعیت وظیفه: 'R' برای Ready, 'W' برای Waiting, 'U' برای Running

    def __str__(self):
        """تابع برای نمایش اطلاعات وظیفه به صورت رشته."""
        info = f"Task {self.name}: Duration={self.duration}, R1={self.required_R1}, R2={self.required_R2}, Arrival={self.arrival_time}"
        if self.destination_core is not None:
            info += f", Destination Core={self.destination_core}"
        if self.period is not None:
            info += f", Period={self.period}, Repetitions={self.repetitions}"
        if self.prerequisite_task is not None:
            info += f", Prerequisite={self.prerequisite_task}"
        return info

class Queue:
    def __init__(self):
        """
        تعریف کلاس Queue برای مدیریت صف وظایف.
        """
        self.tasks = []

    def enqueue(self, task):
        """
        اضافه کردن یک وظیفه به انتهای صف.
        
        پارامترها:
        - task: شیء Task که باید به صف اضافه شود.
        """
        self.tasks.append(task)

    def dequeue(self):
        """
        حذف و بازگرداندن اولین وظیفه از صف.
        
        بازگشت:
        - اولین شیء Task در صف یا None اگر صف خالی باشد.
        """
        if not self.is_empty():
            return self.tasks.pop(0)
        return None

    def is_empty(self):
        """
        بررسی خالی بودن صف.
        
        بازگشت:
        - True اگر صف خالی باشد، در غیر این صورت False.
        """
        return len(self.tasks) == 0

    def __len__(self):
        """
        بازگرداندن تعداد وظایف در صف.
        
        بازگشت:
        - تعداد وظایف در صف.
        """
        return len(self.tasks)

    def sort_by_arrival_time(self):
        """
        مرتب‌سازی صف بر اساس زمان ورود وظایف (از کم به زیاد).
        """
        self.tasks.sort(key=lambda task: task.arrival_time)

    def sort_by_remaining_time(self):
        """
        مرتب‌سازی صف بر اساس زمان باقی‌مانده وظایف (از کم به زیاد).
        """
        self.tasks.sort(key=lambda task: task.duration)

    def peek(self):
        """
        بازگرداندن اولین عنصر صف بدون حذف آن.
        
        بازگشت:
        - اولین شیء Task در صف یا None اگر صف خالی باشد.
        """
        if not self.is_empty():
            return self.tasks[0]
        return None

    
    def assign_quantum(self):
        self.sort_by_remaining_time()  # اول تسک‌ها رو بر اساس duration مرتب کن
        for index, task in enumerate(self.tasks, start=1):
            task.quantum = index  # اختصاص کوانتوم به هر تسک


    def __str__(self):
        """
        نمایش اطلاعات صف به صورت رشته.
        
        بازگشت:
        - رشته‌ای که شامل اطلاعات همه وظایف در صف است.
        """
        return "\n".join(str(task) for task in self.tasks)