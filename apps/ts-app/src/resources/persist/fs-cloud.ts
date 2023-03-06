/**
 * @klotho::persist {
 * id = "fs-cloud"
 * }
 */
import fs = require("fs/promises");
import * as path from "path";
import {isCloudEnv} from "../../util";
import {Stream} from "node:stream";

const prefix = isCloudEnv ? "" : "/tmp/"

async function createParentDir(filepath: string) {
    if (isCloudEnv) {
        return
    }
    await fs.mkdir(path.dirname(filepath), {recursive: true});
}

export async function writeBinary(filepath: string, content: string | NodeJS.ArrayBufferView | Iterable<string | NodeJS.ArrayBufferView> | AsyncIterable<string | NodeJS.ArrayBufferView> | Stream) {
    filepath = path.join(prefix, filepath)
    await createParentDir(filepath);
    return await fs.writeFile(filepath, content)
}

export async function readBinary(filepath: string): Promise<Buffer> {
    return await fs.readFile(path.join(prefix, filepath))
}

export async function writeText(filepath: string, content: any, makePublic: boolean = false) {
    filepath = path.join(prefix, filepath)
    await createParentDir(filepath);
    return await fs.writeFile(filepath, content, {encoding: "utf-8", flag: makePublic ? "w+" : undefined})
}

export async function readText(filepath: string): Promise<string> {
    return await fs.readFile(path.join(prefix, filepath), {encoding: "utf-8"})
}

export async function deleteFile(filepath: string) {
    await fs.rm(path.join(prefix, filepath))
}