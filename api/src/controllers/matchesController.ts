import { Request, Response } from "express";
import MatchCard from "../models/MatchCard";
import { UpcomingMatch, RunningMatch, executeBallActionScript, MatchCommentary } from "../background/services";


export const addUpcomingMatch = async (match: UpcomingMatch) => {
    try {

        const matchInDatabase = await MatchCard.findOne({ matchLink: match.matchLink });
        if (!matchInDatabase) {
            const upcomingMatch = new MatchCard({
                matchLink: match.matchLink,
                team1: match.team1,
                team2: match.team2,
                status: "upcoming"
            });
            upcomingMatch.save();
            console.log("matched saved in database");
        }
        else {
            console.log("match found in database");
        }
    }
    catch (error: any) {
        console.log(error);
    }
}

export const handleRunningMatches = async (match: RunningMatch) => {
    try {
        const matchInDatabase = await MatchCard.findOne({ matchLink: match.matchLink });
        if (!matchInDatabase) {
            const runningMatch = new MatchCard({
                matchLink: match.matchLink,
                team1: match.team1,
                team2: match.team2,
                status: "running",
                team1Players: match.team1Players,
                team2Players: match.team2Players
            });
            await runningMatch.save();
            // console.log("matched saved in database");
        }
        else {
            matchInDatabase.team1 = match.team1;
            matchInDatabase.team2 = match.team2;
            matchInDatabase.status = "running";
            matchInDatabase.team1Players = match.team1Players;
            matchInDatabase.team2Players = match.team2Players;
            await matchInDatabase.save();
            // console.log("Match updated in database");
        }
    }
    catch (error: any) {
        console.log(error);
    }
}

export const updateRunningMatchesCommentaryLoop = async (): Promise<void> => {
    const updateRunningMatchesCommentary = async (): Promise<void> => {
        try {
            const runningMatches = await MatchCard.find({ status: "running" });

            for (const match of runningMatches) {
                let lastOverBall = matchCommentaryMap.get(match.matchLink)?.over ?? "";
                const currentCommentary = await executeBallActionScript(match.matchLink,lastOverBall);
                if (!currentCommentary || currentCommentary.over == null) {
                    console.log(`No commentary data found for match: ${match.matchLink}`);
                    continue;
                }

                if (
                    currentCommentary.batsman === "Unknown" ||
                    currentCommentary.bowler === "Unknown" ||
                    currentCommentary.over === "Unknown" ||
                    currentCommentary.scoreDone === "N/A"
                ) {
                    console.log(`Invalid commentary object: ${JSON.stringify(currentCommentary)}`);
                    continue;
                }

                const currentOver = parseFloat(currentCommentary.over);
                const lastCommentary = matchCommentaryMap.get(match.matchLink);
                if (!lastCommentary || parseFloat(lastCommentary.over) <= currentOver) {
                    matchCommentaryMap.set(match.matchLink, currentCommentary);
                    // console.log(`Updated commentary for match: ${match.matchLink}`);
                    console.log(matchCommentaryMap)
                } else {
                    // console.log(
                    //     `Skipping commentary for match: ${match.matchLink} as it's not newer (current over: ${currentOver}, last over: ${parseFloat(lastCommentary.over)})`
                    // );
                }
            }
        } catch (error) {
            console.error("Error updating running matches commentary:", error);
        }
    };

    const matchCommentaryMap = new Map<string, MatchCommentary>();

    while (true) {
        await updateRunningMatchesCommentary();
    }
};

const sendNotification = async (matchLink: string, commentary: MatchCommentary): Promise<void> => {
    //send notification to the connected users
}



export const fetchUpcomingMatches = async (req: Request, res: Response): Promise<void> => {
    try {
        const matches = await MatchCard.find({ status: 'upcoming' });
        res.status(200).json({
            success: true,
            data: matches
        });
    } catch (error) {
        console.error("Error fetching matches:", error);
        res.status(500).json({
            success: false,
            message: "Failed to fetch matches",
            error: error instanceof Error ? error.message : "Unknown error"
        });
    }
};


export const fetchRunningMatches = async (req: Request, res: Response): Promise<void> => {
    try {
        const matches = await MatchCard.find({ status: 'running' });
        res.status(200).json({
            success: true,
            data: matches
        });
    } catch (error) {
        console.error("Error fetching matches:", error);
        res.status(500).json({
            success: false,
            message: "Failed to fetch matches",
            error: error instanceof Error ? error.message : "Unknown error"
        });
    }
};


export const subscribeMatch = async (req: Request, res: Response): Promise<void> => {
    try {
        const { matchLink, userEmail } = req.body;
        const match = await MatchCard.findOne({
            matchLink
        });
        if (!match) {
            res.status(404).json({
                success: false,
                message: "Match not found"
            });
            return;
        }
        match.subscribersList.push(userEmail);
        await match.save();
        res.status(200).json({
            success: true,
            data: match
        });
    } catch (error) {
        console.error("Error fetching match:", error);
        res.status(500).json({
            success: false,
            message: "Failed to fetch match",
            error: error instanceof Error ? error.message : "Unknown error"
        });
    }
}


export const subscribeMatchPlayer = async(req: Request, res: Response): Promise<void> => {
    try {
        const { matchLink, userEmail, playerName } = req.body;
        const match = await MatchCard.findOne({
            matchLink
        });
        if (!match) {
            res.status(404).json({
                success: false,
                message: "Match not found"
            });
            return;
        }
        if(!match.subscribersList.includes(userEmail)){
            res.status(400).json({
                success: false,
                message: "User not subscribed to the match"
            });
            return;
        }
        if(match.playersSubscribed.has(playerName)){
            if(match.playersSubscribed.get(playerName)?.includes(userEmail)){
                res.status(400).json({
                    success: false,
                    message: "User already subscribed to the player"
                });
                return;
            }
            match.playersSubscribed.get(playerName)?.push(userEmail);
        }
        else{
            match.playersSubscribed.set(playerName,[userEmail]);
        }
        await match.save();
        res.status(200).json({
            success: true,
            data: match
        });
    } catch (error) {
        console.error("Error fetching match:", error);
        res.status(500).json({
            success: false,
            message: "Failed to fetch match",
            error: error instanceof Error ? error.message : "Unknown error"
        });
    }

}