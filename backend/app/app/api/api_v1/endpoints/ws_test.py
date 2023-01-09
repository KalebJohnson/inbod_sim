from fastapi import APIRouter, HTTPException, Response, WebSocket
from fastapi.responses import HTMLResponse
import logging

logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print('yo')
    logging.debug('websocket init')
    await websocket.accept()
    while True:
        logging.debug('websock wait')
        message = await websocket.receive_text()
        # log mouse position
        logging.debug(f"received message: {message}")
        print(f"received message: {message}")
print('hi')


@router.get("/", response_class=HTMLResponse)
def serve_static_page():
    html = """
    <!DOCTYPE html>
    <html>
      <head>
        <title>UDP Socket Test</title>
      </head>
      <body>
        <h1>UDP Socket Test</h1>
        <form id="form">
          <button type="submit" id="button">Send</button>
        </form> 
      </body>
      <script>
        const form = document.getElementById("form");
        const button = document.getElementById("button");
        let sending = false;
        let sendHandler;
        form.addEventListener("submit", e => {
          e.preventDefault();
          if (!sending) {
            sendUdpMessage();
            sending = true;
            button.textContent = "Stop";
          } else {
            stopSendingUdpMessage();
            sending = false;
            button.textContent = "Send";
          }
        });
  
        function sendUdpMessage() {
          const socket = new WebSocket("ws://localhost/api/v1/ws_test/ws");
          socket.onopen = () => {
            sendHandler = e => {
              socket.send(e.clientX + "," + e.clientY);
            };
            window.addEventListener("mousemove", sendHandler);
          };
        }
  
        function stopSendingUdpMessage() {
          window.removeEventListener("mousemove", sendHandler);
        }
      </script>
    </html>
    """
    return HTMLResponse(html)