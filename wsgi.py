from application import create_app

app = create_app()

if __name__ == '__main__':
    
    app.run(
		# host        = '127.0.0.1', # '0.0.0.0',
		host        = '0.0.0.0',
        port        = 443,
        ssl_context = ('./application//static//ssl//cert.pem', './application//static//ssl/key.pem'),
        use_reloader= False
    )