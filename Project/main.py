#!/usr/bin/env python3
import os
import sys
import argparse
import time
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor, as_completed

from src.csv_parser import parse_csv_file, validate_csv_structure
from src.scheduling_algorithms import SchedulingAlgorithm
from src.result_generator import ResultGenerator

class CPUSchedulingSimulator:
    def __init__(self, context_switch_time=0.001):
        self.scheduler = SchedulingAlgorithm(context_switch_time)
        self.result_generator = ResultGenerator()
    
    def run_all_algorithms(self, processes: List, case_name: str) -> Dict[str, object]:
        print(f"\n{case_name} için tüm zamanlama algoritmaları çalıştırılıyor...")
        
        results = {}
        
        algorithms = [
            ("FCFS", lambda p: self.scheduler.schedule_fcfs(p)),
            ("Preemptive SJF", lambda p: self.scheduler.schedule_preemptive_sjf(p)),
            ("Non-Preemptive SJF", lambda p: self.scheduler.schedule_non_preemptive_sjf(p)),
            ("Round Robin", lambda p: self.scheduler.schedule_round_robin(p, time_quantum=2)),
            ("Preemptive Priority", lambda p: self.scheduler.schedule_preemptive_priority(p)),
            ("Non-Preemptive Priority", lambda p: self.scheduler.schedule_non_preemptive_priority(p))
        ]
        
        for algorithm_name, algorithm_func in algorithms:
            print(f"  {algorithm_name} çalıştırılıyor...", end=" ", flush=True)
            start_time = time.time()
            
            fresh_processes = [self._deep_copy_process(p) for p in processes]
            result = algorithm_func(fresh_processes)
            
            execution_time = time.time() - start_time
            print(f"Tamamlandı ({execution_time:.3f}s)")
            
            results[algorithm_name] = result
            
            result_file = self.result_generator.generate_result_file(result, case_name)
            print(f"    Sonuçlar kaydedildi: {result_file}")
        
        comparison_file = self.result_generator.generate_comparison_report(results, case_name)
        print(f"  Karşılaştırma raporu kaydedildi: {comparison_file}")
        
        return results
    
    def _deep_copy_process(self, process):
        from src.process import Process, Priority
        
        return Process(
            process_id=process.process_id,
            arrival_time=process.arrival_time,
            cpu_burst_time=process.cpu_burst_time,
            priority=process.priority
        )
    
    def run_with_threading(self, file_paths: List[str]) -> Dict[str, Dict[str, object]]:
        print("Multi-threading ile çalıştırılıyor (bonus özellik)...")
        
        results = {}
        
        with ThreadPoolExecutor(max_workers=len(file_paths)) as executor:
            future_to_case = {
                executor.submit(self._process_case, file_path): self._extract_case_name(file_path)
                for file_path in file_paths
            }
            
            for future in as_completed(future_to_case):
                case_name = future_to_case[future]
                try:
                    case_results = future.result()
                    results[case_name] = case_results
                    print(f"{case_name} tamamlandı")
                except Exception as exc:
                    print(f"{case_name} senaryosu istisna oluşturdu: {exc}")
        
        return results
    
    def _process_case(self, file_path: str) -> Dict[str, object]:
        case_name = self._extract_case_name(file_path)
        
        if not validate_csv_structure(file_path):
            raise ValueError(f"{file_path} içinde geçersiz CSV yapısı")
        
        processes = parse_csv_file(file_path)
        print(f"\n{case_name} senaryosundan {len(processes)} süreç yüklendi")
        
        return self.run_all_algorithms(processes, case_name)
    
    def _extract_case_name(self, file_path: str) -> str:
        filename = os.path.basename(file_path)
        case_name = filename.replace('.csv', '').replace('.txt', '')
        return case_name
    
    def run_single_case(self, file_path: str):
        case_name = self._extract_case_name(file_path)
        
        print(f"CPU Zamanlama Simülatörü")
        print(f"Dosya işleniyor: {file_path}")
        
        if not validate_csv_structure(file_path):
            print(f"Hata: {file_path} içinde geçersiz CSV yapısı")
            return
        
        processes = parse_csv_file(file_path)
        print(f"{len(processes)} süreç yüklendi")
        
        self.run_all_algorithms(processes, case_name)
        
        print(f"\n{case_name} için tüm sonuçlar oluşturuldu")
        print(f"Detaylı raporlar için 'results' klasörünü kontrol edin.")
    
    def run_both_cases(self, use_threading=False):
        data_dir = "data"
        case1_path = os.path.join(data_dir, "case1.csv")
        case2_path = os.path.join(data_dir, "case2.csv")
        
        if not os.path.exists(case1_path) or not os.path.exists(case2_path):
            print("Hata: data klasöründe case1.csv veya case2.csv bulunamadı")
            return
        
        print("CPU Zamanlama Simülatörü")
        print("Her iki test senaryosu işleniyor...")
        
        if use_threading:
            results = self.run_with_threading([case1_path, case2_path])
        else:
            results = {}
            
            for file_path in [case1_path, case2_path]:
                case_name = self._extract_case_name(file_path)
                results[case_name] = self._process_case(file_path)
        
        self._generate_final_summary(results)
        
        print("\n" + "="*60)
        print("SİMÜLASYON BAŞARILIYLA TAMAMLANDI!")
        print("="*60)
        print("Oluşturulan dosyalar:")
        print("  - Her senaryo için bireysel algoritma sonuçları")
        print("  - Her senaryo için karşılaştırma raporları")
        print("  - Genel özet raporu")
        print(f"  Sonuçlar klasörü: {os.path.abspath('results')}")
    
    def _generate_final_summary(self, results: Dict[str, Dict[str, object]]):
        summary_file = os.path.join("results", "genel_ozet.txt")
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write("CPU ZAMANLAMA ALGORİTMALARI - GENEL ÖZET RAPORU\n")
            f.write("="*80 + "\n\n")
            
            for case_name, case_results in results.items():
                f.write(f"SENARYO: {case_name.upper()}\n")
                f.write("-"*40 + "\n")
                
                metrics_data = {}
                for algorithm_name, result in case_results.items():
                    metrics = result.calculate_metrics()
                    if metrics:
                        metrics_data[algorithm_name] = metrics
                
                if metrics_data:
                    f.write("En iyi performans gösteren algoritmalar:\n")
                    
                    best_wait = min(metrics_data.items(), key=lambda x: x[1]['avg_waiting_time'])
                    f.write(f"  En Düşük Ortalama Bekleme Süresi: {best_wait[0]} ({best_wait[1]['avg_waiting_time']:.3f})\n")
                    
                    best_turnaround = min(metrics_data.items(), key=lambda x: x[1]['avg_turnaround_time'])
                    f.write(f"  En Düşük Ortalama Tamamlanma Süresi: {best_turnaround[0]} ({best_turnaround[1]['avg_turnaround_time']:.3f})\n")
                    
                    best_efficiency = max(metrics_data.items(), key=lambda x: x[1]['cpu_efficiency'])
                    f.write(f"  En Yüksek CPU Verimliliği: {best_efficiency[0]} ({best_efficiency[1]['cpu_efficiency']:.2f}%)\n")
                    
                    best_throughput = max(metrics_data.items(), key=lambda x: x[1]['throughput_100'])
                    f.write(f"  T=100'de En Yüksek Throughput: {best_throughput[0]} ({best_throughput[1]['throughput_100']} süreç)\n")
                
                f.write("\n")
        
        print(f"Genel özet kaydedildi: {summary_file}")

