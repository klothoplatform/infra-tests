import {isCloudEnv} from "./util";

if (!isCloudEnv) {
    require('dotenv').config({path: "./local.env"});
}

import express = require("express");
import {router1} from "./executor-1";
import {router2} from "./executor-2";
import {router3} from "./executor-custom-dockerfile";

process.on('uncaughtException', (error, origin) => {
    console.log('----- Uncaught exception -----')
    console.log(error)
    console.log('----- Exception origin -----')
    console.log(origin)
})

process.on('unhandledRejection', (reason, promise) => {
    console.log('----- Unhandled Rejection at -----')
    console.log(promise)
    console.log('----- Reason -----')
    console.log(reason)
})

function setupExpressApp() {
    const app: any = express();
    app.use(express.urlencoded({ extended: true }));
    app.use(express.json());
    return app;
}

const app = setupExpressApp();
app.use(router1)
app.use(router2)
app.use(router3)

/**
 * @klotho::expose {
 *  target = "public"
 *  id = "ts-gateway-primary"
 * }
 */
app.listen(3000, () => {
    console.log(`App listening locally`)
})

