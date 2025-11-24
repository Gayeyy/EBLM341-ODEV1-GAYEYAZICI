import csv
from typing import List
from .process import Process, Priority

def parse_csv_file(file_path: str) -> List[Process]:
    processes = []
    
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                process = Process(
                    process_id=row['Process_ID'].strip(),
                    arrival_time=float(row['Arrival_Time']),
                    cpu_burst_time=float(row['CPU_Burst_Time']),
                    priority=row['Priority'].strip()
                )
                processes.append(process)
                
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV dosyası bulunamadı: {file_path}")
    except KeyError as e:
        raise KeyError(f"CSV'de eksik required sütun: {e}")
    except ValueError as e:
        raise ValueError(f"CSV'de geçersiz veri formatı: {e}")
    
    return sorted(processes, key=lambda p: p.arrival_time)

def validate_csv_structure(file_path: str) -> bool:
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            required_columns = ['Process_ID', 'Arrival_Time', 'CPU_Burst_Time', 'Priority']
            
            if not all(col in reader.fieldnames for col in required_columns):
                return False
                
            for i, row in enumerate(reader, 1):
                if not row['Process_ID'].strip():
                    print(f"Uyarı: {i}. satırda boş Process_ID")
                    continue
                    
                try:
                    float(row['Arrival_Time'])
                    float(row['CPU_Burst_Time'])
                    priority = row['Priority'].strip().upper()
                    if priority not in ['HIGH', 'NORMAL', 'LOW']:
                        print(f"Uyarı: {i}. satırda geçersiz öncelik '{priority}'")
                except ValueError as e:
                    print(f"Uyarı: {i}. satırda geçersiz sayı formatı: {e}")
                    continue
                    
        return True
        
    except Exception as e:
        print(f"CSV doğrulanırken hata: {e}")
        return False