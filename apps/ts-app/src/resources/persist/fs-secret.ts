/**
 * @klotho::persist {
 *   id = "fs-secret"
 *   type ="secret"
 * }
 */
import fs = require("fs/promises");

export async function readSecret(path: string, encoding: string| null = null): Promise<Buffer | string> {
    return await fs.readFile(path, {encoding: "utf-8"})
}