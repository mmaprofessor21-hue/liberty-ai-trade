const API_BASE_URL = "http://localhost:8080/api/v1";

export const loadTradingConfig = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/controls/trading`);
        return await response.json();
    } catch (err) {
        console.error("Failed to load trading config", err);
        return null;
    }
};

export const updateTradingConfig = async (config) => {
    try {
        const response = await fetch(`${API_BASE_URL}/controls/trading`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(config),
        });
        return await response.json();
    } catch (err) {
        console.error("Failed to update trading config", err);
        return null;
    }
};

export const loadAIConfig = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/controls/ai`);
        return await response.json();
    } catch (err) {
        console.error("Failed to load AI config", err);
        return null;
    }
};

export const updateAIConfig = async (config) => {
    try {
        const response = await fetch(`${API_BASE_URL}/controls/ai`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(config),
        });
        return await response.json();
    } catch (err) {
        console.error("Failed to update AI config", err);
        return null;
    }
};

export const loadSystemConfig = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/controls/system`);
        return await response.json();
    } catch (err) {
        console.error("Failed to load System config", err);
        return null;
    }
};

export const updateSystemConfig = async (config) => {
    try {
        const response = await fetch(`${API_BASE_URL}/controls/system`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(config),
        });
        return await response.json();
    } catch (err) {
        console.error("Failed to update System config", err);
        return null;
    }
};
