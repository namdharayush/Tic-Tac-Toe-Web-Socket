# Tic-Tac-Toe with Websocket Connection using Django, Django Channels, and Redis

**Live website** : [tic-tac-toe](https://tic-tac-toe-web-socket-6x2z.onrender.com/game/create-or-join-room)

This real-time multiplayer **Tic-Tac-Toe game** is developed using **Django**, **Django Channels**, **Django REST Framework**, and **Redis** for handling WebSocket connections. Players can create or join game rooms by entering a room code, offering an engaging real-time experience.

## Features

- **Real-time Gameplay**: Achieved through WebSocket communication using Django Channels.
- **Redis**: Used for WebSocket connection management, ensuring efficient handling of concurrent connections.
- **REST API**: Provides endpoints for room creation and game data retrieval.
- **Game Room Creation**: Players can create a room and share the generated room code.
- **Join an Existing Room**: Players can enter an existing room with a valid room code.
- **Automated Game Logic**: The backend handles the game flow, including turn-based mechanics and result determination.

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Django, Django REST Framework, Django Channels
- **Database**: PostgreSQL (or SQLite for development)
- **Real-time Communication**: Redis
- **WebSocket Support**: Django Channels for real-time updates

## Database Setup with PostgreSQL

For production, it's recommended to use PostgreSQL for its robustness and scalability. To configure PostgreSQL for the project:

1. **Install PostgreSQL**: Make sure PostgreSQL is properly installed on your system.
2. **Create a Database**:
    ```bash
    psql -U postgres
    CREATE DATABASE tic_tac_toe;
    ```
3. **Update `settings.py`**: Modify the `DATABASES` setting to use PostgreSQL.
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'tic_tac_toe',
            'USER': 'your_username',
            'PASSWORD': 'your_password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/namdharayush/Tic-Tac-Toe-Web-Socket.git
    cd Tic-Tac-Toe-Web-Socket
    ```

2. **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate     # Windows
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the database**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Run Redis** (make sure Redis is installed):
    ```bash
    redis-server
    ```

6. **Start the Django server**:
    ```bash
    python manage.py runserver
    ```

7. **Start the ASGI server**:
    ```bash
    python -m daphne -p <PORT> <PROJECT_NAME>.asgi:application
    ```

## How to Play

1. **Create a Room**: Click on "Create Room" to generate a unique room code.
2. **Join a Room**: Enter the room code to join an existing game.
3. **Play**: Take turns placing X's and O's. The system detects winners and draws automatically.

## Environment Variables

Create a `.env` file in your project’s root with the following:

```bash
SECRET_KEY=your_secret_key
DEBUG=True  # Set to False in production
REDIS_URL=redis://127.0.0.1:6379  # Adjust based on your Redis setup
DATABASE_URL=postgresql://your_username:your_password@localhost:5432/tic_tac_toe
