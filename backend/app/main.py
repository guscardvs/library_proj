import uvicorn
from api.asgi import get_asgi_application

app = get_asgi_application()


def main():
    uvicorn.run("main:app", host="0.0.0.0", port=3333, reload=True)


if __name__ == "__main__":
    main()
