/**
 * @klotho::persist {
 * id = "fs-cloud"
 * }
 */
import fs = require("fs/promises");


export async function writeBinary(path: string, content: Buffer) {
    await fs.writeFile(path, content, {encoding: "utf-8"})
}

export async function readBinary(path: string): Promise<Buffer> {
    return await fs.readFile(path)
}

export async function writeText(path: string, content: any) {
    await fs.writeFile(path, content, {encoding: "utf-8"})
}

export async function readText(path: string): Promise<string> {
    return await fs.readFile(path, {encoding: "utf-8"})
}