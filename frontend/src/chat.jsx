import React, { useState } from "react";
import styled from "styled-components";
import Grid from "@mui/material/Unstable_Grid2";
import Stack from "@mui/material/Stack"

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
  { id: 1, sender: "User", text: "Hello there!" },
  { id: 2, sender: "Bot", text: "Hi! How can I assist you?" },
];

const ChatMessage = ({ message }) => {
  return (
    <div className={`message ${message.sender.toLowerCase()}`}>
      <span className="sender">{message.sender}:</span>
      <p className="text">{message.text}</p>
    </div>
  );
};

const ChatApp = () => {
  const [messages, setMessages] = useState(initialMessages);
  const [newMessage, setNewMessage] = useState("");

  const handleNewMessageChange = (event) => {
    setNewMessage(event.target.value);
  };

  const handleSendMessage = () => {
    if (newMessage.trim() === "") return;

    const newMessageObj = {
      id: messages.length + 1,
      sender: "User",
      text: newMessage,
    };

    setMessages([...messages, newMessageObj]);
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
      </Grid>

      <Grid xs={3}>
        <></>
      </Grid>

      <Grid xs={12} display="flex" justifyContent="center">
        <div className="input-area">
          <input
            type="text"
            placeholder="Type your message..."
            value={newMessage}
            onChange={handleNewMessageChange}
          />
          <button onClick={handleSendMessage}>Send</button>
        </div>
      </Grid>
    </Grid>
  );
};

export default ChatApp;
