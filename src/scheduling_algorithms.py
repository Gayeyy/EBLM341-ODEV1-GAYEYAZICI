from typing import List
from .process import Process, TimeSlot, SchedulingResult

class SchedulingAlgorithm:
    def __init__(self, context_switch_time=0.001):
        self.context_switch_time = context_switch_time
    
    def schedule_fcfs(self, processes: List[Process]) -> SchedulingResult:
        if not processes:
            return SchedulingResult("FCFS", [], processes, 0, 0)
        
        time_slots = []
        current_time = 0
        context_switches = 0
        completed_processes = []
        
        ready_queue = []
        process_index = 0
        
        while len(completed_processes) < len(processes):
            arrived_processes = [p for p in processes[process_index:] 
                               if p.arrival_time <= current_time]
            ready_queue.extend(arrived_processes)
            process_index += len(arrived_processes)
            
            if ready_queue:
                current_process = ready_queue.pop(0)
                
                if current_process.start_time is None:
                    current_process.start_time = current_time
                
                start_time = current_time
                end_time = current_time + current_process.cpu_burst_time
                
                time_slot = TimeSlot(
                    process_id=current_process.process_id,
                    start_time=start_time,
                    end_time=end_time
                )
                time_slots.append(time_slot)
                
                current_time = end_time
                current_process.completion_time = current_time
                current_process.remaining_time = 0
                completed_processes.append(current_process)
                
                if len(completed_processes) < len(processes):
                    current_time += self.context_switch_time
                    context_switches += 1
            else:
                next_process = next((p for p in processes[process_index:] 
                                   if p.arrival_time > current_time), None)
                
                if next_process:
                    idle_slot = TimeSlot(
                        process_id="IDLE",
                        start_time=current_time,
                        end_time=next_process.arrival_time
                    )
                    time_slots.append(idle_slot)
                    current_time = next_process.arrival_time
                else:
                    break
        
        return SchedulingResult(
            algorithm_name="FCFS",
            time_slots=time_slots,
            processes=processes,
            context_switches=context_switches,
            total_time=current_time
        )
    
    def schedule_preemptive_sjf(self, processes: List[Process]) -> SchedulingResult:
        if not processes:
            return SchedulingResult("Preemptive SJF", [], processes, 0, 0)
        
        for process in processes:
            process.reset()
        
        time_slots = []
        current_time = 0
        context_switches = 0
        completed_processes = []
        current_process = None
        
        while len(completed_processes) < len(processes):
            ready_processes = [p for p in processes 
                             if p.arrival_time <= current_time and p not in completed_processes 
                             and p.remaining_time > 0]
            
            if ready_processes:
                ready_processes.sort(key=lambda p: p.remaining_time)
                next_process = ready_processes[0]
                
                if current_process != next_process:
                    if current_process is not None and current_process.remaining_time > 0:
                        context_switches += 1
                        current_time += self.context_switch_time
                    
                    if next_process.start_time is None:
                        next_process.start_time = current_time
                    
                    current_process = next_process
                
                execution_time = min(1, current_process.remaining_time)
                start_time = current_time
                current_time += execution_time
                current_process.remaining_time -= execution_time
                
                time_slot = TimeSlot(
                    process_id=current_process.process_id,
                    start_time=start_time,
                    end_time=current_time
                )
                time_slots.append(time_slot)
                
                if current_process.remaining_time == 0:
                    current_process.completion_time = current_time
                    completed_processes.append(current_process)
                    current_process = None
            else:
                next_arrival = min([p.arrival_time for p in processes 
                                  if p not in completed_processes])
                
                idle_slot = TimeSlot(
                    process_id="IDLE",
                    start_time=current_time,
                    end_time=next_arrival
                )
                time_slots.append(idle_slot)
                current_time = next_arrival
        
        return SchedulingResult(
            algorithm_name="Preemptive SJF",
            time_slots=time_slots,
            processes=processes,
            context_switches=context_switches,
            total_time=current_time
        )
    
    def schedule_non_preemptive_sjf(self, processes: List[Process]) -> SchedulingResult:
        if not processes:
            return SchedulingResult("Non-Preemptive SJF", [], processes, 0, 0)
        
        for process in processes:
            process.reset()
        
        time_slots = []
        current_time = 0
        context_switches = 0
        completed_processes = []
        
        while len(completed_processes) < len(processes):
            ready_processes = [p for p in processes 
                             if p.arrival_time <= current_time and p not in completed_processes 
                             and p.remaining_time > 0]
            
            if ready_processes:
                ready_processes.sort(key=lambda p: (p.cpu_burst_time, p.arrival_time))
                current_process = ready_processes[0]
                
                if current_process.start_time is None:
                    current_process.start_time = current_time
                
                start_time = current_time
                end_time = current_time + current_process.cpu_burst_time
                
                time_slot = TimeSlot(
                    process_id=current_process.process_id,
                    start_time=start_time,
                    end_time=end_time
                )
                time_slots.append(time_slot)
                
                current_time = end_time
                current_process.completion_time = current_time
                current_process.remaining_time = 0
                completed_processes.append(current_process)
                
                if len(completed_processes) < len(processes):
                    current_time += self.context_switch_time
                    context_switches += 1
            else:
                next_arrival = min([p.arrival_time for p in processes 
                                  if p not in completed_processes])
                
                idle_slot = TimeSlot(
                    process_id="IDLE",
                    start_time=current_time,
                    end_time=next_arrival
                )
                time_slots.append(idle_slot)
                current_time = next_arrival
        
        return SchedulingResult(
            algorithm_name="Non-Preemptive SJF",
            time_slots=time_slots,
            processes=processes,
            context_switches=context_switches,
            total_time=current_time
        )
    
    def schedule_round_robin(self, processes: List[Process], time_quantum: int = 2) -> SchedulingResult:
        if not processes:
            return SchedulingResult("Round Robin", [], processes, 0, 0)
        
        for process in processes:
            process.reset()
        
        time_slots = []
        current_time = 0
        context_switches = 0
        completed_processes = []
        ready_queue = []
        process_index = 0
        
        while len(completed_processes) < len(processes):
            arrived_processes = [p for p in processes[process_index:] 
                               if p.arrival_time <= current_time and p not in ready_queue 
                               and p not in completed_processes]
            ready_queue.extend(arrived_processes)
            process_index += len(arrived_processes)
            
            if ready_queue:
                current_process = ready_queue.pop(0)
                
                if current_process.start_time is None:
                    current_process.start_time = current_time
                
                execution_time = min(time_quantum, current_process.remaining_time)
                start_time = current_time
                current_time += execution_time
                current_process.remaining_time -= execution_time
                
                time_slot = TimeSlot(
                    process_id=current_process.process_id,
                    start_time=start_time,
                    end_time=current_time
                )
                time_slots.append(time_slot)
                
                if current_process.remaining_time == 0:
                    current_process.completion_time = current_time
                    completed_processes.append(current_process)
                else:
                    newly_arrived = [p for p in processes[process_index:] 
                                   if p.arrival_time <= current_time and p not in ready_queue 
                                   and p not in completed_processes]
                    ready_queue.extend(newly_arrived)
                    process_index += len(newly_arrived)
                    ready_queue.append(current_process)
                
                current_time += self.context_switch_time
                context_switches += 1
            else:
                next_process = next((p for p in processes[process_index:] 
                                   if p.arrival_time > current_time), None)
                
                if next_process:
                    idle_slot = TimeSlot(
                        process_id="IDLE",
                        start_time=current_time,
                        end_time=next_process.arrival_time
                    )
                    time_slots.append(idle_slot)
                    current_time = next_process.arrival_time
                else:
                    break
        
        return SchedulingResult(
            algorithm_name="Round Robin",
            time_slots=time_slots,
            processes=processes,
            context_switches=context_switches,
            total_time=current_time
        )
    
    def schedule_preemptive_priority(self, processes: List[Process]) -> SchedulingResult:
        if not processes:
            return SchedulingResult("Preemptive Priority", [], processes, 0, 0)
        
        for process in processes:
            process.reset()
        
        time_slots = []
        current_time = 0
        context_switches = 0
        completed_processes = []
        current_process = None
        
        while len(completed_processes) < len(processes):
            ready_processes = [p for p in processes 
                             if p.arrival_time <= current_time and p not in completed_processes 
                             and p.remaining_time > 0]
            
            if ready_processes:
                ready_processes.sort(key=lambda p: (-p.priority.value, p.arrival_time))
                next_process = ready_processes[0]
                
                if current_process != next_process:
                    if current_process is not None and current_process.remaining_time > 0:
                        context_switches += 1
                        current_time += self.context_switch_time
                    
                    if next_process.start_time is None:
                        next_process.start_time = current_time
                    
                    current_process = next_process
                
                execution_time = min(1, current_process.remaining_time)
                start_time = current_time
                current_time += execution_time
                current_process.remaining_time -= execution_time
                
                time_slot = TimeSlot(
                    process_id=current_process.process_id,
                    start_time=start_time,
                    end_time=current_time
                )
                time_slots.append(time_slot)
                
                if current_process.remaining_time == 0:
                    current_process.completion_time = current_time
                    completed_processes.append(current_process)
                    current_process = None
            else:
                next_arrival = min([p.arrival_time for p in processes 
                                  if p not in completed_processes])
                
                idle_slot = TimeSlot(
                    process_id="IDLE",
                    start_time=current_time,
                    end_time=next_arrival
                )
                time_slots.append(idle_slot)
                current_time = next_arrival
        
        return SchedulingResult(
            algorithm_name="Preemptive Priority",
            time_slots=time_slots,
            processes=processes,
            context_switches=context_switches,
            total_time=current_time
        )
    
    def schedule_non_preemptive_priority(self, processes: List[Process]) -> SchedulingResult:
        if not processes:
            return SchedulingResult("Non-Preemptive Priority", [], processes, 0, 0)
        
        for process in processes:
            process.reset()
        
        time_slots = []
        current_time = 0
        context_switches = 0
        completed_processes = []
        
        while len(completed_processes) < len(processes):
            ready_processes = [p for p in processes 
                             if p.arrival_time <= current_time and p not in completed_processes 
                             and p.remaining_time > 0]
            
            if ready_processes:
                ready_processes.sort(key=lambda p: (-p.priority.value, p.arrival_time))
                current_process = ready_processes[0]
                
                if current_process.start_time is None:
                    current_process.start_time = current_time
                
                start_time = current_time
                end_time = current_time + current_process.cpu_burst_time
                
                time_slot = TimeSlot(
                    process_id=current_process.process_id,
                    start_time=start_time,
                    end_time=end_time
                )
                time_slots.append(time_slot)
                
                current_time = end_time
                current_process.completion_time = current_time
                current_process.remaining_time = 0
                completed_processes.append(current_process)
                
                if len(completed_processes) < len(processes):
                    current_time += self.context_switch_time
                    context_switches += 1
            else:
                next_arrival = min([p.arrival_time for p in processes 
                                  if p not in completed_processes])
                
                idle_slot = TimeSlot(
                    process_id="IDLE",
                    start_time=current_time,
                    end_time=next_arrival
                )
                time_slots.append(idle_slot)
                current_time = next_arrival
        
        return SchedulingResult(
            algorithm_name="Non-Preemptive Priority",
            time_slots=time_slots,
            processes=processes,
            context_switches=context_switches,
            total_time=current_time
        )