import time

class Timer:
    def __init__(self, time_between=5):
        self.start_time = time.time()
        self.time_between = time_between

    def can_send(self):
        if time.time() > (self.start_time + self.time_between):
            self.start_time = time.time()
            return True
        return False

def progress_bar_str(done, total):
    percent = round(done/total*100, 2)
    strin = "░░░░░░░░░░"
    strin = list(strin)
    for i in range(round(percent)//10):
        strin[i] = "█"
    strin = "".join(strin)
    final = f"Percent: {percent}%\n{human_readable_size(done)}/{human_readable_size(total)}\n{strin}"
    return final 

def human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if size < 1024.0 or unit == 'PB':
            break
        size /= 1024.0
    return f"{size:.{decimal_places}f} {unit}"