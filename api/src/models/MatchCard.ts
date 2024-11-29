import mongoose, { Schema, Document, Model } from "mongoose";

export interface IMatchCard extends Document {
    matchLink: string;
    team1: string;
    team2: string;
    team1Players: string[];
    team2Players: string[];
    subscribersList: string[];
    status: "upcoming" | "live" | "completed";
    matchCommentary: string[];
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
        status: {
            type: String,
            required: true,
            enum: ["upcoming", "live", "completed"],
        },
        matchCommentary: { type: [String], default: [] },
    },
    {
        timestamps: true,
    }
);

const MatchCard: Model<IMatchCard> = mongoose.model<IMatchCard>("MatchCard", matchCardSchema);
export default MatchCard;
