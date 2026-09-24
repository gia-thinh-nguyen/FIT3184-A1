
## Running locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

- API: `http://127.0.0.1:8000/api/find-carparks?uuid=test&n=3`
- Dashboard: `http://127.0.0.1:8000/dashboard/`
- Interactive API docs: `http://127.0.0.1:8000/docs`

## Running with Docker

```bash
docker build -t smart-parking:latest .
docker run -p 8080:8080 smart-parking:latest
```

## Deploying to GKE

```bash
gcloud container clusters get-credentials <cluster-name> --zone <zone>
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl autoscale deployment smart-parking-deployment --cpu-percent=50 --min=1 --max=8
kubectl get service smart-parking-service   # get EXTERNAL-IP
```

## Key design decisions

- **Concurrency**: YOLO inference is synchronous and CPU-bound. Running it directly inside an `async def` route would block FastAPI's single-threaded event loop, stalling all concurrent requests. Inference is offloaded to a `ThreadPoolExecutor` via `run_in_executor`; threads (not processes) are used because PyTorch releases the GIL during tensor computation, giving real parallelism without the memory overhead of loading a separate model copy per process.
- **Resource requests/limits**: set conservatively (`250m`/`1000m` CPU, `512Mi`/`2Gi` memory) after observing that GKE reserves a portion of each node's CPU for system components, and higher requests caused pods to get stuck `Pending` on small node types.
- **Model/image assets**: baked into the Docker image rather than downloaded at runtime, since they are private, non-public files provided for this assignment with no external hosting URL.

## Known limitations

- Car park state and the request log are held in-process memory. Scaling to multiple replicas means each pod has its own separate copy — `OPS-API-2`'s "active users" count and `annotate-carpark`'s image cache are only correct per-pod, not cluster-wide. A production fix would use a shared store (e.g. Redis) so all replicas see consistent state.