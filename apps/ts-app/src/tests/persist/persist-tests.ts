import {deleteFile, readBinary, readText, writeBinary, writeText} from "../../resources/persist/fs-cloud";
import {KV} from "../../resources/persist/orm-typeorm/typeorm-model";
import * as typeorm from "../../resources/persist/orm-typeorm/typeorm-logic";
import * as sequelize from "../../resources/persist/orm-sequelize/sequelize-model"
import * as sequelizeEnvVar from "../../resources/persist/orm-sequelize-envvar/sequelize-envvar-model"
import * as kvMap from "../../resources/persist/kv-map"
import {Event} from "../../resources/pubsub/models";
import {readSecretDotTxt} from "../../resources/persist/fs-secret";

export async function testReadTextSecret(req, res) {
    res.send(await readSecretDotTxt("utf-8"));
}

export async function testReadBinarySecret(req, res) {
    res.send((await readSecretDotTxt()).toString());
}

export async function testWriteTextFile(req, res) {
    await writeText(req.query.path, req.file.buffer, true);
    res.send("success");
}

export async function testWriteFilePublic(req, res) {
    res.json({url: await writeText(req.query.path, req.file.buffer)});
}

export async function testReadTextFile(req, res) {
    res.send(await readText(req.query.path));
}

export async function testWriteBinaryFileDirect(req, res) {
    await writeBinary(req.query.path, req.body);
    res.send("success");
}

export async function testWriteBinaryFileMultipart(req, res) {
    await writeBinary(req.query.path, req.file.buffer);
    res.send("success");
}


export async function testReadBinaryFile(req, res) {
    const path = req.query.path;
    res.contentType(path);
    res.send(await readBinary(path));
}

export async function testDeleteFile(req, res) {
    await deleteFile(req.query.path);
    res.send("success");
}

export async function testWriteTypeOrmKvEntry(req, res) {
    const entry = req.body as KV;
    await typeorm.set(entry.key, entry.value);
    res.send("success");
}

export async function testReadTypeOrmKvEntry(req, res) {
    const entry = await typeorm.get(req.query.key);
    if (entry == undefined) {
        res.status(404).send("not found");
        return;
    }
    res.json(entry);
}

export async function testWriteSequelizeKvEntry(req, res) {
    const entry = req.body as sequelize.Entry;
    await sequelize.set(entry.key, entry.value);
    res.send("success");
}

export async function testReadSequelizeKvEntry(req, res) {
    const entry = await sequelize.get(req.query.key);
    if (entry == undefined) {
        res.status(404).send("not found")
        return;
    }
    res.json({key: entry.key, value: entry.value});
}

export async function testWriteSequelizeEnvVarKvEntry(req, res) {
    const entry = req.body as sequelizeEnvVar.Entry;
    await sequelizeEnvVar.set(entry.key, entry.value);
    res.send("success");
}

export async function testReadSequelizeEnvVarKvEntry(req, res) {
    const entry = await sequelizeEnvVar.get(req.query.key);
    if (entry == undefined) {
        res.status(404).send("not found");
        return;
    }
    res.json({key: entry.key, value: entry.value});
}

export async function testGetKVMapEntry(req, res) {
    const entry = await kvMap.get(req.query.key);
    if (!entry) {
        res.status(404).send("not found");
        return;
    }
    res.json(entry);
}

export async function testSetKVMapEntry(req, res) {
    await kvMap.set(req.body.key, req.body as Event);
    res.send("success");
}

export async function testDeleteKVMapEntry(req, res) {
    res.json({success: await kvMap.delete(req.query.key)});
}

