import express = require("express");
import {primaryRouter} from "./executor";

function setupExpressApp() {
    const app: any = express();
    app.use(express.urlencoded({ extended: true }));
    app.use(express.json());
    return app;
}

const app = setupExpressApp();
app.use(primaryRouter)

/* @klotho::expose {
 *  target = "public"
 *  id = "ts-gateway-primary"
 * }
 */
app.listen(3000, () => {
    console.log(`App listening locally`)
})

