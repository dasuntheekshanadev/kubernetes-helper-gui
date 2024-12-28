# Kubernetes Helper GUI

A user-friendly desktop application built with PyQt5 that provides a graphical interface for managing and monitoring Kubernetes clusters. This tool allows users to view cluster information and perform basic Kubernetes operations with a simple click.

## Features

- Dark mode interface for better visibility
- Real-time cluster information display
- View Kubernetes resources:
  - Nodes and their status
  - Pods across all namespaces
  - Services across all namespaces
- Create new resources:
  - Namespaces
  - Pods (with default Nginx container)
  - Services
- Auto-refresh functionality
- User-friendly input dialogs for resource creation

## Prerequisites

- Python 3.6 or higher
- Kubernetes cluster access configured (`kubectl` config file)
- PyQt5
- kubernetes-python client
- qdarkstyle

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/kubernetes-helper-gui.git
cd kubernetes-helper-gui
```

2. Install required dependencies:
```bash
pip install PyQt5 kubernetes qdarkstyle
```

3. Ensure your Kubernetes configuration is properly set up:
- Your `~/.kube/config` file should be configured with cluster access
- You should have appropriate permissions to list and create resources

## Usage

1. Start the application:
```bash
python main.py
```

2. The main window will display three sections:
   - Nodes: Shows all nodes in the cluster and their status
   - Pods: Displays all pods across namespaces
   - Services: Lists all services across namespaces

3. Available actions:
   - Click "Refresh" to update the cluster information
   - Click "Create Namespace" to create a new namespace
   - Click "Create Pod" to deploy a new Nginx pod
   - Click "Create Service" to create a new service

## Features in Detail

### Viewing Resources
- The application automatically fetches and displays:
  - Node information including ready status
  - Pod information including namespace and current phase
  - Service information including namespace

### Creating Resources
- **Namespaces**: Enter a name for the new namespace
- **Pods**: Specify namespace and pod name (creates an Nginx container)
- **Services**: Specify namespace and service name (creates a service for Nginx pods)

## Error Handling

- The application includes comprehensive error handling for:
  - Kubernetes API connection issues
  - Resource creation failures
  - Invalid input validation
- Error messages are displayed in the application's status bar

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with PyQt5
- Uses the official Kubernetes Python client
- Dark theme provided by QDarkStyle

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.
