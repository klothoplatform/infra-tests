import express = require("express");
import multer = require("multer");
import * as persist from "./tests/persist/persist-tests";
import {invokeCrossExec as task1} from "./tasks/task-1";
import {invokeCrossExec as task2} from "./tasks/task-2";
import {invokeCrossExec as task3} from "./tasks/task-3";
import {testPubSubEvent} from "./tests/pubsub-tests";

import * as bodyParser from "body-parser";
import {subscribeToEvent1} from "./resources/pubsub/events";
import {testIsUsingCustomDockerfile} from "./tests/custom-dockerfile-tests";
import {testHandlesPathParams} from "./tests/expose-tests";

/**
 * @klotho::execution_unit {
 *   id = "executor-1"
 * }
 */

const upload = multer({storage: multer.memoryStorage()})


export const router1 = express.Router();

router1.use(
    bodyParser.raw({
        inflate: false,
        type: "application/octet-stream",
        limit: "10mb",
    })
);


router1.get("/test/exec/execute-cross-exec-tasks", testExecuteCrossExecTasks);
router1.get("/test/exec/execute-custom-dockerfile", testIsUsingCustomDockerfile);

router1.get("/test/persist-secret/read-text-secret", persist.testReadTextSecret);
router1.get("/test/persist-secret/read-binary-secret", persist.testReadBinarySecret);

router1.get("/test/persist-fs/read-text-file", persist.testReadTextFile);
router1.get("/test/persist-fs/read-binary-file", persist.testReadBinaryFile);
router1.post("/test/persist-fs/write-file-public", upload.single("file"), persist.testWriteFilePublic);
router1.post("/test/persist-fs/write-text-file", upload.single("file"), persist.testWriteTextFile);
router1.post("/test/persist-fs/write-binary-file-multipart", upload.single("file"), persist.testWriteBinaryFileMultipart);
router1.post("/test/persist-fs/write-binary-file-direct", persist.testWriteBinaryFileDirect);
router1.delete("/test/persist-fs/delete-file", persist.testDeleteFile);

router1.get("/test/persist-orm/typeorm-read-kv-entry", persist.testReadTypeOrmKvEntry);
router1.post("/test/persist-orm/typeorm-write-kv-entry", persist.testWriteTypeOrmKvEntry);
router1.get("/test/persist-orm/sequelize-read-kv-entry", persist.testReadSequelizeKvEntry);
router1.post("/test/persist-orm/sequelize-write-kv-entry", persist.testWriteSequelizeKvEntry);
router1.get("/test/persist-orm/envvar-read-kv-entry", persist.testReadSequelizeEnvVarKvEntry);
router1.post("/test/persist-orm/envvar-write-kv-entry", persist.testWriteSequelizeEnvVarKvEntry);

router1.get("/test/persist-kv/get-kv-nosql-entry", persist.testGetKVMapEntry);
router1.post("/test/persist-kv/set-kv-nosql-entry", persist.testSetKVMapEntry);
router1.delete("/test/persist-kv/delete-kv-nosql-entry", persist.testDeleteKVMapEntry);

router1.post("/test/pubsub/pubsub-event", testPubSubEvent);

router1.get("/test/expose/handles-path-params/:param", testHandlesPathParams);
// TODO: move testExecuteCrossExecTasks to a separate file after implementation of https://github.com/klothoplatform/klotho-pro/issues/65.
export async function testExecuteCrossExecTasks(req, res) {
    res.json(await Promise.all([
        await task1({id: "task-1"}),
        await task2({id: "task-2"}),
        await task3({id: "task-3"})
    ]));
}

subscribeToEvent1();