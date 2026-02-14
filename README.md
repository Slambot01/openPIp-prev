# openPIP 2.0 Preview

**A Modern Protein Interaction Platform - GSoC 2026 Proof of Concept**

> Complete rewrite of openPIP using Django, React, and Docker - demonstrating a modern tech stack for protein interaction data management.

[![Django](https://img.shields.io/badge/Django-6.0-green.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9-blue.svg)](https://www.typescriptlang.org/)
[![Material-UI](https://img.shields.io/badge/Material--UI-7.0-blue.svg)](https://mui.com/)

---

## 🎯 Project Overview

This is a proof-of-concept for **openPIP 2.0**, a complete modernization of the legacy PHP/Symfony openPIP system. Built as part of a GSoC 2026 proposal, this POC demonstrates:

- ✅ **Modern Backend**: Django 6.0 + Django REST Framework
- ✅ **Modern Frontend**: React 18 + TypeScript + Material-UI
- ✅ **Real-time Search**: Fast protein search across gene names, UniProt IDs, and descriptions
- ✅ **RESTful API**: Well-documented API endpoints with pagination
- ✅ **Clean Architecture**: Separation of concerns, type safety, professional code structure

---

## 🚀 Features

### Backend (Django)
- **Protein Data Model**: Gene names, UniProt IDs, Ensembl IDs, Entrez IDs, descriptions, sequences
- **REST API**: Full CRUD operations with search and filtering
- **Search Functionality**: Multi-field search across protein attributes
- **Admin Panel**: Django admin for easy data management
- **CORS Enabled**: Ready for frontend integration

### Frontend (React)
- **Real-time Search**: Instant protein search as you type
- **Interactive Detail View**: Click any protein row to see full details in a modal
- **External Links**: Direct links to UniProt, Ensembl, and NCBI databases
- **Clean UI**: Professional, minimal design with Material-UI
- **TypeScript**: Full type safety for better code quality
- **Responsive**: Works on desktop and mobile
- **Error Handling**: Graceful error states and loading indicators

---

## 📸 Screenshots

### Search Interface
<img width="1917" height="871" alt="image" src="https://github.com/user-attachments/assets/53da13a8-6f23-4bdf-99e9-a8cdbfad0652" />
<img width="1898" height="868" alt="image" src="https://github.com/user-attachments/assets/106ac11a-808c-4991-81e8-2883ea78b0a6" />
<img width="1915" height="870" alt="image" src="https://github.com/user-attachments/assets/d79aaccf-2259-474b-9d7a-f98592ae3ae6" />


---

## 🛠️ Tech Stack

### Backend
- **Framework**: Django 6.0.2
- **API**: Django REST Framework 3.16
- **Database**: SQLite (easily upgradable to PostgreSQL)
- **CORS**: django-cors-headers

### Frontend
- **Framework**: React 18
- **Language**: TypeScript 5.9
- **UI Library**: Material-UI 7.0
- **HTTP Client**: Axios
- **Build Tool**: Vite 7.3

---

## 🏃 Quick Start

### Prerequisites
- Python 3.13+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\Activate
# On Mac/Linux: source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Load sample data
python manage.py load_sample_proteins

# Start Django server
python manage.py runserver
```

Backend will be running at: **http://127.0.0.1:8000**

API endpoint: **http://127.0.0.1:8000/api/proteins/**

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be running at: **http://localhost:5173**

---

## 📡 API Endpoints

### List/Search Proteins
```
GET /api/proteins/
GET /api/proteins/?search=TP53
```

**Response:**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "gene_name": "TP53",
      "protein_name": "Cellular tumor antigen p53",
      "uniprot_id": "P04637",
      "ensembl_id": "ENSG00000141510",
      "entrez_id": "7157",
      "description": "Acts as a tumor suppressor in many tumor types",
      "sequence": "",
      "created_at": "2026-02-13T12:00:00Z",
      "updated_at": "2026-02-13T12:00:00Z"
    }
  ]
}
```

### Get Single Protein
```
GET /api/proteins/{id}/
```

### Create Protein
```
POST /api/proteins/
Content-Type: application/json

{
  "gene_name": "EGFR",
  "protein_name": "Epidermal growth factor receptor",
  "uniprot_id": "P00533",
  "description": "Receptor tyrosine kinase"
}
```

---

## 📂 Project Structure

```
openpip-2.0-preview/
├── backend/
│   ├── openpip/              # Django project settings
│   ├── proteins/             # Proteins Django app
│   │   ├── models.py         # Protein data model
│   │   ├── serializers.py    # DRF serializers
│   │   ├── views.py          # API endpoints
│   │   ├── urls.py           # URL routing
│   │   └── management/       # Custom commands
│   ├── manage.py
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── api/              # API client
    │   ├── App.tsx           # Main component
    │   └── main.tsx          # Entry point
    ├── package.json
    └── vite.config.ts
```

---

## 🎓 GSoC 2026 Context

This POC was built to demonstrate capability for the **openPIP 2.0 Rewrite** project. It shows:

1. **Technical Proficiency**: Full-stack development with modern frameworks
2. **Quick Execution**: Complete POC built in ~4 hours
3. **Professional Standards**: Clean code, type safety, documentation
4. **Understanding of Domain**: Protein interaction data models and requirements

### Planned Features for Full openPIP 2.0
- Network visualization with Cytoscape.js
- PSI-MI TAB file parser and CSV upload
- User authentication and permissions
- Interaction data models
- Advanced filtering and analytics
- Docker containerization
- PostgreSQL database
- Production deployment

---

## 🧪 Testing

### Test the API
```bash
# With Django server running, visit:
http://127.0.0.1:8000/api/proteins/

# Or use curl:
curl http://127.0.0.1:8000/api/proteins/?search=TP53
```

### Test the Frontend
1. Start both backend and frontend servers
2. Open http://localhost:5173
3. Type "TP53" in the search box
4. Results should appear instantly

---

## 📝 Sample Data

The POC includes 5 sample proteins:
- **TP53** - Cellular tumor antigen p53
- **BRCA1** - Breast cancer type 1 susceptibility protein
- **EGFR** - Epidermal growth factor receptor
- **MYC** - Myc proto-oncogene protein
- **KRAS** - GTPase KRas

Load with: `python manage.py load_sample_proteins`

---

## 🔮 Roadmap & Planned Features

### ✅ Completed (POC - Day 1 & 2)

**Backend:**
- [x] Django 6.0 + REST Framework setup
- [x] Protein data model with full schema
- [x] RESTful API with CRUD operations
- [x] Multi-field search functionality
- [x] Django admin panel
- [x] CORS configuration
- [x] Sample data loader

**Frontend:**
- [x] React 18 + TypeScript + Vite setup
- [x] Material-UI integration
- [x] Real-time search interface
- [x] Type-safe API client
- [x] Protein results table
- [x] **Protein detail modal** - Click-to-view full details
- [x] External database links (UniProt, Ensembl, NCBI)
- [x] Error handling and loading states
- [x] Professional, minimal UI design

---

### 🚧 Planned Enhancements (Next Iterations)

**Frontend Features:**
- [ ] **Network visualization** - Cytoscape.js for interaction networks
- [ ] **Advanced filters** - Filter by organism, interaction count, etc.
- [ ] **Sorting controls** - Sort by gene name, date, relevance
- [ ] **Pagination UI** - Navigate through large result sets
- [ ] **Export functionality** - Download results as CSV/JSON
- [ ] **Dark mode toggle** - User preference for color scheme
- [ ] **Protein comparison** - Side-by-side comparison view
- [ ] **Recent searches** - History of user searches

**Backend Features:**
- [ ] **Interaction model** - Protein-protein interactions
- [ ] **PSI-MI TAB parser** - Import standard interaction data format
- [ ] **CSV upload** - Bulk protein/interaction upload
- [ ] **User authentication** - Django auth with JWT tokens
- [ ] **PostgreSQL migration** - Production-ready database
- [ ] **API versioning** - v1, v2 endpoints
- [ ] **Rate limiting** - Prevent API abuse
- [ ] **Caching layer** - Redis for performance
- [ ] **Full-text search** - PostgreSQL full-text or Elasticsearch

**DevOps & Infrastructure:**
- [ ] **Docker Compose** - One-command deployment
- [ ] **CI/CD pipeline** - GitHub Actions for testing/deployment
- [ ] **Unit tests** - Backend and frontend test coverage
- [ ] **Integration tests** - End-to-end testing
- [ ] **API documentation** - Swagger/OpenAPI spec
- [ ] **Performance monitoring** - Logging and metrics
- [ ] **Production deployment** - AWS/GCP/Heroku setup

---

## 👨‍💻 Author

**Ritesh Pandit**
- GitHub: [@Slambot01](https://github.com/Slambot01)
- Built for: GSoC 2026 - openPIP 2.0 Rewrite

---

## 📄 License

This project is part of the openPIP ecosystem. See the main [openPIP repository](https://github.com/BaderLab/openPIP) for license information.

---

## 🙏 Acknowledgments

- Original openPIP team at BaderLab
- NRNB (National Resource for Network Biology)
- GSoC Program

---




