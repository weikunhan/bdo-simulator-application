from pyngrok import conf, ngrok

def main():
    ngrok.set_auth_token("2DGOwvm1S7DhJeFSqyhmrGszLfR_72NcMpKWQ28YY8XmsiE3H") 
    public_url = ngrok.connect(8501, bind_tls=True)
    print(public_url)

    ngrok_process = ngrok.get_ngrok_process()

    try:
        # Block until CTRL-C or some other terminating event
        ngrok_process.proc.wait()
    except KeyboardInterrupt:
        print(" Shutting down server.")

        ngrok.kill()

if __name__ == '__main__':
    main()
