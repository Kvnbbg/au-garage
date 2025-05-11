# Garage V. Parrot Management System  
**Coding, Gaming & Web Development**  
 
*Design Updates: [Canva Project](https://www.canva.com/design/DAGgJLt8Om8/ZPXG_N-ZqK2XL1trXlw2_g/edit?utm_content=DAGgJLt8Om8&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)*  

---

## Introduction  
Garage V. Parrot is a web application developed to modernize operations for automotive service providers. Originally created for Vincent Parrot of Toulouse, this platform now serves as a scalable solution for garage management, combining service tracking, customer engagement, and inventory control.  

---

## Background  
### Project Origin  
![Logo](https://github.com/Kvnbbg/au-garage/blob/main/app/static/images/logo.png)  
Developed as a capstone project during studies at [STUDI](https://studi.com) (2022–2024), this system was designed to digitize workflows for small automotive businesses. The platform emphasizes reliability, user experience, and adaptability to evolving industry demands.  

### Evolution  
The application has transitioned from a local garage tool to a modular solution for modern entrepreneurs, incorporating advanced features like VR integrations and predictive analytics.  

---

## Key Features  
- **Service Management**: Track repairs, maintenance, and vehicle sales.  
- **Inventory Control**: Real-time stock alerts and automated reordering.  
- **Customer Portal**: Direct communication, appointment booking, and invoice generation.  
- **Role-Based Access**: Admin, staff, and mechanic permissions.  
- **Analytics Dashboard**: Performance metrics and reporting tools.  

---

## Technical Overview  
### Architecture  
- **Backend**: Python/Flask with object-oriented design.  
- **Database**: PostgreSQL (migrated via Flask-Migrate).  
- **Frontend**: Responsive UI with dynamic transitions.  
- **Integrations**: SMTP for notifications, payment gateways, and VR tools.  

### Code Standards  
- Modular, reusable components.  
- Comprehensive error handling and logging.  
- RESTful API structure.  

---

## Setup & Deployment  
### Prerequisites  
- Python 3.8+  
- PostgreSQL  
- pip  

### Installation  
```bash  
git clone https://github.com/Kvnbbg/au-garage  
cd au-garage  
python3 -m venv venv  
source venv/bin/activate  # Unix/macOS | For Windows: .\venv\Scripts\activate  
pip install -r requirements.txt  
flask db upgrade  
flask run  
```  
**Configure `.env`**: Include `DATABASE_URL`, `SECRET_KEY`, and SMTP credentials.  

---

## Project Management  
- **Trello**: [Task Tracking](https://trello.com/b/eR2X9dfh)  
- **Live Demo App Running**: [Production Build](https://web-production-d728.up.railway.app/)  
- **Documentation**: See `/STUDI` folder for flowcharts, exam materials, and technical specs.  

---

## Contributions & Licensing  
- **Contributions**: Follow [CONTRIBUTING.md](https://github.com/Kvnbbg/au-garage/CONTRIBUTING.md).  
- **License**: Custom license for commercial/developmental use ([Details](https://github.com/Kvnbbg/au-garage/LICENSE)).  

--- 

![Signature](https://i.imgur.com/wmxtaI7.jpg)  
*Maintained by Kévin Marville | 2025*  
