const express = require("express");
const bodyParser = require("body-parser");
const axios = require("axios");
require("dotenv").config();

const app = express();
const PORT = 5001;

app.use(bodyParser.json());

const GROQ_API_KEY = process.env.GROQ_API_KEY;
const GROQ_URL = "https://api.groq.com/openai/v1/chat/completions";

if (!GROQ_API_KEY) {
  console.error("Error: GROQ_API_KEY is not defined in the .env file.");
  process.exit(1);
}

app.post("/chatbot", async (req, res) => {
  const userInput = req.body.prompt;

  if (!userInput) {
    return res.status(400).json({ error: "No prompt provided" });
  }

  try {
    const response = await axios.post(
      GROQ_URL,
      {
        model: "llama3-8b-8192",
        messages: [{ role: "user", content: userInput }],
      },
      {
        headers: {
          Authorization: `Bearer ${GROQ_API_KEY}`,
          "Content-Type": "application/json",
        },
      }
    );

    const botReply =
      response.data?.choices?.[0]?.message?.content ||
      "No response from the chatbot.";
    return res.status(200).json({ reply: botReply });
  } catch (error) {
    if (
      error.code === "ECONNREFUSED" ||
      error.code === "ENOTFOUND" ||
      error.message.includes("Network Error")
    ) {
      console.error("Network Error: Please check your internet connection.");
      return res.status(500).json({
        error: "Network Error. Please check your internet connection.",
      });
    }

    console.error("Groq API Error:", error.response?.data || error.message);
    return res
      .status(500)
      .json({ error: "Groq API Error", details: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`Chatbot backend running on http://localhost:${PORT}`);
});
