export function testIsUsingCustomDockerfile(req, res) {
    return res.json({usingCustomDockerfile: process.env?.CUSTOM_DOCKERFILE != undefined});
}