# Kudos System Specification

## Overview
An internal employee portal feature enabling colleagues to recognize and appreciate one another through public "Kudos" messages, backed by administrative content moderation capabilities.

---

## Functional Requirements

### User Stories

1. **User Authentication & Authorization**: As a user, I can log into the system with my corporate credentials and be assigned a role (Employee or Administrator).
2. **Colleague Selection**: As a user, I can select another user from a searchable dropdown list of colleagues.
3. **Kudos Creation & Submission**: As a user, I can write a short message of appreciation (max 500 characters) to a selected colleague and submit it.
4. **Public Feed Display**: As a user, I can view a public feed on the main dashboard displaying recently submitted, visible kudos in real-time.
5. **Content Moderation**: As an administrator, I can view all submitted kudos, including hidden ones, and hide or delete inappropriate kudos messages.
6. **Input Validation & Error Handling**: As a user, I receive clear error messages if I submit empty messages, exceed character limits, or select invalid recipients.
7. **Responsive Design**: As a user, I can access and use the Kudos portal seamlessly across desktop, tablet, and mobile screen sizes.

### Acceptance Criteria

- **User Story 1**: Unauthenticated users are redirected to login. Employees can give kudos; only users with the `admin` role can access the moderation dashboard.
- **User Story 2**: The recipient dropdown lists all active users except the currently logged-in user.
- **User Story 3**: Submitting kudos successfully clears the form, increments success counters, and instantly updates the public dashboard feed.
- **User Story 4**: The dashboard feed shows sender name, recipient name, timestamp, message body, and category/badge if applicable, omitting any records where `is_visible = false`.
- **User Story 5**: Administrators can toggle `is_visible` to `false` (hide) or permanently delete records, with audit fields (`moderated_by`, `moderated_at`) updated automatically.
- **User Story 6**: Client-side and server-side validation reject messages over 500 characters or containing malicious scripts.

---

## Technical Design

### Database Schema

SQLite / PostgreSQL relational schema:

1. **Users Table**
   - `id` (INTEGER, Primary Key)
   - `username` (VARCHAR, Unique, Not Null)
   - `name` (VARCHAR, Not Null)
   - `role` (VARCHAR, Default: 'employee') — 'employee' or 'admin'

2. **Kudos Table**
   - `id` (INTEGER, Primary Key)
   - `sender_id` (INTEGER, Foreign Key referencing Users.id)
   - `recipient_id` (INTEGER, Foreign Key referencing Users.id)
   - `message` (TEXT, Not Null, Max 500 chars)
   - `created_at` (DATETIME, Default: CURRENT_TIMESTAMP)
   - `is_visible` (BOOLEAN, Default: TRUE)
   - `moderated_by` (INTEGER, Nullable, Foreign Key referencing Users.id)
   - `moderated_at` (DATETIME, Nullable)

### API Endpoints

- `GET /api/users`: Retrieve list of active colleagues for selection.
- `GET /api/kudos`: Retrieve public feed of recent visible kudos.
- `POST /api/kudos`: Submit a new kudos message (`sender_id`, `recipient_id`, `message`).
- `GET /api/admin/kudos`: Retrieve all kudos (visible and hidden) for moderation (Admin only).
- `POST /api/admin/kudos/<id>/moderate`: Hide, unhide, or delete a specific kudos entry (Admin only).

### Frontend Components

- **Navigation Bar**: Displays current user context and navigation links (Dashboard vs. Admin Portal).
- **Kudos Submission Form**: Interactive dropdown for recipient selection, textarea with live character counter, and submit button.
- **Kudos Feed Component**: Card-based grid layout rendering recent appreciations with timestamps and smooth transitions.
- **Admin Moderation Table**: Tabular view with action buttons (`Hide`, `Delete`) for content management.

### Security, Performance & Error Handling

- **Security**: Password hashing (bcrypt), parameterized SQL queries via SQLAlchemy ORM to prevent SQL injection, and HTML sanitization for XSS prevention.
- **Performance**: Indexed foreign keys (`sender_id`, `recipient_id`) and timestamp columns; server-side pagination for feeds exceeding 50 items.
- **Error Handling**: Graceful error catching on API requests with structured JSON error responses and user-friendly toast notifications.

---

## Implementation Plan

### Step-by-Step Task Breakdown

1. **Environment Setup**: Initialize Python virtual environment, install dependencies (`Flask`, `Flask-SQLAlchemy`), and structure project directories (`templates`, `static`).
2. **Database Models**: Implement SQLAlchemy models for `User` and `Kudos` with all required moderation fields (`is_visible`, `moderated_by`, etc.).
3. **Core API Routes**: Develop endpoints for retrieving users, submitting kudos, and fetching the public feed.
4. **Moderation API & Views**: Build administrator endpoints and views to handle hiding/deleting inappropriate content.
5. **Frontend UI**: Design responsive dashboard and admin templates using HTML/CSS (Bootstrap/Tailwind).
6. **Testing & Validation**: Write unit tests verifying kudos creation, pagination, character limits, and admin moderation toggles.