import axios from "axios";
import { GITRICS_API_BASE_URL } from "@/core/config/settings";

export const GITRICS_API = axios.create({
    baseURL: GITRICS_API_BASE_URL,
    withCredentials: true,
})