function getEnvVariable(name: string): string {
    const value = import.meta.env[name];
    if (!value) {
        throw new Error(`Environment variable ${name} is not defined`);
    }
    return value;
}

export const GITRICS_API_BASE_URL: string = getEnvVariable("VITE_GITRICS_API_BASE_URL");