import { Dependency } from "../../types/analysis";

export const downloadDependencyFile = (filename: string, deps: Dependency[], projectName: string) => {
    let content = "";
    let mimeType = "text/plain";

    const lowerFilename = filename.toLowerCase();

    if (lowerFilename.endsWith('.txt') || lowerFilename.includes('requirements')) {
        content = deps.map(d => `${d.name}==${d.version}`).join('\n');
    } else if (lowerFilename.endsWith('.json')) {
        const pkg: any = {
            name: projectName.toLowerCase().replace(/\s+/g, '-'),
            dependencies: {}
        };
        deps.forEach(d => {
            pkg.dependencies[d.name] = d.version;
        });
        content = JSON.stringify(pkg, null, 2);
        mimeType = "application/json";
    } else {
        content = deps.map(d => `${d.name}: ${d.version} (${d.ecosystem})`).join('\n');
    }

    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
};
