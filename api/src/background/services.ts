import { spawn } from 'child_process';
import { addUpcomingMatch, handleRunningMatches } from '../controllers/matchesController';
import { Request } from "zeromq";
import { json } from 'stream/consumers';
export interface RunningMatch {
    matchLink: string;
    team1: string;
    team2: string;
    matchType: string;
    team1Players: string[];
    team2Players: string[];
}

export interface UpcomingMatch {
    matchLink: string;
    team1: string;
    team2: string;
    matchType: string;
    matchTiming: string;
}

export interface MatchCommentary {
    scoreDone: string;
    bowler: string;
    batsman: string;
    over: string;
}


export function executePythonScript(): void {
    const socket = new Request();

    (async () => {
        try {
            socket.connect("tcp://localhost:5556");
            const message = { task: "getMatches" };
            await socket.send(JSON.stringify(message));
            const [response] = await socket.receive();
            const jsonResponse = JSON.parse(response.toString());
            if (jsonResponse.status === "success" && jsonResponse.data) {
                if (jsonResponse.data.runningMatches) {
                    parseRunningMatches(jsonResponse.data.runningMatches);
                }
                if (jsonResponse.data.upcomingMatches) {
                    parseUpcomingMatches(jsonResponse.data.upcomingMatches);
                }
            } else {
                console.error("Error in Python response:", jsonResponse.message || "Unknown error");
            }
        } catch (error) {
            console.error("Error communicating with Python service:", error);
        } finally {
            socket.close();
        }
    })();
}

export function executeBallActionScript(matchLink: string, lastOverBall: string): Promise<MatchCommentary | null> {
    return new Promise(async (resolve) => {
        const socket = new Request();
        try {
            socket.connect("tcp://localhost:5555");
            const message = JSON.stringify({ task: "getLastBallAction", matchLink, lastOverBall });
            await socket.send(message);
            const [response] = await socket.receive();
            try {
                const rawString = response.toString();
                const cleanedString = JSON.parse(rawString);
                const jsonResponse = JSON.parse(cleanedString);
                resolve(jsonResponse);
            } catch (error) {
                console.error("Error parsing JSON response:", (error as Error).message);
                resolve(null);
            }
        } catch (error) {
            console.error("ZeroMQ communication error:", (error as Error).message);
            resolve(null);
        } finally {
            socket.close();
        }
    });
}




function parseUpcomingMatches(upcomingMatchesArray: UpcomingMatch[]) {
    upcomingMatchesArray.forEach((match) => {
        addUpcomingMatch(match);
    });
}

function parseRunningMatches(runningMatchesArray: RunningMatch[]): void {
    runningMatchesArray.forEach((match) => {
        handleRunningMatches(match);
    });
}
