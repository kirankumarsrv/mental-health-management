# MindSim - Deployment Guide

## Quick Start - Local Docker Deployment

### Prerequisites
- Docker and Docker Compose installed
- Git

### Steps

1. **Clone/Extract Project**
   ```bash
   cd dbms_lab_el
   ```

2. **Build and Run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

3. **Access the Application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

4. **Initialize Database** (on first run)
   The database will auto-initialize. If needed, seed data:
   ```bash
   docker-compose exec backend python seed_database.py
   ```

---

## Deploy to Railway (Free 24-Hour Trial)

### Steps

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Create New Project**
   - Click "Create New Project"
   - Select "Deploy from GitHub"
   - Connect your GitHub repo (or upload ZIP)

3. **Add Services**
   - **MySQL Database**
     - Add MySQL service
     - Set environment variables in settings
   
   - **Backend (FastAPI)**
     - Select Dockerfile → `Dockerfile.backend`
     - Set environment variables:
       ```
       DATABASE_URL=mysql+pymysql://user:password@mysql_host:3306/ptsd_simulation
       ```
   
   - **Frontend (React)**
     - Select Dockerfile → `Dockerfile.frontend`

4. **Deploy**
   - Railway auto-deploys on push
   - Get public URLs from Railway dashboard

---

## Deploy to Render (Free Tier)

### Steps

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up

2. **Deploy Backend**
   - New → Web Service
   - Connect GitHub repo
   - Runtime: Docker
   - Port: 8000
   - Set environment variables

3. **Deploy Frontend**
   - New → Static Site
   - Build command: `cd frontend && npm install && npm run build`
   - Publish directory: `frontend/dist`

4. **Connect Services**
   - Update frontend API URL to backend Render URL

---

## Test Accounts

### Admin
- Username: `admin`
- Password: `admin123`

### Therapists
- Username: `sarah.mitchell`
- Password: `therapist123`

- Username: `james.anderson`
- Password: `therapist123`

### Soldiers
- Username: `ryan.davis29`
- Password: `soldier123`

- Username: `alex.garcia0`
- Password: `soldier123`

---

## Features to Test

1. **Soldier Flow**
   - Login as soldier
   - Take assessment (questionnaire)
   - Run simulation
   - View personal results

2. **Therapist Flow**
   - Login as therapist
   - View assigned patients
   - Send recommendations to patients
   - Monitor patient progress
   - View analytics

3. **Admin Flow** (if implemented)
   - View system-wide statistics
   - Monitor all users

---

## Troubleshooting

### Database Connection Issues
```bash
# Check MySQL is running
docker-compose logs mysql

# Reinitialize database
docker-compose down -v
docker-compose up --build
```

### Frontend Not Loading
```bash
# Rebuild frontend
docker-compose build frontend
docker-compose up
```

### API Not Responding
```bash
# Check backend logs
docker-compose logs backend

# Rebuild backend
docker-compose build backend
```

---

## Duration

- **Railway**: Free tier has limited credits (~$5)
- **Render**: Free tier available, but limited
- For persistent deployment, consider paid plans

Enjoy testing!
