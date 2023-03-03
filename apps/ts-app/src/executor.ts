import express = require("express");
import * as persist from "./tests/persist-tests";
import {invokeCrossExec as task1} from "./tasks/task-1";
import {invokeCrossExec as task2} from "./tasks/task-2";
import {invokeCrossExec as task3} from "./tasks/task-3";
import {ExecResult} from "./tasks/models";
import multer = require("multer");

/**
 * @klotho::execution_unit {
 *   id = "executor"
 * }
 */

const upload = multer({ storage: multer.memoryStorage() })

export const primaryRouter = express.Router();

primaryRouter.get("/test/exec/execute-cross-exec-tasks", testExecuteCrossExecTasks);

primaryRouter.get("/test/persist-secret/read-text-secret", persist.testReadTextSecret);
primaryRouter.get("/test/persist-secret/read-binary-secret", persist.testReadBinarySecret);

primaryRouter.get("/test/persist-fs/read-text-file", persist.testReadTextFile);
primaryRouter.get("/test/persist-fs/read-binary-file", persist.testReadBinaryFile);
primaryRouter.post("/test/persist-fs/write-text-file", upload.single("file"), persist.testWriteTextFile);
primaryRouter.post("/test/persist-fs/write-binary-file",upload.single("file"), persist.testWriteBinaryFile);
primaryRouter.delete("/test/persist-fs/delete-file", persist.testDeleteFile);

primaryRouter.get("/test/persist-orm/typeorm-read-kv-entry", persist.testReadTypeOrmKvEntry);
primaryRouter.post("/test/persist-orm/typeorm-write-kv-entry", persist.testWriteTypeOrmKvEntry);
primaryRouter.get("/test/persist-orm/sequelize-read-kv-entry", persist.testReadSequelizeKvEntry);
primaryRouter.post("/test/persist-orm/sequelize-write-kv-entry", persist.testWriteSequelizeKvEntry);
primaryRouter.get("/test/persist-orm/envvar-read-kv-entry", persist.testReadSequelizeEnvVarKvEntry);
primaryRouter.post("/test/persist-orm/envvar-write-kv-entry", persist.testWriteSequelizeEnvVarKvEntry);


// move testExecuteCrossExecTasks to a separate file after implementation of https://github.com/klothoplatform/klotho-pro/issues/65.
export async function testExecuteCrossExecTasks(req, res) {
    res.json(await Promise.all([
        await task1({id: "task-1"}),
        await task2({id: "task-2"}),
        await task3({id: "task-3"})
    ]));
}