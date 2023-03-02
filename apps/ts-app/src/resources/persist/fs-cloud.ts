/**
 * @klotho::persist {
 * id = "fs-cloud"
 * }
 */
import fs = require("fs/promises");
import * as path from "path";

const isCloudEnv = process.env["CLOUDCC"] == "true";
const prefix = isCloudEnv ? "" : "/tmp/"

async function createParentDir(filepath: string) {
    if (isCloudEnv) {
        return
    }
    await fs.mkdir(path.dirname(filepath), {recursive: true});
}

export async function writeBinary(filepath: string, content: Buffer) {
    filepath = path.join(prefix, filepath)
    await createParentDir(filepath);
    await fs.writeFile(filepath, content, {encoding: "utf-8", flag: "w+"})
}

export async function readBinary(filepath: string): Promise<Buffer> {
    return await fs.readFile(path.join(prefix, filepath))
}

export async function writeText(filepath: string, content: any) {
    filepath = path.join(prefix, filepath)
    await createParentDir(filepath);
    await fs.writeFile(filepath, content, {encoding: "utf-8", flag: "w+"})
}

export async function readText(filepath: string): Promise<string> {
    return await fs.readFile(path.join(prefix, filepath), {encoding: "utf-8"})
}