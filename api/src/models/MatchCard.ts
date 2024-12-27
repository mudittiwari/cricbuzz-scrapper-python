import mongoose, { Schema, Document, Model } from "mongoose";
import { MatchCommentary } from "../background/services";

export interface IMatchCard extends Document {
    matchLink: string;
    team1: string;
    team2: string;
    team1Players: string[];
    team2Players: string[];
    subscribersList: string[];
    status: "upcoming" | "running" | "completed";
    playersSubscribed: Map<string, string[]>;
    matchTiming: string;
    createdAt: Date;
    updatedAt: Date;
}
const matchCardSchema: Schema<IMatchCard> = new Schema(
    {
        matchLink: { type: String, required: true, unique: true },
        team1: { type: String, required: true },
        team2: { type: String, required: true },
        matchTiming: {type: String},
        team1Players: { type: [String], default:[] },
        team2Players: { type: [String], default:[] },
        subscribersList: { type: [String], default: [] },
        playersSubscribed: { type: Map, of: [String], default: () => new Map()  },
        status: {
            type: String,
            required: true,
            enum: ["upcoming", "running", "completed"],
        },
    },
    {
        timestamps: true,
    }
);

const MatchCard: Model<IMatchCard> = mongoose.model<IMatchCard>("MatchCard", matchCardSchema);
export default MatchCard;
