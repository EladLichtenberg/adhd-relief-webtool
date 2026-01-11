# ADHD Relief Web Tool

A full-stack web application designed to help users manage ADHD-related challenges through task tracking, reminders, and structured workflows. The app focuses on simplicity, usability, and reliability, providing users with tools to improve focus and daily organization.

## 🚀 Features
- Secure user authentication with Google OAuth2
- Personal task and activity tracking
- Automated email notifications and reminders
- Clean and responsive user interface
- Persistent data storage with MySQL
- Scalable backend architecture following Clean Code principles

## 🛠 Tech Stack
### Backend
- Python
- Flask
- REST APIs
- Authlib (OAuth2)
- SMTP (Email Notifications)

### Frontend
- JavaScript
- HTML
- CSS

### Database
- MySQL

### Tools & Environment
- Git
- Linux / Unix
- Agile development practices

## 📦 Installation

1. Clone the repository:
```bash
git clone https://github.com/EladLichtenberg/adhd-relief-webtool.git
cd adhd-relief-webtool
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
- Google OAuth credentials
- Database connection details
- SMTP email settings

5. Run the application:
```bash
flask run
```

## ▶️ Usage
- Sign in using Google authentication
- Create and manage tasks tailored to personal workflows
- Receive automated email reminders
- Track progress through a structured and user-friendly interface

## 📂 Project Structure
```
adhd-relief-webtool/
│── app/
│   ├── routes/
│   ├── models/
│   ├── templates/
│   ├── static/
│── config/
│── tests/
│── requirements.txt
│── README.md
```

## 🧪 Testing
- Manual and automated testing performed during development
- Focus on debugging complex flows and maintaining long-term stability

## 🎯 Project Goals
- Help users reduce cognitive overload
- Provide practical tools for ADHD management
- Apply real-world backend development practices
- Demonstrate clean architecture and maintainable code

## 🤝 Contributing
Contributions are welcome.  
Feel free to open issues or submit pull requests for improvements or new features.

## 📄 License
This project is for educational and portfolio purposes.

## 👤 Author
**Elad Lichtenberg**  
Software Developer (B.Sc. Software Engineering)

- GitHub: https://github.com/EladLichtenberg
- LinkedIn: https://www.linkedin.com/in/elad-lichtenberg-8a62bb287/
