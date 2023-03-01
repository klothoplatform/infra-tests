import {readSecret} from "../resources/persist/fs-secret";
import {readBinary, readText, writeBinary, writeText} from "../resources/persist/fs-cloud";
import {KV} from "../resources/persist/orm-typeorm/typeorm-model";
import * as typeorm from "../resources/persist/orm-typeorm/typeorm-logic";
import {Entry} from "../resources/persist/orm-sequelize/sequelize-model";
import * as sequelize from "../resources/persist/orm-sequelize/sequelize-model"
// const typeOrmDs = typeorm.initialize()

export async function testReadTextSecret(path: string): Promise<string> {
    return await readSecret(path, "utf-8") as string;
}

export async function testReadBinarySecret(path: string): Promise<Buffer> {
    return await readSecret(path) as Buffer;
}

export async function testWriteTextFile(path: string, content: any) {
    await writeText(path, content);
}

export async function testReadTextFile(path: string): Promise<string> {
    return await readText(path);
}

export async function testWriteBinaryFile(path: string, content: any) {
    await writeBinary(path, content);
}

export async function testReadBinaryFile(path: string): Promise<Buffer> {
    return await readBinary(path);
}

export async function testWriteTypeOrmKvEntry(entry: KV) {
    // await typeOrmDs;
    await typeorm.write(entry.key, entry.value)
}

export async function testReadTypeOrmKvEntry(key: string): Promise<KV | null> {
    // await typeOrmDs;
    return await typeorm.find(key)
}

export async function testWriteSequelizeKvEntry(entry: Entry) {
    await sequelize.set(entry.key, entry.value)
}

export async function testReadSequelizeKvEntry(key: string): Promise<Entry | null> {
    return await sequelize.get(key)
}