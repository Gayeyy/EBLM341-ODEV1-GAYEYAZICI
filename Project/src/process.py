from dataclasses import dataclass
from typing import Optional
from enum import Enum

class Priority(Enum):
    HIGH = 3
    NORMAL = 2
    LOW = 1

@dataclass
class Process:
    process_id: str
    arrival_time: float
    cpu_burst_time: float
    priority: Priority
    remaining_time: float = None
    start_time: float = None
    completion_time: float = None
    turnaround_time: float = None
    waiting_time: float = None
    response_time: float = None
    
    def __post_init__(self):
        if self.remaining_time is None:
            self.remaining_time = self.cpu_burst_time
        if isinstance(self.priority, str):
            self.priority = Priority[self.priority.upper()]
    
    def reset(self):
        self.remaining_time = self.cpu_burst_time
        self.start_time = None
        self.completion_time = None
        self.turnaround_time = None
        self.waiting_time = None
        self.response_time = None

@dataclass
class TimeSlot:
    process_id: str
    start_time: float
    end_time: float
    
    def __post_init__(self):
        self.duration = self.end_time - self.start_time

@dataclass
class SchedulingResult:
    algorithm_name: str
    time_slots: list[TimeSlot]
    processes: list[Process]
    context_switches: int = 0
    total_time: float = 0
    
    def calculate_metrics(self):
        if not self.processes:
            return None
        
        waiting_times = []
        turnaround_times = []
        
        for process in self.processes:
            if process.completion_time is not None:
                process.turnaround_time = process.completion_time - process.arrival_time
                process.waiting_time = process.turnaround_time - process.cpu_burst_time
                
                waiting_times.append(process.waiting_time)
                turnaround_times.append(process.turnaround_time)
        
        if not waiting_times:
            return None
            
        avg_waiting_time = sum(waiting_times) / len(waiting_times)
        max_waiting_time = max(waiting_times)
        avg_turnaround_time = sum(turnaround_times) / len(turnaround_times)
        max_turnaround_time = max(turnaround_times)
        
        busy_time = sum(slot.duration for slot in self.time_slots 
                       if slot.process_id != "IDLE")
        cpu_efficiency = (busy_time / self.total_time * 100) if self.total_time > 0 else 0
        
        throughput_50 = sum(1 for p in self.processes 
                          if p.completion_time and p.completion_time <= 50)
        throughput_100 = sum(1 for p in self.processes 
                           if p.completion_time and p.completion_time <= 100)
        throughput_150 = sum(1 for p in self.processes 
                           if p.completion_time and p.completion_time <= 150)
        throughput_200 = sum(1 for p in self.processes 
                           if p.completion_time and p.completion_time <= 200)
        
        return {
            'avg_waiting_time': avg_waiting_time,
            'max_waiting_time': max_waiting_time,
            'avg_turnaround_time': avg_turnaround_time,
            'max_turnaround_time': max_turnaround_time,
            'cpu_efficiency': cpu_efficiency,
            'context_switches': self.context_switches,
            'throughput_50': throughput_50,
            'throughput_100': throughput_100,
            'throughput_150': throughput_150,
            'throughput_200': throughput_200
        }