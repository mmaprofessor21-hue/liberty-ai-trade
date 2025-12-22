
export function parseSymbol(raw) {
    if (!raw || typeof raw !== "string") return null;

    let text = raw.trim().toUpperCase();

    if (text.includes(":")) text = text.split(":")[1];

    text = text.replace(/\s+/g, "");

    if (text.includes("/")) return norm(text.split("/")[0]);

    if (text.includes("-")) return norm(text.split("-")[0]);

    if (text.endsWith(".P")) text = text.replace(".P", "");

    text = text.replace("PERP", "");

    const lev = text.match(/^([A-Z]{2,6})(\d+)(L|S)$/);
    if (lev) return norm(lev[1]);

    const base = text.match(/^([A-Z0-9]{2,6})(USD|USDT|BUSD|EUR|GBP|USDC)$/);
    if (base) return norm(base[1]);

    const clean = text.replace(/[^A-Z]/g, "");
    if (clean.length >= 2 && clean.length <= 6) return norm(clean);

    return null;
}

function norm(token) {
    if (!token) return null;

    const banned = [
        "SPX", "DJI", "NDX", "QQQ", "SPY", "AAPL", "TSLA", "EUR",
        "GBP", "JPY", "CHF", "CAD", "AUD"
    ];
    if (banned.includes(token)) return null;

    return token.toUpperCase();
}
