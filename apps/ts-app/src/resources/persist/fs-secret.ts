/**
 * @klotho::persist {
 *   id = "fs-secret"
 *   secret = true
 * }
 */
import fs = require("fs/promises");

export async function readSecretDotTxt(encoding: BufferEncoding| undefined = undefined): Promise<Buffer | string> {
    const secret = await fs.readFile("secrets/secret.txt");
    return encoding ? secret.toString(encoding) : secret;
}