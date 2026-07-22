# Pocket Doctor

A full-stack healthcare platform where patients describe symptoms in plain language, get matched to a specialist by a trained classifier, and book an appointment — with separate portals for patients, doctors, and admins.

Built with Django, a symptom-classification model trained from scratch, and a hand-built frontend (no CSS framework).

---

## What it does

**Patients** can:
- Sign up and describe symptoms in free text
- Get a specialist recommendation from a trained ML classifier, with an LLM-generated explanation
- Book an appointment with real availability checking (no double-booking)
- Message their doctor and view prescriptions on each appointment

**Doctors** can:
- View their assigned appointments on a dashboard
- Message patients and update appointment status
- Write and edit digital prescriptions
- Set their own weekly availability

**Admins** can:
- View system-wide stats (patients, doctors, appointments, pending reviews)
- Add doctors, optionally with a login account created at the same time
- View doctor and patient detail pages, including appointment history
- Suspend patient accounts or deactivate doctor listings (no destructive deletion)

---

## The ML model — and an honest note on its accuracy

The symptom checker is a **TF-IDF + Linear SVM classifier** trained on the [Symptom2Disease dataset](https://www.kaggle.com/datasets/niyarrbarman/symptom2disease) (1,200 rows, 24 disease categories, 50 examples each). Each predicted disease maps to a medical specialty through a lookup table I defined.

**Two accuracy numbers matter here, and both are reported honestly:**

- **~94% cross-validated accuracy** on the training dataset (5-fold stratified cross-validation)
- **62.5% accuracy** on 24 independently written test phrases I wrote myself, covering every disease category, using natural phrasing rather than the dataset's own style

That gap is a textbook **generalization problem** — the model performs well on data similar to what it was trained on, but less reliably on genuinely novel phrasing. This is exactly why the system doesn't just output a confident-sounding answer every time.

**The confidence gate:** predictions below a probability threshold are shown as "no clear match — see a General Physician" instead of a specific (and possibly wrong) disease. The system is designed to know when it doesn't know, rather than presenting every guess as objectively true.

**The LLM's actual job:** Groq's Llama 3 model is used *only* to explain the classifier's prediction in natural language — it never makes the diagnosis itself and is explicitly prompted not to override the model's output. This separation matters: an LLM asked to diagnose directly can hallucinate a different answer on every call, while a trained, evaluated classifier gives a consistent, auditable prediction that the LLM then explains in plain English.

---

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Django 6.0, Python 3.14 |
| Database | SQLite (dev) |
| ML | scikit-learn (TF-IDF, Linear SVM), joblib for model persistence |
| LLM | Groq API (Llama 3) |
| Frontend | Hand-written HTML/CSS/JS — no framework |
| Auth | Django's built-in auth, extended with a custom `User` model and `role` field |

---

## Architecture notes

- **Custom `User` model** (`accounts.User`) extends Django's `AbstractUser` with a `role` field (`patient` / `doctor` / `admin`), set up before the first migration as Django requires.
- **Doctor accounts are optional.** The `Doctor` model has a nullable `OneToOneField` to `User` — a doctor can exist as a listing without a login, or be linked to a real account for portal access. Admins can create both at once.
- **Access control is enforced server-side**, not just hidden in the UI. Doctors and patients each get `@login_required`-style decorators that check role and redirect appropriately; a doctor account cannot book appointments, and a patient account cannot access `/doctors/`.
- **Availability checking** uses a `DoctorTimeSlot` model. The booking form validates against a doctor's actual weekly slots and rejects double-bookings at the same exact time, server-side, in the form's `clean()` method — not just client-side.
- **Messages and prescriptions** are tied to a specific `Appointment`, not floating independently, so conversations and prescriptions are always scoped to the visit they belong to.

---

## Project structure

```
PocketDoctor/
├── accounts/       # Custom User model, signup/login/logout
├── appointments/   # Doctor, Appointment, Message, Prescription models + patient-facing booking
├── triage/         # ML model loading, prediction, LLM explanation layer
├── doctors/        # Doctor portal: dashboard, messaging, prescriptions, availability
├── staffadmin/     # Admin dashboard: stats, doctor/patient management
├── core/           # Project settings, root URLs
├── ml/             # Model training script (train_triage_model.py)
├── ml_data/        # Dataset + trained model files (.joblib)
├── static/         # CSS, JS
└── templates/      # Shared templates (base, home)
```

---

## Running it locally

**1. Clone and set up a virtual environment**
```bash
git clone https://github.com/yogeshpan1/PocketDoctor.git
cd PocketDoctor
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up environment variables**

Create a `.env` file in the project root:
```
SECRET_KEY=your-django-secret-key-here
DEBUG=True
GROQ_API_KEY=your-groq-api-key-here
```
Get a free Groq API key at [console.groq.com](https://console.groq.com).

**4. Run migrations**
```bash
python manage.py migrate
```

**5. Create a superuser (admin account)**
```bash
python manage.py createsuperuser
```
This account can log in and will be redirected to `/staff/` automatically.

**6. (Optional) Retrain the ML model**

A trained model is already included in `ml_data/`, so this step isn't required to run the app. To retrain from scratch:
```bash
python ml/train_triage_model.py
```

**7. Run the server**
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/`.

---

## Creating a doctor account

Doctors aren't self-service — an admin creates them. Two ways:

**Via the admin dashboard** (recommended): log in as a superuser, go to `/staff/doctors/add/`, and optionally provide a username/password to create a login account at the same time as the doctor listing.

**Via the Django shell** (for scripting/testing):
```python
python manage.py shell
```
```python
from accounts.models import User
from appointments.models import Doctor

doc_user = User.objects.create_user(username='dr_example', password='SecurePass123!', role='doctor')
doctor = Doctor.objects.create(name='Example Doctor', department='cardiology')
doctor.user = doc_user
doctor.save()
```

---

## Known limitations

- The triage model's real-world accuracy (62.5% on independent test phrasing) is meaningfully lower than its cross-validated benchmark (~94%) — documented above, not hidden. It's a lightweight triage aid, not a diagnostic tool.
- Only 24 disease categories are covered — anything outside that scope (injuries, rare conditions, etc.) correctly falls back to "no clear match" rather than a wrong guess, but isn't a full symptom checker.
- No real-time notifications — the app is refresh-based rather than using WebSockets or polling.
- SQLite is used for development; a production deployment would move to PostgreSQL.

---

## Credits

Built as a portfolio project by Yogesh Pant.
