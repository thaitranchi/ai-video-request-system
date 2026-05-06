# AI Video Request System (Chemistry)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Build](https://img.shields.io/github/actions/workflow/status/thaitranchi/ai-video-request-system/ci.yml)
![Status](https://img.shields.io/badge/status-prototype-orange)
![Flutter](https://img.shields.io/badge/frontend-Flutter-blue)
![FastAPI](https://img.shields.io/badge/backend-FastAPI-green)

An asynchronous AI-powered system that generates short educational chemistry videos from user queries.

Built with **FastAPI (backend)** and **Flutter (frontend)**, this prototype focuses on validating the **video request → processing → delivery workflow**, rather than optimizing generation fidelity.

---

## 🎯 Problem

Learners want quick, visual explanations of chemistry concepts, but generating educational videos is inherently **slow and compute-heavy**.

This system treats video generation as an **asynchronous job**, allowing users to:
- submit requests instantly
- track progress
- consume results when ready

---

## 🧠 Key Design Decisions

### 1. Async-first architecture
Video generation is handled as a background job:
- avoids blocking UX
- mirrors real-world AI workloads

### 2. “Perceived AI video” strategy
Instead of full generative video:
- Script → TTS → Visual slides → FFmpeg merge

This delivers:
- fast iteration
- deterministic output
- realistic demo experience

### 3. Narrow but extensible scope
Supports 3 required queries:
- pH scale
- covalent bonds
- ionic vs covalent bonding

Designed to extend to broader STEM topics via modular pipeline.

---

## 🏗️ Architecture

```

Flutter App
↓
FastAPI Backend
↓
Async Job Worker
↓
Video Generation Pipeline
↓
Local Storage (video artifacts)

````

---

## ⚙️ Backend Overview (FastAPI)

### Core Model

```python
VideoRequest {
    id: str
    query: str
    status: "pending" | "processing" | "completed" | "failed"
    video_url: str | null
}
````

---

### API Endpoints

| Method | Endpoint     | Description          |
| ------ | ------------ | -------------------- |
| POST   | /requests    | Create video request |
| GET    | /videos      | List all requests    |
| GET    | /videos/{id} | Get video details    |

---

## 🔄 Video Generation Pipeline

1. Generate script (LLM)
2. Convert script → audio (TTS)
3. Generate simple visuals (slides/images)
4. Merge audio + visuals using FFmpeg
5. Store video and update status

---

## 📱 Frontend (Flutter)

* Submit request
* View list of videos
* Track status (pending → processing → completed)
* Play generated video

---

## 🎬 Demo

This repository includes:

* 3 generated videos (required queries)
* Corresponding input prompts

---

## 📦 Project Structure

```
/backend
  /app
    routes/
    services/
    models/

/frontend_flutter
  /lib
    screens/
    services/

/generated_videos
```

---

## ⚖️ Tradeoffs & Limitations

* No real-time video generation (intentionally async)
* Simplified visuals (slides instead of full animation)
* Local storage instead of cloud

These choices prioritize **clarity, reliability, and speed of execution**.

---

## 🔮 Future Improvements

* Queue system (Celery / Redis)
* Cloud storage (S3)
* Richer animations
* Multi-topic support beyond chemistry
* AI-driven visual generation

---

## 🧪 Required Queries Supported

* How does the pH scale work?
* Why do atoms form covalent bonds?
* Difference between ionic and covalent bonding

---

## 👨‍💻 Author

Trần Chí Thái
Software Engineer | AI Systems Builder

## License
This project is licensed under the MIT License.
