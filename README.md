# Fall 2025 CS 3200 Project 

# 📘 TeamTracker – Backend API

TeamTracker is a **data-driven backend service** designed to support college soccer teams in managing rosters, events, attendance, performance statistics, injuries, strategies, and team communication—all in one platform.

This project was built as part of **CS3200 – Databases** at Northeastern University (Fall 2025).

The backend exposes a REST API which supports the main user personas—**Player**, **Coach**, **Analyst**, and **Team Admin**—and implements CRUD operations and data retrieval required by the system user stories.

---

## Features

### TeamTracker enables:
- Creating teams, players, coaches, and admins
- Scheduling events (games, practices, meetings)
- RSVP tracking per event
- Player performance and game statistics
- Injury tracking & recovery timelines
- Strategy tracking and results
- Comments & coaching feedback

### User Personas
- **Players** – view schedule, RSVP, review stats & injuries
- **Coaches** – analyze lineup, coaching feedback, team trends
- **Analysts** – statistics, comments, and data insights
- **Team Admin** – roster & event management

---

## Tech Stack

- Python
- Flask
- MySQL
- Docker + Docker Compose
- REST API
- SQL schemas executed automatically on startup

---

## Getting Started

### Requirements
- Docker Desktop
- Git

---

## Setup Instructions

### 1. Clone the repository

```sh
git clone https://github.com/7fi/CS320025F-TeamTracker.git
cd CS320025F-TeamTracker
```

### 2. Create `.env`

Inside `/api`, copy `.env.template`:

```sh
cp api/.env.template api/.env
```

Then edit `.env` and set:

```
MYSQL_PASSWORD=yourpassword
```

### 3. Start the containers

```sh
docker compose up -d
```

This automatically:
- starts MySQL
- builds the DB
- executes schema + bootstrap SQL
- starts Flask API

### 4. Confirm backend is running

Open:
```
http://localhost:4000/
```

---

## API Usage

REST endpoints follow the API spec matrix.

Example routes:
```
/team/{teamID}
/events/{eventID}
/events/rsvp/{eventID}
/players/{playerID}
/players/{playerID}/comments
/strategy/{strategyID}
```

---

## Project Structure

```
api/
  backend/
    routes/
    db_connection.py
  .env.template
docker-compose.yml
```

---

## Team Members — Team BETAS

| Name |
|-------|
| Carter Anderson |
| Naanlong Clement Baba | 
| Marc Sawaya | 
| Sebastian Tutos-Zub | 
| Freddy Elyas | 

---

## Development Notes

Stop containers:
```sh
docker compose down
```

Rebuild:
```sh
docker compose down
docker compose up --build -d
```

---

## Status
- Dockerized
- REST routes completed
- SQL schemas executed automatically
- .env based config

---

## Future Enhancements
- Authentication
- Front-End UI
- Email notifications
- Analytics dashboards

---

## Acknowledgements
Built for **CS3200 – Introduction to Databases**, Fall 2025, Northeastern University.
