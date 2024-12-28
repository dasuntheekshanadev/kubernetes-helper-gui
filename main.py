import sys
import qdarkstyle
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QWidget, QTableWidget, QTableWidgetItem, QInputDialog
)

from kubernetes import client, config

class KubernetesViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Kubernetes Cluster Info")
        self.setGeometry(100, 100, 900, 700)

        # Apply dark mode
        self.setStyleSheet(qdarkstyle.load_stylesheet())

        # Main layout
        self.main_layout = QVBoxLayout()

        # Widgets
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.fetch_cluster_info)

        self.create_namespace_button = QPushButton("Create Namespace")
        self.create_namespace_button.clicked.connect(self.create_namespace)

        self.create_pod_button = QPushButton("Create Pod")
        self.create_pod_button.clicked.connect(self.create_pod)

        self.create_service_button = QPushButton("Create Service")
        self.create_service_button.clicked.connect(self.create_service)

        # Table for Nodes
        self.nodes_table = QTableWidget()
        self.nodes_table.setColumnCount(2)
        self.nodes_table.setHorizontalHeaderLabels(["Node Name", "Status"])

        # Table for Pods
        self.pods_table = QTableWidget()
        self.pods_table.setColumnCount(3)
        self.pods_table.setHorizontalHeaderLabels(["Namespace", "Pod Name", "Status"])

        # Table for Services
        self.services_table = QTableWidget()
        self.services_table.setColumnCount(2)
        self.services_table.setHorizontalHeaderLabels(["Namespace", "Service Name"])

        # Add widgets to layout
        self.main_layout.addWidget(QLabel("Nodes"))
        self.main_layout.addWidget(self.nodes_table)
        self.main_layout.addWidget(QLabel("Pods"))
        self.main_layout.addWidget(self.pods_table)
        self.main_layout.addWidget(QLabel("Services"))
        self.main_layout.addWidget(self.services_table)
        self.main_layout.addWidget(self.refresh_button)
        self.main_layout.addWidget(self.create_namespace_button)
        self.main_layout.addWidget(self.create_pod_button)
        self.main_layout.addWidget(self.create_service_button)

        # Set the central widget and layout
        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

        # Fetch initial data
        self.fetch_cluster_info()

    def fetch_cluster_info(self):
        try:
            # Load Kubernetes configuration
            config.load_kube_config()
            v1 = client.CoreV1Api()

            # Fetch nodes
            nodes = v1.list_node()
            self.nodes_table.setRowCount(len(nodes.items))
            for i, node in enumerate(nodes.items):
                self.nodes_table.setItem(i, 0, QTableWidgetItem(node.metadata.name))
                status = "Ready" if "Ready" in [condition.type for condition in node.status.conditions] else "Not Ready"
                self.nodes_table.setItem(i, 1, QTableWidgetItem(status))

            # Fetch pods
            pods = v1.list_pod_for_all_namespaces()
            self.pods_table.setRowCount(len(pods.items))
            for i, pod in enumerate(pods.items):
                self.pods_table.setItem(i, 0, QTableWidgetItem(pod.metadata.namespace))
                self.pods_table.setItem(i, 1, QTableWidgetItem(pod.metadata.name))
                self.pods_table.setItem(i, 2, QTableWidgetItem(pod.status.phase))

            # Fetch services
            services = v1.list_service_for_all_namespaces()
            self.services_table.setRowCount(len(services.items))
            for i, svc in enumerate(services.items):
                self.services_table.setItem(i, 0, QTableWidgetItem(svc.metadata.namespace))
                self.services_table.setItem(i, 1, QTableWidgetItem(svc.metadata.name))

        except Exception as e:
            print(f"Error fetching Kubernetes data: {e}")
            self.statusBar().showMessage(f"Error: {e}")

    def create_namespace(self):
        namespace, ok = self.prompt_user_input("Enter Namespace Name:")
        if ok and namespace:
            try:
                config.load_kube_config()
                v1 = client.CoreV1Api()
                namespace_body = client.V1Namespace(metadata=client.V1ObjectMeta(name=namespace))
                v1.create_namespace(namespace_body)
                QMessageBox.information(self, "Success", f"Namespace '{namespace}' created successfully!")
                self.fetch_cluster_info()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create namespace: {e}")

    def create_pod(self):
        namespace, ok = self.prompt_user_input("Enter Namespace for Pod:")
        if not ok or not namespace:
            return
        pod_name, ok = self.prompt_user_input("Enter Pod Name:")
        if not ok or not pod_name:
            return
        try:
            config.load_kube_config()
            v1 = client.CoreV1Api()
            pod_body = client.V1Pod(
                metadata=client.V1ObjectMeta(name=pod_name),
                spec=client.V1PodSpec(
                    containers=[client.V1Container(name="nginx", image="nginx")]
                )
            )
            v1.create_namespaced_pod(namespace, pod_body)
            QMessageBox.information(self, "Success", f"Pod '{pod_name}' created successfully in namespace '{namespace}'!")
            self.fetch_cluster_info()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create pod: {e}")

    def create_service(self):
        namespace, ok = self.prompt_user_input("Enter Namespace for Service:")
        if not ok or not namespace:
            return
        service_name, ok = self.prompt_user_input("Enter Service Name:")
        if not ok or not service_name:
            return
        try:
            config.load_kube_config()
            v1 = client.CoreV1Api()
            service_body = client.V1Service(
                metadata=client.V1ObjectMeta(name=service_name),
                spec=client.V1ServiceSpec(
                    selector={"app": "nginx"},
                    ports=[client.V1ServicePort(port=80, target_port=80)]
                )
            )
            v1.create_namespaced_service(namespace, service_body)
            QMessageBox.information(self, "Success", f"Service '{service_name}' created successfully in namespace '{namespace}'!")
            self.fetch_cluster_info()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create service: {e}")

    def prompt_user_input(self, message):
        text, ok = QInputDialog.getText(self, "Input", message)
        return text, ok

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create the main window
    window = KubernetesViewer()

    # Show the window
    window.show()

    # Start the application event loop
    sys.exit(app.exec_())
