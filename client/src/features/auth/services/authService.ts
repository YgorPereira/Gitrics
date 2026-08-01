import { GITRICS_API_BASE_URL } from "@/core/config/settings";


export function login(): void {
    window.location.href = `${GITRICS_API_BASE_URL}/auth/github/login`;
}