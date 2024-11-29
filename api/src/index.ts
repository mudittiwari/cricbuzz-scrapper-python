import express from 'express';
import {connectToDatabase} from './config/DBConnection';
import dotenv from "dotenv";
import AuthRouter from "./routes/authRoute";
import { executeBallActionScript, executePythonScript } from './background/services';

const app = express();
const port = 5000;

dotenv.config()
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use("/api/auth",AuthRouter);

connectToDatabase()
setInterval(() => {
  console.log("Executing Python script...");
  // executePythonScript();
  executeBallActionScript("https://www.cricbuzz.com/live-cricket-scores/109558/nys-vs-dbl-29th-match-abu-dhabi-t10-league-2024");
}, 12000);

app.get('/', (req, res) => {
  res.send('Hello, TypeScript Node Express!');
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
