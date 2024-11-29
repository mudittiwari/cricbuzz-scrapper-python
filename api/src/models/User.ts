import mongoose, { Schema, Document, Date, Model } from "mongoose";

export interface IUser extends Document {
    username: string;
    email: string;
    mobileNumber: string;
    password: string;
    role:'user' | 'admin';
    createdAt: Date;
    modifiedAt: Date;
}

const userSchema: Schema<IUser> = new Schema(
    {
        username: { type: String, required: true },
        email: { type: String, required: true, unique: true },
        mobileNumber: { type: String, required: true },
        password: { type: String, required: true },
        role:{
            type:String,
            default:'user',
            enum: ['user', 'admin']
        }
    },
    {
        timestamps: true
    }
);

const User: Model<IUser> = mongoose.model<IUser>('User', userSchema);
export default User;
