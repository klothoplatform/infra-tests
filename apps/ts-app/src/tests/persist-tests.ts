import {readSecret} from "../resources/persist/fs-secret";
import {readBinary, readText, writeBinary, writeText} from "../resources/persist/fs-cloud";
import {KV} from "../resources/persist/orm-typeorm/typeorm-model";
import * as typeorm from "../resources/persist/orm-typeorm/typeorm-logic";
import {Entry} from "../resources/persist/orm-sequelize/sequelize-model";
import * as sequelize from "../resources/persist/orm-sequelize/sequelize-model"

export async function testReadTextSecret(req, res) {
    res.send(await readSecret(req.query.name, "utf-8"));
}

export async function testReadBinarySecret(req, res) {
    res.send(await readSecret(req.query.name));
}

export async function testWriteTextFile(req, res) {
    await writeText(req.query.path, req.file.buffer);
    res.send("success");
}

export async function testReadTextFile(req, res) {
    res.send(await readText(req.query.path));
}

export async function testWriteBinaryFile(req, res) {
    await writeBinary(req.query.path, req.file.buffer);
    res.send("success");
}

export async function testReadBinaryFile(req, res) {
    const path = req.query.path;
    res.contentType(path);
    res.send(await readBinary(path));
}

export async function testWriteTypeOrmKvEntry(req, res) {
    const entry = req.body as KV;
    await typeorm.set(entry.key, entry.value);
    res.send("success");
}

export async function testReadTypeOrmKvEntry(req, res) {
    const entry = await typeorm.get(req.query.key);
    if (entry == undefined) {
        res.statusCode(404).send("not found")
    }
    res.json(entry);
}

export async function testWriteSequelizeKvEntry(req, res) {
    const entry = req.body as Entry;
    await sequelize.set(entry.key, entry.value);
    res.send("success");
}

export async function testReadSequelizeKvEntry(req, res) {
    const entry = await sequelize.get(req.query.key);
    if (entry == undefined) {
        res.statusCode(404).send("not found")
    }
    res.json(entry);
}