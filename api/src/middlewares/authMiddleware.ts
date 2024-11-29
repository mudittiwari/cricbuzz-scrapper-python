import { Request, Response, NextFunction } from "express";
import jwt, { JwtPayload } from "jsonwebtoken";
import User, { IUser } from "../models/User";

interface AuthenticatedRequest extends Request {
    user?: IUser;
}

const authMiddleware = async (
    req: AuthenticatedRequest,
    res: Response,
    next: NextFunction
): Promise<void> => {
    try {
        const authHeader = req.header("Authorization");
        if (!authHeader) {
            res.status(401).send({ message: "No token provided" });
            return;
        }
        const token = authHeader.replace("Bearer ", "");
        if (!token) {
            res.status(401).send({ message: "Token is missing" });
            return;
        }
        const decoded = jwt.verify(token, process.env.JWT_SECRET || "") as JwtPayload;
        const user = await User.findById(decoded.id);
        if (!user) {
            res.status(404).send({ message: "User not found" });
            return;
        }
        req.user = user;
        next();
    } catch (error) {
        res.status(401).send({ message: "Invalid token" });
    }
};

export default authMiddleware;
