<div align="center">

<img src="flowdesk_crm/static/assets/images/flow-logo-full.png" alt="FlowDesk CRM Logo" width="220"/>

# FlowDesk CRM

**A powerful, all-in-one CRM built for training institutes and educational centers.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://mysql.com)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)](https://getbootstrap.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

</div>

---

## Overview

FlowDesk CRM is a full-featured Customer Relationship Management system designed specifically for **training institutes, coaching centers, and educational organizations**. It streamlines the entire student lifecycle — from lead capture to course completion — in one unified platform.

---

## Features

### Lead & Enquiry Management
- Capture and track student enquiries with detailed profiles
- Lead type classification — New, Hot, Warm, Cold, DNP, Done
- Multi-course interest tracking per lead
- Campaign tracking (name, adset, content)
- Follow-up scheduling with status management (Pending / Completed / Cancelled)
- Lead activity log for full audit trail

### Student Management
- Convert leads to enrolled students seamlessly
- Manage student profiles with address, contact, and enrollment details
- Track student status — Enrolled, Active, Completed, Dropped

### Batch & Course Management
- Create and manage batches with trainer assignment
- Support for Online, Offline, and Hybrid modes
- Seat capacity tracking with real-time availability
- Course-wise module and topic syllabus management
- Trainer specialization mapping

### Fee & Payment Management
- Flexible fee structure with installment plans
- Advance payment tracking with configurable minimum amounts
- Auto-allocation of payments to installments
- Payment modes — Cash, UPI, Card, Bank Transfer
- Fee status tracking — Pending, Partial, Paid, Overdue
- Invoice generation

### Attendance & Session Tracking
- Mark daily attendance — Present, Late, Leave, Absent
- Full-day / Half-day duration support
- Session updates with assignment tracking
- Topic progress tracking per batch

### Exams & Assignments
- Create exams with question papers and multi-part structure
- Record and track student exam performance
- Assignment creation, distribution, and submission tracking

### Email Notifications
- Automated emails for batch assignments, payment confirmations, and overdue fees
- Mail log with sent/failed status tracking
- Pending mail queue management
- Configurable SMTP with fallback to console backend

### Reports & Analytics
- Lead reports, student reports, payment reports
- Batch, course, exam, and assignment reports
- Individual student performance reports
- Trainer attendance and syllabus reports

### Role-Based Access Control
- Roles — Admin, Trainer, CRE (Customer Relationship Executive)
- Route-level access control via decorators and middleware
- Session timeout and browser-close expiry for security

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Django |
| Database | MySQL |
| Frontend | Bootstrap 5, jQuery, ApexCharts |
| UI Components | Select2, SweetAlert2, DataTables, Quill Editor |
| Email | Django Email (SMTP / Console) |
| Auth | Django Auth + Custom Role System |

---

## Project Structure

```
FlowDesk-CRM/
├── flowdesk_crm/
│   ├── core/                   # Main application
│   │   ├── migrations/         # Database migrations
│   │   ├── templates/          # HTML templates
│   │   │   ├── auth/           # Password reset pages
│   │   │   ├── email/          # Email templates
│   │   │   └── reports/        # Report pages
│   │   ├── templatetags/       # Custom template filters
│   │   ├── models.py           # All data models
│   │   ├── views.py            # View logic
│   │   ├── forms.py            # Django forms
│   │   ├── urls.py             # URL routing
│   │   ├── decorators.py       # Role-based access decorators
│   │   └── middleware.py       # Custom middleware
│   ├── flowdesk_crm/           # Django project settings
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── static/                 # Static assets (CSS, JS, images)
│   └── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- MySQL 8.0+
- pip

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/<your-username>/FlowDesk-CRM.git
cd FlowDesk-CRM
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file inside the `flowdesk_crm/` folder:
```env
# Database
DB_NAME=crm_db
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306

# Email (optional — falls back to console if not set)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=your_email@gmail.com
```

**5. Create the MySQL database**
```sql
CREATE DATABASE crm_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**6. Run migrations**
```bash
cd flowdesk_crm
python manage.py migrate
```

**7. Create a superuser**
```bash
python manage.py createsuperuser
```

**8. Run the development server**
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

---

## Environment Variables Reference

| Variable | Description | Default |
|---|---|---|
| `DB_NAME` | MySQL database name | `crm_db` |
| `DB_USER` | MySQL username | `root` |
| `DB_PASSWORD` | MySQL password | — |
| `EMAIL_HOST` | SMTP server host | — |
| `EMAIL_HOST_USER` | SMTP email address | — |
| `EMAIL_HOST_PASSWORD` | SMTP password / app password | — |
| `EMAIL_USE_TLS` | Enable TLS | `True` |

---

## Screenshots

> _Add screenshots of your dashboard, leads page, and reports here._

---

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

<div align="center">

Built with ❤️ using Django & Bootstrap

</div>
