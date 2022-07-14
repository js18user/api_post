import uvicorn
import api_control
if __name__ == "__main__":
    uvicorn.run('api_control:app', host='localhost', port=8000, )
