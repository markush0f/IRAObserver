// Helper for devicon URLs
export const getIconUrl = (name: string) => {
    const normalized = name.toLowerCase().replace(".", "").replace("js", "js").replace(" ", "");

    const map: Record<string, string> = {
        "c#": "csharp",
        "c++": "cplusplus",
        "next.js": "nextjs",
        "nextjs": "nextjs",
        "node.js": "nodejs",
        "nodejs": "nodejs",
        "react": "react",
        "vue": "vuejs",
        "angular": "angularjs",
        "go": "go",
        "golang": "go",
        "docker": "docker",
        "docker compose": "docker",
        "kubernetes": "kubernetes",
        "fastapi": "fastapi",
        "python": "python",
        "typescript": "typescript",
        "javascript": "javascript",
        "astro": "astro",
    };

    const key = map[normalized] || normalized;
    return `https://cdn.jsdelivr.net/gh/devicons/devicon/icons/${key}/${key}-original.svg`;
};
