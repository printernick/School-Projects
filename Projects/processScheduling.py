'''

This programs takes in a line of input from a 
file in the format of a line of ints separated
by spaces. For example:

0 4 0 2 3 1

The numbers are to be read in pairs with the 
first number being the arrival time and the second
number being the burst time. This program uses
4 different scheduling algorithms:

1. First Come, First Serve
2. Shortest Job First
3. Shortest Remaining Time First
4. Multilevel Feedback

After processing all processes using all algorithms,
outputs the average real time followed by the 
real times of each process for each algorithm. For the
above example, it would output in this format

4.66 4 6 4
4.00 6 2 4
3.33 7 2 1
4.66 7 6 1


'''

class Scheduler:
    
    class process():
            
            def __init__(self, PID, arrival_time, burst_time):
                
                self.PID = PID
                self.arrival_time = arrival_time
                self.burst_time = burst_time
            
            def __str__(self):
                
                return f'PID = {self.PID}, arrival_time = {self.arrival_time}, burst_time = {self.burst_time}'
    
    def __init__(self, arrival_times = [int], burst_times = [int]):
        self.arrival_times = arrival_times
        self.burst_times = burst_times
    
    def generate_FCFS_output(self) -> list:
        '''Return a list with the first item being average 
        turnaround time and each subsequent item being the real time
        (waiting time) of each process. 
        
        Uses a first come,first serve scheduling
        algorithm'''
        
        processes = [Scheduler.process(PID, times[0], times[1]) for PID, times in enumerate(zip(self.arrival_times, self.burst_times))]
        
        def calculate_wait_times(processes: [Scheduler.process]):
            wait_times = []
            time = 0            
            arrived = False
    
            while len(processes) != 0:
                arrived = processes[0].arrival_time <= time
