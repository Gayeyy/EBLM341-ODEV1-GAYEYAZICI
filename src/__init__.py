

# Paket versiyonu
__version__ = "1.0"
__author__ = "CPU Zamanlama Projesi"
__description__ = "CPU Zamanlama Algoritmaları Simülatörü"

# Ana modülleri import et
from .process import Process, Priority, TimeSlot, SchedulingResult
from .csv_parser import parse_csv_file, validate_csv_structure
from .scheduling_algorithms import SchedulingAlgorithm
from .result_generator import ResultGenerator

# Paket seviyesinde kullanılabilecek fonksiyonlar
__all__ = [
    'Process',
    'Priority', 
    'TimeSlot',
    'SchedulingResult',
    'parse_csv_file',
    'validate_csv_structure',
    'SchedulingAlgorithm',
    'ResultGenerator'
]
