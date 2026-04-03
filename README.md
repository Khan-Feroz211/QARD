# QARD — Virtual Student Card Platform

Pakistan's first digital student identity + benefits platform. QARD gives every university student a beautiful virtual ID card, seamless benefit redemptions, academic record access, and a multi-tenant SaaS engine for universities.

---

## What is QARD?

QARD (pronounced _card_) is a SaaS platform that digitises the student ID card experience for Pakistani universities. Students get a mobile virtual card with a QR code, instant access to their academic records, and exclusive partner discounts. Universities get a white-label admin portal to manage students, branding, and analytics.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend API | Python 3.11 + FastAPI (async, multi-tenant) |
| Mobile App | React Native 0.74 (iOS + Android) |
| Admin Portal | React 18 + Vite 5 |
| Database | PostgreSQL 16 (schema-per-tenant) |
| Cache | Redis 7 |
| Queue | Celery 5 + RabbitMQ 3 |
| Storage | MinIO (S3-compatible) |
| Payments | Stripe (international) + JazzCash (Pakistan) |
| Push Notifications | Firebase FCM |
| SMS OTP | Twilio |
| Infra (local) | Docker Compose |
| Infra (prod) | Kubernetes + NGINX Ingress |
| CI/CD | GitHub Actions |
| Monitoring | Prometheus + Grafana |

---

## Project Structure

```
qard/
├── backend/          ← FastAPI application
│   ├── app/
│   │   ├── main.py         ← App factory, CORS, lifespan
│   │   ├── config.py       ← pydantic-settings env config
│   │   ├── dependencies.py ← DI: get_db, get_current_user
│   │   ├── db/             ← ORM models, engine, tenant routing
│   │   ├── routers/        ← auth, card, academic, benefits, usage, billing, admin, health
│   │   ├── services/       ← Business logic layer
│   │   ├── tasks/          ← Celery async tasks
│   │   ├── middleware/      ← Tenant + logging middleware
│   │   └── models/         ← Pydantic v2 schemas
│   ├── alembic/            ← Database migrations
│   ├── tests/              ← pytest test suite
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
├── mobile/           ← React Native app
│   ├── src/
│   │   ├── screens/        ← 9 screens (Splash → Profile)
│   │   ├── components/     ← VirtualCard, QRCode, BenefitCard, UsageItem
│   │   ├── navigation/     ← Stack + Tab navigators
│   │   ├── services/       ← axios API client, auth, AsyncStorage
│   │   ├── store/          ← Zustand state management
│   │   └── theme/          ← Colors and typography
│   └── package.json
├── admin/            ← University admin portal (React + Vite)
│   ├── src/
│   │   ├── pages/          ← Login, Dashboard, Students, Benefits, Branding, Analytics
│   │   ├── services/       ← axios admin API client
│   │   └── App.jsx         ← BrowserRouter + route layout
│   └── package.json
├── infra/
│   ├── k8s/                ← Kubernetes manifests (deployment, HPA, ingress)
│   ├── monitoring/         ← Prometheus + Grafana dashboards
│   └── nginx/              ← nginx.conf for reverse proxy
├── docker-compose.yml      ← Full local stack (10 services)
├── docker-compose.prod.yml ← Production compose
├── Makefile                ← Developer workflow commands
└── .gitignore
```

---

## SaaS Tiers

| Feature | Free | Pro | University Enterprise |
|---|---|---|---|
| Virtual student card | ✅ | ✅ | ✅ |
| QR code | ✅ | ✅ | ✅ |
| Academic records | ✅ | ✅ | ✅ |
| Benefits catalog (global) | ✅ | ✅ | ✅ |
| University-specific benefits | ❌ | ✅ | ✅ |
| Custom branding | ❌ | ✅ | ✅ |
| LMS sync | ❌ | ✅ | ✅ |
| Analytics dashboard | ❌ | ✅ | ✅ |
| Dedicated support | ❌ | ❌ | ✅ |
| On-premise deployment | ❌ | ❌ | ✅ |

---

## Prerequisites

| Tool | Version |
|---|---|
| Docker + Docker Compose | 24+ |
| Node.js | 20+ |
| Python | 3.11+ |
| React Native CLI | latest |

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/Khan-Feroz211/QARD.git
cd QARD

# 2. Copy environment file
cp .env.docker.example .env  # edit as needed

# 3. Start all services
make up

