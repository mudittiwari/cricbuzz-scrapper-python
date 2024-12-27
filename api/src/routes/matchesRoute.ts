import { Router} from "express";
import { fetchRunningMatches, fetchUpcomingMatches, subscribeMatch, subscribeMatchPlayer } from "../controllers/matchesController";
import authMiddleware from "../middlewares/authMiddleware";
const router = Router();


router.get('/fetchUpcomingMatches', authMiddleware ,fetchUpcomingMatches);
router.get('/fetchRunningMatches', authMiddleware ,fetchRunningMatches);
router.post('/subscribeMatch', authMiddleware ,subscribeMatch);
router.post('/subscribeMatchPlayer', authMiddleware ,subscribeMatchPlayer);
export default router;