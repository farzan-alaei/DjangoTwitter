# DjangoTwitter

Hey there! Welcome to **DjangoTwitter**, a project I passionately crafted as part of my journey through the **Daneshkar
Bootcamp**. This is my take on building a simplified version of Twitter, showcasing what I’ve learned in backend
development with **Django**.

## 🐦 What’s Inside?

- **Backend**: Built with Django REST Framework, providing a powerful API that lets users create and manage tweets.
- **User Authentication**: Secure user login and registration to keep everything safe and sound.
- **Tweet Management**: Users can create, read, update, and delete their tweets, just like in Twitter!
- **Follow System**: Users can follow each other to keep up with their friends' tweets and interactions.

## 🛠 Tech Stack

- **Django REST Framework**: For the backend API, making it robust and scalable.
- **SQLite**: A simple database that’s perfect for this project (but you can easily switch to PostgreSQL if needed).
- **JWT**: For secure authentication and session management.

## 💡 Why I Built This

I’ve always been fascinated by social media and the way it connects people. With this project, I wanted to explore the
fundamentals of how platforms like Twitter operate. It was an exciting challenge to recreate essential features, and I
learned so much about backend development along the way.

Even though it’s not a fully-fledged Twitter clone, this project reflects my journey and growth as a developer. I had a
lot of fun building it, and it pushed me to enhance my skills in API design and user management.

## 🚀 How to Get it Running

### Manual Setup

If you want to run the project locally, follow these steps:

#### Backend Setup:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/farzan-alaei/DjangoTwitter.git
   ```

2. **Navigate to the backend directory and set up a virtual environment**:
   ```bash
   cd DjangoTwitter
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install the requirements**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the migrations and start the server**:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

## 🔮 What’s Next?

- Improving the frontend design for a better user experience.
- Adding features like direct messaging and notifications.
- Expanding the following system to enhance user engagement.
- Writing more tests to ensure everything runs smoothly.