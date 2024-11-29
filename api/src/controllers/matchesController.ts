import { Request, Response } from "express";
import MatchCard from "../models/MatchCard"; 
import { UpcomingMatch } from "../background/services";
import { match } from "assert";


export const addUpcomingMatch = async (match:UpcomingMatch) =>{
    try{

        const matchInDatabase = await MatchCard.findOne({ matchLink:match.matchLink });
        if (!matchInDatabase) {
            const upcomingMatch=new MatchCard({
                matchLink:match.matchLink,
                team1:match.team1,
                team2:match.team2,
                status:"upcoming"
            });
            upcomingMatch.save();
            console.log("matched saved in database");
        }
        else{
            console.log("match found in database");
        }
    }
    catch(error:any){
        console.log(error);
    }
}