import Network
import Char
import Control.Concurrent
import System.IO (hGetChar, hGetLine, hClose, hPutStr, hSetBuffering, BufferMode(..), Handle,stdout)


main = withSocketsDo $ do
	putStrLn "Welcome to my haskell websocket example"
	hSetBuffering stdout NoBuffering
	server --or client
	putStrLn "Done"
	
	
	
--client
client = putStrLn("Not Yet")

--server
server = do
	sock <- listenOn (PortNumber 1234)
	putStrLn("Listening...")
	(h, host, port) <- accept sock --Accept the socket
	putStrLn $ "connection!"
	hSetBuffering h NoBuffering
	putStrLn "Handshaking..."
	handShake h
	putStrLn "Handshaken!"
	--forkIO $ doTick h 0 --Not yet
	wsInteract h sock 0
	putStrLn "Stopping Server" 
	hClose h
	sClose sock

wsInteract :: Handle -> Socket -> Int -> IO ()
wsInteract h s tick = do
	stuff <- receive h ""
	wsSend h $ "out ! "++stuff
	doTick h tick
	wsInteract h s (tick + 1)
	
doTick :: Handle -> Int -> IO ()
doTick h tick = do
	wsSend h $ "clock ! tick"++show(tick)

handShake h = do
	stuff <- hGetLine h
	putStrLn $ "Handshake got: "++stuff
	stuff <- hGetLine h
	putStrLn $ "Handshake got: "++stuff
	stuff <- hGetLine h
	putStrLn $ "Handshake got: "++stuff
	stuff <- hGetLine h
	putStrLn $ "Handshake got: "++stuff
	stuff <- hGetLine h
	putStrLn $ "Handshake got: "++stuff
	stuff <- hGetLine h
	putStrLn $ "Handshake got: "++stuff
	putStrLn "Done getting header - now sending ours"
	hPutStr h "HTTP/1.1 101 Web Socket Protocol Handshake\r\nUpgrade: WebSocket\r\nConnection: Upgrade\r\nWebSocket-Origin: http://localhost:8888\r\nWebSocket-Location: ws://localhost:1234/websession\r\n\r\n"

wsSend :: Handle -> String -> IO ()
wsSend h str = do
	putStr "wsSending: "
	putStrLn str
	hPutStr h $ "\x00"++str++"\xff"
	
receive h str = do
	new <- hGetChar h
	putChar new
	if new == chr 0 -- "\x00"
		then receive h ""
		else if new == chr 255 --"\xff"
		then return str
		else receive h (str++[new])
	