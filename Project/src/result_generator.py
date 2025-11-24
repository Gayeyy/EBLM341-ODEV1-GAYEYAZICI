import os
from typing import Dict, Any
from .process import SchedulingResult

class ResultGenerator:
    def __init__(self, results_dir: str = "results"):
        self.results_dir = results_dir
        os.makedirs(results_dir, exist_ok=True)
    
    def generate_result_file(self, result: SchedulingResult, case_name: str) -> str:
        filename = f"{case_name}_{result.algorithm_name.replace(' ', '_').replace('-', '_').lower()}_sonuclari.txt"
        filepath = os.path.join(self.results_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write(f"CPU Zamanlama Algoritması: {result.algorithm_name}\n")
            f.write(f"Senaryo: {case_name}\n")
            f.write("=" * 80 + "\n\n")
            
            metrics = result.calculate_metrics()
            
            if metrics:
                self._write_performance_metrics(f, metrics)
                self._write_throughput_metrics(f, metrics)
            
            self._write_time_table(f, result.time_slots)
            
            if metrics:
                self._write_summary_statistics(f, metrics)
        
        return filepath
    
    def _write_performance_metrics(self, f, metrics: Dict[str, Any]):
        f.write("PERFORMANS METRİKLERİ\n")
        f.write("-" * 40 + "\n")
        f.write(f"Maksimum Bekleme Süresi: {metrics['max_waiting_time']:.3f} birim\n")
        f.write(f"Ortalama Bekleme Süresi: {metrics['avg_waiting_time']:.3f} birim\n")
        f.write(f"Maksimum Tamamlanma Süresi: {metrics['max_turnaround_time']:.3f} birim\n")
        f.write(f"Ortalama Tamamlanma Süresi: {metrics['avg_turnaround_time']:.3f} birim\n")
        f.write(f"Ortalama CPU Verimliliği: {metrics['cpu_efficiency']:.2f}%\n")
        f.write(f"Toplam Bağlam Değiştirme: {metrics['context_switches']}\n")
        f.write("\n")
    
    def _write_throughput_metrics(self, f, metrics: Dict[str, Any]):
        f.write("THROUGHPUT METRİKLERİ\n")
        f.write("-" * 40 + "\n")
        f.write(f"T=50'de tamamlanan süreçler: {metrics['throughput_50']}\n")
        f.write(f"T=100'de tamamlanan süreçler: {metrics['throughput_100']}\n")
        f.write(f"T=150'de tamamlanan süreçler: {metrics['throughput_150']}\n")
        f.write(f"T=200'de tamamlanan süreçler: {metrics['throughput_200']}\n")
        f.write("\n")
    
    def _write_time_table(self, f, time_slots):
        f.write("ZAMAN ÇİZELGESİ\n")
        f.write("-" * 80 + "\n")
        f.write("Süreç yürütme zaman çizelgesini gösteren zaman aralıkları:\n")
        f.write("\n")
        
        for slot in time_slots:
            if slot.process_id == "IDLE":
                f.write(f"[ {int(slot.start_time):4d} ] - - BOŞTA - - [ {int(slot.end_time):4d} ]\n")
            else:
                f.write(f"[ {int(slot.start_time):4d} ] - - {slot.process_id} - - [ {int(slot.end_time):4d} ]\n")
        
        f.write("\n")
    
    def _write_summary_statistics(self, f, metrics: Dict[str, Any]):
        f.write("ÖZET İSTATİSTİKLER\n")
        f.write("-" * 40 + "\n")
        f.write(f"Bağlam Değiştirme Gecikmesi: {metrics['context_switches'] * 0.001:.6f} zaman birimi\n")
        f.write(f"CPU Kullanımı: {metrics['cpu_efficiency']:.2f}%\n")
        f.write("Genel Performans: ")
        
        if metrics['avg_waiting_time'] < 5:
            f.write("MÜKEMMEL (Düşük bekleme süreleri)\n")
        elif metrics['avg_waiting_time'] < 15:
            f.write("İYİ (Orta bekleme süreleri)\n")
        elif metrics['avg_waiting_time'] < 30:
            f.write("ORTA (Yüksek bekleme süreleri)\n")
        else:
            f.write("ZAYIF (Çok yüksek bekleme süreleri)\n")
        
        f.write("\n")
    
    def generate_comparison_report(self, results: Dict[str, SchedulingResult], case_name: str) -> str:
        filename = f"{case_name}_karsilastirma_raporu.txt"
        filepath = os.path.join(self.results_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("=" * 100 + "\n")
            f.write(f"CPU ZAMANLAMA ALGORİTMALARI KARŞILAŞTIRMA RAPORU\n")
            f.write(f"Senaryo: {case_name}\n")
            f.write("=" * 100 + "\n\n")
            
            self._write_comparison_table(f, results)
            self._write_algorithm_rankings(f, results)
        
        return filepath
    
    def _write_comparison_table(self, f, results: Dict[str, SchedulingResult]):
        f.write("KARŞILAŞTIRMA TABLOSU\n")
        f.write("-" * 140 + "\n")
        f.write(f"{'Algoritma':<25} {'Ort Bek':<12} {'Max Bek':<12} {'Ort Tam':<12} {'Max Tam':<12} {'CPU Ver%':<10} {'Bğm Dğş':<8} {'Thr@100':<8}\n")
        f.write("-" * 140 + "\n")
        
        for algorithm_name, result in results.items():
            metrics = result.calculate_metrics()
            if metrics:
                f.write(f"{algorithm_name:<25} ")
                f.write(f"{metrics['avg_waiting_time']:<12.3f} ")
                f.write(f"{metrics['max_waiting_time']:<12.3f} ")
                f.write(f"{metrics['avg_turnaround_time']:<12.3f} ")
                f.write(f"{metrics['max_turnaround_time']:<12.3f} ")
                f.write(f"{metrics['cpu_efficiency']:<10.2f} ")
                f.write(f"{metrics['context_switches']:<8} ")
                f.write(f"{metrics['throughput_100']:<8}\n")
        
        f.write("\n")
    
    def _write_algorithm_rankings(self, f, results: Dict[str, SchedulingResult]):
        f.write("METRİKLERE GÖRE ALGORİTMA SIRALAMALARI\n")
        f.write("=" * 40 + "\n\n")
        
        metrics_data = {}
        for algorithm_name, result in results.items():
            metrics = result.calculate_metrics()
            if metrics:
                metrics_data[algorithm_name] = metrics
        
        if metrics_data:
            f.write("1. Ortalama Bekleme Süresine Göre (düşük daha iyi):\n")
            sorted_by_wait = sorted(metrics_data.items(), key=lambda x: x[1]['avg_waiting_time'])
            for i, (alg, metrics) in enumerate(sorted_by_wait, 1):
                f.write(f"   {i}. {alg}: {metrics['avg_waiting_time']:.3f}\n")
            f.write("\n")
            
            f.write("2. Ortalama Tamamlanma Süresine Göre (düşük daha iyi):\n")
            sorted_by_turnaround = sorted(metrics_data.items(), key=lambda x: x[1]['avg_turnaround_time'])
            for i, (alg, metrics) in enumerate(sorted_by_turnaround, 1):
                f.write(f"   {i}. {alg}: {metrics['avg_turnaround_time']:.3f}\n")
            f.write("\n")
            
            f.write("3. CPU Verimliliğine Göre (yüksek daha iyi):\n")
            sorted_by_efficiency = sorted(metrics_data.items(), key=lambda x: x[1]['cpu_efficiency'], reverse=True)
            for i, (alg, metrics) in enumerate(sorted_by_efficiency, 1):
                f.write(f"   {i}. {alg}: {metrics['cpu_efficiency']:.2f}%\n")
            f.write("\n")
            
            f.write("4. T=100'de Throughput'a Göre (yüksek daha iyi):\n")
            sorted_by_throughput = sorted(metrics_data.items(), key=lambda x: x[1]['throughput_100'], reverse=True)
            for i, (alg, metrics) in enumerate(sorted_by_throughput, 1):
                f.write(f"   {i}. {alg}: {metrics['throughput_100']}\n")
            f.write("\n")