#                         
                if arrived:
                    current_process = processes.pop(0)
                    wait_times.append((time - current_process.arrival_time, current_process.PID))
                    time += current_process.burst_time
                else:
                    time += 1
            
            return [wait_time for wait_time, _ in sorted(wait_times, key = lambda x: x[1])]
        
        def calculate_turnaround_time(burst_times: [int], wait_times: [int]):
            turnaround_times = [0 for _ in range(len(burst_times))]
            
            for i in range(len(turnaround_times)):
                turnaround_times[i] = burst_times[i] - wait_times[i]
            return turnaround_times
            
        
        return self.convert_output_to_str(self.format_output(self.calculate_real_times(
            self.burst_times, calculate_wait_times(processes))))
    
    def generate_SJF_output(self) -> list:
        '''Generates the same output as the
        FCFS output but uses the SJF algorithm
        to schedule each process'''
        
        processes = [Scheduler.process(i, times[0], times[1]) for i, times in enumerate(zip(self.arrival_times, self.burst_times))]
        sorted_by_burst_times = sorted(processes, key = lambda x: (x.burst_time, x.arrival_time, x.PID))
        
        
        def calculate_wait_times(sorted_processes: [Scheduler.process]) -> [int]:
                
            wait_times = []
            time = 0            
            foundOne = False
    
            while len(sorted_processes) != 0:
                for i, process in enumerate(sorted_processes):                    
                    if process.arrival_time <= time:
                        foundOne = True
                        break
                    #last process
                    elif i == len(sorted_processes) - 1:
                        foundOne = False
                        time += 1
                        
                if foundOne:
                    current_process = sorted_processes.pop(i)
                    wait_times.append((time - current_process.arrival_time, current_process.PID))
                    time += current_process.burst_time
            
            return [wait_time for wait_time, _ in sorted(wait_times, key = lambda x: x[1])]
    
        return self.convert_output_to_str(self.format_output(self.calculate_real_times(
            self.burst_times, calculate_wait_times(sorted_by_burst_times))))
    
    def generate_SRT_output(self) -> list:
        '''Shortest remaining time first algorithm.
        
        Pre-emptive shortest job first'''
        
        processes = [Scheduler.process(i, times[0], times[1]) for i, times in enumerate(zip(self.arrival_times, self.burst_times))]
        sorted_by_burst_times = sorted(processes, key = lambda x: (x.burst_time, x.arrival_time, x.PID))
        
        def calculate_wait_times(sorted_processes: [Scheduler.process]) -> [int]:
                
            wait_times = []
            time = 0
            foundOne = False
            copy = dict([(process.PID, process.burst_time) for process in sorted_processes])
            
            while len(sorted_processes) != 0:
                
                sorted_processes = sorted(sorted_processes, key = lambda x: (x.burst_time, x.arrival_time, x.PID))
                #select correct process
                for i, process in enumerate(sorted_processes):                    
                    if process.arrival_time <= time:
                        foundOne = True
                        break
                    #last process
                    elif i == len(sorted_processes) - 1:
                        foundOne = False
                        
                if foundOne:
                    sorted_processes[i].burst_time -= 1
                    if sorted_processes[i].burst_time == 0:
                        wait_times.append((time+1 - sorted_processes[i].arrival_time - copy[sorted_processes[i].PID],
                                          sorted_processes[i].PID))
                        sorted_processes.pop(i)
                
                time += 1
                
            
            return [wait_time for wait_time, _ in sorted(wait_times, key = lambda x: x[1])]
    
        return self.convert_output_to_str(self.format_output(self.calculate_real_times(
            self.burst_times, calculate_wait_times(sorted_by_burst_times))))
    
    def generate_MLF_output(self):
        '''Multilevel feedback queue scheduling algorithm'''
        
        class multi_process(Scheduler.process):
            
            def __init__(self, PID, arrival_time, burst_time):
                Scheduler.process.__init__(self, PID, arrival_time, burst_time)
                self.level = 5
                self.quantum_left = 1
                
            def __str__(self):
                return Scheduler.process.__str__(self) + f', level = {self.level}, quantum_left = {self.quantum_left}'
            
        processes = [multi_process(PID, times[0], times[1]) for PID, times in enumerate(zip(self.arrival_times, self.burst_times))]
        
        def calculate_wait_times(processes: [multi_process]):
            wait_times = []
            time = 0
            foundOne = False
            copy = dict([(process.PID, process.burst_time) for process in processes])
            
            while len(processes) != 0:
                processes = sorted(processes, key = lambda x: (-x.level, x.arrival_time, x.PID))
                for i in range(len(processes)):
                    if processes[i].arrival_time <= time:
                        foundOne = True
                        break
                    elif i == len(processes) - 1:
                        foundOne = False
                    
                if foundOne:
                    processes[i].burst_time -= 1
                    
                    popped = False
 
                    if processes[i].burst_time == 0:
                        wait_times.append((time+1 - processes[i].arrival_time - copy[processes[i].PID],
                                          processes[i].PID))
                        processes.pop(i)
                        popped = True
                    
                    if not popped:
                        processes[i].quantum_left -= 1
                        if processes[i].quantum_left == 0:
                            if processes[i].level != 1:
                                processes[i].level -= 1
                            
                            processes[i].quantum_left = 2 ** (5 - processes[i].level)
                 
                time += 1
                
            return [wait_time for wait_time, _ in sorted(wait_times, key = lambda x: x[1])]
    
        return self.convert_output_to_str(self.format_output(self.calculate_real_times(
            self.burst_times, calculate_wait_times(processes))))
    
    def calculate_real_times(self, burst_times: [int], wait_times: [int]) -> [int]:
            
        return [wait_time + burst_time for wait_time, burst_time in zip(wait_times, burst_times)]
    

    def format_output(self, real_times: [int]) -> [int]:
        
        return [round(float(sum(real_times)/len(real_times)), 2)] + real_times
    
    def convert_output_to_str(self, output: list) -> str:
        
        return ' '.join([f'{output[i]:.2f}' if i == 0 else str(output[i]) for i in range(len(output))])

if __name__ == '__main__':
    #raw_input = input().split()
    input_file = open('input.txt', 'r')
    raw_input = input_file.read().split()
    input_file.close()
    
    arrival_times = [int(arr_time) for arr_time in raw_input[:-1:2]]
    burst_times = [int(burst_time) for burst_time in raw_input[1::2]]
    
    s = Scheduler(arrival_times, burst_times)
    FCFS_output = s.generate_FCFS_output()
    SJF_output = s.generate_SJF_output()
    SRT_output = s.generate_SRT_output()
    MLF_output = s.generate_MLF_output()
    
    
    output_file = open('output.txt', "w+")
    output_file.write(FCFS_output + '\n')
    output_file.write(SJF_output + '\n')
    output_file.write(SRT_output + '\n')
    output_file.write(MLF_output + '\n')
    
    output_file.close()
