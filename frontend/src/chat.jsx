import React, { useRef, useState, useEffect } from "react";
import {styled} from "styled-components";
import Grid from "@mui/material/Unstable_Grid2";
import Stack from "@mui/material/Stack";
import { TextField, Button } from "@mui/material";

export const MainContainer = styled.main`
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100dvh;
  background-color: #white;
  transition: background-color 0.2s linear;
`;

const ChatContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 70vh; /* Max height for the chat container */
  width: 100%;
  overflow-y: auto; /* Add a scrollbar when content overflows */
`;

// A mock array of messages
const initialMessages = [
  { id: 1, sender: "Bot", text: "How can I help you?" },
];

const ChatMessage = ({ message }) => {
  return (
    <div className={`message ${message.sender.toLowerCase()}`}>
      <span className="sender">{message.sender}:</span>
      <p className="text">{message.text}</p>
      <p className="source">{message.source}</p>
    </div>
  );
};

function ChatApp() {


  const chatContainerRef = useRef(null);

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

    setMessages([...messages, userMessageObj])
    setNewMessage("");

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
      sender: "Bot",
      text: responseMessage.message,
      source: responseMessage.source,
    };

    setMessages([...messages, userMessageObj, responseMessageObj]);
  };

  const handleClearClick = async () => {
    await fetch("/clear_history", {
      method: "POST",
    });

    setMessages([]);
    setNewMessage("");
  }

  return (
    <>
      <Grid container spacing={2} alignItems="center" justify="center">
        <Grid item xs={12}>
          {/* Add Appian Logo */}
          <h1 style={{ textAlign: "center" }}>APPIAN CHAT</h1>
        </Grid>
      </Grid>
        <MainContainer>

          <Grid container spacing={2}>
            <Grid xs={2}>
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

              <Grid item xs={10}>
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
                  }} />
              </Grid>
              <Grid item xs={2}>
                <Button variant="contained" size="large" onClick={handleSendMessage}>
                  Send
                </Button>
                <Button variant="outlined" size="large" onClick={handleClearClick}>
                  Clear
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
