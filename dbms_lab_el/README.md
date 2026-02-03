# MindSim - PTSD Simulation System

A comprehensive web-based platform for PTSD assessment and simulation therapy using multi-agent systems.

## Features

- **Soldier Portal**: Take assessments, run simulations, track progress
- **Therapist Dashboard**: Manage patients, send recommendations, monitor analytics
- **Admin Panel**: System-wide statistics and monitoring
- **Mesa ABM Simulation**: Agent-based modeling for trauma scenarios
- **Real-time Analytics**: Track recovery metrics and therapy effectiveness

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, MySQL
- **Frontend**: React, Vite, Axios
- **Simulation**: Mesa (Agent-Based Modeling)
- **Auth**: JWT, bcrypt/argon2

## Quick Start

### Local Development

1. **Setup Environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   pip install -r requirements.txt
   ```

2. **Initialize Database**
   ```bash
   python seed_database.py
   ```

3. **Run Backend**
   ```bash
   python -m uvicorn backend.main:app --reload
   ```

4. **Run Frontend** (in another terminal)
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

5. **Access Application**
   - Frontend: http://localhost:5173
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Docker Deployment

```bash
docker-compose up --build
```

## Test Accounts

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Therapist | sarah.mitchell | therapist123 |
| Soldier | ryan.davis29 | soldier123 |

*30 soldier accounts and 8 therapist accounts pre-seeded*

## Project Structure

```
├── backend/
│   ├── main.py              # FastAPI app
│   ├── models.py            # Database models
│   ├── schemas.py           # Data validation
│   ├── database.py          # DB connection
│   ├── mesa_model.py        # Simulation engine
│   └── routers/             # API endpoints
├── frontend/
│   ├── src/
│   │   ├── pages/           # React pages
│   │   ├── components/      # React components
│   │   └── api.js           # Axios client
│   └── package.json
├── requirements.txt         # Python dependencies
├── docker-compose.yml       # Local deployment
└── Dockerfile.*             # Container images
```

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for Railway, Render, or cloud deployment instructions.

## Database Schema

- **User**: Authentication (soldier/therapist/admin roles)
- **Person**: Soldier demographics (name, rank, service years)
- **Therapist**: Therapist profiles (qualification, specialization)
- **Assessment**: Questionnaire responses
- **TherapistRecommendation**: Therapist-to-soldier recommendations
- **Scenario**: Simulation templates
- **Reaction**: User simulation interactions
- **Report**: Therapy reports

## API Documentation

Full API docs available at `/docs` endpoint in running backend.

### Key Endpoints

**Authentication**
- POST `/auth/register` - Create account
- POST `/auth/login` - Login
- GET `/auth/me/profile` - Get user profile

**Therapist**
- GET `/therapist/patients` - List assigned patients
- POST `/therapist/recommend/{patient_id}` - Send recommendation
- GET `/therapist/recommendations/{patient_id}` - Get pending recommendations
- GET `/therapist/dashboard/stats/{therapist_id}` - Get analytics

**Soldier**
- GET `/assessments/questionnaire` - Get assessment form
- POST `/assessments` - Submit assessment
- GET `/scenarios` - List simulation scenarios
- POST `/simulations/run` - Run simulation

## License

MIT

## Contact

For questions, contact project maintainer.
