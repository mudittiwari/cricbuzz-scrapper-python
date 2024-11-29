import { spawn } from 'child_process';
import { addUpcomingMatch } from '../controllers/matchesController';

export interface RunningMatch {
    matchLink: string;
    team1: string;
    team2: string;
    matchType: string;
    team1Players: string[];
    team2Players: string[];
}

export interface UpcomingMatch{
    matchLink: string;
    team1: string;
    team2: string;
    matchType: string;
    matchTiming: string;
}


export function executePythonScript(): void {
    const pythonProcess = spawn('python3', ['../scrapper/main.py']);
    pythonProcess.stdout.on('data', (data: Buffer) => {
        const textData = data.toString('utf-8');
        try {
            const jsonResponse = JSON.parse(textData);
            // console.log("Received JSON from Python:", jsonResponse);
            // if(jsonResponse.runningMatches){
            //     parseRunningMatches(jsonResponse.runningMatches);
            // }
            if(jsonResponse.upcomingMatches){
                parseUpcomingMatches(jsonResponse.upcomingMatches)
            }
        } catch (error) {
            console.error("Error parsing JSON:", (error as Error).message);
        }
    });

    pythonProcess.stderr.on('data', (data: Buffer) => {
        console.error("Python Error:", data.toString('utf-8'));
    });
    pythonProcess.on('close', (code: number) => {
        console.log(`Python process exited with code ${code}`);
    });
}

export function executeBallActionScript(matchLink:string): void {
    // Pass the argument to the Python script
    const pythonProcess = spawn('python3', ['../scrapper/ballAction.py', matchLink]);
    pythonProcess.stdout.on('data', (data: Buffer) => {
        const textData = data.toString('utf-8');
        try {
            const jsonResponse = JSON.parse(textData);
            console.log(jsonResponse);
        } catch (error) {
            console.error("Error parsing JSON:", (error as Error).message);
        }
    });

    pythonProcess.stderr.on('data', (data: Buffer) => {
        console.error("Python Error:", data.toString('utf-8'));
    });

    pythonProcess.on('close', (code: number) => {
        console.log(`Python process exited with code ${code}`);
    });
}



function parseUpcomingMatches(upcomingMatchesArray: UpcomingMatch[]){
    upcomingMatchesArray.forEach((match)=>{
        addUpcomingMatch(match);
    });
}

function parseRunningMatches(runningMatchesArray: RunningMatch[]): void {
    runningMatchesArray.forEach((match) => {
        console.log(match.matchLink, match.team1, match.team2, match.team1Players, match.team2Players);
    });
}
