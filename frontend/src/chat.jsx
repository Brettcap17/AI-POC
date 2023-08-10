import React, { useState } from "react";
import styled from "styled-components";
import Grid from "@mui/material/Unstable_Grid2";
import Stack from "@mui/material/Stack";
import { TextField, Button, Container } from "@mui/material";

export const MainContainer = styled.main`
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100dvh;
  background-color: ${(props) => props.theme.main};
  transition: background-color 0.2s linear;
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
  const [messages, setMessages] = useState(initialMessages);
  const [newMessage, setNewMessage] = useState("");

  const handleNewMessageChange = (event) => {
    setNewMessage(event.target.value);
  };

  const handleSendMessage = async () => {
    if (newMessage.trim() === "") return;

    const userMessageObj = {
      id: messages.length + 1,
      sender: "User",
      text: newMessage,
    };

    setMessages([...messages, userMessageObj])

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
    setNewMessage("");
  };

  return (
    <Grid container spacing={2}>
      <Grid xs={3}>
        <></>
      </Grid>

      <Grid xs={6}>
        <Stack>
          {messages.map((message) => (
            <ChatMessage key={message.id} message={message} />
          ))}
        </Stack>

        <br></br>

        <Container>
          <TextField
            fullWidth
            id="filled-basic"
            label="Enter Prompt"
            variant="filled"
            onChange={handleNewMessageChange}
          />
          <Button variant="contained" onClick={handleSendMessage}>
            Send
          </Button>
        </Container>
      </Grid>

      <Grid xs={3}>
        <></>
      </Grid>

      <Grid xs={8}>
        {/* <div className="input-area">
          <input
            type="text"
            placeholder="Type your message..."
            value={newMessage}
            onChange={handleNewMessageChange}
          />

          <button onClick={handleSendMessage}>Send</button>
        </div> */}
      </Grid>
    </Grid>
  );
};

export default ChatApp;
