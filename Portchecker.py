import sys
import socket
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit, QProgressBar, QMessageBox
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
import csv
import threading

aktive_threads = 0

class ScanThread(QThread):
    update_progress_signal = pyqtSignal()
    add_result_signal = pyqtSignal(str, str, int)  # IP, Hostname, Port
    scan_complete_signal = pyqtSignal()

    def __init__(self, ip, port, parent=None):
        super(ScanThread, self).__init__(parent)
        self.ip = ip
        self.port = port

    def run(self):
        global aktive_threads
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex((self.ip, self.port))
            if result == 0:
                host_name = "Unbekannter Host"
                try:
                    host_name, _, _ = socket.gethostbyaddr(self.ip)
                except Exception:
                    pass
                self.add_result_signal.emit(self.ip, host_name, self.port)
            s.close()
        except Exception as e:
            self.add_result_signal.emit(self.ip, "Fehler", self.port)
        finally:
            self.update_progress_signal.emit()
            with threading.Lock():
                aktive_threads -= 1
                if aktive_threads == 0:
                    self.scan_complete_signal.emit()

class IPScanner(QMainWindow):
    def __init__(self):
        super().__init__()
        self.offene_ports = {}
        self.setup_ui()
        self.datei_nummer = 1

    def setup_ui(self):
        self.setWindowTitle("PortChecker")
        self.setGeometry(100, 100, 550, 600)

        self.label = QLabel("Gib eine Range an (z.B. 192.168.1.1-255)", self)
        self.label.move(20, 20)
        self.label.resize(400, 20)

        self.ip_input = QLineEdit(self)
        self.ip_input.setGeometry(20, 50, 460, 30)

        self.default_btn = QPushButton("MyNet", self)
        self.default_btn.setGeometry(380, 100, 100, 30)
        self.default_btn.clicked.connect(self.set_default_ip)

        self.btn = QPushButton("Check", self)
        self.btn.setGeometry(20, 100, 100, 30)
        self.btn.clicked.connect(self.scan_starten)

        self.result_area = QTextEdit(self)
        self.result_area.setGeometry(20, 140, 460, 350)
        self.result_area.setReadOnly(True)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(20, 500, 500, 30)

        self.export_btn = QPushButton("Ergebnisse als CSV", self)
        self.export_btn.setGeometry(20, 540, 150, 30)
        self.export_btn.clicked.connect(self.exportiere_ergebnisse_als_csv)


    @pyqtSlot()
    def scan_starten(self):
        global aktive_threads
        ip_basis, ip_ende = self.ip_input.text().split('-')
        start_ip = ip_basis
        end_ip = '.'.join(ip_basis.split('.')[:-1] + [ip_ende])
        start_ip_list = [int(x) for x in start_ip.split('.')]
        end_ip_list = [int(x) for x in end_ip.split('.')]
        self.total_ports = 0
        for i in range(start_ip_list[3], end_ip_list[3] + 1):
            self.total_ports += 2000
        aktive_threads = self.total_ports
        self.progress_bar.setMaximum(self.total_ports)
        self.scan_ip_range(start_ip, end_ip)

    def scan_ip_range(self, start_ip, end_ip):
        global aktive_threads
        start_list = start_ip.split('.')
        end_list = end_ip.split('.')
        for i in range(int(start_list[3]), int(end_list[3]) + 1):
            ip = '.'.join(start_list[:3] + [str(i)])
            for port in range(1, 2024):
                while threading.active_count() > 100:
                    QThread.sleep(1)
                thread = ScanThread(ip, port, self)
                thread.update_progress_signal.connect(self.update_progress)
                thread.add_result_signal.connect(self.add_result)
                thread.scan_complete_signal.connect(self.scan_beendet)
                thread.start()

    @pyqtSlot(str, str, int)
    def add_result(self, ip, host_name, port):
        if ip not in self.offene_ports:
            self.offene_ports[ip] = []
        self.offene_ports[ip].append((port, host_name))
        self.result_area.append(f"Port {port} auf {ip} ({host_name}) ist offen")

    @pyqtSlot()
    def update_progress(self):
        self.progress_bar.setValue(min(self.total_ports, self.progress_bar.value() + 1))

    @pyqtSlot()
    def scan_beendet(self):
        global aktive_threads
        if aktive_threads == 0:
            QMessageBox.information(self, "Scan abgeschlossen", "Der Scanvorgang ist abgeschlossen.")


    def set_default_ip(self):
        self.ip_input.setText("172.20.10.1-15")

    def exportiere_ergebnisse_als_csv(self):
        dateiname = f"scan_ergebnisse{self.datei_nummer}.csv"
        with open(dateiname, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["IP", "Port", "Hostname"])
            for ip, ports in self.offene_ports.items():
                for port, host_name in ports:
                    writer.writerow([ip, port, host_name])

        QMessageBox.information(self, "Export abgeschlossen", f"Ergebnisse wurden in {dateiname} gespeichert.")
        self.datei_nummer += 1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    scanner= IPScanner()
    scanner.show()
    sys.exit(app.exec_())