# 4. Run database migrations
make migrate

# 5. Open the API
open http://localhost:8000/health
# → {"status": "ok", "version": "1.0.0", ...}

# 6. Open the admin portal
open http://localhost:5173

# 7. Open monitoring
open http://localhost:3001   # Grafana (admin/admin)
open http://localhost:9090   # Prometheus
open http://localhost:15672  # RabbitMQ Management
open http://localhost:9001   # MinIO Console
```

---

## Mobile Setup

```bash
cd mobile
npm install

# Android
npx react-native run-android

# iOS
npx react-native run-ios
```

---

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `APP_ENV` | Application environment | `development` |
| `DATABASE_URL` | PostgreSQL async connection string | `postgresql+asyncpg://...` |
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379/0` |
| `RABBITMQ_URL` | RabbitMQ AMQP URL | `amqp://guest:guest@...` |
| `JWT_SECRET` | Secret for signing JWT tokens | — |
| `SECRET_KEY` | App secret key | — |
| `STRIPE_SECRET_KEY` | Stripe API secret | `sk_test_...` |
| `STRIPE_WEBHOOK_SECRET` | Stripe webhook signing secret | `whsec_...` |
| `STRIPE_PRO_PRICE_ID` | Stripe Price ID for Pro plan | `price_...` |
| `JAZZCASH_MERCHANT_ID` | JazzCash merchant ID | — |
| `FIREBASE_CREDENTIALS_JSON` | Path to Firebase service account | — |
| `TWILIO_ACCOUNT_SID` | Twilio account SID | — |
| `MINIO_ENDPOINT` | MinIO endpoint | `localhost:9000` |

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `POST` | `/api/v1/auth/register` | Register student + create card |
| `POST` | `/api/v1/auth/login` | Login → JWT pair |
| `POST` | `/api/v1/auth/otp/send` | Send OTP via SMS |
| `POST` | `/api/v1/auth/otp/verify` | Verify OTP |
| `GET` | `/api/v1/card` | Get virtual card |
| `POST` | `/api/v1/card/scan` | Log scan event |
| `PUT` | `/api/v1/card/regenerate` | Issue new card |
| `GET` | `/api/v1/academic` | Current semester + GPA |
| `GET` | `/api/v1/academic/history` | All semesters |
| `POST` | `/api/v1/academic/sync` | Trigger LMS sync |
| `GET` | `/api/v1/benefits` | List benefits |
| `POST` | `/api/v1/benefits/{id}/claim` | Claim a benefit |
| `GET` | `/api/v1/usage` | Usage history |
| `GET` | `/api/v1/alerts` | Unread alerts |
| `PUT` | `/api/v1/alerts/{id}/read` | Mark alert read |
| `POST` | `/api/v1/billing/upgrade` | Upgrade to Pro |
| `POST` | `/api/v1/billing/webhook` | Stripe webhook |
| `GET` | `/api/v1/billing/status` | Billing status |
| `GET` | `/api/v1/admin/students` | List students (admin) |
| `POST` | `/api/v1/admin/benefits` | Create benefit (admin) |
| `GET` | `/api/v1/admin/analytics` | Analytics (admin) |
| `PUT` | `/api/v1/admin/branding` | Update branding (admin) |
| `POST` | `/api/v1/superadmin/tenants` | Create tenant |
| `GET` | `/api/v1/superadmin/tenants` | List all tenants |
| `GET` | `/health` | Health check |

---

## Multi-Tenancy

Each university is a **Tenant** identified by a unique `slug` (e.g. `nust`, `lums`). Users belong to a tenant via `tenant_id`. The tenant slug is resolved from the JWT payload or HTTP subdomain on every request. Benefits and branding are scoped per tenant, while global benefits are available to all students.

---

## Roadmap

| Day | Milestone |
|---|---|
| Day 1 | Project scaffolding, DB models, auth API |
| Day 2 | Virtual card generation, QR codes, mobile screens |
| Day 3 | Academic records, LMS sync, benefits catalog |
| Day 4 | Stripe billing, JazzCash integration, admin portal |
| Day 5 | MLflow integration, usage analytics, alerts |
| Day 6 | Firebase FCM push notifications, Twilio SMS |
| Day 7 | Kubernetes manifests, CI/CD GitHub Actions |
| Day 8 | Monitoring (Prometheus + Grafana), load testing |
| Day 9 | Production hardening, security audit, launch |
