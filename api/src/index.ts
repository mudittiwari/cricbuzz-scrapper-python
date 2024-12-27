import express from 'express';
import {connectToDatabase} from './config/DBConnection';
import dotenv from "dotenv";
import AuthRouter from "./routes/authRoute";
import MatchRouter from "./routes/matchesRoute";
import { executeBallActionScript, executePythonScript } from './background/services';
import { updateRunningMatchesCommentaryLoop } from './controllers/matchesController';

const app = express();
const port = 5000;

dotenv.config()
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use("/api/auth",AuthRouter);
app.use("/api/matches",MatchRouter);

async function executeTasks(){
  await connectToDatabase();
  executePythonScript();
  updateRunningMatchesCommentaryLoop();
}

// executeBallActionScript("https://www.cricbuzz.com/live-cricket-scores/110045/wiw-vs-indw-3rd-odi-icc-championship-match-west-indies-women-tour-of-india-2024","26.1");

executeTasks();

setInterval(() => {
  executePythonScript();
}, 100000);




app.get('/', (req, res) => {
  res.send('Hello, TypeScript Node Express!');
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
