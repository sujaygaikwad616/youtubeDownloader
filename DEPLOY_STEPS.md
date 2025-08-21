# Deployment Steps (Azure DevOps -> Linux VM with Docker)

## 0. Workflow Order (Push vs Local Build)
You do NOT have to build the Docker image locally before pushing. The pipeline builds the image on the VM automatically. Recommended workflow:
1. (Optional) Build & run locally to test changes.
2. Commit changes locally.
3. Push to `master` (GitHub or Azure Repos).
4. Azure DevOps pipeline triggers automatically.
5. Pipeline copies code to VM, builds fresh image there, restarts container.
6. Verify: `docker ps` then `docker logs ytcaption` on VM.

Initial (first time) repo push (PowerShell):
```powershell
git init
# If remote not added yet
git remote add origin https://github.com/<YOUR_USER>/<NEW_REPO>.git
git add .
git commit -m "Initial pipeline setup"
git branch -M master
git push -u origin master
```
Regular update:
```powershell
git add .
git commit -m "Change: <describe>"
git push
```
Optional local test before push:
```powershell
docker build -t ytcaption:test .
docker run --rm -e VIDEO_URL="https://youtu.be/<id>" ytcaption:test "https://youtu.be/<id>"
```
If satisfied, push; otherwise fix and repeat.

## 1. Prerequisites
- Azure DevOps Project with this repository imported / mirrored.
- Linux VM (Ubuntu recommended) accessible via SSH (public IP / DNS).
- SSH credentials (username + private key or password) you will add as a Service Connection.
- Docker installed on the VM.
- User added to the `docker` group (re-login after adding).

## 2. Prepare the VM (run on VM)
```bash
sudo apt update && sudo apt install -y docker.io git
sudo usermod -aG docker $USER
# Log out & back in (or: exec sudo su - $USER) so group change takes effect
sudo mkdir -p /opt/youtubeDownloader
sudo chown $USER:$USER /opt/youtubeDownloader
```
(Optional) Harden SSH: disable password login after key auth works, adjust firewall, etc.

## 3. Create SSH Service Connection in Azure DevOps
1. Azure DevOps > Project Settings > Service connections > New service connection.
2. Choose: SSH.
3. Fill:
   - Host name: (VM public IP / DNS)
   - Port: 22
   - User name: (your VM user in docker group)
   - Authentication: Private Key or Password (prefer key)
   - Service connection name: `VM-SSH-Service-Connection`
4. Grant access permission to all pipelines.

## 4. Review Pipeline File
`azure-pipelines.yml` is already in repo. It:
1. Triggers on push to `master`.
2. Copies all repo files to `/opt/youtubeDownloader` on the VM.
3. Builds Docker image locally on the VM: `ytcaption:latest`.
4. Stops & removes existing container `ytcaption` (if any).
5. Starts new container (passes `VIDEO_URL` only if pipeline variable `videoUrl` set).

## 5. Create / Run Pipeline
1. Azure DevOps > Pipelines > Create Pipeline.
2. Select your repo (Azure Repos Git or GitHub if connected).
3. Azure DevOps auto-detects `azure-pipelines.yml` – confirm.
4. Run pipeline once manually to verify SSH & Docker access.

## 6. (Optional) Set a Default Video URL
If you want the container to auto-download on each deploy:
- Edit pipeline > Variables > New variable `videoUrl` = `https://youtu.be/<id>` (keep it non-secret).
Otherwise the container starts idle; you can exec into it or re-run with a URL.

## 7. Manual Trigger vs Auto Trigger
- Any push to `master` branch triggers deployment automatically.
- To test without changes: make a trivial commit (e.g., update README) and push.

## 8. Local Development (Optional)
```bash
docker build -t ytcaption:local .
docker run --rm -e VIDEO_URL="https://youtu.be/<id>" ytcaption:local "https://youtu.be/<id>"
```
Output captions stored inside container `/downloads` (mapped to volume in pipeline run).

## 9. Checking Container on VM
```bash
docker ps
# View logs
docker logs -f ytcaption
# Enter container (if shell needed)
docker exec -it ytcaption /bin/bash
```

## 10. Updating Only Code (No Structural Changes)
Just edit files, commit, push to `master`. Pipeline rebuilds image & restarts container.

## 11. If Deployment Fails
Common issues:
- SSH connection denied: check security group / NSG / firewall & credentials.
- Permission denied building image: user not in `docker` group (re-login required).
- Container immediately exits: run `docker logs ytcaption` to inspect.
- Video URL missing: set pipeline variable `videoUrl` or pass argument manually.

## 12. Manually Re-run Container With New URL
```bash
docker rm -f ytcaption || true
docker run -d --name ytcaption --restart unless-stopped -e VIDEO_URL="https://youtu.be/<id>" -v /opt/youtubeDownloader/downloads:/downloads ytcaption:latest "https://youtu.be/<id>"
```

## 13. Cleaning Up Old Images / Containers
Current simple pipeline does not prune. Occasionally run:
```bash
docker image prune -f
```
Or to remove dangling & unused images:
```bash
docker system prune -f
```

## 14. Windows Developer Notes
Develop on Windows, push – pipeline uses Linux VM. Paths inside container use `/downloads`. Host mount path on VM is `/opt/youtubeDownloader/downloads`.

## 15. Security Recommendations
- Use SSH key instead of password.
- Restrict VM inbound to your IP(s) if possible.
- Keep OS & Docker updated (`sudo apt upgrade -y`).

## 16. Quick Reference (Minimal)
1. (Optional) docker build/test locally.
2. git add . ; git commit -m "msg" ; git push (master).
3. Pipeline auto-runs.
4. VM builds image & restarts container.
5. Verify with logs.

---
Need enhancements (logging, rollback tags, notifications)? Ask to extend the pipeline.
