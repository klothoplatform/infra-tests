import {promises as fs} from "fs";
import {resolve} from "path";

export async function testGetEmbeddedAsset(req, res) {
    try {
        const file = await fs.readFile(req.query.path, {encoding: req.query?.encoding});
        res.contentType(req.query.path);
        res.send(file);
    } catch (e) {
        res.status(404).send("not found");
    }
}

export async function debugListEmbeddedAssets(req, res) {
    res.json(await getFiles("embedded-assets"));
}

async function getFiles(dir) {
    const dirEntries = await fs.readdir(dir, {withFileTypes: true});
    const files = await Promise.all(dirEntries.map((dirent) => {
        const res = resolve(dir, dirent.name);
        return dirent.isDirectory() ? getFiles(res) : res;
    }));
    return files.flat();
}