def main():
    parser = argparse.ArgumentParser(description="CPU Zamanlama Algoritmaları Simülatörü")
    parser.add_argument("--file", "-f", type=str, help="Süreç verilerini içeren CSV dosyasının yolu")
    parser.add_argument("--both", "-b", action="store_true", help="Her iki test senaryosunu çalıştır (case1.csv ve case2.csv)")
    parser.add_argument("--threading", "-t", action="store_true", help="Paralel çalıştırma için multi-threading kullan")
    parser.add_argument("--context-switch", "-c", type=float, default=0.001, 
                       help="Zaman birimi cinsinden bağlam değiştirme süresi (varsayılan: 0.001)")
    
    args = parser.parse_args()
    
    simulator = CPUSchedulingSimulator(args.context_switch)
    
    try:
        if args.both:
            simulator.run_both_cases(use_threading=args.threading)
        elif args.file:
            if not os.path.exists(args.file):
                print(f"Hata: Dosya '{args.file}' bulunamadı")
                sys.exit(1)
            simulator.run_single_case(args.file)
        else:
            print("CPU Zamanlama Simülatörü")
            print("Kullanım örnekleri:")
            print("  python main.py --both                    # Her iki test senaryosunu çalıştır")
            print("  python main.py --both --threading        # Threading ile her iki senaryoyu çalıştır")
            print("  python main.py --file data/case1.csv     # Özel dosya çalıştır")
            print("  python main.py --file benim_sureclerim.csv   # Özel süreç dosyası çalıştır")
            print("\nDaha fazla seçenek için --help kullanın")
            
            choice = input("\nHer iki test senaryosunu çalıştırmak ister misiniz? (e/h): ").lower().strip()
            if choice in ['e', 'evet']:
                threading_choice = input("Daha hızlı çalıştırma için multi-threading kullanılsın mı? (e/h): ").lower().strip()
                use_threading = threading_choice in ['e', 'evet']
                simulator.run_both_cases(use_threading=use_threading)
    
    except KeyboardInterrupt:
        print("\n\nSimülasyon kullanıcı tarafından durduruldu")
        sys.exit(1)
    except Exception as e:
        print(f"\nSimülasyon sırasında hata: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()