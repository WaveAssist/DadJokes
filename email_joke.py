import waveassist
waveassist.init()

joke = waveassist.fetch_data("joke") or "No joke today, but here's a smile anyway 🙂"

# Create simple HTML content for the email
html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Daily Dad Joke</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
    <h2 style="color: #2c3e50; border-bottom: 2px solid #428d4f; padding-bottom: 10px;">
        🤣 Your Daily Dad Joke
    </h2>
    
    <div style="background-color: #f8f9fa; border-left: 4px solid #428d4f; padding: 20px; margin: 20px 0; border-radius: 5px;">
        <p style="font-size: 18px; margin: 0; font-style: italic;">
            "{joke}"
        </p>
    </div>
    
    <p style="color: #7f8c8d; font-size: 14px; text-align: center; margin-top: 30px;">
        Powered by WaveAssist • Have a great day! 😊
    </p>
</body>
</html>
"""

waveassist.send_email(
    subject="Your Daily Dad Joke from WaveAssist",
    html_content=html.strip()
)

waveassist.store_data("email_sent", True)
print("Daily dad joke email sent successfully!")
