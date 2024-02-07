To reproduce:

1. Pull docker and create network
```bash
make prepare_docker
```

2. Run the cluster
```bash
make run_hazelcast_cluster
```

3. Install libs and run lab
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

Logs will be stored in logs/
app_logs.log contains logs from main.py
claster.logs contains logs from all three clusters.