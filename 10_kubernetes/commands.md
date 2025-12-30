wget https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)

docker run -it --rm  -p 8500:8500  -v $(pwd)/clothing-model:/models/clothing-model/1  -e MODEL_NAME="clothing-model"  tensorflow/serving:2.7.0


curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.34.2/2025-11-13/bin/linux/amd64/kubectl
wget https://kind.sigs.k8s.io/dl/v0.31.0/kind-linux-amd64 -O kind

touch Pipfile

docker build -t clothing-10-model:xception-v4-001 .
docker run -it --rm -p 9696:9696 clothing-10-model:xception-v4-001


docker build -t clothing-model-gateway:v001 .
docker run -it --rm -p 9696:9696 clothing-model-gateway:001


docker build -t ping:v001 .
docker run -it --rm -p 9696:9696 ping:v001

curl localhost:9696/ping

kind create cluster --image kindest/node:v1.32.0
kind get clusters
kubectl cluster-info --context kind-kind

kubectl get deployment
kind load docker-image ping:v001
kubectl port-forward ping-deployment 9696:9696

docker compose up 
docker compose up -d
docker compose down

kind load docker-image clothing-10-model:xception-v4-001
kind load docker-image clothing-model-gateway:001

kubectl apply -f model-deployment.yaml
kubectl port-forward tf-serving-clothing-model-5cf8846568-k5p27 8500:8500
python gateway.py

kubectl apply -f model-service.yaml
kubectl port-forward service/tf-serving-clothing-model 8500:8500
python gateway.py

kubectl apply -f gateway-deployment.yaml
kubectl port-forward gateway-fdb5bb4b9-24vbl 9696:9696
python test.py

kubectl apply -f gateway-service.yaml
kubectl port-forward service/gateway 8080:80
python test.py



kubectl get service
kubectl get pod
kubectl describe pod tf-serving-clothing-model-9bdd675b9-mcf5x
kubectl exec -it tf-serving-clothing-model-5cf8846568-k5p27 -- bash [PODNAME]
kubectl exec -it gateway-fdb5bb4b9-bxcxd -- bash



# for ARM systems, set ARCH to: `arm64`, `armv6` or `armv7`
ARCH=amd64
PLATFORM=$(uname -s)_$ARCH

curl -sLO "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_$PLATFORM.tar.gz"

# (Optional) Verify checksum
curl -sL "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_checksums.txt" | grep $PLATFORM | sha256sum --check

tar -xzf eksctl_$PLATFORM.tar.gz -C /bin && rm eksctl_$PLATFORM.tar.gz


eksctl create cluster -f eks-config.yaml



aws ecr create-repository --repository-name mlzoomcamp-images

ACCOUNT_ID=946055848646
REGION=us-east-1
REGISTRY_NAME=mlzoomcamp-images
PREFIX=${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${REGISTRY_NAME}

GATEWAY_LOCAL=clothing-model-gateway:001
GATEWAY_REMOTE=${PREFIX}:clothing-model-gateway-001
docker tag ${GATEWAY_LOCAL} ${GATEWAY_REMOTE}

MODEL_LOCAL=clothing-10-model:xception-v4-001
MODEL_REMOTE=${PREFIX}:clothing-10-model-xception-v4-001
docker tag ${MODEL_LOCAL} ${MODEL_REMOTE}

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 946055848646.dkr.ecr.us-east-1.amazonaws.com

docker push ${MODEL_REMOTE}
docker push ${GATEWAY_REMOTE}