# Student Marks API

A simple REST API for managing student marks records, built with Python + FastAPI.  
This project demonstrates a complete DevOps pipeline: Git → Jenkins → Docker → Ansible → Kubernetes.

---

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check (used by Kubernetes probes) |
| GET | `/students` | List all student records |
| GET | `/students/{id}` | Get a student by ID |
| POST | `/students` | Add a new student record |

### Example requests
```bash
# List all students
curl http://localhost:8000/students

# Add a student
curl -X POST http://localhost:8000/students \
  -H "Content-Type: application/json" \
  -d '{"name": "Eve Adams", "subject": "Chemistry", "marks": 79}'

# Health check
curl http://localhost:8000/health
```

---

## Run Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Run Tests

```bash
pytest tests/ -v
```

## Docker

```bash
docker build -t student-marks-api:latest .
docker run -p 8000:8000 student-marks-api:latest
```

## Kubernetes (Minikube)

```bash
minikube start
eval $(minikube docker-env)          # point Docker to Minikube's daemon
docker build -t student-marks-api:latest .

kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

kubectl get pods
minikube service student-marks-api-svc --url
```

## Ansible

```bash
cd ansible
ansible-playbook -i inventory playbook.yml
```

---

## Project Structure

```
student-marks-api/
├── app/
│   └── main.py                  # FastAPI application
├── tests/
│   └── test_api.py              # pytest unit tests
├── ansible/
│   ├── inventory                # target hosts
│   ├── playbook.yml             # main playbook
│   └── roles/
│       └── app_setup/
│           ├── tasks/main.yml
│           ├── handlers/main.yml
│           ├── vars/main.yml
│           └── templates/student-marks-api.service.j2
├── k8s/
│   ├── configmap.yaml
│   ├── deployment.yaml          # 3 replicas + liveness/readiness probes
│   └── service.yaml             # NodePort on 30080
├── .github/
│   └── workflows/ci.yml         # GitHub Actions CI
├── Dockerfile                   # Multi-stage build
├── Jenkinsfile                  # Jenkins pipeline
├── requirements.txt
├── repo_link.txt
└── README.md
```
