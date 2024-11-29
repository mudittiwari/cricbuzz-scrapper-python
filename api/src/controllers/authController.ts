import { Request, Response } from "express";
import User from "../models/User";
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";

export const registerUser = async (req: Request, res: Response): Promise<void> => {
    try {
        const { username, email, mobileNumber, password } = req.body;
        const hashedPassword = await bcrypt.hash(password, 10);
        const newUser = new User({
            username,
            email,
            mobileNumber,
            password: hashedPassword
        });
        await newUser.save();
        res.status(201).json({ message: "User registered successfully", user: newUser });
    } catch (error: any) {
        if (error.code === 11000) {
            res.status(400).json({
                message: "Email already exists. Please use a different one.",
            });
        } else {
            console.error("Error registering user:", error);
            res.status(500).json({ message: "Internal Server Error" });
        }
    }
};

export const loginUser = async (req: Request, res: Response): Promise<void> => {
    try {
        const { email, password } = req.body;
        const user = await User.findOne({ email });
        if (!user) {
            res.status(404).json({ message: "User not found" });
            return;
        }
        const isPasswordValid = await bcrypt.compare(password, user.password);
        if (!isPasswordValid) {
            res.status(401).json({ message: "Invalid credentials" });
            return;
        }
        const tokenOptions = user.role === "user" ? { expiresIn: "1h" } : {};
        const token = jwt.sign(
            { id: user._id, email: user.email },
            process.env.JWT_SECRET || "defaultsecret",
            tokenOptions
        );
        res.status(200).json({ message: "Login successful", token });
    } catch (error) {
        console.error("Error logging in user:", error);
        res.status(500).json({ message: "Internal Server Error" });
    }
};
