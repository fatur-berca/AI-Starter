# 🗺️ Master Index & Context Map

This file serves as the master navigation map for developers, business analysts, QAs, and AI assistants. It maps features to their specifications, UI mockups, database tables, and codebase components.

---

## 🚀 Active Feature Registry

| ID | Feature Name | Spec Document | UI Mockup | DB Tables Involved | Code Components | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **F01** | User Management | [F01-manajemen-user.md](file:///c:/AI%20Starter/docs/features/F01-manajemen-user.md) | [F01-login.html](file:///c:/AI%20Starter/docs/mockups/F01-login.html) | `users`, `roles`, `user_sessions` | `src/controllers/AuthController.js`<br>`src/models/User.js` | 🟢 In Development |
| **F02** | Payment System | [F02-sistem-bayar.md](file:///c:/AI%20Starter/docs/features/F02-sistem-bayar.md) *(Draft)* | *None* | `transactions`, `wallets` | `src/controllers/PaymentController.js`<br>`src/models/Transaction.js` | 🟡 Planning |

---

## 🗄️ Database Schema & References

- **Master SQL Schema**: [01-master-schema.sql](file:///c:/AI%20Starter/docs/database/01-master-schema.sql) — Contains all table structures, relationships, keys, and indexes.
- **Reference Seed Data**: [02-seed-data.sql](file:///c:/AI%20Starter/docs/database/02-seed-data.sql) — Initial lookups, roles, and mock data for development.

---

## 🎨 Centralized UI Mockups

All mockups are located in the [mockups/](file:///c:/AI%20Starter/docs/mockups/) directory and share the [global-style.css](file:///c:/AI%20Starter/docs/mockups/global-style.css).
- [F01-login.html](file:///c:/AI%20Starter/docs/mockups/F01-login.html) — User Login & Registration interface.

---

## 📂 Dokumen Eksternal & Proposal

- **Dokumen Masukan dari User (Client)**: [docs/user-docs/](file:///c:/AI%20Starter/docs/user-docs/) — Tempat dokumen, spesifikasi, atau data excel/pdf asli yang diberikan oleh user/client.
- **Proposal Proyek**: [docs/proposals/](file:///c:/AI%20Starter/docs/proposals/) — Proposal penawaran, proposal fitur, atau solusi bisnis yang dibuat oleh tim (terpisah dari data user).

---

## 🛠️ Program Utilitas (Utilities)

Seluruh skrip dan program pembantu diletakkan di folder [utility/](file:///c:/AI%20Starter/utility/).
- **Markdown to Word (.docx) Converter**: Berisi program python (`md_to_docx.py`, `super_humanized_docs_generator.py`) untuk mengonversi spesifikasi markdown menjadi dokumen Word.

---

## 📊 Repositori Data Uji & Master

- **Data Master**: [data/master/](file:///c:/AI%20Starter/data/master/) — Penyimpanan master data awal.
- **Sample File Upload**: [data/samples/uploads/](file:///c:/AI%20Starter/data/samples/uploads/) — Contoh file (seperti gambar, excel) yang digunakan untuk skenario pengunggahan berkas oleh user.
- **Sample File Output**: [data/samples/outputs/](file:///c:/AI%20Starter/data/samples/outputs/) — Contoh format file hasil eksekusi sistem yang diunduh user.

---

## 🔄 AI Collaboration & Versioning Protocol

### 1. Specs as Code (Docs-as-Code)
All requirements are versioned inside the Git repository. Business Analysts (BAs) check in markdown updates. Developers pull and check diffs before coding.

### 2. Update Protocol
1. **BA Proposes Change**: BA creates a branch `docs/FXX-update` and updates the markdown files (e.g. `docs/features/F01-manajemen-user.md`).
2. **Review & Merge**: Dev and QA review the changes (e.g. database schema impacts, test case impacts) and merge them into `main`.
3. **Dev Pulls & Syncs**: Dev pulls the latest changes. In the AI assistant, the Dev runs:
   ```
   Show me the git diff for docs/features/F01-manajemen-user.md and list what code in src/ needs to be modified.
   ```
4. **Code Update**: Dev updates logic in `src/` and unit tests in `tests/`.
5. **QA Update**: QA updates automated test scripts to reflect new test cases.
