# D1 Softball Stats - Deployment Guide

## Overview
This guide will help you deploy the D1 Softball Stats site to your GoDaddy hosting account.

## Prerequisites
- GoDaddy hosting account with FTP access
- FTP credentials (hostname, username, password)
- Windows computer (for the batch script)

## Step 1: Get Your GoDaddy FTP Information

1. Log into your GoDaddy account
2. Go to your hosting control panel
3. Look for "FTP Management" or "File Manager"
4. Note down:
   - FTP Hostname (usually something like `ftp.yourdomain.com`)
   - FTP Username
   - FTP Password
   - Document root directory (usually `public_html`)

## Step 2: Prepare the Deployment

1. Open `deploy_to_godaddy.bat` in a text editor
2. Replace the placeholder variables at the top:
   ```batch
   set FTP_HOST=ftp.yourdomain.com
   set FTP_USERNAME=your_username
   set FTP_PASSWORD=your_password
   set FTP_DIRECTORY=public_html/stats
   ```

## Step 3: Generate and Upload

1. Run the deployment script:
   ```batch
   deploy_to_godaddy.bat
   ```

2. The script will:
   - Generate the static site from your CSV data
   - Create an FTP upload script
   - Upload all files to your GoDaddy server

## Step 4: Test the Live Site

1. Visit your site at: `http://yourdomain.com/stats/`
2. Test all the main features:
   - Players page with search and sorting
   - Individual player details
   - Seasons page
   - Team standings
   - Game results
   - Player game logs

## Step 5: Link from Main D1 Site

Add a link to your main D1 website pointing to:
```
http://yourdomain.com/stats/
```

## Alternative: Manual Upload

If the batch script doesn't work, you can manually upload:

1. **Generate the site:**
   ```bash
   python generate_static_site.py
   ```

2. **Use an FTP client** (like FileZilla, WinSCP, or GoDaddy's File Manager):
   - Connect to your FTP server
   - Navigate to `public_html/stats/` (create the directory if needed)
   - Upload all files from the `site/` directory

## File Structure on Server

Your GoDaddy server should have this structure:
```
public_html/
└── stats/
    ├── index.html
    ├── players/
    │   ├── 1.html
    │   ├── 2.html
    │   └── ... (all player pages)
    └── seasons/
        ├── index.html
        ├── W24.html
        ├── S15.html
        └── ... (all season pages)
```

## Troubleshooting

### Common Issues:

1. **"Permission Denied" errors:**
   - Make sure you're uploading to the correct directory
   - Check that your FTP user has write permissions

2. **Files not showing up:**
   - Verify the files uploaded to the correct location
   - Check file permissions (should be 644 for HTML files)

3. **Links not working:**
   - Make sure all relative paths are correct
   - Test that the directory structure matches the local site

4. **CSS/JavaScript not loading:**
   - The site uses inline CSS/JS, so this shouldn't be an issue

## Security Notes

- Delete the `deploy_to_godaddy.bat` file after successful deployment
- Don't commit FTP credentials to version control
- Consider using SFTP instead of FTP for better security

## Updating the Site

To update the live site with new data:

1. Update your CSV files in the `data/` directory
2. Run the deployment script again
3. The new files will overwrite the old ones

## Support

If you encounter issues:
1. Check the GoDaddy hosting logs
2. Verify FTP credentials are correct
3. Test with a simple HTML file first
4. Contact GoDaddy support if FTP access isn't working 