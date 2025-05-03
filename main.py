from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0") #Que no sea visible para todo el mundo - para eso usar un host ="0.0.0.0"