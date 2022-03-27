# Auth API
An authentication API made using python. (Uses JWT)

### Features
- JWT token generation
- Access token and Refresh token
- Protect routes using token

### Installation
- Clone the repo
- Install postgresql
- Rename `.env.example` to `.env` and put correct credentials
- Install dependencies from `requirements.txt`
- Run `python manage.py initdb` to initialize the database with correct tables defined in `./basicauth/helpers/db.py [schemas, indexes]`
- Edit server and put whatever port you want to run the API server

### Routes
- `/api/auth/register` Register new user
- `/api/auth/authorize` Login user
- `/api/auth/refresh` Generate a new pair of access and refresh token using the refreshToken

