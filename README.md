# 📊 BrokerMint - Financial Compliance Dashboard

**BrokerMint** is an intelligent and user-friendly **financial compliance dashboard** built for brokerage firms and regulators.  
It provides **real-time monitoring** of trading activities, ensures **regulatory compliance**, and helps organizations mitigate risks by detecting anomalies and verifying client identities.  

With a combination of **machine learning**, **data visualization**, and **compliance automation**, BrokerMint acts as a centralized hub for:  

- Tracking suspicious trading patterns  
- Automating **eKYC (Know Your Customer)** checks  
- Maintaining an immutable **audit trail** of all activities  
- Generating compliance-ready reports for auditors and regulators  

Designed with **scalability** and **security** in mind, BrokerMint is suitable for both small brokerage firms and large financial enterprises.  
Its **responsive web interface** makes it accessible across devices, ensuring compliance officers, analysts, and regulators can act quickly and efficiently from anywhere.

---

## 🚀 Features

- **Dashboard Overview** – Real-time statistics and compliance metrics  
- **Anomaly Detection** – Identify suspicious trading patterns using ML models  
- **eKYC Verification** – Electronic Know Your Customer identity verification  
- **Compliance Reports** – Generate regulatory compliance reports for auditing  
- **Audit Trail** – Track all system activities and user actions  
- **Responsive Design** – Works seamlessly on **desktop** and **mobile devices**

---

## 🛠️ Tech Stack

### Backend
- [Flask](https://flask.palletsprojects.com/) – REST API backend  
- [Flask-CORS](https://flask-cors.readthedocs.io/) – Cross-Origin Resource Sharing  
- [Pandas](https://pandas.pydata.org/) – Data processing  
- [NumPy](https://numpy.org/) – Numerical computations  
- [Scikit-learn](https://scikit-learn.org/) – Machine learning for anomaly detection  
- [bcrypt](https://pypi.org/project/bcrypt/) – Secure password hashing  
- [PyJWT](https://pyjwt.readthedocs.io/) – JWT authentication  
- [python-dotenv](https://pypi.org/project/python-dotenv/) – Environment variable management  
- [SQLite3](https://www.sqlite.org/index.html) – Lightweight database  

### Frontend
- [React 18](https://react.dev/) – Frontend framework  
- [React DOM](https://react.dev/)  
- [React Router DOM](https://reactrouter.com/) – Routing  
- [Axios](https://axios-http.com/) – API requests  
- [Bootstrap 5](https://getbootstrap.com/) – Styling framework  
- [React Bootstrap](https://react-bootstrap.github.io/) – UI components  

---

## ⚙️ Installation & Setup

Follow the steps below to run **BrokerMint** locally.

---

### Clone the Repository
```bash
git clone https://github.com/your-username/BrokerMint.git
cd BrokerMint
```

### Backend Setup

```bash
# Navigate to backend folder
cd backend

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows (PowerShell):
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the Flask server
flask run
```

### Frontend Setup

```bash
# Open a new terminal & navigate to frontend folder
cd frontend

# Install dependencies
npm install

# Start the React development server
npm start
```

### Environment Variables

Create a .env file in the backend folder with the following (example):

```bash
SECRET_KEY=your_jwt_secret_key
DATABASE_URL=sqlite:///brokermint.db
```


## 📹 Video Demonstration

# Demo

![App Demo](demo/demo.gif)