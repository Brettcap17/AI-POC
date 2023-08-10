import React, { useRef, useState, useEffect } from "react";
import { styled } from "styled-components";
import Grid from "@mui/material/Unstable_Grid2";
import Stack from "@mui/material/Stack";
import { TextField, Button } from "@mui/material";
import CircularProgress from '@mui/material/CircularProgress';

export const MainContainer = styled.main`
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: max;
  height: max;
  background-color: #white;
  transition: background-color 0.2s linear;
`;

const ChatContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 70vh; /* Max height for the chat container */
  width: max;
  overflow-y: auto; /* Add a scrollbar when content overflows */
`;

// A mock array of messages
const initialMessages = [
  { id: 1, sender: "appie", text: "How can I help you?" },
];

const appielogo = process.env.PUBLIC_URL + '/appie_logo.jpeg'
const userlogo = process.env.PUBLIC_URL + '/user-icon.png'

const ChatMessage = ({ message }) => {
  return (
    <div className={`message ${message.sender.toLowerCase()}`}>
      <div className="message-content">
        {message.sender === "appie" ? (
          <img src={appielogo} alt="Profile" style={{ width: "28px", height: "28px", marginRight: "5px", marginBottom: "-5px" }} />
        ) : null}
        {message.sender === "User" ? (
          <img src={userlogo} alt="Profile" style={{ width: "28px", height: "28px", marginRight: "5px", marginBottom: "-8px" }} />
        ) : null}
        <span className="sender">
          <strong>{message.sender}</strong>
          :</span>
        <div className="message-text">
          <p className="text">
            {message && message.text
              ? message.text.split('\n').map((line, index, array) => (
                <React.Fragment key={index}>
                  {line}
                  {index !== array.length - 1 && <br />}
                </React.Fragment>
              ))
              : null}
          </p>

          <p className="source">
            <a href={message.source} target="_blank" rel="noopener noreferrer">
              {message.source}
            </a>
          </p>
        </div>
      </div>
    </div>
  );
};



const CustomButton = styled(Button)`
  background-color: #2824f4; /* Your custom color */
  color: red; /* Text color */
  &:hover {
    background-color: black; /* Change color on hover */
  }
  margin: 10px
`;

function ChatApp() {

  const [loadingSendMessage, setLoadingSendMessage] = useState(false);
  const appianLogo = process.env.PUBLIC_URL + '/appian-white.png'


  const chatContainerRef = useRef(null);
  const buttonStyle = {
    margin: '10px 10px 10px 0px',// Add margin around the button
  };
  const [messages, setMessages] = useState(initialMessages);
  const [newMessage, setNewMessage] = useState("");

  const handleNewMessageChange = (event) => {
    setNewMessage(event.target.value);
  };

  useEffect(() => {
    // Scroll the chat container to the bottom when messages change
    chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
  }, [messages]);

  const handleSendMessage = async () => {
    if (newMessage.trim() === "") return;

    const userMessageObj = {
      id: messages.length + 1,
      sender: "User",
      text: newMessage,
    };

    setMessages([...messages, userMessageObj]);
    setNewMessage("");
    setLoadingSendMessage(true);

    try {
      const response = await fetch("/process_text", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: newMessage }),
      });

      const responseMessage = await response.json();

      const responseMessageObj = {
        id: messages.length + 2,
        sender: "appie",
        text: responseMessage.message,
        source: responseMessage.source,
      };

      setMessages([...messages, userMessageObj, responseMessageObj]);
    } catch (error) {
      // error
      console.error('Error sending message', error)
    } finally {
      setLoadingSendMessage(false)
    }
  };

  const handleClearClick = async () => {
    await fetch("/clear_history", {
      method: "POST",
    });

    setMessages([]);
    setNewMessage("");
  }

  const handleEndClick = async () => {
    await fetch("/end", {
      method: "POST",
    });

    setMessages([]);
    setNewMessage("");
  }

  return (
    <>
      <div className="container" style={{ backgroundColor: "#020A51", borderBottom: "1px solid #cccc", marginBottom: "10px", display: "flex", alignItems: "center" }}>
        <img src={appianLogo} alt="Appian Logo" style={{ width: "100px", height: "auto", padding: "10px", marginLeft: "5px" }} />
        <div style={{ flex: 1, textAlign: "center" }}>
          <Stack direction="row" marginLeft="39vw" alignItems="center">
            <h1 style={{ fontSize: "40px", color: "white", marginBottom: "10px" }}>appie</h1>
          </Stack>
        </div>
      </div>
      <MainContainer>
        <Grid container spacing={2}>
          <Grid item xs={2}>
            <></>
          </Grid>

          <Grid xs={8}>

            <ChatContainer ref={chatContainerRef}>
              <Stack>
                {messages.map((message) => (
                  <ChatMessage key={message.id} message={message} />
                ))}
              </Stack>

            </ChatContainer>

            <Grid item xs={9}>
              <TextField
                autoFocus
                fullWidth
                id="filled-basic"
                label="Enter Prompt"
                variant="filled"
                value={newMessage}
                onChange={handleNewMessageChange}
                onKeyDown={(event) => {
                  if (event.key === 'Enter') {
                    handleSendMessage();
                  }
                }}
                style={{ padding: '10px 0px' }}
              />
            </Grid>
            <Grid item xs={3}>
              <CustomButton variant="contained" size="large" onClick={handleSendMessage} disabled={loadingSendMessage} style={buttonStyle}>
                {loadingSendMessage ? <CircularProgress size={24} /> : 'Send'}
              </CustomButton>
              <Button variant="outlined" size="large" onClick={handleClearClick} style={buttonStyle}>
                Clear
              </Button>
              <Button variant="outlined" size="large" onClick={handleEndClick} style={buttonStyle}>
                End
              </Button>
            </Grid>
          </Grid>
          <Grid xs={2}>
            <></>
          </Grid>

        </Grid>

      </MainContainer></>
  );
};

export default ChatApp;
