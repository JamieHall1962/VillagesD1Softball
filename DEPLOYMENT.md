# D1 Softball Stats App - Deployment Guide

## Quick Deploy to Render (Recommended)

1. **Fork or clone this repository** to your GitHub account

2. **Sign up for Render** at https://render.com (free tier available)

3. **Create a new Web Service**:
   - Connect your GitHub repository
   - Select the `clean-backup-20250706` branch
   - Render will automatically detect the `render.yaml` configuration

4. **Deploy** - Render will automatically:
   - Install Python dependencies
   - Build the application
   - Deploy to a live URL

## Manual Deployment

### Prerequisites
- Python 3.8+
- Git

### Local Development
```bash
# Clone the repository
git clone https://github.com/your-username/VillagesD1Softball.git
cd VillagesD1Softball

# Install dependencies
cd apps/drill_down
pip install -r requirements.txt

# Run the app
python simple_csv_app.py

# Visit http://localhost:5000
```

### Other Deployment Options

#### Heroku
1. Create a `Procfile`:
   ```
   web: cd apps/drill_down && python simple_csv_app.py
   ```

2. Deploy using Heroku CLI or GitHub integration

#### Railway
1. Connect your GitHub repository
2. Railway will auto-detect the Python app
3. Set the start command: `cd apps/drill_down && python simple_csv_app.py`

#### Vercel
1. Create a `vercel.json`:
   ```json
   {
     "builds": [
       {
         "src": "apps/drill_down/simple_csv_app.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "apps/drill_down/simple_csv_app.py"
       }
     ]
   }
   ```

## Environment Variables

The app currently doesn't require any environment variables, but you can add:
- `FLASK_ENV=production` for production mode
- `PORT=5000` for custom port (Render sets this automatically)

## Data Files

All CSV data files are included in `apps/drill_down/data/` and will be deployed with the application.

## Support

If you encounter issues:
1. Check the Render logs for error messages
2. Verify all dependencies are in `requirements.txt`
3. Ensure the start command is correct for your platform 