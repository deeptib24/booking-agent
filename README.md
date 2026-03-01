# Booking Agent 🗓️

A full-stack booking assistant built using FastAPI and React.

This project allows users to check availability, book appointments, reschedule, and cancel bookings through a simple frontend interface connected to a REST API backend.

---

## 🚀 Features

- ✅ Check availability by date  
- ✅ Book an appointment  
- ✅ Reschedule an existing booking  
- ✅ Cancel a booking  
- ✅ React frontend connected to FastAPI backend  
- ✅ SQLite database integration  
- ✅ Proper CORS configuration  

---

## 🛠️ Tech Stack

### Backend
- FastAPI
- Pydantic
- SQLite
- Uvicorn

### Frontend
- React
- Vite
- Fetch API

---

## 🧠 Architecture

Frontend (React - Port 5173)  
⬇  
Backend (FastAPI - Port 8000)  
⬇  
SQLite Database  

---

## ⚙️ How to Run Locally

### 1️⃣ Backend
cd backend
python -m venv .venv
.venv\Scripts\activate (Windows)
pip install -r requirements.txt
uvicorn main:app --reload

Backend runs on:
http://localhost:8000


---

### 2️⃣ Frontend
cd frontend
npm install
npm run dev


Frontend runs on:
http://localhost:5173


---

## 📌 API Endpoints

- `POST /availability` → Get open slots for a date  
- `POST /book` → Create a booking  
- `POST /reschedule` → Reschedule an appointment  
- `POST /cancel` → Cancel an appointment  

Swagger Docs available at:
http://localhost:8000/docs


---

## ⚠️ Note on AI Endpoint

The `/chat` endpoint requires a valid OpenAI API key with active billing.  
If quota is exceeded, core booking functionality still works independently.

---

## 🎯 Project Purpose

This project demonstrates:

- Full-stack development  
- API design and integration  
- Database handling  
- CORS management  
- Frontend ↔ Backend communication  
- Error debugging and system architecture  

---

## 👩‍💻 Author

Built as a full-stack practice project to strengthen backend + frontend integration skills.
