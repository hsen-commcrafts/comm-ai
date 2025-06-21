    

## 🧠 FastText WhatsApp Intent Classifier (FastAPI)

This app is a FastAPI-based API that classifies WhatsApp messages into predefined intents using a trained [FastText](https://fasttext.cc/) model.

---

## 📦 Features

* 🔤 FastText-based sentence classification
* 🔐 HMAC-based secure API access
* 🚀 FastAPI REST endpoint (`/api/flow`)
* ⚡ Trained using multilingual and Arabizi data

---

## 📁 Folder Structure

```
.
├── main.py              # FastAPI server
├── train_model.py       # FastText trainer
├── model.ftz            # Trained FastText model (generated after training)
├── .env                 # Environment variables
```

---

## 🛠️ Setup Instructions

### 1. Clone the project

```bash
cd comm-ai
```

### 2. Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip3 install -r requirements.txt
```

---

## 🔐 Environment Setup

Create a `.env` file:

```env
MODEL_PATH=model.ftz
API_SECRET=your_shared_secret_key
```

> 🔐 `HMAC_SECRET` must match what Laravel uses when calling this API.

---

## 🎓 Training the Model

1. Prepare a labeled dataset (e.g., `training_data.txt`):

```
__label__make_order I want to order something
__label__track_order Where is my order?
...
```

2. Run training:

```bash
python3 train_model.py
```

This will save `model.ftz` in the current directory.

---

## 🚀 Run the API Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Swagger UI and ReDoc are disabled for security.

---

## 🔐 Secure HMAC Integration

All API requests must include these headers:

```http
X-Timestamp: <current_unix_timestamp>
X-Signature: <HMAC_SHA256_signature>
```

Signature is:

```text
signature = HMAC_SHA256(timestamp + "|flow_request", HMAC_SECRET)
```

Example Laravel usage:

```php
$timestamp = time();
$message = $timestamp . '|flow_request';
$signature = hash_hmac('sha256', $message, env('HMAC_SECRET'));

$response = Http::withHeaders([
    'X-Timestamp' => $timestamp,
    'X-Signature' => $signature,
])->post('http://localhost:8000/api/flow', [
    'text' => 'i want to make an order'
]);
```

---

## ✅ API Endpoint

**POST** `/api/flow`

Request body:

```json
{
  "text": "i want to make an order"
}
```

Response:

```json
{
  "label": "make_order",
  "confidence": 0.92
}
```

---


